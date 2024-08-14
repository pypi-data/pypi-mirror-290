import json
import os
from datetime import datetime, timedelta
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import dotenv # type: ignore
import shutil

from botrun_drive_webhook.folder_path_cache import FolderTree


def get_google_drive_folder_path_to_root(service, folder_id, max_depth=5):
    """
    遞迴獲取從給定 folder ID 到 root 的所有父文件夾 ID，最多遞迴到指定的層級。

    :param service: Google Drive API service 對象
    :param folder_id: 起始文件夾的 ID
    :param max_depth: 最大遞迴深度，預設為 5
    :return: 包含從給定文件夾到 root 的所有文件夾 ID 的列表
    """
    folder_path = []
    current_folder_id = folder_id
    depth = 0

    while current_folder_id and depth < max_depth:
        try:
            # 獲取當前文件夾的信息
            folder = service.files().get(fileId=current_folder_id, 
                                         fields='id, name, parents').execute()
            
            # 將當前文件夾 ID 添加到路徑中
            folder_path.append(current_folder_id)
            
            # 檢查是否有父文件夾
            if 'parents' in folder:
                # 如果有父文件夾，更新 current_folder_id 為父文件夾的 ID
                current_folder_id = folder['parents'][0]
            else:
                # 如果沒有父文件夾，說明已經到達 root，退出循環
                break
            
            depth += 1
                
        except HttpError as error:
            print(f'[get_google_drive_folder_path_to_root]發生錯誤: {error}')
            break

    # 反轉列表，使其從 root 到給定文件夾的順序
    folder_path.reverse()
    return folder_path


class FileUpdateQueue:
    def __init__(self, service_account_file=None, data_dir="./data/botrun_drive_webhook/"):
        self.data_dir = data_dir
        self.queue_dir = os.path.join(self.data_dir, 'queue')
        os.makedirs(self.queue_dir, exist_ok=True)
        self.service_account_file=service_account_file
        # google drive change notification 更新模式
        self.monitor_file_path=os.path.join(self.data_dir, f"monitor_list.json")
        self.monitor_list = []
        self.path_cache = FolderTree("path_cache", data_dir=self.data_dir)
        self.non_monitoring_cache = FolderTree("non_monitoring_cache", data_dir=self.data_dir)
        self.load_monitor_list()
        # crontab 更新模式
        self.crontab_file_path = os.path.join(self.data_dir, "crontab_list.json")
        self.crontab_list = self.load_crontab_list()

    def load_google_service_account(self, service_account_file=None):
        if not service_account_file:
            dotenv.load_dotenv()
            service_account_file=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            print(f"service_account_file={service_account_file}")

        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        return service

    def initialize_monitor_list(self):
        """初始化 monitor_list.json 檔案"""
        self.monitor_list = []
        self.save_monitor_list()
        print("已創建新的 monitor_list.json 檔案")

    def initialize_path_cache(self):
        """初始化 path_cache.csv 檔案"""
        self.path_cache = FolderTree("path_cache")
        self.save_path_cache()
        print("已創建新的 path_cache.csv 檔案")

    def initialize_non_monitoring_cache(self):
        """初始化 non_monitoring_cache.csv 檔案"""
        self.non_monitoring_cache = FolderTree("non_monitoring_cache")
        self.save_non_monitoring_cache()
        print("已創建新的 non_monitoring_cache.csv 檔案")

    def load_monitor_list(self):
        try:
            with open(self.monitor_file_path, 'r') as f:
                data = json.load(f)
                self.monitor_list = data['folder_ids']
        except FileNotFoundError:
            print("monitor_list.json 不存在，正在創建...")
            self.initialize_monitor_list()

    def save_monitor_list(self):
        with open(self.monitor_file_path, 'w') as f:
            json.dump({'folder_ids': self.monitor_list}, f, indent=2)

    def load_crontab_list(self):
        try:
            with open(self.crontab_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_crontab_list(self):
        with open(self.crontab_file_path, 'w') as f:
            json.dump(self.crontab_list, f, indent=2)

    def load_path_cache(self):
        try:
            self.path_cache.load_from_csv('path_cache.csv')
        except FileNotFoundError:
            print("path_cache.csv 不存在，正在創建...")
            self.initialize_path_cache()

    def load_non_monitoring_cache(self):
        try:
            self.non_monitoring_cache.load_from_csv('non_monitoring_cache.csv')
        except FileNotFoundError:
            print("non_monitoring_cache.csv 不存在，正在創建...")
            self.initialize_non_monitoring_cache()

    def save_path_cache(self):
        self.path_cache.to_csv('path_cache.csv')

    def save_non_monitoring_cache(self):
        self.non_monitoring_cache.to_csv('non_monitoring_cache.csv')



    def register_folder_ids(self, folder_id, mode=None):
        """
        註冊新的 folder ID 到監控列表中。
        
        :param folder_id: 單個 folder ID 字符串
        :param mode: 註冊模式，可以是 "change" 或 "crontab_12h"
        """
        if mode == "crontab_12h":
            if folder_id not in self.crontab_list:
                next_update_time = (datetime.now() + timedelta(hours=12)).isoformat()
                self.crontab_list[folder_id] = next_update_time
                self.save_crontab_list()
        else:
            #預設模式
            if folder_id not in self.monitor_list:
                self.monitor_list.append(folder_id)
                # 監控的清單有變動，為避免誤擋資料夾，所以更新刪除阻擋的cache
                self.non_monitoring_cache.del_branch(folder_id)
                self.save_monitor_list()
        print(f"已成功註冊 folder ID: {folder_id} 使用模式: {mode}")


        """
        #註冊新的 folder ID 到監控列表中。
        
        #:param folder_ids: 單個 folder ID 字符串或 folder ID 列表
        if isinstance(folder_ids, str):
            folder_ids = [folder_ids]
        
        for folder_id in folder_ids:
            if folder_id not in self.monitor_list:
                self.monitor_list.append(folder_id)
                # 監控的清單有變動，為避免誤擋資料夾，所以更新刪除阻擋的cache
                self.non_monitoring_cache.del_branch(folder_id)
        
        self.save_monitor_list()

        print(f"已成功註冊以下 folder ID: {folder_ids}")
        """

    def unregister_folder_ids(self, folder_ids):
        """
        從監控列表中移除指定的 folder ID。
        
        :param folder_ids: 單個 folder ID 字符串或 folder ID 列表
        """
        if isinstance(folder_ids, str):
            folder_ids = [folder_ids]
        
        for folder_id in folder_ids:
            if folder_id in self.monitor_list:
                self.monitor_list.remove(folder_id)
                # 監控的清單有變動，為避免誤擋資料夾，所以更新刪除阻擋的cache
                self.path_cache.del_branch(folder_id)

        
        self.save_monitor_list()
        print(f"已成功移除以下 folder ID: {folder_ids}")


    def get_monitored_folders(self):
        """
        獲取當前所有被監控的 folder ID。
        
        :return: folder ID 列表
        """
        return self.monitor_list


    def update_crontab(self):
        # 處理 crontab_list
        change_num=0
        current_time = datetime.now()
        for folder_id, next_update_time in list(self.crontab_list.items()):
            #print(f"[update_crontab] folder_id={folder_id}, next_update_time={next_update_time}, current_time={current_time}")
            if datetime.fromisoformat(next_update_time) <= current_time:
                self.add_to_update_queue(monitoring_folder_id=folder_id,
                                         updated_time=current_time.isoformat(),
                                         mode="crontab")                
                # 更新下次更新時間
                self.crontab_list[folder_id] = (current_time + timedelta(hours=12)).isoformat()
                change_num+=1
        
        self.save_crontab_list()
        print(f"[update_crontab] crontab_list done, {change_num} files changed")

    def update_function(self, file_id, file_name, updated_time, parent_folderid):
        # 原有的 change 文件更新邏輯
        # 處理檔案變更的主要邏輯
        print(f"file_id={file_id}, file_name={file_name}, updated_time={updated_time}, parents_folderid={parent_folderid}")

        # 先去 path_cache 中查找 parent_folderid 的所有父文件夾
        print(f"searching cache...")
        folder_id_list = self.path_cache.search(parent_folderid)
        non_monitoring_folder_id_list = self.non_monitoring_cache.search(parent_folderid)
        print(f"search result folder_id_list={folder_id_list}\nnon_monitoring_folder_id_list={non_monitoring_folder_id_list}\n")

        # 1.如果資料夾已經出現過在 non_monitoring_cache 就跳過不處理
        if non_monitoring_folder_id_list:
            print(f"Folder in non_monitoring_cache, skip this file: file_id={file_id}, file_name={file_name}")
            return

        # 2. 如果 path_cache 中沒有 parent_folderid 的路徑，則去 Google Drive API 查找
        if not folder_id_list:
            if self.service_account_file:
                service = self.load_google_service_account()
                folder_id_list = get_google_drive_folder_path_to_root(service=service, folder_id=parent_folderid)
                print(f"Get new folder_id_list={folder_id_list}")
        
        # 3.如果找到的路徑中有任何一個資料夾在 monitor_list 中，就加入 path_cache 中
        is_match=False
        for folder_id in folder_id_list:
            #print(f"step 3. check folder_id={folder_id} \n self.monitor_list={self.monitor_list}")
            if folder_id in self.monitor_list:
                is_match=True
                self.path_cache.add_branch(folder_id_list)
                print(f"Match Monitor list! Add new folder_id_list={folder_id_list} to path_cache")
                print(f"Matched monitoring_folder_id={folder_id}")
                self.add_to_update_queue(file_id=file_id, 
                                    file_name=file_name, 
                                    monitoring_folder_id=folder_id,
                                    updated_time=updated_time)
                
        # 如果都沒有比對到，就把此 Folder id 加入到 non_monitoring_cache
        if not is_match:
            self.non_monitoring_cache.add_branch(folder_id_list)
            print(f"No match... Add new folder_id_list={folder_id_list} to non_monitoring_cache")

    def add_to_update_queue(self, file_id=None, file_name=None, monitoring_folder_id=None, updated_time=None, mode=None):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        queue_file = os.path.join(self.queue_dir, f"update_queue_{current_time}.json")
        
        if mode == "crontab":            
            update_task = {
                "collection_id": monitoring_folder_id,
                "file_id": "",
                "file_name": "",
                "updated_time": updated_time,
                "mode": "crontab",
            }
            print(f"[add_to_update_queue] crontab changed! Add crontab task: {update_task}")
        else:
            update_task = {
                "collection_id": monitoring_folder_id,
                "file_id": file_id,
                "file_name": file_name,
                "updated_time": updated_time,
                "mode": "change",
            }
        
        if os.path.exists(queue_file):
            with open(queue_file, 'r+') as f:
                tasks = json.load(f)
                tasks.append(update_task)
                f.seek(0)
                json.dump(tasks, f, indent=2)
        else:
            with open(queue_file, 'w') as f:
                json.dump([update_task], f, indent=2)

    def process_update_queue(self, check_interval=60, limit=100):
        current_time = datetime.now()
        queue_files = sorted([f for f in os.listdir(self.queue_dir) if f.startswith("update_queue_") and f.endswith(".json")])
        
        all_tasks = []
        latest_file_name = ""
        latest_file_time = datetime.min

        for queue_file in queue_files:
            file_time = queue_file[13:-5]  # 取得檔案名稱中的時間部分
            file_datetime = datetime.strptime(file_time, "%Y%m%d_%H%M%S")
            
            # 如果檔案建立時間超過 check_interval 秒，則處理該檔案
            if (current_time - file_datetime).total_seconds() > check_interval:
                queue_file_path = os.path.join(self.queue_dir, queue_file)
                with open(queue_file_path, 'r') as f:
                    tasks = json.load(f)
                all_tasks.extend(tasks)

                # 更新最新的檔案名稱
                if file_datetime > latest_file_time:
                    latest_file_time = file_datetime
                    latest_file_name = queue_file

        # 去除重複的任務，優先保留最新的
        unique_tasks = {}
        for task in all_tasks:
            key = task.get('file_id') or task.get('collection_id')
            if key not in unique_tasks or datetime.fromisoformat(task['updated_time']) > datetime.fromisoformat(unique_tasks[key]['updated_time']):
                unique_tasks[key] = task

        updated_list = list(unique_tasks.values())

        # 限制回傳數量
        updated_list = updated_list[:limit]

        return updated_list, latest_file_name
    
    # 將處理完的檔案移動到指定資料夾
    def finish_queue_process(self, latest_file_name, is_mv_to_folder=None):
        if not latest_file_name.startswith("update_queue_") or not latest_file_name.endswith(".json"):
            raise ValueError("Invalid file name format")

        print(f"latest_file_name={latest_file_name}")

        latest_file_time = latest_file_name[13:-5]  # 取得檔案名稱中的時間部分
        latest_datetime = datetime.strptime(latest_file_time, "%Y%m%d_%H%M%S")
        queue_files = [f for f in os.listdir(self.queue_dir) if f.startswith("update_queue_") and f.endswith(".json")]

        if is_mv_to_folder:
            archive_dir = os.path.join(self.queue_dir, is_mv_to_folder)
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)

        processed_files_count = 0

        for queue_file in queue_files:
            file_time = queue_file[13:-5]
            file_datetime = datetime.strptime(file_time, "%Y%m%d_%H%M%S")
            
            if file_datetime <= latest_datetime:
                file_path = os.path.join(self.queue_dir, queue_file)
                if is_mv_to_folder:
                    shutil.move(file_path, os.path.join(archive_dir, queue_file))
                else:
                    os.remove(file_path)
                processed_files_count += 1

        action = "moved" if is_mv_to_folder else "deleted"
        result_message = f"{latest_datetime.strftime('%Y-%m-%d %H:%M:%S')} - {processed_files_count} files are {action} from queue"
        
        return result_message



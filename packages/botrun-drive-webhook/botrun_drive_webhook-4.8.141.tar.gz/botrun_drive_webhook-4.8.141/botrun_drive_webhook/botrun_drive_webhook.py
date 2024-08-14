import time
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import uuid
import re
import dotenv 
from botrun_drive_webhook.file_update_queue import FileUpdateQueue
import requests
import csv
from io import StringIO

version=f"4.8.141"
print(f"\n\n\n .................init botrun_drive_webhook....................version={version}")
print(f"Current working directory: {os.getcwd()}")
dotenv_path = os.getenv('MY_DOTENV_PATH', '.env')
print(f"Current dotenv_path directory:{dotenv_path}")
dotenv.load_dotenv(dotenv_path)

def botrun_drive_webhook(service_account_file, 
                         folder_id, 
                         webhook_url, 
                         force_reset_webhook_channel=False,
                         file_pattern='*', 
                         call_back_function=None, 
                         notification_info_path="./data/botrun_drive_webhook/notification_info.json"
                        ):
    try:

        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)


        print("==============init_google_drive_webhook=========================================")
        print(f"step 1. init_google_drive_webhook... ")
        notification_info=init_google_drive_webhook(service,
                                folder_id=folder_id,
                                webhook_url=webhook_url,
                                force_reset_webhook_channel=force_reset_webhook_channel,
                                notification_info_path=notification_info_path
                                )
        
        print("==============check_folder_notifications=========================================")
        print(f"step 2. Start check_folder_notifications")
        check_folder_notifications(service, 
                                file_pattern=file_pattern, 
                                call_back_function=call_back_function,
                                notification_info=notification_info,
                                notification_info_path=notification_info_path
                                )

        return 

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def init_google_drive_webhook(service, 
                        folder_id, 
                        webhook_url, 
                        force_reset_webhook_channel=False,
                        notification_info_path="./data/botrun_drive_webhook/notification_info.json"
                         ):
    try:
        os.makedirs("./data/botrun_drive_webhook/", exist_ok=True)
        if os.path.exists(notification_info_path):
            with open(notification_info_path, 'r') as f:
                info = json.load(f)
            
            current_time = datetime.datetime.now()
            expiration_time = datetime.datetime.fromtimestamp(int(info['expiration']) / 1000)

            if not force_reset_webhook_channel and current_time < expiration_time:
                print(f"Existing notification is still valid. Using the current one. expiration_time={expiration_time}")
                return info
            else:
                # stop the notification channel for reseting
                try:
                    service.channels().stop(body={
                        'id': info['channelId'],
                        'resourceId': info['resourceId']
                    }).execute()
                    print(f"Stopped expired notification: {info['channelId']}")
                except HttpError as error:
                    print(f"Error stopping expired notification: {error}")
            
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error reading notification_info.json: {e}")
    
    print("Creating new notification_info.json and establishing new connection.")
    channel = {
        'id': f"google_drive_webhook_{str(uuid.uuid4())}",
        'type': 'web_hook',
        'address': webhook_url,
        'expiration': int((datetime.datetime.now() + datetime.timedelta(days=7)).timestamp() * 1000)
    }

    try:
        
        # 設置監控
        # 使用 service.files().watch 監控
        response = service.changes().watch(
            pageToken='1',  # 從最新的更改開始
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            restrictToMyDrive=False,
            spaces='drive',
            body=channel
        ).execute()

        print(f"New notification channel set up: {json.dumps(response, indent=2)}")

        # 獲取起始頁面令牌
        start_page_token = service.changes().getStartPageToken(
            supportsAllDrives=True
        ).execute().get('startPageToken')

        print(f"Start page token: {start_page_token}")

        '''
        # 使用 service.files().watch 監控
        response = service.files().watch(
            fileId=folder_id,
            supportsAllDrives=True,
            body=channel
        ).execute()

        print(f"New notification channel set up: {json.dumps(response, indent=2)}")
    
        page_token_result = service.changes().getStartPageToken().execute()
        print(f"page_token_result={page_token_result}")
        start_page_token=page_token_result["startPageToken"]
        '''

        new_info = {
            'channelId': response['id'],
            'resourceId': response['resourceId'],
            'expiration': response['expiration'],
            'startPageToken': start_page_token
        }
    
        with open(notification_info_path, 'w') as f:
            json.dump(new_info, f)
        
        print(f"Initial start page token: {start_page_token}")

        return new_info

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def check_folder_notifications(service, 
                               file_pattern='*', 
                               call_back_function=None,
                               notification_info=None,
                               notification_info_path="./data/botrun_drive_webhook/notification_info.json"
                               ):

    file_regex = re.compile(file_pattern.replace('*', '.*'))

    try:
        start_page_token = None
        if notification_info:
            start_page_token = notification_info['startPageToken']
        else:
            with open(notification_info_path, 'r') as f:
                notification_info = json.load(f)
            start_page_token = notification_info['startPageToken']

        response = service.changes().list(
            pageToken=start_page_token,
            spaces='drive',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            pageSize=1000,
            fields='newStartPageToken, changes(fileId, time, file(name, parents))'
        ).execute()

        if 'newStartPageToken' in response:
            new_start_page_token = response['newStartPageToken']
            notification_info['startPageToken'] = new_start_page_token
            with open(notification_info_path, 'w') as f:
                json.dump(notification_info, f)
            
            str_change_info = "Change detected!" if start_page_token != new_start_page_token else "No change."
            print(f"[check_folder_notifications] Get new page token: {new_start_page_token}  status={str_change_info}")
            start_page_token = new_start_page_token
        
        
        #print("==============change=====")
        #demo_change = response.get('changes', [])
        #print(demo_change)
        #print("==============change end====")


        for change in response.get('changes', []):
            print(f"Changed file:")
            file_id = change.get('fileId', 'N/A')
            updated_time = change.get('time', 'N/A')
            print(f"File ID: {file_id}")
            print(f"Change Time: {updated_time}")
            
            if 'file' in change:
                file_info = change['file']
                file_name = file_info.get('name', 'N/A')
                parents = file_info.get('parents', 'N/A')
                print(f"File Name: {file_name}")
                print(f"Parent Folder IDs: {', '.join(parents)}")


                if call_back_function and file_regex.match(file_name):
                    # Call the callback function
                    call_back_function(file_id, file_name, updated_time, parents)
                    print("Callback function executed.")
            else:
                print("File information not available (possibly deleted)")

            print("---")
        print(f"""Done. time={time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}""")

    except Exception as e:
        print(f"[check_folder_notifications] An error occurred: {e}")
        # If the error is due to channel expiration, reinitialize the webhook

        print(f"""Exception! time={time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}""")
    

# Example usage:
# def my_callback(file_id, file_name, updated_time, file_path=None):
#     print(f"File {file_name} (ID: {file_id}) was updated at {updated_time}")
#     if file_path:
#         print(f"File path: {file_path}")

# botrun_drive_webhook(
#     service_account_file='path/to/service_account.json',
#     folder_id='your_folder_id',
#     webhook_url='your_webhook_url',
#     file_pattern='*.txt',
#     call_back_function=my_callback
# )


# interface for get the update queue
def get_update_queue(time=None, check_interval=60, limit=100): # check_interval=60 秒之前的資料, limit=100 個檔案 (最多處理100分鐘)
    env_data_dir = os.getenv("BOTRUN_DRIVE_WEBHOOK_FOLDER", "./data/botrun_drive_webhook/")
    env_service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    print(f"env_queue_data_dir={env_data_dir}")
    #print(f"env_service_account_file={env_service_account_file}")

    # 初始化 update queue
    file_update_queue = FileUpdateQueue(service_account_file=env_service_account_file,
                                        data_dir=env_data_dir)

    updated_list, latest_file = file_update_queue.process_update_queue(check_interval=check_interval, limit=limit)
    print(f"更新列表: {updated_list}")
    print(f"最新檔案: {latest_file}")

    print("[get_update_queue] done")
    return updated_list, latest_file

# interface for finish the queue process
def finish_queue_process(latest_file=None, collection_id=None, file_id=None, updated_time=None):
    info=""
    if latest_file:

        env_data_dir = os.getenv("BOTRUN_DRIVE_WEBHOOK_FOLDER", "./data/botrun_drive_webhook/")
        env_service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        print(f"env_service_account_file={env_service_account_file}")

        # 初始化 update queue
        file_update_queue = FileUpdateQueue(service_account_file=env_service_account_file,
                                            data_dir=env_data_dir)

        info=file_update_queue.finish_queue_process(latest_file)

        info+=f"\n[finish_queue_process] done"
        print(info)
    return info


def register_folder_ids_from_csv(csv_url, file_update_queue, cache_dir="./data/botrun_drive_webhook/cache", cache_duration=2):
    try:
        # 創建緩存目錄（如果不存在）
        os.makedirs(cache_dir, exist_ok=True)
        
        # 生成緩存文件路徑
        cache_file = os.path.join(cache_dir, "folder_ids.csv")
        
        # 檢查是否需要更新緩存
        should_update = True
        if os.path.exists(cache_file):
            file_time = os.path.getmtime(cache_file)
            if datetime.datetime.now() - datetime.datetime.fromtimestamp(file_time) < datetime.timedelta(hours=cache_duration):
                should_update = False
        
        # 如果需要更新，則下載新的 CSV 文件
        if should_update:
            try:
                response = requests.get(csv_url)
                response.raise_for_status()
                
                with open(cache_file, 'w', newline='', encoding='utf-8') as f:
                    f.write(response.text)
                
                print("監控資料夾 id 清單的 CSV 文件已更新")
            except requests.RequestException as e:
                print(f"下載 監控資料夾 id 清單的 CSV 文件時發生錯誤: {e}")
                if not os.path.exists(cache_file):
                    raise  # 如果缓存文件不存在，则抛出异常
        else:
            print("使用緩存的 監控資料夾 id 清單的 CSV 文件")
        
        # 讀取 CSV 文件
        with open(cache_file, 'r', newline='', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            
            # 跳過第一行（解說資訊）
            next(csv_reader, None)
            
            # 遍歷剩餘的行，提取 collection_id 並註冊
            for row in csv_reader:
                collection_id = row.get('collection_id', None)
                mode = row.get('mode', None)
                if collection_id:
                    file_update_queue.register_folder_ids(collection_id, mode)
        
        print("所有 collection_id 已成功註冊")
    except IOError as e:
        print(f"讀取 監控資料夾 id 清單的 CSV 文件時發生錯誤: {e}")
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")



def monitor_update(*args):
    print("Hello, world! botrun_drive_webhook")

    env_data_dir = os.getenv("BOTRUN_DRIVE_WEBHOOK_FOLDER", "./data/botrun_drive_webhook/")
    env_service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    #print(f"env_service_account_file={env_service_account_file}")

    # 初始化 update queue，註冊要監控的 google drive folder id
    file_update_queue = FileUpdateQueue(service_account_file=env_service_account_file,
                                        data_dir=env_data_dir)
    
    csv_url=os.getenv("BOTRUN_DRIVE_WEBHOOK_REG_FOLDERIDS", None) 
    register_folder_ids_from_csv(csv_url=csv_url, file_update_queue=file_update_queue) # 改成讀取 google sheet

    # call back function 下方檢查到要更新時，才會呼叫這個 funciton
    def do_update_queue(file_id, file_name, updated_time, parents_id):
        print("DoUpdateQueue()...")
        print(f"file_id={file_id}, file_name={file_name}, updated_time={updated_time}, parents_id={parents_id}")
        # 模擬檔案變更
        file_update_queue.update_function(
                file_id=file_id,
                file_name=file_name,
                updated_time=updated_time,
                parent_folderid=parents_id[0]
        )

    # 呼叫 google drive notification 檢查是否有檔案更新
    env_service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    #print(f"env_service_account_file={env_service_account_file}")
    print("---botrun_drive_webhook start---")
    botrun_drive_webhook(        
            service_account_file=env_service_account_file, #os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            folder_id=os.getenv("BOTRUN_DRIVE_WEBHOOK_DEFAULT_FOLDERID"),
            force_reset_webhook_channel=False,
            webhook_url=os.getenv("BOTRUN_DRIVE_WEBHOOK_NOTIFICATION_URL"),
            file_pattern='*', 
            call_back_function=do_update_queue,
            notification_info_path=f"{env_data_dir}notification_info.json"
    )
    print("---botrun_drive_webhook done---")

    print("---botrun_drive_crontab start---")
    file_update_queue.update_crontab()
    print("---botrun_drive_crontab done---")

def main(*args):
    monitor_update(*args)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        args = sys.argv[2:]  # 所有其他參數
        print(f"[main] function_name={function_name}")
        
        if function_name == "get_update_queue":
            get_update_queue(*args)
        if function_name == "finish_queue_process":
            finish_queue_process(*args)
        if function_name == "botrun_drive_webhook":
            main(*args)
        if function_name == "botrun_drive_webhook_orig":
            botrun_drive_webhook(*args)
        if function_name == "monitor_update":
            monitor_update(*args)

    else:
        print(f"[main] call main function")
        main()
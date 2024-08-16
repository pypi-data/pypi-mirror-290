import os
import requests
from tqdm import tqdm
from .login import LoginClass
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class HttpToolClient:
    errtime = 0

    def __init__(self):
        self.base_url = "http://121.40.53.97:8080"
        self.model_search_url = "http://121.40.53.97:8081/search"

    def upload_file(self, file_path):
        login_instance=LoginClass()
        token = login_instance.load_token()

        url = f"{self.base_url}/upload/import"


        with open(file_path, 'rb') as file:
            
            e = MultipartEncoder(fields={'insts': ('filename', file)})
            # 上传进度条，unit=B 单位为字节
            bar = tqdm(range(0,e.len), unit='B', unit_scale=True, desc='Uploading')
            # 回调更新进度条
            def my_callback(monitor):
                bar.update(monitor.bytes_read - bar.n)
                bar.refresh() 

            m = MultipartEncoderMonitor(e, my_callback)
            headers = {
                'Authorization': token,
                'user-Agent'   : 'ostutor/tool',
                'Content-Type': m.content_type
            }
            response = requests.post(url, data=m, headers=headers)
            bar.close()
            if response.status_code == 200:
                print("File uploaded successfully.")
            elif response.status_code == 403 and self.errtime < 1:
                    self.errtime+=1
                    import click
                    login=LoginClass()
                    username = click.prompt("Email")
                    password = click.prompt("Password", hide_input=True)
                    login.login( username, password)
                    self.upload_file(file_path)
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
                print(response.text)
                return

    def download_file(self, file_name, save_dir, uuid):
        url = f"{self.base_url}/export/downloadinst?uuid={uuid}"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(save_dir, exist_ok=True)

            save_path = os.path.join(save_dir, file_name)

            # Get the total file size from the response headers
            total_size = int(response.headers.get('content-length', 0))
            with open(save_path, 'wb') as file, tqdm(
                desc='Downloading',
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk: 
                        file.write(chunk)
                        bar.update(len(chunk))
            
            # print(f"File downloaded successfully and saved to {save_path}.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            print(response.text)


    def model_search(self, keyword):
        import json
        response = requests.get(self.model_search_url,params={"keyword":keyword})
        try:
            return response.json()
        except json.JSONDecodeError:
            return "error"
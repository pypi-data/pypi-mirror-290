import requests
import json
from .config import cfg

class LoginClass:
    def __init__(self):
        self.base_url = "http://121.40.53.97/signon/login"
        self.token=None

    def login(self, email, password):
        data = {
            'email': email,
            'password': password
        }
        headers = {
            'user-Agent'   : 'ostutor/tool'
        }
        response = requests.post(self.base_url, data=data, headers=headers)
    
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            print("\nUnable to parse the server response.")
            return
    
        if response.status_code == 200:
            if response_data.get('code') == 0:
                print("\nLogin successful!") 
                self.token = response_data.get('data', {}).get('token')
                self.save_token()  # 将 token 保存到配置文件中
            else:
                print(f"Login Failure: {response_data.get('message')}")
        else:
            print(f"\nLogin Failure: {response_data.get('message')}")

    def save_token(self):
        cfg.update('token', self.token)

    def load_token(self):
        self.token = cfg.get('token')
        return self.token

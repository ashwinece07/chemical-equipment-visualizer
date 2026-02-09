import requests
import json
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api/"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_data: Optional[Dict] = None

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def signup(self, username: str, email: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}signup/",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 201:
            data = response.json()
            self.access_token = data.get("access")
            self.refresh_token = data.get("refresh")
            self.user_data = data.get("user")
        return response.json()

    def login(self, username: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access")
            self.refresh_token = data.get("refresh")
            self.user_data = data.get("user")
        return response.json()

    def logout(self) -> bool:
        if not self.refresh_token:
            return False
        try:
            requests.post(
                f"{self.base_url}logout/",
                json={"refresh_token": self.refresh_token},
                headers=self._headers()
            )
        except:
            pass
        self.access_token = None
        self.refresh_token = None
        self.user_data = None
        return True

    def get_profile(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}profile/", headers=self._headers())
        return response.json()

    def update_profile(self, data: Dict) -> Dict[str, Any]:
        response = requests.put(f"{self.base_url}profile/", json=data, headers=self._headers())
        return response.json()

    def change_password(self, old_password: str, new_password: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}profile/password/",
            json={"old_password": old_password, "new_password": new_password},
            headers=self._headers()
        )
        return response.json()

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{self.base_url}upload/", files=files, headers=headers)
        return response.json()

    def get_analysis(self, file_id: int) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}analysis/{file_id}/", headers=self._headers())
        return response.json()

    def get_history(self) -> list:
        response = requests.get(f"{self.base_url}history/", headers=self._headers())
        return response.json()

    def delete_file(self, file_id: int) -> bool:
        response = requests.delete(f"{self.base_url}delete/{file_id}/", headers=self._headers())
        return response.status_code == 200

    def compare_datasets(self, file_id_1: int, file_id_2: int) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}compare/",
            json={"file_id_1": file_id_1, "file_id_2": file_id_2},
            headers=self._headers()
        )
        return response.json()

    def export_pdf(self, file_id: int, password: str) -> bytes:
        response = requests.post(
            f"{self.base_url}export/pdf/{file_id}/",
            json={"password": password},
            headers=self._headers()
        )
        return response.content

    def export_excel(self, file_id: int, password: str) -> bytes:
        response = requests.post(
            f"{self.base_url}export/excel/{file_id}/",
            json={"password": password},
            headers=self._headers()
        )
        return response.content

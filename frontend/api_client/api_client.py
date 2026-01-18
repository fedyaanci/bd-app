import httpx
from typing import Optional, Dict, Any, List

class AsyncAPIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def set_token(self, token: str):
        """Установить токен авторизации"""
        self.token = token
    
    def clear_token(self):
        """Очистить токен"""
        self.token = None
    
    def _headers(self):
        """Получить заголовки с токеном"""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    # ========== USER ENDPOINTS ==========
    
    async def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Вход в систему"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/users/login",
                    json={"username": username, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.set_token(data["access_token"])
                    return data
                return None
        except Exception as e:
            print(f"Login error: {e}")
            return None
    
    async def register(self, username: str, password: str, is_artist: bool = False, avatar_url: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Регистрация нового пользователя"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "username": username,
                    "password": password,
                    "is_artist": is_artist
                }
                if avatar_url:
                    payload["avatar_url"] = avatar_url
                    
                response = await client.post(
                    f"{self.base_url}/users/register",
                    json=payload
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Register error: {e}")
            return None
    
    async def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Получить информацию о текущем пользователе"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/users/me",
                    headers=self._headers()
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Get current user error: {e}")
            return None
    
    # ========== ARTWORK ENDPOINTS ==========
    
    async def get_artworks(self) -> List[Dict[str, Any]]:
        """Получить все работы"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/artworks/")
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"Get artworks error: {e}")
            return []
    
    async def get_artwork(self, artwork_id: int) -> Optional[Dict[str, Any]]:
        """Получить работу по ID"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/artworks/{artwork_id}")
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Get artwork error: {e}")
            return None
    
    async def create_artwork(self, title: str, image_url: str) -> Optional[Dict[str, Any]]:
        """Создать новую работу (только для художников)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/artworks/create",
                    json={"title": title, "image_url": image_url},
                    headers=self._headers()
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Create artwork error: {e}")
            return None
    
    # ========== LISTING ENDPOINTS ==========
    
    async def get_listings(self) -> List[Dict[str, Any]]:
        """Получить все листинги"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/listing/")
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"Get listings error: {e}")
            return []
    
    async def create_listing(self, artwork_id: int, price: float) -> Optional[Dict[str, Any]]:
        """Создать новый листинг (только для художников)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/listing/",
                    json={"artwork_id": artwork_id, "price": price},
                    headers=self._headers()
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Create listing error: {e}")
            return None
    
    # ========== ORDER ENDPOINTS ==========
    
    async def create_order(self, listing_id: int) -> Optional[Dict[str, Any]]:
        """Создать заказ (купить листинг)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/orders/create",
                    json={"listing_id": listing_id},
                    headers=self._headers()
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Create order error: {e}")
            return None
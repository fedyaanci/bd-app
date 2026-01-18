import flet as ft
from api_client.api_client import AsyncAPIClient
from state import get_state, set_state

class LoginPage(ft.View):
    def __init__(self, page: ft.Page, api_client: AsyncAPIClient):
        super().__init__(route="/login")
        self._page_ref = page
        self.api_client = api_client
        
        self.username_field = ft.TextField(
            label="Имя пользователя",
            autofocus=True,
            width=300
        )
        
        self.password_field = ft.TextField(
            label="Пароль",
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        self.error_text = ft.Text(
            value="",
            color=ft.Colors.RED,
            visible=False
        )
        
        self.login_button = ft.ElevatedButton(
            "Войти",
            on_click=self.login_click,
            width=300
        )
        
        self.appbar = ft.AppBar(
            title=ft.Text("Вход"),
            bgcolor=ft.Colors.PURPLE_800
        )
        
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Вход в систему", size=24, weight="bold"),
                        ft.Divider(height=20),
                        self.username_field,
                        self.password_field,
                        self.error_text,
                        self.login_button,
                        ft.TextButton(
                            "Нет аккаунта? Зарегистрируйтесь",
                            on_click=lambda e: self._page_ref.go("/register")
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=20,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ]
    
    async def do_login(self, username: str, password: str):
        """Асинхронная функция для входа"""
        result = await self.api_client.login(username, password)
        if result:
            # Получаем информацию о пользователе
            user = await self.api_client.get_current_user()
            if user:
                set_state("user_id", user["id"])
                set_state("username", user["username"])
                set_state("is_artist", user["is_artist"])
                set_state("token", self.api_client.token)
                
                # Перенаправляем на нужную страницу
                if user["is_artist"]:
                    self._page_ref.go("/artist")
                else:
                    self._page_ref.go("/buyer")
            else:
                self.show_error("Не удалось получить информацию о пользователе")
        else:
            self.show_error("Неверное имя пользователя или пароль")
        
        self.login_button.disabled = False
        self._page_ref.update()
    
    def login_click(self, e):
        """Обработчик нажатия кнопки входа"""
        username = self.username_field.value
        password = self.password_field.value
        
        if not username or not password:
            self.show_error("Заполните все поля")
            return
        
        self.login_button.disabled = True
        self.hide_error()
        self._page_ref.update()
        
        self._page_ref.run_task(self.do_login, username, password)
    
    def show_error(self, message: str):
        """Показать сообщение об ошибке"""
        self.error_text.value = message
        self.error_text.visible = True
        self._page_ref.update()
    
    def hide_error(self):
        """Скрыть сообщение об ошибке"""
        self.error_text.visible = False
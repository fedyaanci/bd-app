import flet as ft
from api_client.api_client import AsyncAPIClient

class RegisterPage(ft.View):
    def __init__(self, page: ft.Page, api_client: AsyncAPIClient):
        super().__init__(route="/register")
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
        
        self.confirm_password_field = ft.TextField(
            label="Подтвердите пароль",
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        self.is_artist_checkbox = ft.Checkbox(
            label="Я художник",
            value=False
        )
        
        self.error_text = ft.Text(
            value="",
            color=ft.Colors.RED,
            visible=False
        )
        
        self.success_text = ft.Text(
            value="",
            color=ft.Colors.GREEN,
            visible=False
        )
        
        self.register_button = ft.ElevatedButton(
            "Зарегистрироваться",
            on_click=self.register_click,
            width=300
        )
        
        self.appbar = ft.AppBar(
            title=ft.Text("Регистрация"),
            bgcolor=ft.Colors.PURPLE_800
        )
        
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Регистрация", size=24, weight="bold"),
                        ft.Divider(height=20),
                        self.username_field,
                        self.password_field,
                        self.confirm_password_field,
                        self.is_artist_checkbox,
                        self.error_text,
                        self.success_text,
                        self.register_button,
                        ft.TextButton(
                            "Уже есть аккаунт? Войдите",
                            on_click=lambda e: self._page_ref.go("/login")
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=20,
                alignment=ft.alignment.Axis.VERTICAL,
                expand=True
            )
        ]
    
    async def do_register(self, username: str, password: str, is_artist: bool):
        """Асинхронная функция для регистрации"""
        result = await self.api_client.register(username, password, is_artist)
        if result:
            self.show_success("Регистрация успешна! Перенаправление на страницу входа...")
            # Перенаправляем на страницу входа после небольшой задержки через run_task
            self._page_ref.run_task(self.delayed_redirect)
        else:
            self.show_error("Ошибка регистрации. Возможно, имя пользователя уже занято")
        
        self.register_button.disabled = False
        self._page_ref.update()
    
    def register_click(self, e):
        """Обработчик нажатия кнопки регистрации"""
        username = self.username_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value
        is_artist = self.is_artist_checkbox.value
        
        if not username or not password:
            self.show_error("Заполните все поля")
            return
        
        if password != confirm_password:
            self.show_error("Пароли не совпадают")
            return
        
        if len(password) < 4:
            self.show_error("Пароль должен содержать минимум 4 символа")
            return
        
        self.register_button.disabled = True
        self.hide_error()
        self._page_ref.update()
        
        self._page_ref.run_task(self.do_register, username, password, is_artist)
    
    def show_error(self, message: str):
        """Показать сообщение об ошибке"""
        self.error_text.value = message
        self.error_text.visible = True
        self.success_text.visible = False
        self._page_ref.update()
    
    def show_success(self, message: str):
        """Показать сообщение об успехе"""
        self.success_text.value = message
        self.success_text.visible = True
        self.error_text.visible = False
        self._page_ref.update()
    
    def hide_error(self):
        """Скрыть сообщение об ошибке"""
        self.error_text.visible = False
    
    async def delayed_redirect(self):
        """Перенаправление на страницу входа с небольшой задержкой"""
        import asyncio
        await asyncio.sleep(1.5)
        self._page_ref.go("/login")
        self._page_ref.update()
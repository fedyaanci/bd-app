import flet as ft
from api_client.api_client import AsyncAPIClient
from state import get_state, clear_state

class ArtistPage(ft.View):
    def __init__(self, page: ft.Page, api_client: AsyncAPIClient):
        super().__init__(route="/artist")
        self.page = page
        self.api_client = api_client
        
        # Данные
        self.artworks = []
        self.listings = []
        
        # Диалог создания работы
        self.create_artwork_dialog = self.create_artwork_dialog_ui()
        
        # Диалог создания листинга
        self.create_listing_dialog = self.create_listing_dialog_ui()
        
        # Grid для работ
        self.artworks_grid = ft.GridView(
            expand=1,
            runs_count=3,
            max_extent=250,
            child_aspect_ratio=0.8,
            spacing=10,
            run_spacing=10,
            padding=20
        )
        
        # AppBar
        username = get_state("username") or "Artist"
        self.appbar = ft.AppBar(
            title=ft.Text(f"Панель художника: {username}"),
            bgcolor=ft.Colors.PURPLE_800,
            actions=[
                ft.ElevatedButton("Каталог", on_click=lambda e: self.page.go("/")),
                ft.ElevatedButton("Выйти", on_click=self.logout)
            ]
        )
        
        # Основной контент
        self.controls = [
            ft.Column([
                ft.Row([
                    ft.Text("Мои работы", size=24, weight="bold"),
                    ft.ElevatedButton(
                        "Создать работу",
                        icon=ft.icons.ADD,
                        on_click=self.open_create_artwork_dialog
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=20),
                self.artworks_grid
            ], expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)
        ]
        
        # Загружаем данные
        self.page.run_task(self.load_data)
    
    async def load_data(self):
        """Загрузить все работы и листинги"""
        self.page.snack_bar = ft.SnackBar(ft.Text("Загрузка данных..."))
        self.page.snack_bar.open = True
        self.page.update()
        
        # Получаем все работы
        all_artworks = await self.api_client.get_artworks()
        # Получаем все листинги
        all_listings = await self.api_client.get_listings()
        
        # Фильтруем только работы текущего пользователя
        user_id = get_state("user_id")
        self.artworks = [a for a in all_artworks if a.get("artist_id") == user_id]
        
        # Создаем множество artwork_id из листингов
        artwork_ids_with_listings = {l.get("artwork_id") for l in all_listings}
        
        # Очищаем и заполняем grid
        self.artworks_grid.controls.clear()
        
        for artwork in self.artworks:
            has_listing = artwork["id"] in artwork_ids_with_listings
            card = self.create_artwork_card(artwork, has_listing)
            self.artworks_grid.controls.append(card)
        
        self.page.snack_bar.open = False
        self.page.update()
    
    def create_artwork_card(self, artwork: dict, has_listing: bool) -> ft.Card:
        """Создать карточку работы"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=artwork.get("image_url", ""),
                            width=230,
                            height=150,
                            fit=ft.ImageFit.COVER,
                            error_content=ft.Text("Нет изображения")
                        ),
                        ft.Text(
                            artwork.get("title", "Без названия"),
                            size=14,
                            weight="bold",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Text(
                            "✓ В продаже" if has_listing else "Не в продаже",
                            size=12,
                            color=ft.Colors.GREEN_700 if has_listing else ft.Colors.GREY
                        ),
                        ft.ElevatedButton(
                            "Создать листинг" if not has_listing else "Обновить",
                            on_click=lambda e, aid=artwork["id"]: self.open_create_listing_dialog(aid),
                            width=210,
                            disabled=has_listing
                        )
                    ],
                    spacing=5,
                    tight=True
                ),
                padding=10,
                width=230
            )
        )
    
    def create_artwork_dialog_ui(self):
        """Создать UI диалога создания работы"""
        title_field = ft.TextField(label="Название работы", autofocus=True)
        image_url_field = ft.TextField(label="URL изображения")
        
        create_artwork_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Создать новую работу"),
            content=ft.Column([
                title_field,
                image_url_field
            ], tight=True, width=400),
            actions=[],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        def close_dialog(e):
            create_artwork_dialog.open = False
            self.page.update()
        
        def create_click(e):
            title = title_field.value
            image_url = image_url_field.value
            
            if not title or not image_url:
                self.page.snack_bar = ft.SnackBar(ft.Text("Заполните все поля"))
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            self.page.run_task(self.do_create_artwork, title, image_url)
            close_dialog(e)
        
        create_artwork_dialog.actions = [
            ft.TextButton("Отмена", on_click=close_dialog),
            ft.ElevatedButton("Создать", on_click=create_click)
        ]
        
        return create_artwork_dialog
    
    def create_listing_dialog_ui(self):
        """Создать UI диалога создания листинга"""
        price_field = ft.TextField(label="Цена", suffix_text="₽", autofocus=True)
        
        create_listing_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Создать листинг"),
            content=ft.Column([
                price_field
            ], tight=True, width=400),
            actions=[],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        def close_dialog(e):
            create_listing_dialog.open = False
            self.page.update()
        
        def create_click(e):
            price_str = price_field.value
            
            if not price_str:
                self.page.snack_bar = ft.SnackBar(ft.Text("Введите цену"))
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError("Цена должна быть положительной")
                
                artwork_id = getattr(self, '_current_artwork_id', None)
                if artwork_id:
                    self.page.run_task(self.do_create_listing, artwork_id, price)
                close_dialog(e)
            except ValueError:
                self.page.snack_bar = ft.SnackBar(ft.Text("Введите корректную цену"))
                self.page.snack_bar.open = True
                self.page.update()
        
        create_listing_dialog.actions = [
            ft.TextButton("Отмена", on_click=close_dialog),
            ft.ElevatedButton("Создать", on_click=create_click)
        ]
        
        return create_listing_dialog
    
    def open_create_artwork_dialog(self, e):
        """Открыть диалог создания работы"""
        self.page.dialog = self.create_artwork_dialog
        self.create_artwork_dialog.open = True
        self.page.update()
    
    def open_create_listing_dialog(self, artwork_id: int):
        """Открыть диалог создания листинга"""
        self._current_artwork_id = artwork_id
        self.page.dialog = self.create_listing_dialog
        self.create_listing_dialog.open = True
        self.page.update()
    
    async def do_create_artwork(self, title: str, image_url: str):
        """Асинхронная функция создания работы"""
        result = await self.api_client.create_artwork(title, image_url)
        if result:
            self.page.snack_bar = ft.SnackBar(ft.Text("Работа создана успешно!"))
            self.page.snack_bar.open = True
            await self.load_data()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Ошибка создания работы"))
            self.page.snack_bar.open = True
        
        self.page.update()
    
    async def do_create_listing(self, artwork_id: int, price: float):
        """Асинхронная функция создания листинга"""
        result = await self.api_client.create_listing(artwork_id, price)
        if result:
            self.page.snack_bar = ft.SnackBar(ft.Text("Листинг создан успешно!"))
            self.page.snack_bar.open = True
            await self.load_data()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Ошибка создания листинга"))
            self.page.snack_bar.open = True
        
        self.page.update()
    
    def logout(self, e):
        """Выход из системы"""
        clear_state()
        self.api_client.clear_token()
        self.page.go("/")
        self.page.update()
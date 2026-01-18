import flet as ft
from api_client.api_client import AsyncAPIClient
from state import get_state, set_state, clear_state

class CatalogPage(ft.View):
    def __init__(self, page: ft.Page, api_client: AsyncAPIClient):
        super().__init__(route="/")
        self._page_ref = page
        self.api_client = api_client
    
    # Используем _page_ref для хранения ссылки на page
    # После добавления view в page.views, page будет доступен автоматически
    # Но мы используем _page_ref для совместимости
        self.listings_data = []
        self.artworks_data = {}
        
        # Создаем контейнер для карточек
        self.listings_grid = ft.GridView(
            expand=1,
            runs_count=2,
            max_extent=300,
            child_aspect_ratio=0.8,
            spacing=10,
            run_spacing=10,
            padding=20
        )
        
        # AppBar с кнопками
        user_token = get_state("token")
        actions = [
            ft.ElevatedButton("Login", on_click=self.go_to_login),
            ft.ElevatedButton("Register", on_click=self.go_to_register)
        ]
        
        if user_token:
            username = get_state("username") or "User"
            actions = [
                ft.Text(f"Привет, {username}!", color=ft.Colors.WHITE),
                ft.ElevatedButton("Выйти", on_click=self.logout)
            ]
            self.api_client.set_token(user_token)
        
        self.appbar = ft.AppBar(
            title=ft.Text("Art Marketplace"),
            bgcolor=ft.Colors.PURPLE_800,
            actions=actions
        )
        
        # Основной контент
        self.controls = [
            ft.Column([
                ft.Row([
                    ft.Text("Каталог работ", size=24, weight="bold"),
                    ft.ElevatedButton(
                        "Обновить",
                        #icon=ft.icons.REFRESH,
                        on_click=self.load_listings
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=20),
                self.listings_grid
            ], expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)
        ]
        
        # Загружаем листинги при инициализации (после добавления view в page.views)
        # Отложим загрузку, чтобы page был доступен
    
    async def load_listings_async(self):
        """Асинхронная загрузка листингов"""
        page = self._page_ref
        page.snack_bar = ft.SnackBar(ft.Text("Загрузка каталога..."))
        page.snack_bar.open = True
        page.update()
        
        # Получаем все листинги и работы
        listings = await self.api_client.get_listings()
        artworks = await self.api_client.get_artworks()
        
        # Создаем словарь работ для быстрого доступа
        self.artworks_data = {art["id"]: art for art in artworks}
        
        # Фильтруем только доступные листинги (не проданные)
        available_listings = [l for l in listings if not l.get("is_sold", False)]
        self.listings_data = available_listings
        
        # Очищаем и заполняем grid
        self.listings_grid.controls.clear()
        
        for listing in available_listings:
            artwork_id = listing.get("artwork_id")
            artwork = self.artworks_data.get(artwork_id)
            
            if artwork:
                card = self.create_listing_card(listing, artwork)
                self.listings_grid.controls.append(card)
        
        page = self._page_ref
        page.snack_bar.open = False
        page.update()
    
    def load_listings(self, e):
        """Обработчик кнопки обновления"""
        self._page_ref.run_task(self.load_listings_async)
    
    def create_listing_card(self, listing: dict, artwork: dict) -> ft.Card:
        """Создать карточку листинга"""
        price = float(listing.get("price", 0))
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=artwork.get("image_url", ""),
                            width=280,
                            height=200,
                            error_content=ft.Text("Нет изображения")
                        ),
                        ft.Text(
                            artwork.get("title", "Без названия"),
                            size=16,
                            weight="bold",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Text(
                            f"Цена: {price:.2f} ₽",
                            size=14,
                            color=ft.Colors.GREEN_700,
                            weight="bold"
                        ),
                        ft.ElevatedButton(
                            "Купить",
                            on_click=lambda e, lid=listing["id"]: self.buy_listing(lid),
                            width=250,
                            disabled=not get_state("token")
                        )
                    ],
                    spacing=5,
                    tight=True
                ),
                padding=10,
                width=280
            )
        )
    
    def buy_listing(self, listing_id: int):
        """Обработчик покупки листинга"""
        if not get_state("token"):
            self._page_ref.snack_bar = ft.SnackBar(
                ft.Text("Войдите в систему для покупки")
            )
            self._page_ref.snack_bar.open = True
            self._page_ref.update()
            return
        
        self._page_ref.run_task(self.do_buy_listing, listing_id)
    
    async def do_buy_listing(self, listing_id: int):
        """Асинхронная функция покупки"""
        result = await self.api_client.create_order(listing_id)
        if result:
            self._page_ref.snack_bar = ft.SnackBar(ft.Text("Покупка успешна!"))
            self._page_ref.snack_bar.open = True
            # Перезагружаем листинги
            await self.load_listings_async()
        else:
            self._page_ref.snack_bar = ft.SnackBar(ft.Text("Ошибка покупки"))
            self._page_ref.snack_bar.open = True
        
        self._page_ref.update()
    
    def go_to_login(self, e):
        self._page_ref.go("/login")
        self._page_ref.update()
    
    def go_to_register(self, e):
        self._page_ref.go("/register")
        self._page_ref.update()
    
    def logout(self, e):
        """Выход из системы"""
        clear_state()
        self.api_client.clear_token()
        self._page_ref.go("/")
        self._page_ref.update()
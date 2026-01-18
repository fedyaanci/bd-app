import flet as ft
from api_client.api_client import AsyncAPIClient
from state import get_state, clear_state

class BuyerPage(ft.View):
    def __init__(self, page: ft.Page, api_client: AsyncAPIClient):
        super().__init__(route="/buyer")
        self.page = page
        self.api_client = api_client
        self.listings_data = []
        self.artworks_data = {}
        
        # Grid для листингов
        self.listings_grid = ft.GridView(
            expand=1,
            runs_count=2,
            max_extent=300,
            child_aspect_ratio=0.8,
            spacing=10,
            run_spacing=10,
            padding=20
        )
        
        # AppBar
        username = get_state("username") or "Buyer"
        self.appbar = ft.AppBar(
            title=ft.Text(f"Панель покупателя: {username}"),
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
                    ft.Text("Доступные работы", size=24, weight="bold"),
                    ft.ElevatedButton(
                        "Обновить",
                        icon=ft.icons.REFRESH,
                        on_click=self.load_listings
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=20),
                self.listings_grid
            ], expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)
        ]
        
        # Загружаем листинги
        self.page.run_task(self.load_listings_async)
    
    async def load_listings_async(self):
        """Асинхронная загрузка листингов"""
        self.page.snack_bar = ft.SnackBar(ft.Text("Загрузка каталога..."))
        self.page.snack_bar.open = True
        self.page.update()
        
        # Получаем все листинги и работы
        listings = await self.api_client.get_listings()
        artworks = await self.api_client.get_artworks()
        
        # Создаем словарь работ
        self.artworks_data = {art["id"]: art for art in artworks}
        
        # Фильтруем только доступные листинги (не проданные)
        available_listings = [l for l in listings if not l.get("is_sold", False)]
        self.listings_data = available_listings
        
        # Очищаем и заполняем grid
        self.listings_grid.controls.clear()
        
        user_id = get_state("user_id")
        
        for listing in available_listings:
            artwork_id = listing.get("artwork_id")
            artwork = self.artworks_data.get(artwork_id)
            
            # Не показываем листинги, созданные самим пользователем
            if artwork and listing.get("seller_id") != user_id:
                card = self.create_listing_card(listing, artwork)
                self.listings_grid.controls.append(card)
        
        self.page.snack_bar.open = False
        self.page.update()
    
    def load_listings(self, e):
        """Обработчик кнопки обновления"""
        self.page.run_task(self.load_listings_async)
    
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
                            fit=ft.ImageFit.COVER,
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
                            "Купить сейчас",
                            icon=ft.icons.SHOPPING_CART,
                            on_click=lambda e, lid=listing["id"]: self.buy_listing(lid),
                            width=250,
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREEN_700
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
        self.page.run_task(self.do_buy_listing, listing_id)
    
    async def do_buy_listing(self, listing_id: int):
        """Асинхронная функция покупки"""
        self.page.snack_bar = ft.SnackBar(ft.Text("Обработка покупки..."))
        self.page.snack_bar.open = True
        self.page.update()
        
        result = await self.api_client.create_order(listing_id)
        if result:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("✓ Покупка успешна! Поздравляем с приобретением!"),
                bgcolor=ft.Colors.GREEN
            )
            self.page.snack_bar.open = True
            # Перезагружаем листинги
            await self.load_listings_async()
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("✗ Ошибка покупки. Попробуйте снова."),
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
        
        self.page.update()
    
    def logout(self, e):
        """Выход из системы"""
        clear_state()
        self.api_client.clear_token()
        self.page.go("/")
        self.page.update()
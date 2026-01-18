import flet as ft
from api_client.api_client import AsyncAPIClient
from pages.catalog import CatalogPage
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.artist import ArtistPage
from pages.buyer import BuyerPage
from state import get_state

def main(page: ft.Page):

    page.title = "Art Marketplace"
    page.window.width = 900
    page.window.height = 600
    page.window.min_width = 800
    page.window.min_height = 600
    
    # Создаем API клиент
    api_client = AsyncAPIClient()
    
    # Восстанавливаем токен из состояния
    saved_token = get_state("token")
    if saved_token:
        api_client.set_token(saved_token)
    
    def route_change(e):
        """Обработчик изменения маршрута"""
        # Получаем текущий route (может быть None при первом вызове)
        route = page.route if hasattr(page, 'route') and page.route else "/"
        
        page.views.clear()
        
        # Проверяем авторизацию для защищенных страниц
        protected_routes = ["/artist", "/buyer"]
        if route in protected_routes:
            if not api_client.token:
                page.route = "/login"
                route = "/login"
        
        # Создаем нужную страницу
        view = None
        if route == "/" or route == "":
            view = CatalogPage(page, api_client)
            page.views.append(view)
        elif route == "/login":
            view = LoginPage(page, api_client)
            page.views.append(view)
        elif route == "/register":
            view = RegisterPage(page, api_client)
            page.views.append(view)
        elif route == "/artist":
            view = ArtistPage(page, api_client)
            page.views.append(view)
        elif route == "/buyer":
            view = BuyerPage(page, api_client)
            page.views.append(view)
        else:
            # Неизвестный маршрут - перенаправляем на главную
            page.route = "/"
            view = CatalogPage(page, api_client)
            page.views.append(view)
        
        page.update()
        
        # Запускаем асинхронную загрузку данных для каталога после добавления view
        if route == "/" or route == "":
            page.run_task(view.load_listings_async)
    
    def view_pop(e):
        """Обработчик возврата назад"""
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    # Устанавливаем обработчики
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Инициализируем начальную страницу
    # page.route может быть None при первом вызове, поэтому устанавливаем "/"
    if not hasattr(page, 'route') or not page.route or page.route == "":
        page.route = "/"
    
    # Вызываем route_change вручную для инициализации первой страницы
    # Это гарантирует, что первая страница будет отображена
    try:
        route_change(None)
    except Exception as ex:
        # Если что-то пошло не так, просто переходим на главную
        print(f"Error initializing route: {ex}")
        page.route = "/"
        page.views.clear()
        page.views.append(CatalogPage(page, api_client))
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
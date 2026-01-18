# Глобальное хранилище состояния приложения
app_state = {
    "token": None,
    "user_id": None,
    "username": None,
    "is_artist": None
}

def get_state(key):
    """Получить значение из состояния"""
    return app_state.get(key)

def set_state(key, value):
    """Установить значение в состояние"""
    app_state[key] = value

def clear_state():
    """Очистить состояние"""
    app_state.clear()
    app_state.update({
        "token": None,
        "user_id": None,
        "username": None,
        "is_artist": None
    })

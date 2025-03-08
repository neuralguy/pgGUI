import pygame
from .Widgets import WidgetManager


class Scene:
    def __init__(self, name: str):
        """
        Базовый класс для сцен.

        :param name: Имя сцены.
        """
        self.name = name  # Имя сцены
        self.widget_manager = WidgetManager()  # Менеджер виджетов для управления элементами сцены
        self.background_color = (240, 240, 240)  # Цвет фона сцены по умолчанию
        self.background_image = None  # Изображение фона сцены (опционально)
        self.is_initialized = False  # Флаг инициализации сцены

    def on_enter(self, previous_scene=None, data=None):
        """
        Вызывается при активации сцены.

        :param previous_scene: Предыдущая сцена (если есть).
        :param data: Данные, переданные при переходе на сцену.
        """
        if not self.is_initialized:
            self.setup()  # Инициализация сцены при первом входе
            self.is_initialized = True
        self.on_resume(data)  # Вызов метода возобновления

    def on_exit(self):
        """
        Вызывается при деактивации сцены.
        """
        pass

    def on_resume(self, data=None):
        """
        Вызывается при возврате на сцену из другой сцены.

        :param data: Данные, переданные при возврате на сцену.
        """
        pass

    def on_pause(self):
        """
        Вызывается при переходе с этой сцены на другую.
        """
        pass

    def setup(self):
        """
        Инициализация сцены. Должна быть переопределена в дочерних классах.
        """
        pass

    def handle_events(self, event: pygame.event.Event):
        """
        Обработка событий сцены.

        :param event: Событие Pygame.
        """
        self.widget_manager.handle_events(event)  # Передача событий менеджеру виджетов

    def update(self):
        """
        Обновление состояния сцены.
        """
        self.widget_manager.update()  # Обновление виджетов через менеджер

    def draw(self, surface: pygame.Surface):
        """
        Отрисовка сцены.

        :param surface: Поверхность для отрисовки.
        """
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(self.background_color)
        self.widget_manager.draw(surface)  # Отрисовка виджетов через менеджер
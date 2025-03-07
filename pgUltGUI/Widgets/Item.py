import pygame
from .Widget import Widget
from .Image import Image


class Item:
    def __init__(self, image: str or pygame.Surface, name: str = "Item", description: str = "", 
                 is_available: bool = True, quantity: int = 1, 
                 on_click: callable = None, data: dict = None):
        """
        Инициализация элемента.

        :param image: Путь к изображению или объект pygame.Surface.
        :param name: Название элемента.
        :param description: Описание элемента.
        :param is_available: Доступность элемента (можно ли использовать).
        :param quantity: Количество элемента.
        :param on_click: Функция, вызываемая при клике на элемент.
        :param data: Дополнительные данные элемента (словарь).
        """
        self.name = name  # Название элемента
        self.description = description  # Описание элемента
        self.is_available = is_available  # Доступность элемента
        self.quantity = quantity  # Количество элемента
        self.on_click = on_click  # Функция, вызываемая при клике
        self.data = data  # Дополнительные данные элемента

        # Загрузка изображения
        if isinstance(image, str):
            # Загрузка изображения из файла
            self.image_surface = pygame.image.load(image).convert_alpha()
        elif isinstance(image, pygame.Surface):
            # Использование переданной поверхности
            self.image_surface = image
        else:
            # Если изображение не передано, используем None
            self.image_surface = None
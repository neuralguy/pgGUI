import pygame
from .Widget import Widget


class Label(Widget):
    def __init__(self, x: int, y: int, text: str, 
                 font: pygame.font.Font = None, text_color: tuple = (255, 255, 255),
                 **kwargs):
        """
        Инициализация текстовой метки.

        :param x: Координата X верхнего левого угла метки.
        :param y: Координата Y верхнего левого угла метки.
        :param text: Текст, отображаемый на метке.
        :param font: Шрифт текста. Если None, используется шрифт по умолчанию.
        :param text_color: Цвет текста.
        :param kwargs: Дополнительные аргументы для родительского класса Widget.
        """
        # Инициализация родительского класса Widget
        super().__init__(x, y, **kwargs)

        # Основные свойства метки
        self.text = text  # Текст метки
        self.font = font or pygame.font.Font(None, 24)  # Шрифт текста (по умолчанию размер 24)
        self.text_color = text_color  # Цвет текста
        self.text_surface = self.font.render(self.text, True, self.text_color)  # Поверхность с текстом
        
        # Автоматические размеры метки на основе текста и отступов
        text_width, text_height = self.font.size(text)
        self.auto_width = text_width + self.padding['left'] + self.padding['right']
        self.auto_height = text_height + self.padding['top'] + self.padding['bottom']

        self._update_rect()

        self.text_rect = self.text_surface.get_rect(center=(
            self.rect.left + self.rect.width // 2 - self.padding['left'] + self.padding['right'],
            self.rect.top + self.rect.height // 2 - self.padding['bottom'] + self.padding['top']
        ))
        
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Отрисовка метки на указанной поверхности.

        :param surface: Поверхность для отрисовки.
        """
        # Отрисовка фона метки (если он есть)
        self.render_background(surface)
        # Отрисовка текста на метке
        surface.blit(self.text_surface, self.text_rect)
import pygame
from .Widget import Widget


class Slider(Widget):
    def __init__(self, x: int, y: int, width: int = 200, height: int = 20, 
                min_val: int = 0, max_val: int = 100, 
                orientation: str = 'horizontal',
                track_color: tuple = (200, 200, 200),
                fill_color: tuple = (150, 0, 250),
                handle_color: tuple = (50, 150, 250),
                handle_hover_color: tuple = (80, 180, 250),
                handle_radius: int = 8,
                text_color: tuple = (0, 0, 0),
                font: pygame.font.Font = None,
                **kwargs):
        """
        Инициализация слайдера.

        :param x: Координата X слайдера.
        :param y: Координата Y слайдера.
        :param width: Ширина слайдера.
        :param height: Высота слайдера.
        :param min_val: Минимальное значение слайдера.
        :param max_val: Максимальное значение слайдера.
        :param orientation: Ориентация слайдера ('horizontal' или 'vertical').
        :param track_color: Цвет трека слайдера.
        :param fill_color: Цвет заполненной части слайдера.
        :param handle_color: Цвет ползунка.
        :param handle_hover_color: Цвет ползунка при наведении.
        :param handle_radius: Радиус ползунка.
        :param text_color: Цвет текста значения слайдера.
        :param font: Шрифт для отображения значения слайдера.
        :param kwargs: Дополнительные параметры для базового класса Widget.
        """
        super().__init__(x, y, width, height, **kwargs)
        
        # Параметры слайдера
        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val  # Текущее значение слайдера
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)  # Прямоугольник слайдера
        self.orientation = orientation.lower()  # Ориентация слайдера
        self.text_color = text_color
        self.font = font or pygame.font.Font(None, 32)  # Шрифт по умолчанию
        
        # Цветовые параметры
        self.track_color = track_color
        self.fill_color = fill_color
        self.handle_color = handle_color
        self.handle_hover_color = handle_hover_color
        self.handle_radius = handle_radius
        
        # Состояния слайдера
        self.is_dragging = False  # Флаг перетаскивания ползунка
        self.is_hovered = False   # Флаг наведения на ползунок
        
        # Автоматическая настройка размеров для вертикальной ориентации
        if self.orientation == 'vertical':
            self.width, self.height = height, width
            self.rect = pygame.Rect(x, y, self.width, self.height)

    def handle_event(self, event: pygame.event.Event):
        """
        Обработка событий слайдера.

        :param event: Событие Pygame.
        """
        mouse_pos = pygame.mouse.get_pos()
        handle_rect = self._get_handle_rect()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.is_dragging = True
                self._update_value_from_mouse(mouse_pos)
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
            
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = handle_rect.collidepoint(mouse_pos)
            if self.is_dragging:
                self._update_value_from_mouse(mouse_pos)

    def _update_value_from_mouse(self, mouse_pos: tuple):
        """
        Обновление значения слайдера на основе позиции мыши.

        :param mouse_pos: Позиция мыши (x, y).
        """
        if self.orientation == 'horizontal':
            pos = mouse_pos[0] - self.rect.left
            total = self.rect.width
        else:  # Вертикальная ориентация
            pos = self.rect.bottom - mouse_pos[1]  # Инверсия для вертикального слайдера
            total = self.rect.height


        pos = max(0, min(pos, total))
        self.value = self.min_val + (pos / total) * (self.max_val - self.min_val)    

    def render(self, surface: pygame.Surface):
        """
        Отрисовка слайдера на поверхности.

        :param surface: Поверхность для отрисовки.
        """
        # Отрисовка трека
        pygame.draw.rect(surface, self.track_color, self.rect, border_radius=4)
        
        # Отрисовка заполненной части
        fill_rect = self._get_fill_rect()
        pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=4)
        
        # Отрисовка ползунка
        handle_rect = self._get_handle_rect()
        handle_color = self.handle_hover_color if (self.is_hovered or self.is_dragging) else self.handle_color
        pygame.draw.circle(surface, handle_color, handle_rect.center, self.handle_radius)
        
        # Эффект глубины для ползунка
        pygame.draw.circle(surface, (0, 0, 0), handle_rect.center, self.handle_radius, 1)

        # Отрисовка значения
        self._draw_value(surface)

    def _draw_value(self, surface: pygame.Surface):
        """
        Отрисовка текущего значения слайдера.

        :param surface: Поверхность для отрисовки.
        """
        text = f"{float(self.value):,.2f}".rstrip('0').rstrip('.')
        text_surf = self.font.render(text, True, self.text_color)

        if self.orientation == "vertical":
            # Вертикальный текст с поворотом
            text_surf = pygame.transform.rotate(text_surf, 90)

        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def _get_handle_rect(self) -> pygame.Rect:
        """
        Получение прямоугольника ползунка.

        :return: Прямоугольник ползунка.
        """
        if self.orientation == 'horizontal':
            handle_x = self.rect.left + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            return pygame.Rect(handle_x - self.handle_radius,
                               self.rect.centery - self.handle_radius,
                               self.handle_radius * 2,
                               self.handle_radius * 2)
        else:  # Вертикальная ориентация
            # Инвертируем расчет позиции для вертикального слайдера
            handle_y = self.rect.bottom - (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.height
            return pygame.Rect(self.rect.centerx - self.handle_radius,
                               handle_y - self.handle_radius,
                               self.handle_radius * 2,
                               self.handle_radius * 2)

    def _get_fill_rect(self) -> pygame.Rect:
        """
        Получение прямоугольника заполненной части слайдера.

        :return: Прямоугольник заполненной части.
        """
        if self.orientation == 'horizontal':
            fill_width = (self.value - self.min_val)/(self.max_val - self.min_val) * self.rect.width
            return pygame.Rect(self.rect.left, self.rect.top, fill_width, self.rect.height)
        else:
            fill_height = (self.value - self.min_val)/(self.max_val - self.min_val) * self.rect.height
            return pygame.Rect(self.rect.left, self.rect.bottom - fill_height, 
                             self.rect.width, fill_height)
import pygame
from .Widget import Widget


class ProgressBar(Widget):
    def __init__(self, x: int, y: int, width: int = 200, height: int = 20, 
                min_val: int = 0, max_val: int = 100, value: int = 0,
                orientation: str = 'horizontal', 
                background_color: tuple = (200, 200, 200),
                fill_color: tuple = (150, 0, 250), 
                border_radius: int = 4, show_text: bool = True,
                text_color: tuple = (0, 0, 0), 
                font: pygame.font.Font = None,
                text_format: str = "{percent}%",
                animation_speed: int = 10):
        """
        Инициализация прогресс-бара.

        :param x: Координата X прогресс-бара.
        :param y: Координата Y прогресс-бара.
        :param width: Ширина прогресс-бара.
        :param height: Высота прогресс-бара.
        :param min_val: Минимальное значение шкалы.
        :param max_val: Максимальное значение шкалы.
        :param value: Начальное значение прогресс-бара.
        :param orientation: Ориентация ('horizontal' или 'vertical').
        :param background_color: Цвет фона прогресс-бара.
        :param fill_color: Цвет заполненной части.
        :param border_radius: Скругление углов элементов.
        :param show_text: Отображать текстовое значение.
        :param text_color: Цвет текста.
        :param font: Шрифт для текста (по умолчанию размер 24).
        :param text_format: Формат строки для отображения:
            {value} - текущее значение
            {percent} - процент заполнения
            {min} - минимальное значение
            {max} - максимальное значение
        :param animation_speed: Скорость анимации изменения значения (ед./сек).
        """
        super().__init__(x, y, width, height)
        
        # Основные параметры
        self.min_val = min_val
        self.max_val = max_val
        self._target_value = value
        self._current_value = value or min_val
        self.orientation = orientation.lower()
        self.border_radius = border_radius
        self.show_text = show_text
        self.text_format = text_format
        self.animation_speed = animation_speed
        
        # Цветовые параметры
        self.background_color = background_color
        self.fill_color = fill_color
        self.text_color = text_color
        
        # Текст и шрифт
        self.font = font or pygame.font.Font(None, 24)
        
        # Состояния анимации
        self._is_animating = False
        self._animation_queue = []
        self._current_animation = None
        self.last_update_time = pygame.time.get_ticks()

        # Автоматическая настройка размеров
        if self.orientation == 'vertical':
            self._width, self._height = height, width
            self.rect = pygame.Rect(x, y, self._width, self._height)

        self._update_rect()

    def to_value(self, value: float, animation_speed: int = 0):
        """
        Плавное изменение значения прогресс-бара.

        :param value: Целевое значение.
        :param animation_speed: Скорость анимации (0 - использовать значение по умолчанию).
        """
        if value != self._current_value:
            target = max(self.min_val, min(value, self.max_val))
            speed = animation_speed or self.animation_speed
            self._animation_queue.append({
                'target': target,
                'speed': speed
            })

            if not self._is_animating:
                self._start_next_animation()

    def _start_next_animation(self):
        """Запуск следующей анимации из очереди."""
        if self._animation_queue:
            params = self._animation_queue.pop(0)
            self._target_value = params['target']
            self.animation_speed = params['speed']
            self._is_animating = True
            self._dirty = True
        else:
            self._is_animating = False

    def update(self):
        """
        Обновление состояния анимации. 
        """
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update_time) / 1000.0
        self.last_update_time = current_time

        if self._is_animating:
            value_range = abs(self._current_value - self._target_value)
            if value_range >= 0.1:
                step = self.animation_speed * (self.max_val - self.min_val) * delta_time / 100
                self._current_value += step * (1 if self._target_value > self._current_value else -1)
                if step > value_range:
                    self._current_value = self._target_value
            else:
                self._current_value = self._target_value
                self._start_next_animation()

    def _get_fill_rect(self) -> pygame.Rect:
        """
        Вычисляет прямоугольник заполненной части.

        :return: Область заполнения в текущем состоянии.
        """
        progress = (self._current_value - self.min_val) / (self.max_val - self.min_val)
        if self.orientation == 'horizontal':
            fill_width = max(10, int(self._width * progress))
            return pygame.Rect(self.x, self.y, fill_width, self._height)
        else:
            fill_height = max(10, int(self._height * progress))
            return pygame.Rect(self.x, self.y + self._height - fill_height, self._width, fill_height)

    def render(self, surface: pygame.Surface):
        """
        Отрисовка прогресс-бара на поверхности.

        :param surface: Целевая поверхность для отрисовки.
        """
        # Отрисовка фона
        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=self.border_radius)
        
        # Отрисовка заполненной части
        fill_rect = self._get_fill_rect()
        pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=self.border_radius)
        
        # Отрисовка текста
        if self.show_text:
            percent = int(self._current_value)
            text = self.text_format.format(
                value=int(self._current_value),
                percent=percent,
                min=self.min_val,
                max=self.max_val
            )
            text_surf = self.font.render(text, True, self.text_color)

            if self.orientation == "vertical":
                text_surf = pygame.transform.rotate(text_surf, 90)

            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
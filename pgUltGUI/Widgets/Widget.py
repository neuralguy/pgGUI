import pygame


class Widget:
    def __init__(self, x: int, y: int, width: int = None, height: int = None, 
                 margin: dict = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0},
                 padding: dict = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0},
                 background_color: tuple = None, 
                 background_image: pygame.Surface = None,
                 border_radius: int = 0,
                 visible: bool = True):
        """
        Базовый класс для виджетов.

        :param x: Координата X виджета.
        :param y: Координата Y виджета.
        :param width: Ширина виджета (если None, вычисляется автоматически).
        :param height: Высота виджета (если None, вычисляется автоматически).
        :param margin: Отступы вокруг виджета (словарь с ключами 'top', 'right', 'bottom', 'left').
        :param padding: Внутренние отступы виджета (словарь с ключами 'top', 'right', 'bottom', 'left').
        :param background_color: Цвет фона виджета.
        :param background_image: Изображение фона виджета.
        :param border_radius: Радиус скругления углов.
        """
        # Учет отступов (margin) при установке позиции
        self.x = x + margin['left']
        self.y = y + margin['top']

        self._width = width  # Ширина (может быть None для автоматического расчета)
        self._height = height  # Высота (может быть None для автоматического расчета)

        self.margin = margin  # Внешние отступы
        self.padding = padding  # Внутренние отступы

        self.background_color = background_color  # Цвет фона
        self.background_image = background_image  # Изображение фона

        self.border_radius = border_radius  # Радиус скругления углов
        self.rect = pygame.Rect(self.x, self.y, 0, 0)  # Прямоугольник виджета
        self._dirty = False  # Флаг для отслеживания изменений
    
        self._cached_bg = None  # Кэшированная поверхность фона
        self._last_bg_params = (None, None)  # (цвет, размер)

        self.visible = visible

    def render(self, surface: pygame.Surface):
        """
        Отрисовка виджета на поверхности. Должен быть переопределен в дочерних классах.

        :param surface: Поверхность для отрисовки.
        """
        pass
    
    def update(self):
        """
        Обновление состояния виджета. Должен быть переопределен в дочерних классах.
        """
        pass
        
    def _calc_auto_size(self):
        """
        Вычисление автоматических размеров виджета. Должен быть переопределен в дочерних классах.
        """
        pass

    def _update_rect(self):
        """
        Обновление прямоугольника виджета на основе текущих размеров.
        """
        width = self._width if self._width is not None else self.auto_width
        height = self._height if self._height is not None else self.auto_height
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def render_background(self, surface: pygame.Surface):
        if self.background_image:
            image = pygame.transform.scale(self.background_image, (self.rect.size))
            surface.blit(image, self.rect.topleft)
        elif self.background_color:
            # Текущие параметры
            current_color = self.background_color
            current_size = self.rect.size

            # Если параметры изменились — пересоздаем кэш
            if (current_color, current_size) != self._last_bg_params:
                self._last_bg_params = (current_color, current_size)
                
                # Создаем поверхность с альфа-каналом
                self._cached_bg = pygame.Surface(current_size, pygame.SRCALPHA)
                color = current_color
                if len(color) == 3:
                    color = (*color, 255)
                
                # Рисуем фон
                pygame.draw.rect(
                    self._cached_bg,
                    color,
                    (0, 0, *current_size),
                    border_radius=self.border_radius
                )

            # Наложение кэшированной поверхности
            surface.blit(self._cached_bg, self.rect.topleft)
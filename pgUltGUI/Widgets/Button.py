import pygame
from .Widget import Widget


class Button(Widget):
    # Кэш для хранения шрифтов, чтобы избежать повторного создания одинаковых шрифтов
    _font_cache = {}
    # Кэш для хранения текстовых поверхностей, чтобы избежать повторного рендеринга одинакового текста
    _text_cache = {}

    def __init__(self, x: int, y: int, text: str, on_click: callable = None, width: int = None, height: int = None, 
                 normal_color: tuple = (60, 60, 60), hover_color: tuple = (80, 80, 80), 
                 active_color: tuple = (40, 40, 40), shadow_color: tuple = (30, 30, 30), 
                 text_color: tuple = (255, 255, 255), font: pygame.font.Font = None, shadow_offset: int = 5, 
                 active_offset: int = 5, border_color: tuple = (160, 130, 150), border_width: int = 2, 
                 border_radius: int = 80, **kwargs):
        """
        Инициализация кнопки.

        :param x: Координата X верхнего левого угла кнопки.
        :param y: Координата Y верхнего левого угла кнопки.
        :param text: Текст, отображаемый на кнопке.
        :param on_click: Функция, которая будет вызвана при клике на кнопку.
        :param width: Ширина кнопки. Если None, ширина будет вычислена автоматически на основе текста.
        :param height: Высота кнопки. Если None, высота будет вычислена автоматически на основе текста.
        :param normal_color: Цвет кнопки в обычном состоянии (когда не наведена и не нажата).
        :param hover_color: Цвет кнопки при наведении курсора.
        :param active_color: Цвет кнопки при нажатии.
        :param shadow_color: Цвет тени кнопки.
        :param text_color: Цвет текста на кнопке.
        :param font: Шрифт текста. Если None, используется шрифт по умолчанию.
        :param shadow_offset: Смещение тени относительно кнопки.
        :param active_offset: Смещение кнопки при нажатии (эффект "вдавливания").
        :param border_color: Цвет границы кнопки.
        :param border_width: Ширина границы кнопки.
        :param border_radius: Радиус скругления углов кнопки.
        :param kwargs: Дополнительные аргументы для родительского класса Widget.
        """
        # Инициализация родительского класса Widget
        super().__init__(x, y, width, height, border_radius=border_radius, **kwargs)
        
        # Основные свойства кнопки
        self.text = text  # Текст кнопки
        self.font = self._get_cached_font(font or pygame.font.Font(None, 24))  # Шрифт текста
        self.text_color = text_color  # Цвет текста
        self.normal_color = normal_color  # Цвет кнопки в обычном состоянии
        self.hover_color = hover_color  # Цвет кнопки при наведении
        self.active_color = active_color  # Цвет кнопки при нажатии
        self.shadow_color = shadow_color  # Цвет тени
        self.border_color = border_color  # Цвет границы
        self.border_width = border_width  # Ширина границы
        self.shadow_offset = shadow_offset  # Смещение тени
        self.active_offset = active_offset  # Смещение при нажатии
        self.base_position = (x, y)  # Базовая позиция кнопки (без учета смещений)
        self.current_offset = 0  # Текущее смещение кнопки (используется для эффекта нажатия)
        self.is_hovered = False  # Флаг, указывающий, наведен ли курсор на кнопку
        self.is_active = False  # Флаг, указывающий, нажата ли кнопка
        self.on_click = on_click  # Функция, вызываемая при клике
        self._text_surf = None  # Поверхность с текстом
        self._surfaces = {}  # Кэш для хранения поверхностей кнопки (для оптимизации)
        self._dirty = True  # Флаг, указывающий, нужно ли перерисовать кнопку

        # Вычисление размеров кнопки на основе текста и отступов
        text_width, text_height = self.font.size(text)
        self.auto_width = text_width + self.padding['left'] + self.padding['right']
        self.auto_height = text_height + self.padding['top'] + self.padding['bottom']

        # Кэширование текстовой поверхности и обновление прямоугольников
        self._cache_text_surface()  # Создание текстовой поверхности
        self._update_rect()         # Обновление прямоугольников кнопки и текста

    def _get_cached_font(self, font: pygame.font.Font) -> pygame.font.Font:
        """
        Получение шрифта из кэша или его добавление, если он отсутствует.

        :param font: Шрифт для кэширования.
        :return: Кэшированный шрифт.
        """
        key = (font.name, font.size)  # Ключ для кэша (имя и размер шрифта)
        return self._font_cache.setdefault(key, font)  # Возврат шрифта из кэша или добавление нового

    def _cache_text_surface(self) -> None:
        """
        Кэширование текстовой поверхности для избежания повторного рендеринга.
        """
        cache_key = (self.text, self.font, self.text_color)  # Ключ для кэша (текст, шрифт, цвет)
        if cache_key not in self._text_cache:
            # Рендеринг текста, если он еще не был закэширован
            self._text_cache[cache_key] = self.font.render(self.text, True, self.text_color)
        self._text_surf = self._text_cache[cache_key]  # Сохранение текстовой поверхности

    def _update_rect(self) -> None:
        """
        Обновление прямоугольников кнопки и текста.
        """
        # Обновление прямоугольника кнопки
        self.rect = pygame.Rect(self.x, self.y, 
                               self._width or self.auto_width, 
                               self._height or self.auto_height)
        
        # Обновление прямоугольника текста (центрирование текста внутри кнопки)
        if self._text_surf:  # Проверка на наличие текстовой поверхности
            self.text_rect = self._text_surf.get_rect(center=self.rect.center)

    def _generate_cached_surface(self, color: tuple, border: bool = False) -> pygame.Surface:
        """
        Генерация кэшированной поверхности для кнопки.

        :param color: Цвет поверхности.
        :param border: Флаг, указывающий, нужно ли рисовать границу.
        :return: Сгенерированная поверхность.
        """
        key = (self.rect.size, color, self.border_radius)  # Ключ для кэша (размер, цвет, радиус скругления)
        if key not in self._surfaces:
            # Создание новой поверхности с прозрачностью
            surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            if border:
                # Рисование границы, если указан флаг border
                pygame.draw.rect(surface, color, surface.get_rect(), self.border_width, border_radius=self.border_radius)
            else:
                # Рисование залитого прямоугольника с скругленными углами
                pygame.draw.rect(surface, color, surface.get_rect(), border_radius=self.border_radius)
            self._surfaces[key] = surface  # Сохранение поверхности в кэше
        return self._surfaces[key]  # Возврат поверхности из кэша

    def handle_event(self, event: pygame.event.Event) -> True:
        """
        Обработка событий, связанных с кнопкой.

        :param event: Событие для обработки.
        """
        handled = False

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            handled = True

        if event.type == pygame.MOUSEMOTION:
            # Проверка, наведен ли курсор на кнопку
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Обработка нажатия левой кнопки мыши
            if self.is_hovered:
                self.is_active = True  # Установка флага нажатия
                self.current_offset = self.active_offset  # Смещение кнопки при нажатии
                self._dirty = True  # Установка флага для перерисовки

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Обработка отпускания левой кнопки мыши
            if self.is_active:
                self.is_active = False  # Сброс флага нажатия
                self.current_offset = 0  # Сброс смещения
                self._dirty = True  # Установка флага для перерисовки
                # Вызов функции on_click, если курсор все еще на кнопке
                if self.rect.collidepoint(event.pos) and self.on_click:
                    self.on_click()
        return handled

    def update(self) -> None:
        """
        Обновление состояния кнопки (позиции и текста).
        """
        if self._dirty:
            # Обновление позиции кнопки с учетом смещения при нажатии
            self.rect.topleft = (self.base_position[0], self.base_position[1] + self.current_offset)
            # Обновление позиции текста с учетом смещения
            self.text_rect.center = (self.rect.centerx, self.rect.centery + self.current_offset // 2)
            self._dirty = False  # Сброс флага перерисовки

    def render(self, surface: pygame.Surface) -> None:
        """
        Отрисовка кнопки на указанной поверхности.

        :param surface: Поверхность для отрисовки.
        """
        # Отрисовка тени, если она включена и кнопка не нажата
        if self.shadow_offset and not self.is_active:
            shadow = self._generate_cached_surface(self.shadow_color)
            surface.blit(shadow, (self.rect.x + self.shadow_offset, self.rect.y + self.shadow_offset))
        
        # Выбор цвета кнопки в зависимости от состояния
        color = self.active_color if self.is_active else self.hover_color if self.is_hovered else self.normal_color
        # Генерация и отрисовка основной поверхности кнопки
        main_surf = self._generate_cached_surface(color)
        surface.blit(main_surf, self.rect)
        # Отрисовка текста на кнопке
        surface.blit(self._text_surf, self.text_rect)

        # Отрисовка границы, если кнопка наведена и не нажата
        if self.is_hovered and not self.is_active:
            border = self._generate_cached_surface(self.border_color, border=True)
            surface.blit(border, self.rect)
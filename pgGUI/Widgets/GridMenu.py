import pygame
from copy import copy
from .Widget import Widget


class GridMenu(Widget):
    def __init__(self, x: int, y: int, rows: int, cols: int, 
                 cell_size: int = 64, spacing: int = 5,
                 padding: dict = None,
                 border_color: tuple = (255, 50, 50, 100), 
                 border_width: int = 1, 
                 reset_pick: bool = False, 
                 on_item_selected: callable = None, 
                 grid_color: tuple = (100, 100, 100),  
                 grid_width: int = 1,                
                 show_grid: bool = True,              
                 **kwargs):
        """
        Инициализация сеточного меню.

        :param x: Координата X верхнего левого угла меню.
        :param y: Координата Y верхнего левого угла меню.
        :param rows: Количество строк в сетке.
        :param cols: Количество столбцов в сетке.
        :param cell_size: Размер ячейки (ширина и высота).
        :param spacing: Расстояние между ячейками.
        :param padding: Отступы вокруг сетки (словарь с ключами 'left', 'right', 'top', 'bottom').
        :param border_color: Цвет границы выбранной ячейки (RGBA).
        :param border_width: Ширина границы выбранной ячейки.
        :param reset_pick: Сбрасывать ли выбор ячейки после отпускания кнопки мыши.
        :param on_item_selected: Функция, вызываемая при выборе элемента.
        :param grid_color: Цвет линий сетки.
        :param grid_width: Ширина линий сетки.
        :param show_grid: Показывать ли сетку.
        :param kwargs: Дополнительные аргументы для базового класса Widget.
        """
        super().__init__(x, y, **kwargs)
        self.rows = rows  # Количество строк в сетке
        self.cols = cols  # Количество столбцов в сетке
        self.cell_size = cell_size  # Размер каждой ячейки (ширина и высота)
        self.spacing = spacing  # Расстояние между ячейками
        self.padding = padding if padding else {"left": 0, "right": 0, "top": 0, "bottom": 0}  # Отступы вокруг сетки

        self.items = {}  # Словарь для хранения элементов в ячейках сетки
        self.selected_cell = None  # Текущая выбранная ячейка (строка, столбец)
        self.hovered_cell = None  # Ячейка, над которой находится курсор мыши
        self.highlight_color = (120, 255, 120, 50)  # Цвет подсветки ячейки при наведении (RGBA)
        self.border_color = border_color  # Цвет границы выбранной ячейки
        self.border_width = border_width  # Ширина границы выбранной ячейки
        self.reset_pick = reset_pick  # Флаг для сброса выбора ячейки после отпускания кнопки мыши
        self.on_item_selected = on_item_selected  # Функция обратного вызова при выборе элемента
        self.grid_color = grid_color  # Цвет линий сетки
        self.grid_width = grid_width  # Ширина линий сетки
        self.show_grid = show_grid  # Флаг для отображения сетки

        # Кэшированные поверхности и данные для оптимизации отрисовки
        self.grid_surface = None  # Поверхность для отрисовки сетки
        self.cell_rects = {}  # Словарь для хранения прямоугольников ячеек
        self.quantity_font = None  # Шрифт для отображения количества элементов в ячейке
        self.highlight_surface = None  # Поверхность для подсветки ячейки при наведении
        self.darken_surface = None  # Поверхность для затемнения недоступных ячеек

        # Инициализация размеров и обновление всех связанных параметров
        self._calc_auto_size()  # Расчет автоматических размеров меню
        self._update_rect()  # Обновление прямоугольника меню
        self._update_cell_rects()  # Обновление прямоугольников ячеек
        self._update_quantity_font()  # Обновление шрифта для отображения количества
        self._update_highlight_surface()  # Обновление поверхности подсветки
        self._update_darken_surface()  # Обновление поверхности затемнения

    def _calc_auto_size(self):
        """
        Расчет автоматических размеров меню на основе количества строк, столбцов, размера ячеек и отступов.
        """
        # Ширина меню = (количество столбцов * (размер ячейки + расстояние)) - расстояние + отступы слева и справа
        self.auto_width = (self.cols * (self.cell_size + self.spacing) 
                          - self.spacing + self.padding['left'] + self.padding['right'])
        # Высота меню = (количество строк * (размер ячейки + расстояние)) - расстояние + отступы сверху и снизу
        self.auto_height = (self.rows * (self.cell_size + self.spacing) 
                           - self.spacing + self.padding['top'] + self.padding['bottom'])

    def _update_grid_surface(self):
        """
        Обновление поверхности для отрисовки сетки.
        """
        # Общая ширина и высота сетки
        total_width = self.cols * (self.cell_size + self.spacing) - self.spacing
        total_height = self.rows * (self.cell_size + self.spacing) - self.spacing
        # Создание поверхности с прозрачным фоном
        self.grid_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        self.grid_surface.fill((0, 0, 0, 0))  # Заполнение прозрачным цветом
        
        # Отрисовка границ сетки
        pygame.draw.rect(self.grid_surface, self.grid_color, (0, 0, total_width, total_height), self.grid_width)
        
        # Отрисовка вертикальных линий сетки
        for col in range(1, self.cols):
            x = col * (self.cell_size + self.spacing) - self.spacing // 2
            pygame.draw.line(self.grid_surface, self.grid_color, (x, 0), (x, total_height), self.grid_width)
        
        # Отрисовка горизонтальных линий сетки
        for row in range(1, self.rows):
            y = row * (self.cell_size + self.spacing) - self.spacing // 2
            pygame.draw.line(self.grid_surface, self.grid_color, (0, y), (total_width, y), self.grid_width)

    def _update_cell_rects(self):
        """
        Обновление прямоугольников ячеек на основе текущих параметров.
        """
        self.cell_rects.clear()  # Очистка предыдущих данных
        for row in range(self.rows):
            for col in range(self.cols):
                # Расчет координат ячейки с учетом отступов и расстояния между ячейками
                x = (self.rect.x + self.padding['left'] 
                     + col * (self.cell_size + self.spacing))
                y = (self.rect.y + self.padding['top'] 
                     + row * (self.cell_size + self.spacing))
                # Создание прямоугольника для ячейки
                self.cell_rects[(row, col)] = pygame.Rect(x, y, self.cell_size, self.cell_size)

    def _update_quantity_font(self):
        """
        Обновление шрифта для отображения количества элементов в ячейке.
        """
        # Размер шрифта зависит от размера ячейки
        self.quantity_font = pygame.font.Font(None, self.cell_size // 2)

    def _update_highlight_surface(self):
        """
        Обновление поверхности для подсветки ячейки при наведении.
        """
        self.highlight_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        self.highlight_surface.fill(self.highlight_color)  # Заполнение цветом подсветки

    def _update_darken_surface(self):
        """
        Обновление поверхности для затемнения недоступных ячеек.
        """
        self.darken_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        self.darken_surface.fill((0, 0, 0, 180))  # Заполнение полупрозрачным черным цветом

    def set_cell_size(self, value: int):
        """
        Установка нового размера ячейки и обновление связанных параметров.

        :param value: Новый размер ячейки.
        """
        if self.cell_size != value:
            self.cell_size = value  # Обновление размера ячейки
            self._update_quantity_font()  # Обновление шрифта
            self._update_highlight_surface()  # Обновление поверхности подсветки
            self._update_darken_surface()  # Обновление поверхности затемнения
            # Масштабирование изображений всех элементов
            for item in self.items.values():
                item.image_surface = pygame.transform.scale(item.original_image, (self.cell_size, self.cell_size))
            self._calc_auto_size()  # Пересчет размеров меню
            self._update_rect()  # Обновление прямоугольника меню
            self._update_cell_rects()  # Обновление прямоугольников ячеек
            self.grid_surface = None  # Сброс кэшированной поверхности сетки

    def add_item(self, item, row: int, col: int):
        """
        Добавление элемента в сетку.

        :param item: Элемент для добавления.
        :param row: Строка, в которую добавляется элемент.
        :param col: Столбец, в который добавляется элемент.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:  # Проверка корректности координат
            item = copy(item)  # Создание копии элемента
            item.original_image = item.image_surface.copy()  # Сохранение оригинального изображения
            item.image_surface = pygame.transform.scale(item.original_image, (self.cell_size, self.cell_size))  # Масштабирование изображения
            self.items[(row, col)] = item  # Добавление элемента в словарь
            item.cell_rect = self.cell_rects[(row, col)]  # Привязка прямоугольника ячейки к элементу

    def handle_event(self, event: pygame.event.Event):
        """
        Обработка событий.

        :param event: Событие для обработки.
        """
        if event.type == pygame.MOUSEMOTION:  # Обработка движения мыши
            self.hovered_cell = None  # Сброс текущей подсвеченной ячейки
            mouse_pos = event.pos  # Получение позиции курсора
            if self.rect.collidepoint(mouse_pos):  # Проверка, находится ли курсор в пределах меню
                # Локальные координаты курсора относительно меню
                local_x = mouse_pos[0] - self.rect.x - self.padding['left']
                local_y = mouse_pos[1] - self.rect.y - self.padding['top']
                # Определение столбца и строки, над которыми находится курсор
                col = local_x // (self.cell_size + self.spacing)
                row = local_y // (self.cell_size + self.spacing)
                if 0 <= row < self.rows and 0 <= col < self.cols:  # Проверка корректности координат
                    # Координаты ячейки
                    cell_x = col * (self.cell_size + self.spacing)
                    cell_y = row * (self.cell_size + self.spacing)
                    # Проверка, находится ли курсор внутри ячейки
                    if (local_x >= cell_x and local_x < cell_x + self.cell_size and
                        local_y >= cell_y and local_y < cell_y + self.cell_size):
                        self.hovered_cell = (row, col)  # Установка текущей подсвеченной ячейки

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Обработка нажатия левой кнопки мыши
            if self.hovered_cell:  # Если есть подсвеченная ячейка
                row, col = self.hovered_cell  # Получение координат ячейки
                item = self.items.get((row, col))  # Получение элемента из ячейки
                if item and item.is_available:  # Если элемент существует и доступен
                    self.selected_cell = (row, col)  # Установка выбранной ячейки
                    if item.on_click:  # Если у элемента есть функция обратного вызова
                        item.on_click(item)  # Вызов функции
                    if self.on_item_selected:  # Если задана функция обратного вызова для выбора элемента
                        self.on_item_selected(item)  # Вызов функции
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.reset_pick:  # Обработка отпускания кнопки мыши
            self.selected_cell = None  # Сброс выбранной ячейки

    def render(self, surface: pygame.Surface):
        """
        Отрисовка меню на поверхности.

        :param surface: Поверхность для отрисовки.
        """
        self.render_background(surface)  # Отрисовка фона
        
        if self.show_grid:  # Если сетка должна быть видимой
            if not self.grid_surface:  # Если поверхность сетки не создана
                self._update_grid_surface()  # Обновление поверхности сетки
            # Отрисовка сетки на поверхности меню
            surface.blit(self.grid_surface, (self.rect.x + self.padding['left'], self.rect.y + self.padding['top']))

        # Отрисовка всех элементов в ячейках
        for (row, col), item in self.items.items():
            cell_rect = self.cell_rects[(row, col)]  # Получение прямоугольника ячейки
            if item.image_surface:  # Если у элемента есть изображение
                surface.blit(item.image_surface, cell_rect)  # Отрисовка изображения
            
            if (row, col) == self.selected_cell:  # Если ячейка выбрана
                # Отрисовка границы выбранной ячейки
                pygame.draw.rect(surface, self.border_color, cell_rect, self.border_width)
            
            if (row, col) == self.hovered_cell:  # Если ячейка подсвечена
                surface.blit(self.highlight_surface, cell_rect.topleft)  # Отрисовка подсветки
            
            if item.quantity > 1:  # Если количество элементов больше 1
                # Отрисовка текста с количеством элементов
                text = self.quantity_font.render(str(item.quantity), True, (255, 255, 255))
                surface.blit(text, cell_rect.move(2, -text.get_height() // 1.5).bottomleft)
            
            if not item.is_available:  # Если элемент недоступен
                surface.blit(self.darken_surface, cell_rect.topleft)  # Отрисовка затемнения
import pygame
from .Widget import Widget


class TextInput(Widget):
    def __init__(self, x: int, y: int, width: int = None, height: int = None,
                 line_length: int = 20,
                 font: pygame.font.Font = None,
                 text_color: tuple = (0, 0, 0),
                 background_color: tuple = (255, 255, 255),
                 border_color: tuple = (100, 100, 100),
                 active_border_color: tuple = (50, 150, 255),
                 cursor_color: tuple = (50, 150, 255),
                 padding: int = 5,
                 border_radius: int = 4,
                 **kwargs):
        """
        Инициализация текстового поля ввода.

        :param x: Координата X текстового поля.
        :param y: Координата Y текстового поля.
        :param width: Ширина текстового поля (если None, вычисляется автоматически).
        :param height: Высота текстового поля (если None, вычисляется автоматически).
        :param line_length: Максимальная длина строки перед переносом.
        :param font: Шрифт для текста.
        :param text_color: Цвет текста.
        :param background_color: Цвет фона.
        :param border_color: Цвет границы.
        :param active_border_color: Цвет границы при активном состоянии.
        :param cursor_color: Цвет курсора.
        :param padding: Внутренний отступ.
        :param border_radius: Радиус скругления углов.
        :param kwargs: Дополнительные параметры для базового класса Widget.
        """
        super().__init__(x, y, width, height, 
                        background_color=background_color,
                        border_radius=border_radius,
                        **kwargs)
        
        # Текстовые параметры
        self.text = ""  # Текущий текст
        self.font = font or pygame.font.Font(None, 24)  # Шрифт по умолчанию
        self.text_color = text_color
        self.line_length = line_length  # Максимальная длина строки
        self.lines = [""]  # Список строк текста
        
        # Стилевые параметры
        self.border_color = border_color
        self.active_border_color = active_border_color
        self.cursor_color = cursor_color
        self.padding = padding
        
        # Состояния
        self.active = False  # Активно ли текстовое поле
        self.cursor_pos = (0, 0)  # Позиция курсора (строка, позиция в строке)
        self.cursor_visible = True  # Видимость курсора
        
        # Автоматический расчет размеров
        self.line_height = self.font.get_height() + 2  # Высота строки
        self._calculate_size()

    def _calculate_size(self):
        """
        Вычисление размеров текстового поля на основе содержимого.
        """
        if self._width is None:
            max_line_width = max(self.font.size(line)[0] for line in self.lines)
            self.auto_width = max_line_width + self.padding * 2
        else:
            self.auto_width = self._width
            
        if self._height is None:
            self.auto_height = len(self.lines) * self.line_height + self.padding * 2
        else:
            self.auto_height = self._height
            
        self._update_rect()

    def handle_event(self, event: pygame.event.Event):
        """
        Обработка событий текстового поля.

        :param event: Событие Pygame.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                # Расчет позиции курсора по клику
                x, y = event.pos
                rel_x = x - self.rect.left - self.padding
                rel_y = y - self.rect.top - self.padding
                
                line = min(len(self.lines) - 1, rel_y // self.line_height)
                col = 0
                current_width = 0
                for i, char in enumerate(self.lines[line]):
                    char_width = self.font.size(char)[0]
                    if current_width + char_width / 2 > rel_x:
                        break
                    current_width += char_width
                    col = i + 1
                self.cursor_pos = (line, col)
                
        if self.active and event.type == pygame.KEYDOWN:
            self._handle_key(event)
            self._handle_arrows(event)

    def _handle_key(self, event: pygame.event.Event):
        """
        Обработка нажатий клавиш.

        :param event: Событие Pygame.
        """
        line, pos = self.cursor_pos
        current_line = self.lines[line]
        
        if event.key == pygame.K_BACKSPACE:
            if pos > 0:
                new_line = current_line[:pos - 1] + current_line[pos:]
                self.lines[line] = new_line
                self.cursor_pos = (line, pos - 1)
            elif line > 0:
                prev_line = self.lines[line - 1]
                new_line = prev_line + current_line
                self.lines.pop(line)
                self.lines[line - 1] = new_line
                self.cursor_pos = (line - 1, len(prev_line))
                
        elif event.key == pygame.K_RETURN:
            new_line = current_line[pos:]
            self.lines[line] = current_line[:pos]
            self.lines.insert(line + 1, new_line)
            self.cursor_pos = (line + 1, 0)
            
        elif event.unicode:
            self._insert_text(event.unicode)

        self._wrap_text()
        self._calculate_size()

    def _handle_arrows(self, event: pygame.event.Event):
        """
        Обработка нажатий стрелок для перемещения курсора.

        :param event: Событие Pygame.
        """
        line, pos = self.cursor_pos
        if event.key == pygame.K_LEFT:
            if pos > 0:
                self.cursor_pos = (line, pos - 1)
            elif line > 0:
                self.cursor_pos = (line - 1, len(self.lines[line - 1]))
        elif event.key == pygame.K_RIGHT:
            if pos < len(self.lines[line]):
                self.cursor_pos = (line, pos + 1)
            elif line < len(self.lines) - 1:
                self.cursor_pos = (line + 1, 0)
        elif event.key == pygame.K_UP:
            if line > 0:
                new_pos = min(pos, len(self.lines[line - 1]))
                self.cursor_pos = (line - 1, new_pos)
        elif event.key == pygame.K_DOWN:
            if line < len(self.lines) - 1:
                new_pos = min(pos, len(self.lines[line + 1]))
                self.cursor_pos = (line + 1, new_pos)

    def _insert_text(self, text: str):
        """
        Вставка текста в текущую позицию курсора.

        :param text: Текст для вставки.
        """
        line, pos = self.cursor_pos
        current_line = self.lines[line]
        new_line = current_line[:pos] + text + current_line[pos:]
        self.lines[line] = new_line
        self.cursor_pos = (line, pos + len(text))

    def _wrap_text(self):
        """
        Перенос текста на новую строку, если он превышает максимальную длину.
        """
        new_lines = []
        cursor_adjust = 0  # Смещение курсора из-за переноса
        original_line, original_pos = self.cursor_pos
        
        for line_idx, line in enumerate(self.lines):
            while len(line) > self.line_length:
                split_pos = line.rfind(' ', 0, self.line_length) 
                split_pos = self.line_length if split_pos == -1 else split_pos
                
                # Если курсор находится в области переноса
                if line_idx == original_line and original_pos > split_pos:
                    cursor_adjust += 1
                    original_pos -= split_pos
                
                new_lines.append(line[:split_pos])
                line = line[split_pos:].lstrip()
            
            new_lines.append(line)
        
        # Обновляем позицию курсора
        if cursor_adjust > 0:
            self.cursor_pos = (original_line + cursor_adjust, original_pos)
        
        self.lines = new_lines

    def render(self, surface: pygame.Surface):
        """
        Отрисовка текстового поля на поверхности.

        :param surface: Поверхность для отрисовки.
        """
        # Рендер фона
        self.render_background(surface)
        
        # Рендер границы
        border_color = self.active_border_color if self.active else self.border_color
        pygame.draw.rect(surface, border_color, self.rect, 2, self.border_radius)
        
        # Рендер текста
        y = self.rect.top + self.padding
        for i, line in enumerate(self.lines):
            text_surf = self.font.render(line, True, self.text_color)
            surface.blit(text_surf, (self.rect.left + self.padding, y))
            y += self.line_height
            
        # Рендер курсора
        if self.active and self.cursor_visible:
            line, pos = self.cursor_pos
            text_before_cursor = self.lines[line][:pos]
            cursor_x = self.rect.left + self.padding + self.font.size(text_before_cursor)[0]
            cursor_y = self.rect.top + self.padding + line * self.line_height
            pygame.draw.line(surface, self.cursor_color,
                            (cursor_x, cursor_y),
                            (cursor_x, cursor_y + self.line_height - 2), 2)
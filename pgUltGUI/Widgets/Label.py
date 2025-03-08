import pygame
from .Widget import Widget


class Label(Widget):
    def __init__(self, x: int, y: int, text: str, 
                 font: pygame.font.Font = None, 
                 text_color: tuple = (255, 255, 255),
                 text_align: str = 'center',
                 line_length: int = None,
                 **kwargs):
        super().__init__(x, y, **kwargs)
        
        self.text = text
        self.font = font or pygame.font.Font(None, 24)
        self.text_color = text_color
        self.text_align = text_align.lower()
        self.line_length = line_length
        self.lines = []
        
        self._wrap_text()
        self._update_text_surface()
        self._update_rect()

    def _wrap_text(self):
        """Автоматический перенос текста с учётом максимальной длины строки"""
        if not self.line_length or not self.text:
            self.lines = [self.text]
            return

        self.lines = []
        current_line = []
        current_length = 0
        
        for word in self.text.split():
            word_width = self.font.size(word + ' ')[0]
            
            if current_length + word_width <= self.line_length:
                current_line.append(word)
                current_length += word_width
            else:
                self.lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_width
        
        if current_line:
            self.lines.append(' '.join(current_line))

    def _update_text_surface(self):
        """Создание многострочной текстовой поверхности"""
        if not self.lines:
            self.text_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
            return

        line_height = self.font.get_height()
        max_width = max(self.font.size(line)[0] for line in self.lines)
        total_height = line_height * len(self.lines)
        
        self.text_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        y = 0
        for line in self.lines:
            line_surf = self.font.render(line, True, self.text_color)
            self.text_surface.blit(line_surf, (0, y))
            y += line_height

    def _update_rect(self):
        """Обновление размеров и позиционирования текста"""
        if not self.text_surface:
            return

        # Рассчитываем размеры с учётом padding
        content_width = self.text_surface.get_width()
        content_height = self.text_surface.get_height()
        
        self.auto_width = content_width + self.padding['left'] + self.padding['right']
        self.auto_height = content_height + self.padding['top'] + self.padding['bottom']
        
        # Обновляем основной прямоугольник
        self.rect = pygame.Rect(
            self.x, 
            self.y, 
            self._width or self.auto_width, 
            self._height or self.auto_height
        )
        
        # Позиционируем текст в зависимости от выравнивания
        if self.text_align == 'left':
            self.text_rect = self.text_surface.get_rect(
                midleft=(
                    self.rect.left + self.padding['left'],
                    self.rect.centery
                )
            )
        elif self.text_align == 'right':
            self.text_rect = self.text_surface.get_rect(
                midright=(
                    self.rect.right - self.padding['right'],
                    self.rect.centery
                )
            )
        else:  # center и другие варианты по умолчанию
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def set_text(self, new_text: str):
        """Обновление текста с полным перерасчётом геометрии"""
        if self.text != new_text:
            self.text = new_text
            self._wrap_text()
            self._update_text_surface()
            self._update_rect()

    def set_alignment(self, align: str):
        """Изменение выравнивания без полного перерасчёта"""
        valid_alignments = {'left', 'center', 'right'}
        if align.lower() in valid_alignments:
            self.text_align = align.lower()
            self._update_rect()

    def render(self, surface: pygame.Surface) -> None:
        """Отрисовка виджета с учётом фона и текста"""
        self.render_background(surface)
        if self.text_surface:
            surface.blit(self.text_surface, self.text_rect)
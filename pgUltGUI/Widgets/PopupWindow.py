import pygame
from pygame import Color
from .Widget import Widget
from .Button import Button
from .Label import Label

class PopupWindow(Widget):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 title: str = "Window",
                 content: str = "",
                 text_align: str = 'center',
                 line_length: int = None,
                 header_color: tuple = (80, 80, 80, 220),
                 body_color: tuple = (120, 120, 120, 220),
                 header_height: int = 30,
                 close_button_color: tuple = (255, 80, 80),
                 font: pygame.font.Font = None,
                 text_padding: int = 10,
                 shadow_offset: int = 6,
                 shadow_color: tuple = (0, 0, 0, 70),
                 shadow_blur_radius: int = 8,
                 border_highlight: tuple = (180, 180, 180, 80),
                 border_shadow: tuple = (60, 60, 60, 80),
                 border_size: int = 2,
                 depth_intensity: float = 0.3,
                 **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        
        # Основные параметры
        self.title = title
        self.content = content
        self.header_color = header_color
        self.body_color = body_color
        self.header_height = header_height
        self.text_padding = text_padding
        self.is_dragging = False
        self.drag_offset = (0, 0)
        self.visible = True
        self._cache_valid = False
        
        # Параметры глубины и теней
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color
        self.shadow_blur_radius = shadow_blur_radius
        self.border_highlight = border_highlight
        self.border_shadow = border_shadow
        self.border_size = border_size
        self.depth_intensity = depth_intensity
        
        # Элементы интерфейса
        self.close_button = Button(
            x = x + width - (header_height - 10) - 5,
            y = y + 5,
            width = header_height - 10,
            height = header_height - 10,
            text = "×",
            normal_color = close_button_color,
            hover_color = (255, 100, 100),
            shadow_offset = 3,
            border_radius = 25,
            on_click = self.hide,
            shadow_color=(0, 0, 0, 40)
            )
        self.close_button.font = pygame.font.Font(None, header_height + 5)
        
        self.content_label = Label(
            x = x + text_padding,
            y = y + header_height + text_padding,
            text = content,
            line_length = line_length,
            font = font or pygame.font.Font(None, 24),
            text_color = (255, 255, 255),
            text_align = text_align
        )
        
        # Шрифты и кэши
        self.font = font or pygame.font.Font(None, 20)
        self._shadow_surface = None
        self._shadow_rect = None
        self._header_surface = None
        self._body_surface = None
        
        self._update_title_surface()
        self.update()
        self._update_rect()

    def _update_title_surface(self):
        self.title_surface = self.font.render(self.title, True, (255, 255, 255))
        
    def _update_shadow_surface(self):
        """Создание многоуровневой размытой тени"""
        shadow_size = (
            self._width + self.shadow_offset * 2 + self.shadow_blur_radius * 2,
            self._height + self.shadow_offset * 2 + self.shadow_blur_radius * 2
        )
        self._shadow_surface = pygame.Surface(shadow_size, pygame.SRCALPHA)
        
        base_rect = pygame.Rect(
            self.shadow_blur_radius,
            self.shadow_blur_radius,
            self._width + self.shadow_offset * 2,
            self._height + self.shadow_offset * 2
        )
        
        # Рисуем серию размытых прямоугольников
        for i in range(self.shadow_blur_radius * 2 + 1):
            alpha = int(self.shadow_color[3] * (1 - i/(self.shadow_blur_radius * 2)) * self.depth_intensity)
            radius = i
            rect = base_rect.inflate(radius * 2, radius * 2)
            pygame.draw.rect(
                self._shadow_surface,
                (*self.shadow_color[:3], alpha),
                rect,
                border_radius=self.border_radius + radius
            )

        self._shadow_rect = pygame.Rect(
            self.x - self.shadow_offset - self.shadow_blur_radius,
            self.y - self.shadow_offset - self.shadow_blur_radius,
            *shadow_size
        )

    def _update_header_surface(self):
        """Создание поверхности заголовка с градиентом"""
        self._header_surface = pygame.Surface((self._width, self.header_height), pygame.SRCALPHA)
        
        # Вертикальный градиент
        for i in range(self.header_height):
            alpha = int(255 * (1 - i/self.header_height * 0.3))
            color = tuple(min(c + int(30 * (i/self.header_height)), 255) for c in self.header_color[:3]) + (alpha,)
            pygame.draw.line(self._header_surface, color, (0, i), (self._width, i))

        # Внешняя обводка
        pygame.draw.rect(
            self._header_surface,
            self.border_highlight,
            (0, 0, self._width, self.header_height),
            border_top_left_radius=self.border_radius,
            border_top_right_radius=self.border_radius,
            width=self.border_size
        )

        # Верхняя подсветка
        highlight = pygame.Surface((self._width, 2), pygame.SRCALPHA)
        highlight.fill((*self.border_highlight[:3], 120))
        self._header_surface.blit(highlight, (0, 0))

    def _update_body_surface(self):
        """Создание поверхности тела окна с градиентом"""
        self._body_surface = pygame.Surface((self._width, self._height - self.header_height), pygame.SRCALPHA)
        
        # Вертикальный градиент
        body_height = self._height - self.header_height
        for i in range(body_height):
            alpha = int(self.body_color[3] * (1 - i/body_height * 0.2))
            color = self.body_color[:3] + (alpha,)
            pygame.draw.line(self._body_surface, color, (0, i), (self._width, i))

        # Внешняя обводка
        pygame.draw.rect(
            self._body_surface,
            self.border_highlight,
            (0, 0, self._width, body_height),
            border_radius=self.border_radius,
            width=self.border_size
        )

        # Внутренняя тень
        inner_shadow = pygame.Rect(2, 2, self._width - 4, body_height - 4)
        pygame.draw.rect(
            self._body_surface,
            self.border_shadow,
            inner_shadow,
            border_radius=max(self.border_radius - 2, 0),
            width=2
        )

    def _update_elements_position(self):
        self.close_button.x = self.x + self._width - self.close_button._width - 5
        self.close_button.y = self.y + 5
        self.close_button._update_rect()
        
        self.content_label.x = self.x + self.text_padding
        self.content_label.y = self.y + self.header_height + self.text_padding
        self.content_label._update_rect()
        
        self._cache_valid = False

    def _update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self._width, self._height)

    def update(self):
        if not self._cache_valid:
            self._update_shadow_surface()
            self._update_header_surface()
            self._update_body_surface()
            self._cache_valid = True

    def handle_event(self, event: pygame.event.Event):
        handled = False

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            handled = True

        # Обработка событий кнопки закрытия
        self.close_button.handle_event(event)
        
        # Проверка клика по кнопке закрытия
        button_clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_clicked = self.close_button.rect.collidepoint(event.pos)
        
        # Обработка перемещения только если не кликнули по кнопке
        if event.type == pygame.MOUSEBUTTONDOWN and not button_clicked:
            header_rect = pygame.Rect(self.x, self.y, self._width, self.header_height)
            if header_rect.collidepoint(event.pos):
                self.is_dragging = True
                self.drag_offset = (event.pos[0] - self.x, event.pos[1] - self.y)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.x = event.pos[0] - self.drag_offset[0]
            self.y = event.pos[1] - self.drag_offset[1]
            self._update_elements_position()
            self._update_rect()
            

        return handled

    def render(self, surface: pygame.Surface):
        # Отрисовка тени
        surface.blit(self._shadow_surface, self._shadow_rect)
        
        # Смещение основного окна для эффекта глубины
        offset = int(self.shadow_offset * 0.6)
        main_x = self.x + offset
        main_y = self.y + offset
        
        # Отрисовка тела и заголовка
        surface.blit(self._body_surface, (main_x, main_y + self.header_height))
        surface.blit(self._header_surface, (main_x, main_y))
        
        # Заголовок
        title_pos = (
            main_x + 10,
            main_y + self.header_height//2 - self.title_surface.get_height()//2
        )
        surface.blit(self.title_surface, title_pos)
        
        # Обновление позиций элементов
        self.close_button.x = main_x + self._width - self.close_button._width - 5
        self.close_button.y = main_y + 5
        self.content_label.x = main_x + self.text_padding
        self.content_label.y = main_y + self.header_height + self.text_padding
        
        # Отрисовка элементов
        self.close_button.render(surface)
        self.content_label.render(surface)

    def set_content(self, text: str):
        if self.content != text:
            self.content = text
            self.content_label.set_text(text)
            self.content_label._update_rect()
            self._cache_valid = False

    def hide(self):
        self.visible = False
        if self._manager:
            self._manager.remove(self)
            
    def show(self):
        self.visible = True
        if self._manager:
            self._manager.add(self)
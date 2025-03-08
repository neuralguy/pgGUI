# Widgets/Scroll.py
import pygame
from .Widget import Widget
from pygame import Rect
from .WidgetManager import WidgetManager


class Scroll(Widget):
    def __init__(self, x: int, y: int, width: int, height: int, 
                 scroll_speed: int = 20, scrollbar_width: int = 15,
                 scrollbar_color: tuple = (100, 100, 100),
                 **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        
        self.content_height = 0
        self.scroll_offset = 0
        self.scroll_speed = scroll_speed
        self.is_dragging = False
        self.drag_start_y = 0
        
        self.scrollbar_width = scrollbar_width
        self.scrollbar_color = scrollbar_color
        self.scrollbar_rect = None
        self.scroll_handle_rect = None

        self.content_manager = WidgetManager()
        self.content_surface = pygame.Surface((self._width, 1), pygame.SRCALPHA)
        
        self.viewport_rect = Rect(0, 0, self._width, self._height) 

        self._update_scroll_elements()
        self._update_rect()

        self.border_color = kwargs.get('border_color', (200, 200, 200))
        self.border_width = kwargs.get('border_width', 2)
        self.border_rect = pygame.Rect(
            self.rect.left-self.border_width, 
            self.rect.top-self.border_width, 
            self.rect.width+2*self.border_width,
            self.rect.height+2*self.border_width
            )
        

    def add(self, widget: Widget):
        self.content_manager.add(widget)
        self._update_content_size()
        
    def remove(self, widget: Widget):
        self.content_manager.remove(widget)
        self._update_content_size()

    def _update_content_size(self):
        max_y = 0
        for layer in self.content_manager._layers.values():
            for w in layer.values():
                if w.rect.bottom > max_y:
                    max_y = w.rect.bottom
        self.content_height = max(max_y, self._height) 
        self.content_surface = pygame.Surface((self._width, self.content_height), pygame.SRCALPHA)
        self._update_scroll_elements()

    def _update_scroll_elements(self):
        # Защита от деления на ноль
        if self.content_height <= 0 or self._height <= 0:
            self.scroll_handle_rect = None
            self.scrollbar_rect = None
            return

        # Расчет высоты ползунка с минимальным значением 20px
        ratio = min(1.0, self._height / self.content_height)
        handle_height = max(20, self._height * ratio)
        
        # Расчет позиции ползунка
        scroll_range = self.content_height - self._height
        if scroll_range <= 0:
            handle_position = 0
        else:
            handle_position = (self.scroll_offset / scroll_range) * (self._height - handle_height)

        # Обновление прямоугольников
        self.scroll_handle_rect = Rect(
            self.rect.right - self.scrollbar_width,
            self.rect.top + handle_position,
            self.scrollbar_width,
            handle_height
        )
        
        self.scrollbar_rect = Rect(
            self.rect.right - self.scrollbar_width,
            self.rect.top,
            self.scrollbar_width,
            self._height
        )

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.scroll_handle_rect.collidepoint(event.pos):
                self.is_dragging = True
                self.drag_start_y = event.pos[1] - self.scroll_handle_rect.top
                
            elif event.button in (4, 5):
                delta = -self.scroll_speed if event.button == 4 else self.scroll_speed
                self.scroll_offset = max(0, min(self.content_height - self._height,
                                             self.scroll_offset + delta))
                self._update_scroll_elements()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            new_y = event.pos[1] - self.drag_start_y
            self.scroll_offset = (new_y - self.rect.top) / self._height * self.content_height 
            self.scroll_offset = max(0, min(self.content_height - self._height, 
                                         self.scroll_offset))
            self._update_scroll_elements()

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            adjusted_event = pygame.event.Event(event.type, {
                **event.__dict__,
                'pos': (event.pos[0] - self.rect.x, 
                       event.pos[1] - self.rect.y + self.scroll_offset)
            })
            self.content_manager.handle_events(adjusted_event)

    def update(self):
        """Обновление состояния дочерних виджетов"""
        self.content_manager.update()

    def render(self, surface: pygame.Surface):
        # Отрисовка фона
        self.render_background(surface)

        # Отрисовка рамки
        pygame.draw.rect(
            surface, 
            self.border_color, 
            self.border_rect, 
            width=self.border_width, 
            border_radius=self.border_radius
        )
        
        if self.content_surface:
            self.content_surface.fill((0, 0, 0, 0))
            
            # Отрисовка всех виджетов с проверкой на существование атрибута visible
            for layer in sorted(self.content_manager._layers.keys()):
                for widget in self.content_manager._layers[layer].values():
                    # Безопасная проверка видимости
                    if getattr(widget, 'visible', True):  # <-- Используем getattr с default=True
                        widget.render(self.content_surface)
        
        # Обрезка контента по viewport
        clipped = self.content_surface.subsurface(self.viewport_rect.move(0, self.scroll_offset))
        surface.blit(clipped, self.rect.topleft)
        
        # Отрисовка полосы прокрутки
        if self.content_height > self.rect.height:
            pygame.draw.rect(surface, self.scrollbar_color, self.scrollbar_rect, border_radius=5)
            pygame.draw.rect(surface, (200, 200, 200), self.scroll_handle_rect, border_radius=5)
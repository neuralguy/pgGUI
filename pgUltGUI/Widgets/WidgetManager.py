import pygame
from collections import OrderedDict, defaultdict


class WidgetManager:
    def __init__(self):
        """
        Менеджер для управления виджетами, их рендерингом и обработкой событий.

        Атрибуты:
            _layers: Словарь слоев, где каждый слой содержит OrderedDict виджетов.
            named_widgets: Словарь для хранения именованных виджетов.
            focused_widget: Виджет, который в данный момент имеет фокус.
            _event_handlers: Список виджетов, которые могут обрабатывать события.
            _update_handlers: Список виджетов, которые требуют обновления.
            _reverse_order: Флаг для определения порядка обработки событий (обычный или обратный).
        """
        self._layers = defaultdict(OrderedDict)  # Слои для упорядоченного рендеринга
        self.named_widgets = {}                  # Именованные виджеты
        self.focused_widget = None               # Виджет с фокусом
        self._event_handlers = []                # Приоритетные обработчики событий
        self._update_handlers = []               # Виджеты для обновления
        self._reverse_order = False              # Флаг обратного порядка обработки

    def add(self, widget, name: str = None, layer: int = 0):
        """
        Добавление виджета в менеджер.

        :param widget: Виджет для добавления.
        :param name: Имя виджета (опционально).
        :param layer: Слой, на котором будет отрисовываться виджет.
        """
        widget_id = id(widget)
        self._layers[layer][widget_id] = widget  # Добавление виджета в слой
        widget._layer = layer  # Сохранение слоя в виджете
        widget._manager = self  # Ссылка на менеджер в виджете
        
        if name:
            self.named_widgets[name] = widget  # Сохранение именованного виджета
            
        if hasattr(widget, 'handle_event'):
            self._event_handlers.append(widget)  # Добавление в обработчики событий
            
        if hasattr(widget, 'update'):
            self._update_handlers.append(widget)  # Добавление в обработчики обновления
            
    def remove(self, widget):
        """
        Удаление виджета из менеджера.

        :param widget: Виджет для удаления.
        """
        widget_id = id(widget)
        layer = getattr(widget, '_layer', 0)
        
        if widget_id in self._layers[layer]:
            del self._layers[layer][widget_id]  # Удаление из слоя
            
        if widget in self.named_widgets.values():
            for name, w in self.named_widgets.items():
                if w == widget:
                    del self.named_widgets[name]  # Удаление из именованных виджетов
                    break
                    
        if widget in self._event_handlers:
            self._event_handlers.remove(widget)  # Удаление из обработчиков событий
            
        if widget in self._update_handlers:
            self._update_handlers.remove(widget)  # Удаление из обработчиков обновления
            
    def get(self, name: str):
        """
        Получение виджета по имени.

        :param name: Имя виджета.
        :return: Виджет или None, если виджет не найден.
        """
        return self.named_widgets.get(name)

    def handle_events(self, event: pygame.event.Event):
        """
        Обработка событий для всех виджетов в порядке слоев (сверху вниз).
        """
        for widget in reversed(self._event_handlers):
            if not widget.visible:
                continue  # Пропускаем невидимые виджеты

            # Если виджет обработал событие, прекращаем дальнейшую обработку
            if widget.handle_event(event):
                break

    def update(self):
        """
        Обновление всех виджетов, которые требуют обновления.
        """
        for widget in self._update_handlers:
            if widget.visible and widget._dirty or getattr(widget, 'always_update', False):
                widget.update()  # Обновление виджета
                
        # Оптимизация для группового обновления
        if pygame.get_init():
            now = pygame.time.get_ticks()
            for widget in self._update_handlers:
                if hasattr(widget, 'tick_update'):
                    widget.tick_update(now)  # Обновление с учетом времени

    def draw(self, surface: pygame.Surface):
        """
        Отрисовка всех виджетов на поверхности.

        :param surface: Поверхность для отрисовки.
        """
        for layer in self._layers.values():
            for widget in layer.values():
                if widget.visible:
                    widget.render(surface)  # Отрисовка виджета

    def bring_to_front(self, widget):
        """
        Перемещение виджета на верхний слой.

        :param widget: Виджет для перемещения.
        """
        self.remove(widget)
        self.add(widget, layer=max(self._layers.keys()) + 1)  # Добавление на верхний слой

    def send_to_back(self, widget):
        """
        Перемещение виджета на нижний слой.

        :param widget: Виджет для перемещения.
        """
        self.remove(widget)
        self.add(widget, layer=min(self._layers.keys()) - 1)  # Добавление на нижний слой
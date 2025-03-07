import pygame


class SceneManager:
    def __init__(self):
        """
        Менеджер для управления сценами в приложении.

        Атрибуты:
            scenes: Словарь для хранения всех сцен.
            current_scene: Текущая активная сцена.
            previous_scene: Предыдущая сцена.
            scene_stack: Стек для хранения сцен (например, для паузы).
            transition_data: Данные, передаваемые между сценами.
        """
        self.scenes = {}  # Словарь сцен (ключ - имя сцены, значение - объект сцены)
        self.current_scene = None  # Текущая активная сцена
        self.previous_scene = None  # Предыдущая сцена
        self.scene_stack = []  # Стек для хранения сцен (например, для паузы)
        self.transition_data = {}  # Данные для передачи между сценами

    def add(self, scene):
        """
        Добавление сцены в менеджер.

        :param scene: Объект сцены для добавления.
        """
        scene.manager = self
        self.scenes[scene.name] = scene  # Сохранение сцены в словаре

    def switch(self, scene_name: str, data=None):
        """
        Переключение на новую сцену с полной заменой текущей.

        :param scene_name: Имя сцены для переключения.
        :param data: Данные, передаваемые при переходе на новую сцену.
        """
        if self.current_scene:
            self.current_scene.on_pause()  # Приостановка текущей сцены
            self.current_scene.on_exit()  # Выход из текущей сцены
            self.previous_scene = self.current_scene  # Сохранение текущей сцены как предыдущей

        self.current_scene = self.scenes[scene_name]  # Установка новой сцены
        self.current_scene.on_enter(self.previous_scene, data)  # Вход в новую сцену

    def push(self, scene_name: str, data=None):
        """
        Добавление новой сцены поверх текущей (например, для паузы).

        :param scene_name: Имя сцены для добавления.
        :param data: Данные, передаваемые при переходе на новую сцену.
        """
        if self.current_scene:
            self.scene_stack.append(self.current_scene)  # Сохранение текущей сцены в стек
            self.current_scene.on_pause()  # Приостановка текущей сцены

        self.current_scene = self.scenes[scene_name]  # Установка новой сцены
        self.current_scene.on_enter(None, data)  # Вход в новую сцену

    def pop(self, data=None):
        """
        Возврат к предыдущей сцене (например, после паузы).

        :param data: Данные, передаваемые при возврате на предыдущую сцену.
        :return: True, если возврат успешен, иначе False.
        """
        if self.scene_stack:
            old_scene = self.current_scene  # Сохранение текущей сцены
            self.current_scene = self.scene_stack.pop()  # Восстановление предыдущей сцены из стека
            old_scene.on_exit()  # Выход из старой сцены
            self.current_scene.on_resume(data)  # Возобновление предыдущей сцены
            return True
        return False  # Возврат False, если стек пуст

    def handle_events(self, event: pygame.event.Event):
        """
        Обработка событий для текущей сцены.

        :param event: Событие Pygame.
        """
        if self.current_scene:
            self.current_scene.handle_events(event)  # Передача события текущей сцене

    def update(self):
        """
        Обновление текущей сцены.
        """
        if self.current_scene:
            self.current_scene.update()  # Обновление текущей сцены

    def draw(self, surface: pygame.Surface):
        """
        Отрисовка текущей сцены.

        :param surface: Поверхность для отрисовки.
        """
        if self.current_scene:
            self.current_scene.draw(surface)  # Отрисовка текущей сцены
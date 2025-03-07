import pygame
from .Image import Image


class Animation(Image):
    def __init__(self, x: int, y: int, width: int = 100, height: int = 100, frames: list = None, 
                 fps: int = 12, loop: bool = True, auto_play: bool = True,
                 preload_frames: bool = True, **kwargs):
        """
        Инициализация анимации.

        :param x: Координата X верхнего левого угла.
        :param y: Координата Y верхнего левого угла.
        :param width: Ширина анимации.
        :param height: Высота анимации.
        :param frames: Список кадров анимации.
        :param fps: Количество кадров в секунду.
        :param loop: Зацикленность анимации.
        :param auto_play: Автоматический запуск анимации.
        :param preload_frames: Предварительная обработка кадров.
        :param kwargs: Дополнительные аргументы для родительского класса.
        """
        super().__init__(x, y, width=width, height=height, **kwargs)

        # Анимационные параметры
        self.raw_frames: list = []  # Сырые кадры
        self.processed_frames: list = []  # Обработанные кадры
        self.current_frame: int = 0  # Текущий кадр
        self.fps: int = fps  # Кадры в секунду
        self.loop: bool = loop  # Зацикленность
        self.is_playing: bool = auto_play  # Состояние воспроизведения
        self.frame_duration: int = 1000 // self.fps  # Длительность одного кадра в мс
        self.last_update: int = 0  # Время последнего обновления
        self.preload_frames: bool = preload_frames  # Предварительная обработка кадров

        if frames:
            self.add_frames(frames)

    def _update_rect(self) -> None:
        """Обновление прямоугольника, ограничивающего анимацию."""
        if self._width and self._height:
            self.rect = pygame.Rect(
                self.x,
                self.y,
                self._width,
                self._height
            )
        elif self.original_image:
            # Используем размеры первого кадра, если размеры не заданы
            self.rect = self.original_image.get_rect(topleft=(self.x, self.y))

    def add_frame(self, frame: str or pygame.Surface) -> None:
        """
        Добавление кадра в анимацию.

        :param frame: Путь к изображению или объект pygame.Surface.
        """
        raw_frame = self._load_frame(frame)
        self.raw_frames.append(raw_frame)
        
        if self.preload_frames:
            processed = self._process_frame(raw_frame)
            self.processed_frames.append(processed)
        
        if len(self.raw_frames) == 0:
            self.set_image(raw_frame)
            self._update_rect()

    def insert_frame(self, frame: str or pygame.Surface, idx: int) -> None:
        """
        Вставка кадра в анимацию по указанному индексу.

        :param frame: Путь к изображению или объект pygame.Surface.
        :param idx: Индекс для вставки.
        """
        raw_frame = self._load_frame(frame)
        self.raw_frames.insert(idx, raw_frame)
        
        if self.preload_frames:
            processed = self._process_frame(raw_frame)
            self.processed_frames.insert(idx, processed)
        
        if len(self.raw_frames) == 0:
            self.set_image(raw_frame)
            self._update_rect()

    def add_frames(self, frames: list) -> None:
        """
        Пакетное добавление кадров.

        :param frames: Список кадров.
        """
        for frame in frames:
            self.add_frame(frame)

    def load_from_spritesheet(self, filename: str, frame_size: tuple, rows: int, columns: int) -> None:
        """
        Загрузка кадров из спрайтшита.

        :param filename: Путь к файлу спрайтшита.
        :param frame_size: Размер одного кадра (ширина, высота).
        :param rows: Количество строк в спрайтшите.
        :param columns: Количество столбцов в спрайтшите.
        """
        sheet = pygame.image.load(filename).convert_alpha()
        frames = []
        for row in range(rows):
            for col in range(columns):
                x = col * frame_size[0]
                y = row * frame_size[1]
                frames.append(sheet.subsurface((x, y, frame_size[0], frame_size[1])))
        self.add_frames(frames)

    def _load_frame(self, frame: str or pygame.Surface) -> pygame.Surface:
        """
        Загрузка и кэширование кадра.

        :param frame: Путь к изображению или объект pygame.Surface.
        :return: Загруженный кадр.
        """
        if isinstance(frame, str):
            return pygame.image.load(frame).convert_alpha()
        return frame.copy()

    def _apply_scaling(self, frame: pygame.Surface) -> pygame.Surface:
        """
        Масштабирование кадра согласно настройкам виджета.

        :param frame: Кадр для масштабирования.
        :return: Масштабированный кадр.
        """
        orig_w, orig_h = frame.get_size()

        # Режим сохранения пропорций
        if self.keep_aspect_ratio:
            ratio_w = self.width / orig_w
            ratio_h = self.height / orig_h
            
            ratio = min(ratio_w, ratio_h)
                
            new_w = int(orig_w * ratio)
            new_h = int(orig_h * ratio)
        else:
            # Произвольное растяжение
            new_w, new_h = self.width, self.height

        # Применяем сглаженное масштабирование
        return pygame.transform.smoothscale(frame, (new_w, new_h))

    def _process_frame(self, frame: pygame.Surface) -> pygame.Surface:
        """
        Предварительная обработка кадра.

        :param frame: Кадр для обработки.
        :return: Обработанный кадр.
        """
        frame = frame.copy()
        
        # Применение текущих трансформаций
        frame = self._apply_scaling(frame)

        if self.rotation != 0:
            frame = pygame.transform.rotate(frame, self.rotation)
        if self.flip_x or self.flip_y:
            frame = pygame.transform.flip(frame, self.flip_x, self.flip_y)
        
        return frame

    def set_image(self, image: pygame.Surface) -> None:
        """
        Установка изображения.

        :param image: Изображение для установки.
        """
        super().set_image(image)
        if image:
            self._width = image.get_width()
            self._height = image.get_height()
            self._update_rect()

    def update(self) -> None:
        """Обновление анимации с таймингом."""
        if not self.is_playing or not self.raw_frames:
            return
            
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_duration:
            self.current_frame += 1
            
            if self.current_frame >= len(self.raw_frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.raw_frames) - 1
                    self.is_playing = False
            
            self._set_current_frame(self.current_frame)
            self.last_update = now

    def _set_current_frame(self, index: int) -> None:
        """
        Установка текущего кадра.

        :param index: Индекс кадра.
        """
        if self.preload_frames and self.processed_frames:
            self.processed_image = self.processed_frames[index]
        else:
            self.processed_image = self._process_frame(self.raw_frames[index])
        self._update_alignment()

    @property
    def width(self) -> int:
        """Получение ширины анимации."""
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """Установка ширины анимации."""
        self._width = value
        self._dirty = True
        self._update_rect()

    @property
    def height(self) -> int:
        """Получение высоты анимации."""
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        """Установка высоты анимации."""
        self._height = value
        self._dirty = True
        self._update_rect()
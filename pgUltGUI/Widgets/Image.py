import pygame
from pygame.surfarray import array3d, array_alpha, make_surface
from .Widget import Widget


class Image(Widget):
    _image_cache = {}  # Кэш для хранения загруженных изображений

    def __init__(self, x: int, y: int, image=None,
                 keep_aspect_ratio: bool = False,
                 alias: bool = False,
                 rotation: int = 0,
                 flip_x: bool = False,
                 flip_y: bool = False,
                 grayscale: bool = False,
                 opacity: int = 255,
                 **kwargs):
        """
        Инициализация виджета изображения.

        :param x: Координата X верхнего левого угла изображения.
        :param y: Координата Y верхнего левого угла изображения.
        :param image: Путь к изображению или объект pygame.Surface.
        :param keep_aspect_ratio: Сохранять пропорции изображения при масштабировании.
        :param alias: Использовать сглаживание при повороте изображения.
        :param rotation: Угол поворота изображения (в градусах).
        :param flip_x: Отразить изображение по горизонтали.
        :param flip_y: Отразить изображение по вертикали.
        :param grayscale: Преобразовать изображение в градации серого.
        :param opacity: Прозрачность изображения (0-255).
        :param kwargs: Дополнительные аргументы для родительского класса Widget.
        """
        super().__init__(x, y, **kwargs)

        self.original_image = None  # Оригинальное изображение
        self.processed_image = None  # Обработанное изображение (с примененными трансформациями)
        self.keep_aspect_ratio = keep_aspect_ratio  # Сохранение пропорций
        self.alias = alias  # Использование сглаживания
        self._rotation = rotation % 360  # Угол поворота (нормализованный до 0-360 градусов)
        self._flip_x = flip_x  # Отразить по горизонтали
        self._flip_y = flip_y  # Отразить по вертикали
        self._grayscale = grayscale  # Градации серого
        self._opacity = opacity  # Прозрачность
        self._dirty = True  # Флаг, указывающий, нужно ли перерисовывать изображение

        if image:
            self.set_image(image)  # Установка изображения, если оно передано

    def set_image(self, image) -> None:
        """
        Установка изображения.

        :param image: Путь к изображению или объект pygame.Surface.
        """
        try:
            if isinstance(image, str):
                # Использование кэша для загруженных изображений
                if image in Image._image_cache:
                    self.original_image = Image._image_cache[image]
                else:
                    loaded_image = pygame.image.load(image).convert_alpha()
                    Image._image_cache[image] = loaded_image
                    self.original_image = loaded_image
            elif isinstance(image, pygame.Surface):
                self.original_image = image.copy()  # Копирование поверхности
            self._update_rect()  # Обновление прямоугольника изображения
            self._dirty = True  # Установка флага для перерисовки
        except Exception as e:
            print(f"Error loading image: {e}")  # Обработка ошибок загрузки
            self.original_image = None

    def _apply_transformations(self) -> None:
        """
        Применение всех трансформаций к изображению (масштабирование, отражение, поворот и т.д.).
        """
        if not self.original_image or not self._dirty:
            return

        img = self.original_image.copy()  # Копирование оригинального изображения
        orig_w, orig_h = img.get_size()  # Получение размеров оригинального изображения
        
        # Определение целевого размера
        target_w = self.rect.width if self._width is not None else orig_w
        target_h = self.rect.height if self._height is not None else orig_h

        # Масштабирование изображения
        if (orig_w, orig_h) != (target_w, target_h):
            if self.keep_aspect_ratio:
                # Сохранение пропорций
                ratio = min(target_w / orig_w, target_h / orig_h)
                new_size = (int(orig_w * ratio), int(orig_h * ratio))
            else:
                # Произвольное масштабирование
                new_size = (target_w, target_h)
            
            img = pygame.transform.smoothscale(img, new_size)  # Сглаженное масштабирование

        # Отражение изображения
        if self._flip_x or self._flip_y:
            img = pygame.transform.flip(img, self._flip_x, self._flip_y)

        # Поворот изображения
        if self._rotation != 0:
            img = self._rotate_image(img)

        # Преобразование в градации серого
        if self._grayscale:
            img = self._apply_grayscale(img)

        # Применение прозрачности
        if self._opacity < 255:
            img = self._apply_opacity(img, self._opacity)

        self.processed_image = img  # Сохранение обработанного изображения
        self._update_alignment()  # Обновление выравнивания
        self._dirty = False  # Сброс флага перерисовки

    def _rotate_image(self, img: pygame.Surface) -> pygame.Surface:
        """
        Поворот изображения с учетом сглаживания.

        :param img: Изображение для поворота.
        :return: Повернутое изображение.
        """
        if self.alias:
            return pygame.transform.rotozoom(img, self._rotation, 1)  # Сглаженный поворот
        else:
            return pygame.transform.rotate(img, self._rotation)  # Обычный поворот

    def _apply_grayscale(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Преобразование изображения в градации серого.  (Pygame only - slower!)

        :param surface: Изображение для преобразования.
        :return: Изображение в градациях серого.
        """

        gray_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                r, g, b, a = surface.get_at((x, y)) 

                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                gray_surface.set_at((x, y), (gray, gray, gray, a))

        return gray_surface

    def _apply_opacity(self, surface: pygame.Surface, opacity: int) -> pygame.Surface:
        """
        Применение прозрачности к изображению.

        :param surface: Изображение для обработки.
        :param opacity: Уровень прозрачности (0-255).
        :return: Изображение с примененной прозрачностью.
        """
        surface = surface.copy()  # Копирование поверхности
        surface.fill((255, 255, 255, opacity), special_flags=pygame.BLEND_RGBA_MULT)  # Применение прозрачности
        return surface

    def _update_alignment(self) -> None:
        """
        Обновление выравнивания изображения.
        """
        if self.processed_image:
            self.image_rect = self.processed_image.get_rect(center=self.rect.center)  # Центрирование изображения

    def render(self, surface: pygame.Surface) -> None:
        """
        Отрисовка изображения на указанной поверхности.

        :param surface: Поверхность для отрисовки.
        """
        if self._dirty:
            self._apply_transformations()  # Применение трансформаций, если необходимо
        if self.processed_image:
            surface.blit(self.processed_image, self.image_rect)  # Отрисовка изображения

    # Оптимизированные свойства
    @property
    def width(self) -> int:
        """Получение ширины изображения."""
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """Установка ширины изображения."""
        self._width = value
        self._dirty = True  # Установка флага для перерисовки
        self._update_rect()  # Обновление прямоугольника

    @property
    def height(self) -> int:
        """Получение высоты изображения."""
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        """Установка высоты изображения."""
        self._height = value
        self._dirty = True  # Установка флага для перерисовки
        self._update_rect()  # Обновление прямоугольника

    @property
    def rotation(self) -> int:
        """Получение угла поворота изображения."""
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: int) -> None:
        """Установка угла поворота изображения."""
        self._rotation = value % 360  # Нормализация угла
        self._dirty = True  # Установка флага для перерисовки

    @property
    def flip_x(self) -> bool:
        """Получение состояния отражения по горизонтали."""
        return self._flip_x
    
    @flip_x.setter
    def flip_x(self, value: bool) -> None:
        """Установка отражения по горизонтали."""
        self._flip_x = value
        self._dirty = True  # Установка флага для перерисовки

    @property
    def flip_y(self) -> bool:
        """Получение состояния отражения по вертикали."""
        return self._flip_y
    
    @flip_y.setter
    def flip_y(self, value: bool) -> None:
        """Установка отражения по вертикали."""
        self._flip_y = value
        self._dirty = True  # Установка флага для перерисовки

    @property
    def grayscale(self) -> bool:
        """Получение состояния градаций серого."""
        return self._grayscale
    
    @grayscale.setter
    def grayscale(self, value: bool) -> None:
        """Установка градаций серого."""
        self._grayscale = value
        self._dirty = True  # Установка флага для перерисовки

    @property
    def opacity(self) -> int:
        """Получение уровня прозрачности."""
        return self._opacity
    
    @opacity.setter
    def opacity(self, value: int) -> None:
        """Установка уровня прозрачности."""
        self._opacity = value
        self._dirty = True  # Установка флага для перерисовки

    @property
    def alias(self) -> bool:
        """Получение состояния сглаживания."""
        return self._alias
    
    @alias.setter
    def alias(self, value: bool) -> None:
        """Установка сглаживания."""
        self._alias = value
        self._dirty = True  # Установка флага для перерисовки
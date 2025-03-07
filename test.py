import pygame
import random as rd
from pgUltGUI import *


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("main_menu")
        self.background_color=(128,128,255)

    def setup(self):
        # Создаем элементы интерфейса главного меню
        label = Label(100, 100, "Это просто обычный текст!", background_color=(255,128,128), padding={'top': 10, 'right': 10, 'bottom': 10, 'left': 10})
        slider = Slider(30, 150, max_val=1000)
        slider2 = Slider(20, 200, orientation='vertical', min_val=-1, max_val=1)
        text = TextInput(300, 130)
        start_btn = Button(
            x=300, y=200, width=400, height=50, text="Start Game",
            on_click=lambda: self.manager.switch("game"),
            background_color=(70, 70, 70),
            text_color=(255, 255, 255)
        )

        quit_btn = Button(
            x=300, y=280, width=200, height=50, text="Quit Game",
            on_click=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
            background_color=(70, 70, 70),
            text_color=(255, 255, 255)
        )
        pygame.transform.set_smoothscale_backend('SSE2')
        animation = Animation(700, 50, alias=True, fps=6)
        animation.load_from_spritesheet("res/first_example.jpg", (20,30), 1, 25)
        animation.add_frame("res/second_example1.jpg")

        image = Image(0, 0, "res/second_example1.jpg", width=150, height=100)

        grid = GridMenu(50, 350, rows=5, cols=5, cell_size=40,
               background_color=(40, 40, 40), 
               padding={'top': 5, 'left': 5, 'bottom': 5, 'right': 5},
               spacing=0,
               on_item_selected=lambda item: print(f"Selected: {item.name}"))

        # Создание элемента
        sword_item = Item(
            image="res/second_example2.jpg",
            name="pawn",
            description="Just a pawn",
            quantity=64,
            on_click=lambda item: print(f"Clicked: {item.name}")
        )

        # Добавление элемента в сетку
        for i in range(500):
            for j in range(500):
                grid.add_item(sword_item, i, j)

        bar = ProgressBar(500, 150, min_val=0, max_val=100, animation_speed=15)

        # Добавление виджетов в менеджер
        self.widget_manager.add(label)
        self.widget_manager.add(animation)
        self.widget_manager.add(slider)
        self.widget_manager.add(slider2, "slider2")
        self.widget_manager.add(text)
        self.widget_manager.add(start_btn)
        self.widget_manager.add(quit_btn)
        self.widget_manager.add(image)
        self.widget_manager.add(grid)
        self.widget_manager.add(bar, "bar")

class GameScene(Scene):
    def __init__(self):
        super().__init__("game")
        self.background_color = (150, 200, 70)

    def setup(self):
        # Инициализация игровой сцены
        self.score_label = Label(10, 10, "Score: 0", text_color=(255, 255, 255))
        menu_btn = Button(
            x=300, y=200, width=400, height=50, text="Go to menu",
            on_click=lambda: self.manager.switch("main_menu"),
            background_color=(70, 70, 70),
            text_color=(255, 255, 255)
        )

        
        self.widget_manager.add(self.score_label)
        self.widget_manager.add(menu_btn)

    def update(self):
        super().update()
        # Логика обновления игры


def main():
    pygame.init()
    pygame.transform.set_smoothscale_backend('SSE2')  # Для скорости
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Инициализация менеджера сцен
    scene_manager = SceneManager()
    
    # Создание и регистрация сцен
    main_menu = MainMenuScene()
    scene_manager.add(main_menu)
    
    game_scene = GameScene()
    scene_manager.add(game_scene)

    # Стартовая сцена
    scene_manager.switch("main_menu")
    slider = main_menu.widget_manager.get("slider2")
    bar = main_menu.widget_manager.get("bar")
    for i in range(101):
        bar.to_value(i, rd.randint(1, 51))

    running = True
    max_fps = 0
    sum_fps = 0
    frames = 1
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_events(event)

        # Обновление
        scene_manager.update()

        # Отрисовка
        scene_manager.draw(screen)
        pygame.display.update()
        clock.tick(1000)

        # расчёт фпс
        fps = int(clock.get_fps())
        pygame.display.set_caption(f"FPS: {fps}, Max: {max_fps}, Avg: {sum_fps // frames}")
        max_fps = max(max_fps, fps)
        frames += 1
        sum_fps += fps 


    pygame.quit()

if __name__ == "__main__":
    main()
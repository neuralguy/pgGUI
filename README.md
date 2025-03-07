
# pgUltGUI Library Documentation

Welcome to the Pygame UI Library! This library provides a set of GUI widgets and tools to help you create interactive user interfaces in Pygame. Below, you'll find detailed documentation on how to use each widget, along with examples to get you started.

## Table of Contents
0. [Get Started](#get-started)
1. [Widget](#widget)
2. [Label](#label)
3. [Button](#button)
4. [Slider](#slider)
5. [TextInput](#textinput)
6. [GridMenu](#gridmenu)
7. [Image](#image)
8. [Animation](#animation)
9. [WidgetManager](#widgetmanager)
10. [Scene](#scene)
11. [SceneManager](#scenemanager)

---
## Get Started
#### Basic example with a label and a button:
```python
import pygame
from pgUltGUI import *

pygame.init()
screen = pygame.display.set_mode((600,600))

widget_manager = WidgetManager()

hello_text = Label(text="Hello World!", 
    x=100, y=100,     
    font=pygame.font.Font(None, 64),
    text_color=(180, 90,90),
    background_color=(60,255,60), 
    padding={"top": 5, "bottom": 5, "left":10, "right": 10},
    border_radius=15
) 

btn = Button(x=100,y=300,
    text="Click me!",
    width=300, height=40,
    on_click=lambda: print("You clicked me!")
    )

widget_manager.add(hello_text, "hello_text")
widget_manager.add(btn, "btn")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        widget_manager.handle_events(event)

    widget_manager.update()

    screen.fill((40,40,128))
    widget_manager.draw(screen)
    pygame.display.update()

```
#### Result:
![Program](res/first_example.jpg)

#### Example with scenes:
```python
import pygame
from pgUltGUI import *

pygame.init()
screen = pygame.display.set_mode((600,600))

class First(Scene):
    def __init__(self):
        super().__init__(name="first")
        self.background_color=(128,128,255)

    def setup(self):
        text = Label(text="This is the first scene", 
            x=100, y=100,     
            font=pygame.font.Font(None, 32),
            text_color=(240, 240,240),
            background_color=(60,230,60), 
            padding={"top": 5, "bottom": 5, "left":10, "right": 10},
            border_radius=15
        ) 

        btn = Button(x=100,y=300,
            text="Click me!",
            width=300, height=40,
            on_click=lambda: self.manager.switch("second")
        )

        self.widget_manager.add(text, "text")
        self.widget_manager.add(btn, "btn")

class Second(Scene):
    def __init__(self):
        super().__init__(name="second")
        self.background_color=(255,128,128)

    def setup(self):
        text = Label(text="This is the second scene", 
            x=100, y=100,     
            font=pygame.font.Font(None, 32),
            text_color=(240, 240,240),
            background_color=(60,230,60), 
            padding={"top": 5, "bottom": 5, "left":10, "right": 10},
            border_radius=15
        ) 

        btn = Button(x=100,y=300,
            text="Click me!",
            width=300, height=40,
            on_click=lambda: self.manager.switch("first")
        )

        self.widget_manager.add(text, "text")
        self.widget_manager.add(btn, "btn")

scene_manager = SceneManager()
scene_manager.add(First())
scene_manager.add(Second())
scene_manager.switch("first")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        scene_manager.handle_events(event)

    scene_manager.update()

    scene_manager.draw(screen)
    pygame.display.update()
```
Result:

![First scene](res/second_example1.jpg)
![Second scene](res/second_example2.jpg)

---

## Widget

The `Widget` class is the base class for all UI widgets. It provides basic functionality such as positioning, sizing, and rendering.

### Parameters:
- `x` (int): X-coordinate of the widget.
- `y` (int): Y-coordinate of the widget.
- `width` (int, optional): Width of the widget. If `None`, it will be calculated automatically.
- `height` (int, optional): Height of the widget. If `None`, it will be calculated automatically.
- `margin` (dict): Margin around the widget (default: `{'top': 0, 'right': 0, 'bottom': 0, 'left': 0}`).
- `padding` (dict): Padding inside the widget (default: `{'top': 0, 'right': 0, 'bottom': 0, 'left': 0}`).
- `background_color` (tuple): Background color of the widget.
- `background_image` (pygame.Surface): Background image of the widget.
- `border_radius` (int): Radius of the widget's corners.

### Methods:
- `render(surface: pygame.Surface)`: Renders the widget on the given surface.
- `update()`: Updates the widget's state.
- `_calc_auto_size()`: Calculates the widget's size automatically.
- `render_background(surface: pygame.Surface)`: Renders the widget's background.

### Example:
```python
widget = Widget(x=100, y=100, width=200, height=100, background_color=(255, 0, 0))
widget.render(screen)
```
---
## Label

The Label widget displays text on the screen.

### Parameters:
- `x` (int): X-coordinate of the label.
- `y` (int): Y-coordinate of the label.
- `text` (str): Text to display on the label.
- `font` (pygame.font.Font): Font used for the text (default: None).
- `text_color` (tuple): Color of the text (default: (255, 255, 255)).

### Methods:
- `render`(surface: pygame.Surface): Renders the label on the given surface.

### Example:
```python
label = Label(x=100, y=100, text="Hello, World!", text_color=(255, 255, 255))
label.render(screen)
```
---
## Button

The Button widget is a clickable button with text.

### Parameters:
- `x` (int): X-coordinate of the button.
- `y` (int): Y-coordinate of the button.
- `text` (str): Text displayed on the button.
- `on_click` (callable): Callback function when the button is clicked.
- `width` (int, optional): Width of the button.
- `height` (int, optional): Height of the button.
- `normal_color` (tuple): Color of the button in its normal state (default: (60, 60, 60)).
- `hover_color` (tuple): Color of the button when hovered (default: (80, 80, 80)).
- `active_color` (tuple): Color of the button when clicked (default: (40, 40, 40)).
- `shadow_color` (tuple): Color of the button's shadow (default: (30, 30, 30)).
- `text_color` (tuple): Color of the button's text (default: (255, 255, 255)).
- `font` (pygame.font.Font): Font used for the button's text (default: None).
- `shadow_offset` (int): Offset of the button's shadow (default: 5).
- `active_offset` (int): Offset of the button when clicked (default: 5).
- `border_color` (tuple): Color of the button's border (default: (160, 130, 150)).
- `border_width` (int): Width of the button's border (default: 3).
- `border_radius` (int): Radius of the button's corners (default: 80).

### Methods:
- `handle_event`(event: pygame.event.Event): Handles mouse events for the button.
- `render`(surface: pygame.Surface): Renders the button on the given surface.

### Example:
``` python
button = Button(x=100, y=100, text="Click Me", on_click=lambda: print("Button clicked!"))
button.handle_event(event)
button.render(screen)
```
---
## Slider

The `Slider` widget allows users to select a value by dragging a handle along a track.

### Parameters:
- `x` (int): X-coordinate of the slider.
- `y` (int): Y-coordinate of the slider.
- `width` (int): Width of the slider (default: 200).
- `height` (int): Height of the slider (default: 20).
- `min_val` (int): Minimum value of the slider (default: 0).
- `max_val` (int): Maximum value of the slider (default: 100).
- `orientation` (str): Orientation of the slider (`'horizontal'` or `'vertical'`, default: `'horizontal'`).
- `track_color` (tuple): Color of the slider track (default: (200, 200, 200)).
- `fill_color` (tuple): Color of the filled part of the slider (default: (128, 128, 128)).
- `handle_color` (tuple): Color of the slider handle (default: (50, 150, 250)).
- `handle_hover_color` (tuple): Color of the slider handle when hovered (default: (80, 180, 250)).
- `handle_radius` (int): Radius of the slider handle (default: 8).
- `text_color` (tuple): Color of the slider's value text (default: (180, 40, 180)).
- `font` (pygame.font.Font): Font used for the value text (default: None).

### Methods:
- `handle_event`(event: pygame.event.Event): Handles mouse events for the slider.
- `render`(surface: pygame.Surface): Renders the slider on the given surface.

### Example:
```python
slider = Slider(x=100, y=100, width=200, min_val=0, max_val=100, handle_color=(50, 150, 250))
slider.handle_event(event)
slider.render(screen)
```
---

## TextInput

The `TextInput` widget allows users to input text. It supports multi-line text, cursor movement, and text wrapping.

### Parameters:
- `x` (int): X-coordinate of the text input.
- `y` (int): Y-coordinate of the text input.
- `width` (int, optional): Width of the text input.
- `height` (int, optional): Height of the text input.
- `line_length` (int): Maximum line length before wrapping (default: 20).
- `font` (pygame.font.Font): Font used for the text (default: `None`).
- `text_color` (tuple): Color of the text (default: `(0, 0, 0)`).
- `background_color` (tuple): Background color of the text input (default: `(255, 255, 255)`).
- `border_color` (tuple): Border color of the text input (default: `(100, 100, 100)`).
- `active_border_color` (tuple): Border color when the text input is active (default: `(50, 150, 255)`).
- `cursor_color` (tuple): Color of the cursor (default: `(50, 150, 255)`).
- `padding` (int): Padding inside the text input (default: 5).
- `border_radius` (int): Radius of the text input's corners (default: 4).

### Methods:
- `handle_event(event: pygame.event.Event)`: Handles events such as mouse clicks and key presses.
- `render(surface: pygame.Surface)`: Renders the text input on the given surface.

### Example:
```python
text_input = TextInput(x=100, y=100, width=200, height=50, text_color=(0, 0, 0), background_color=(255, 255, 255))
text_input.handle_event(event)
text_input.render(screen)
```
---

## GridMenu

The GridMenu widget allows you to create a grid-based menu with items.

### Parameters:
- `x` (int): X-coordinate of the grid menu.
- `y` (int): Y-coordinate of the grid menu.
- `rows` (int): Number of rows in the grid.
- `cols` (int): Number of columns in the grid.
- `cell_size` (int): Size of each cell (default: 64).
- `spacing` (int): Spacing between cells (default: 5).
- `padding` (dict): Padding around the grid (default: {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}).
- `border_color` (tuple): Color of the border around selected cells (default: (255, 50, 50, 100)).
- `border_width` (int): Width of the border (default: 1).
- `reset_pick` (bool): Whether to reset the selection after releasing the mouse button (default: False).
- `on_item_selected` (callable): Callback function when an item is selected.
- `grid_color` (tuple): Color of the grid lines (default: (100, 100, 100)).
- `grid_width` (int): Width of the grid lines (default: 1).
- `show_grid` (bool): Whether to show the grid lines (default: True).

### Methods:
- `add_item`(item, row: int, col: int): Adds an item to the grid.
- `handle_event`(event: pygame.event.Event): Handles mouse events for the grid.
- `render`(surface: pygame.Surface): Renders the grid menu on the given surface.

### Example:
```python
grid_menu = GridMenu(x=100, y=100, rows=3, cols=3, cell_size=64)
grid_menu.add_item(item, row=0, col=0)
grid_menu.handle_event(event)
grid_menu.render(screen)
```

---

## Animation

The Animation widget allows you to play animations using a sequence of frames.

### Parameters:
- `x` (int): X-coordinate of the animation.
- `y` (int): Y-coordinate of the animation.
- `width` (int): Width of the animation (default: 100).
- `height` (int): Height of the animation (default: 100).
- `frames` (list): List of frames for the animation.
- `fps` (int): Frames per second (default: 12).
- `loop` (bool): Whether the animation should loop (default: True
- `auto_play` (bool): Whether the animation should start playing automatically (default: True).
- `preload_frames` (bool): Whether to preload frames (default: True).

### Methods:
- `add_frame`(frame: str or pygame.Surface): Adds a frame to the animation.
- `insert_frame`(frame: str or pygame.Surface, idx: int): Inserts a frame at a specific index.
- `add_frames`(frames: list): Adds multiple frames to the animation.
- `load_from_spritesheet`(filename: str, frame_size: tuple, rows: int, columns: int): Loads frames from a spritesheet.
- `update`(): Updates the animation's state.
- `render`(surface: pygame.Surface): Renders the animation on the given surface.

### Example:
```python
animation = Animation(x=100, y=100, frames=["frame1.png", "frame2.png"], fps=12)
animation.update()
animation.render(screen)
```
---
## Image

The Image class is a widget that displays an image. It supports various transformations such as scaling, rotation, flipping, grayscale conversion, and opacity adjustment. The class inherits from the Widget class and extends its functionality to handle image-specific operations.

### Parameters:
- `x` (int): X-coordinate of the top-left corner of the image.
- `y` (int): Y-coordinate of the top-left corner of the image.
- `image` (str or pygame.Surface, optional): Path to the image file or a pygame.Surface object. If not provided, the image will be None.
- `keep_aspect_ratio` (bool, optional): If True, the image will maintain its aspect ratio when scaled. Default is False.
- `alias` (bool, optional): If True, anti-aliasing will be applied during rotation. Default is False.
- `rotation` (int, optional): The rotation angle of the image in degrees. Default is 0.
- `flip_x` (bool, optional): If True, the image will be flipped horizontally. Default is False.
- `flip_y` (bool, optional): If True, the image will be flipped vertically. Default is False.
- `grayscale` (bool, optional): If True, the image will be converted to grayscale. Default is False.
- `opacity` (int, optional): The opacity level of the image (0-255). Default is 255. 
- `**kwargs`: Additional keyword arguments passed to the parent Widget class.

### Methods:
- `set_image`(image: str or pygame.Surface) -> None: Sets the image to be displayed. The image can be a file path or a pygame.Surface object.
- `_apply_transformations()` -> None: Applies all transformations (scaling, flipping, rotation, grayscale, opacity) to the image.
- `_rotate_image`(img: pygame.Surface) -> pygame.Surface: Rotates the image by the specified angle.
- `_apply_grayscale`(surface: pygame.Surface) -> pygame.Surface: Converts the image to grayscale.
- `_apply_opacity`(surface: pygame.Surface, opacity: int) -> pygame.Surface: Applies the specified opacity level to the image.
- `_update_alignment`() -> None: Updates the alignment of the image within the widget.
- `render`(surface: pygame.Surface) -> None: Renders the image on the specified surface.

### Example:
```python
# Create an Image widget
image_widget = Image(x=100, y=100, image="path/to/image.png", keep_aspect_ratio=True, rotation=45, opacity=200)

# Set the image dynamically
image_widget.set_image("path/to/another_image.png")

# Flip the image horizontally
image_widget.flip_x = True

# Render the image on a surface
image_widget.render(screen)
```
---


## WidgetManager

The WidgetManager class manages multiple widgets, handling their rendering, events, and updates.

### Methods:
- `add`(widget, name: str = None, layer: int = 0): Adds a widget to the manager.
- `remove`(widget): Removes a widget from the manager.
- `get`(name: str): Retrieves a widget by name.
- `handle_events`(event: pygame.event.Event): Handles events for all widgets.
- `update`(): Updates all widgets.
- `draw`(surface: pygame.Surface): Renders all widgets on the given surface.
- `bring_to_front`(widget): Brings a widget to the front.
- `send_to_back`(widget): Sends a widget to the back.

### Example:
```python
widget_manager = WidgetManager()
widget_manager.add(button)
widget_manager.handle_events(event)
widget_manager.update()
widget_manager.draw(screen)
```
---

## Scene

The Scene class represents a scene in your application, containing widgets and handling their logic.

### Parameters:
- `name` (str): Name of the scene.

### Methods:
- `on_enter`(previous_scene=None, data=None): Called when the scene is activated.
- `on_exit`(): Called when the scene is deactivated.
- `on_resume`(data=None): Called when the scene is resumed.
- `on_pause`(): Called when the scene is paused.
- `setup`(): Initializes the scene.
- `handle_events`(event: pygame.event.Event): Handles events for the scene.
- `update`(): Updates the scene.
- `draw`(surface: pygame.Surface): Renders the scene.

### Example:
```python
class MainMenu(Scene):
    def __init__(self):
        super().__init__("MainMenu")
    
    def setup(self):
        self.button = Button(x=100, y=100, text="Start Game", on_click=self.start_game)
        self.widget_manager.add(self.button)
    
    def start_game(self):
        print("Game started!")
```
---

## SceneManager

The SceneManager class manages multiple scenes, handling transitions between them.

### Methods:
- `add`(scene): Adds a scene to the manager.
- `switch`(scene_name: str, data=None): Switches to a new scene.
- `push`(scene_name: str, data=None): Pushes a new scene onto the stack.
- `pop`(data=None): Pops the current scene from the stack.
- `handle_events`(event: pygame.event.Event): Handles events for the current scene.
- `update`(): Updates the current scene.
- `draw`(surface: pygame.Surface): Renders the current scene.

### Example:
```python
scene_manager = SceneManager()
scene_manager.add_scene(MainMenu())
scene_manager.switch_scene("MainMenu")
scene_manager.handle_events(event)
scene_manager.update()
scene_manager.draw(screen)
```
---

This documentation should help you get started with the Pygame GUI Library. Each widget and manager is designed to be flexible and easy to use, allowing you to create complex UIs with minimal effort. Happy coding!

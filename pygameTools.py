import pygame
import math
import threading as th


FPS = 30  # the FPS count for any project. A =====NOTE===== sign means something important for future me
screen_size = (640, 341)


class Position:
    global FPS

    def __init__(self, data: list):  # Class for working with position of anything.
        self.position = data

    def move(self, new_pos: list, time: float = 0.0, collision: bool = False):  # A function to change coordinates of object gradually
        dist = [self.position[0] - new_pos[0], self.position[1] - new_pos[1]]  # the change in coordinates
        frames = int(time * FPS)  # the amount of frames which are needed for the animation
        traces = [[self.position[0] + dist[0] / frames * i, self.position[1] + dist[1] / frames * i] for i in range(frames)]  # all the coordinates that the pos will change through
        mover = th.Thread(None, Position.__trace_follow__, "mover", args=[self, traces, frames, collision])  # the thread that will "move" an onject
        mover.start()

    def __trace_follow__(self, traces: list, frames: int, collision: bool = False):  # function that is used by Position.move() to follow the traces
        clock = pygame.time.Clock()  # the FPS limiter clock
        collided = False  # checks if collided with any Sprite. ==========NOTE========== needs to be implemented in future
        for frame in range(frames):  # Runs the loop for all the frames
            clock.tick(FPS)  # FPS limiter at work
            self.position = traces[frame]  # moving the object
            if collided and collision:  # stops the movement at collision
                if frame >= 1:  # moves the object back a bit
                    self.position = traces[frame - 1]
                break  # exits the movement loop


class Sprite:
    def __init__(self, pos: Position, surface: pygame.Surface):
        """
        :param pos: Required positional argument. Takes an instance of Position class used for movement shenanigans
        :param surface: Required positional argument. The image is being displayed by PyGamse
        """

        self.position = pos
        self.surface = surface


class Slider:
    def __init__(self, min_value: int = 0, max_value: int = 100, pos: Position = [0, 0], corners: int = -1,
                 length: int = 150, height: int = 50, bg_color: list = [255, 255, 255],
                 slider_color: list = [0, 0, 0], dot_color: list = [175, 175, 175], text: str = "Title",
                 textColor: list = [0, 0, 0], slider_second_color=None):
        """

        :param slider_second_color: Color of the slider after moving the dot
        :param slider_second_color:
        :param corners: If it's specified, the rectangle will have rounded courners. Default=-1
        :param min_value: A minimal value for the slider. Default is 0
        :param max_value: A maximum value for the slider. Default is 100
        :param pos: The top left corner position of the slider. Default is x:0, y:0
        :param length: The length of the slider. The default is 150
        :param height: The height(width) of the slider. Default is 50
        :param bg_color: The color of the slider. Default is white
        :param slider_color: The color of the slider's moving line. Default is black
        :param dot_color: The slider's dot color. Default color is gray
        :param text: The text on the slider. The default is Title
        """
        self.slider_second_color = slider_second_color
        self.surface = pygame.Surface((length, height), pygame.SRCALPHA, 32)
        self.min_value = min_value
        self.max_value = max_value
        self.coords = pos
        self.length = length
        self.height = height
        self.text = text
        self.length = length
        self.height = height
        self.corners = corners
        self.bg_color = bg_color
        self.slider_color = slider_color
        self.dot_color = dot_color
        self.coeffitients = {"length": 0.75, "height": 0.14, "yOffset": 0.72, "xOffset": 0.125}
        self.sliderlength = 0
        self.textColor = textColor
        self.current_value = max_value
        if slider_second_color is None:
            self.slider_second_color = [int(color * 0.75) for color in self.dot_color]

        self.__generate_slider__()

    def slider_value_interpreter(self):
        userX = pygame.mouse.get_pos()[0]
        userX = userX - self.coords[0] - self.length * self.coeffitients["xOffset"]
        self.coeffitients["length"] = userX / self.sliderlength * 0.75
        self.current_value = round((self.max_value - self.min_value) * userX / self.sliderlength + self.min_value)
        if self.current_value == 0:
            self.current_value += 1
        self.__generate_slider__()

    def value_interpreter(self):
        self.coeffitients["length"] = (self.current_value - self.min_value)/ (self.max_value - self.min_value) * 0.75
        self.__generate_slider__()

    def generate_rect(self, rect):
        return self.surface, self.bg_color, rect, -1, self.corners, self.corners, self.corners, self.corners

    def generate_sliderline(self, rect=None):
        if rect is None:
            coeffitients = self.coeffitients
            sliderlength = (self.length * coeffitients["length"])
            sliderwidth = (self.height * coeffitients["height"])
            sliderX = (self.length * coeffitients["xOffset"])
            sliderY = (self.height * coeffitients["yOffset"])
            return self.surface, self.slider_color, (sliderX, sliderY, sliderlength, sliderwidth)
        else:
            return self.surface, self.slider_color, rect

    # noinspection PyMethodMayBeStatic
    def __generate_slider__(self):
        self.sliderData = {}
        # -- Создание прямоугольника, в котором всё расположено
        rect = [0, 0, self.length, self.height]
        pygame.draw.rect(self.surface, self.bg_color, rect, int(self.height / 2 + 0.5), self.corners, self.corners,
                         self.corners, self.corners)

        # -- Секция для создания ползунка --
        coeffitients = self.coeffitients
        sliderlength = (self.length * coeffitients["length"])
        sliderwidth = (self.height * coeffitients["height"])
        sliderX = (self.length * coeffitients["xOffset"])
        sliderY = (self.height * coeffitients["yOffset"])
        pygame.draw.rect(self.surface, self.slider_second_color, (sliderX, sliderY, self.sliderlength, sliderwidth))
        pygame.draw.rect(self.surface, self.slider_color, (sliderX, sliderY, sliderlength, sliderwidth))

        # -- Секция для перетягиваемой кнопки --
        r = sliderwidth * 1.2 / 2
        dotX = sliderX + sliderlength
        dotY = (2 * sliderY + sliderwidth) / 2
        pygame.draw.circle(self.surface, self.dot_color, (dotX, dotY), r)

        # -- Секция для текста на кнопке --
        fontSize = 24
        font = pygame.font.SysFont("arial", fontSize)
        text = font.render(self.text, True, self.textColor)
        while (text.get_width() >= self.length * 0.8 or fontSize <= 0) or (
                text.get_height() >= self.height * coeffitients["yOffset"] * 0.8):
            fontSize -= 1
            font = pygame.font.SysFont("arial", fontSize)
            text = font.render(self.text, True, self.textColor)
            if fontSize <= 0:
                self.text = ""
        if self.text != "":
            textX = (self.length / 2 - text.get_width() / 2)
            textY = (self.height * coeffitients["yOffset"] / 2 - text.get_height() / 2)
            self.surface.blit(text, [textX, textY])
            self.sliderData["text"] = {"x": textX, "y": textY, "fontSize": fontSize}
        self.sliderData["slider"] = {"coefficients": coeffitients, "length": sliderlength, "height": sliderwidth,
                                     "x": sliderX, "y": sliderY}
        self.sliderData["dot"] = {"r": r, "x": dotX, "y": dotY}
        if self.sliderlength == 0:
            self.sliderlength = sliderlength

        # -- Создание значения слайдера на самом слайдере --
        fontSize = math.ceil(fontSize * 0.5)
        font = pygame.font.SysFont("arial", fontSize)
        text = font.render(str(math.ceil(self.current_value)), True, self.textColor)
        textX = (sliderX + self.sliderlength / 2) - text.get_width() / 2
        textY = (sliderY + sliderwidth / 2) - text.get_height() / 2
        self.surface.blit(text, [textX, textY])

        self.surface.convert_alpha()

    def mouse_inside_slider(self):
        mousepos = pygame.mouse.get_pos()
        sliderData = self.sliderData["slider"]
        if sliderData["x"] + self.coords[0] <= mousepos[0] <= sliderData["x"] + self.coords[0] + self.sliderlength \
                and sliderData["y"] * 0.85 + self.coords[1] <= mousepos[1] <= sliderData["y"] * 1.15 + self.coords[1] + \
                sliderData["height"]:
            return True
        else:
            return False


class Button:
    def __init__(self, coords: list = [0, 0], color: list = [0, 0, 0], text: str = "Test",
                 textcolor: list = [255, 255, 255], actionOnClick="RT", size: list = [250, 90], corners: int = -1,
                 function_args: list = [], icon: pygame.surface.Surface = None):
        """

        :param coords: Coordinates where button is going to be placed at
        :param color: Color of the button
        :param text: Text which will be displayed on the button
        :param textcolor: Color of the displayed text
        :param actionOnClick: This function will be performed on click. By default, will just return True if button was clicked and False else. RT stands for "return True" and can be used by the user.
        :param corners: The corners of a button. If no corners, input -1.
        :param function_args: The argumaents that will be passed into the function
        """
        if icon is None:
            self.surface = pygame.surface.Surface(size, pygame.SRCALPHA, 32)
            self.size = size
            self.textcolor = textcolor
            self.text = text
            self.color = color
            self.corners = corners

            # Generating the button
            self.generateButton()
        else:
            self.surface = icon
            self.size = self.surface.get_size()
        self.actionOnClick = actionOnClick
        self.coords = coords
        self.function_args = function_args

    def button_clicked(self, mouse_pos):
        pos = self.coords
        if pos[0] <= mouse_pos[0] <= pos[0] + self.size[0] and pos[1] <= mouse_pos[1] <= pos[1] + self.size[1]:
            if self.actionOnClick == "RT":
                return True
            else:
                self.actionOnClick(*self.function_args)
        elif self.actionOnClick == "RT":
            return False

    def __center__(self):
        global screen_size
        self.coords[0] = screen_size[0] // 2 - self.size[0] // 2
        self.coords[1] = screen_size[1] // 2 - self.size[1] // 2

    def generateButton(self):
        # -- Создание прямоугольника, в котором всё расположено
        rect = [0, 0, self.size[0], self.size[1]]
        pygame.draw.rect(self.surface, self.color, rect, int(self.size[1] / 2 + 0.5), self.corners, self.corners,
                         self.corners, self.corners)

        # -- Секция для текста на кнопке --
        fontSize = 24
        font = pygame.font.SysFont("arial", fontSize)
        text = font.render(self.text, True, self.textcolor)
        while (text.get_width() >= self.size[0] * 0.8 or fontSize <= 0) or (
                text.get_height() >= self.size[1] * 0.8):
            fontSize -= 1
            font = pygame.font.SysFont("arial", fontSize)
            text = font.render(self.text, True, self.textcolor)
            if fontSize <= 0:
                self.text = ""
        if self.text != "":
            textX = (self.size[0] / 2 - text.get_width() / 2)
            textY = (self.size[1] / 2 - text.get_height() / 2)
            self.surface.blit(text, [textX, textY])


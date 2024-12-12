import random
import pygame
from pygameTools import FPS, screen_size, Button
import math


class Tayson:
    def __init__(self, speed, x, y):
        self.floor = None
        self.going_to = None
        self.x_velocity = 0
        self.jumping_to = None
        costume_names = ["jumping_1", "jumping_2", "stationary_lying", "stationary_sitting", "stationary_sleeping",
                         "walking_close", "walking_far", "stationary_standing"]
        self.costumes = {name: pygame.image.load(f"pictures/tayson_models/png_resized/{name}.png") for name in
                         costume_names}
        self.walking_costumes = ["stationary_standing", "walking_close", "stationary_standing", "walking_far"]
        self.speed = speed
        self.mirrored = 1
        self.walk_costume = 0
        self.current_costume = "stationary_standing"
        self.y_velocity = 0
        self.is_jumping = False
        self.parab_jumping = False
        self.jump_height = 0
        self.reached_peack = False
        self.is_walking = False
        self.distance = 0
        self.points = {"bedhead": [22, 228], "near_wardrobe": [194, 228], "land_on_bed": [115, 181],
                       "go_further_into_bed": [61, 181],
                       "land_on_wardrobe": [244, 168], "near_table": [541, 228], "on_table": [541, 101],
                       "looking_into_the_window": [366, 129],
                       "on_shelf_1": [185, 89], "on_shelf_2": [82, 89]}
        self.routes = {'bedhead': ['go_further_into_bed', 'near_table', 'near_wardrobe'],
         'near_wardrobe': ['bedhead', 'land_on_bed', 'land_on_wardrobe', 'near_table'],
         'go_further_into_bed': ['bedhead', 'land_on_bed'],
         'near_table': ['bedhead', 'on_table', 'near_wardrobe', 'looking_into_the_window'],
         'land_on_bed': ['on_shelf_2', 'go_further_into_bed', 'land_on_wardrobe', 'on_shelf_1', 'near_wardrobe'],
         'land_on_wardrobe': ['land_on_bed', 'on_shelf_2', 'on_shelf_1', 'looking_into_the_window', 'near_wardrobe'],
         'on_shelf_1': ['land_on_bed', 'land_on_wardrobe'], 'on_shelf_2': ['land_on_bed', 'land_on_wardrobe'],
         'looking_into_the_window': ['land_on_wardrobe', 'near_table'], 'on_table': ['near_table']}
        self.current_position = random.choice([i for i in self.points])
        self.x, self.y = self.points[self.current_position]
        self.start_x = x
        self.touching_wall = False

    def jumpto(self, jump_destination):
        if not self.is_jumping:
            self.is_jumping = True
            self.jumping_to = jump_destination
            distance = math.sqrt((self.x-jump_destination[0])**2 + (self.y-jump_destination[1])**2)
            time_of_flight = distance / 20
            self.x_velocity = (self.x - jump_destination[0]) / time_of_flight
            self.y_velocity = (self.y - jump_destination[1]) / time_of_flight
            self.startdist = distance
            if (jump_destination[0] < self.x and self.mirrored == 1) or (jump_destination[0] > self.x and self.mirrored == -1):
                self.mirror()

    def walk(self, dest):
        if not self.touching_wall:
            if (dest < self.x and self.mirrored == 1) or (
                    dest > self.x and self.mirrored == -1):
                self.mirror()
            self.is_walking = True
            self.distance = abs(self.x - dest)
            self.start_x = self.x
            self.going_to = [dest, self.y]
            self.x_velocity = self.speed

    def realistic_jump(self, speed):
        if not self.parab_jumping:
            self.parab_jumping = True
            self.jump_height = pygame.mouse.get_pos()[1]
            self.x_velocity = speed
            self.y_velocity = -1 * ((screen_size[1] - self.jump_height) // 17.5)
            self.reached_peack = False
            self.floor = self.y

    def update(self):
        if self.x <= 0 or self.x >= screen_size[0] - self.costumes[self.current_costume].get_width():
            self.touching_wall = True
            if self.x > 20:
                self.x -= 5
            else:
                self.x += 5
            self.x_velocity = 0
        else:
            self.touching_wall = False

        if self.is_jumping:
            distance = math.sqrt((self.x - self.jumping_to[0]) ** 2 + (self.y - self.jumping_to[1]) ** 2)
            if distance >= self.startdist//3:
                self.current_costume = "jumping_2"
            else:
                self.current_costume = "jumping_1"
            self.y -= self.y_velocity
            self.x -= self.x_velocity
            if distance <= 10:
                self.x_velocity = 0
                self.y_velocity = 0
                self.is_jumping = False
                self.x, self.y = self.jumping_to
                self.current_costume = "stationary_standing"
                return 1

        if self.is_walking and not self.parab_jumping:
            if self.x <= self.x_velocity or self.x >= screen_size[0] - self.costumes[self.current_costume].get_width() - self.x_velocity:
                self.touching_wall = True
                self.x_velocity = 0
                self.distance = 0
                self.current_costume = "stationary_standing"
                self.walk_costume = 0
                self.is_walking = False
                self.going_to = [self.x, self.y]
                return 1
            elif abs(self.going_to[0] - self.x) <= 2:
                self.distance = 0
                self.current_costume = "stationary_standing"
                self.walk_costume = 0
                self.is_walking = False
                self.x, self.y = self.going_to
                if tick_count % 5 == 0:
                    self.walk_costume %= 4
                    self.current_costume = self.walking_costumes[self.walk_costume]
                    self.walk_costume += 1
                return 1
            elif not self.touching_wall:
                self.x += self.x_velocity * self.mirrored

        if self.parab_jumping:
            self.is_walking = False
            if self.x <= 0 or self.x >= screen_size[0] - self.costumes[self.current_costume].get_width():
                self.x_velocity = 0
            self.x += self.x_velocity * self.mirrored
            self.y += self.y_velocity
            self.y_velocity += 0.5
            if not self.reached_peack:
                self.current_costume = "jumping_1"
            if self.y <= self.jump_height and not self.reached_peack:
                self.y_velocity = 0
                self.reached_peack = True
                self.current_costume = "jumping_2"
            if self.y >= self.floor:
                self.y = self.floor
                self.y_velocity = 0
                self.x_velocity = 0
                self.parab_jumping = False
                self.current_costume = "stationary_standing"
                return 1
        return 0

    def mirror(self):
        for costume in self.costumes:
            self.costumes[costume] = pygame.transform.flip(self.costumes[costume], True, False)
        self.mirrored *= -1

    def behave(self):
        if self.current_costume == "stationary_sleeping":
            possibilities = ["stationary_sleeping", "stationary_sitting"]
            do = random.choice(possibilities)
            if do == "stationary_sleeping":
                return 1
            else:
                self.current_costume = possibilities[1]
                self.y += 9
                return 1
        elif self.current_costume == "stationary_sitting":
            possibilities = ["stationary_sleeping", "stationary_sitting", "stationary_standing"]
            do = random.choice(possibilities)
            if do == "stationary_sleeping":
                self.y -= 9
                self.current_costume = possibilities[0]
                return 1
            elif do == possibilities[2]:
                self.current_costume = possibilities[2]
                return 0
            else:
                return 1
        else:
            possibilites = self.routes[self.current_position]
            possibilites.append("sleep")
            do = random.choice(possibilites)
            if do == "sleep":
                self.y += 9
                self.current_costume = "stationary_sleeping"
                return 1
            else:
                if self.x == self.points[do][0]:
                    self.walk(abs(self.x - self.points[do][0]))
                else:
                    self.jumpto(self.points[do])
                self.current_position = do
            return 0


def draw_objects_l1():  # Drawing objects
    global boxes
    global rows
    for i in range(rows):
        pygame.draw.rect(screen, [148, 61, 21], [0, (screen_size[1] - 20) / rows * i + 92, screen_size[0], 5])
    for box_row in boxes:
        for box in box_row:
            screen.blit(box.surface, box.coords)


def draw_flashlight(size=200, transparency=None, bright=None):
    mouse_pos = pygame.mouse.get_pos()
    if not transparency:
        brightness = 10
        if bright is None:
            bright = 255
        mask.fill((brightness, brightness, brightness, 128))
        pygame.draw.circle(mask, (bright, bright, bright), mouse_pos, size)
    else:
        if bright is None:
            bright = 255
        flash_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
        pygame.draw.circle(flash_surface, (bright, bright, bright, transparency), mouse_pos, size)
        screen.blit(flash_surface, (0, 0))


def apply_mask():
    screen.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


def set_level(level):
    global level_id
    global playful_cat
    level_id = level
    music_channel.stop()
    sfx_channel.stop()
    if level == 4:
        playful_cat = Tayson(20, 100, screen_size[1] - 25)


def level_0(keys, buttons):
    bg = pygame.image.load("pictures/start_menu.png")
    screen.blit(bg, (0, 0))
    if not music_channel.get_busy():
        music_channel.play(start_menu_music)
    mouse_pos = pygame.mouse.get_pos()
    if start_button.coords[0] <= mouse_pos[0] <= start_button.coords[0] + start_button.size[0] and \
            start_button.coords[1] <= mouse_pos[1] <= start_button.coords[1] + start_button.size[1]:
        start_button.color = [219, 214, 46]
        start_button.generateButton()

    else:
        start_button.color = [39, 69, 161]
        start_button.generateButton()
    screen.blit(start_button.surface, start_button.coords)
    if buttons[0]:
        start_button.button_clicked(mouse_pos)


def level_1(keys, buttons):
    global tick_count
    global timer

    bg = pygame.image.load("pictures/main_room.png")
    screen.blit(bg, (0, 0))
    if not music_channel.get_busy():
        music_channel.play(main_menu_music)
    screen.blit(cat.costumes[cat.current_costume], [cat.x, cat.y])
    screen.blit(box_button.surface, box_button.coords)
    screen.blit(laser_pointer_icon.surface, laser_pointer_icon.coords)
    action = cat.update()
    if action == 1:
        timer = random.randint(30, 300)
    if timer == 0:
        if cat.behave() == 1:
            timer = random.randint(300, 1800)
        else:
            timer = -1
    elif timer > 0:
        timer -= 1

    if buttons[0]:
        box_button.button_clicked(pygame.mouse.get_pos())
        laser_pointer_icon.button_clicked(pygame.mouse.get_pos())


def level_2(keys, buttons):
    global timer
    global light_flickering
    global jumpscare_going_on
    global timer_jumpscare
    global all_eyed
    global time_since_disappearance
    global inhabited_box

    flashlight_size = 75
    bright = 0

    # Dark BG
    screen.fill((0, 0, 0))
    if not light_flickering or tick_count % 3 != 0:
        # Draw the flashlight
        draw_flashlight(flashlight_size)
    else:
        flashlight_size = random.randint(70, 80)
        bright = random.randint(0, 25) * 10
        draw_flashlight(flashlight_size, bright=bright)

    if jumpscare_going_on:
        for boxrow in boxes:
            for box in boxrow:
                box.surface = pygame.image.load("pictures/other_models/PNG/scaled/box_eyed.png")
        all_eyed = True
    elif all_eyed:
        for boxrow in boxes:
            for box in boxrow:
                box.surface = pygame.image.load("pictures/other_models/PNG/scaled/box.png")
        time_since_disappearance = 0
        inhabited_box = random.choice(random.choice(boxes))
        all_eyed = False

    # Draw game objects
    draw_objects_l1()

    # Draw the mask on top
    apply_mask()

    mask.fill((0, 0, 0, 128))

    if not light_flickering or tick_count % 3 != 0:
        # Draw the visible flashight
        draw_flashlight(flashlight_size, 50)
    else:
        draw_flashlight(flashlight_size, random.randint(15, 50), bright)

    if not music_channel.get_busy():
        music_channel.play(hide_n_seek_music)

    if not sfx_channel.get_busy():
        light_flickering = False
        jumpscare_going_on = False
        if timer == -1:
            timer = random.randint(600, 1200)
        if timer_jumpscare == -1:
            timer_jumpscare = random.randint(1200, 1800)

    if timer == 0 and not jumpscare_going_on:
        sfx_channel.play(flashlight_flicker)
        light_flickering = True
        timer = -1
    elif timer > 0:
        timer -= 1

    if timer_jumpscare == 0 and not light_flickering:
        sfx_channel.play(jumpscare)
        jumpscare_going_on = True
        timer_jumpscare = -1
    elif timer_jumpscare > 0:
        timer_jumpscare -= 1

    if time_since_disappearance >= 0:
        time_since_disappearance += 1
    if time_since_disappearance > FPS * 6:
        inhabited_box.surface = pygame.image.load("pictures/other_models/PNG/scaled/box_eyed.png")
        time_since_disappearance = -1

    mousepos = pygame.mouse.get_pos()
    dist = distance(mousepos[0], mousepos[1], inhabited_box.coords[0] + 36, inhabited_box.coords[1] + 36)
    if dist < flashlight_size * 0.5 and time_since_disappearance == -1 and not jumpscare_going_on:
        inhabited_box.surface = pygame.image.load("pictures/other_models/PNG/scaled/box.png")
        inhabited_box = random.choice(random.choice(boxes))
        inhabited_box.surface = pygame.image.load("pictures/other_models/PNG/scaled/box_eyed.png")
        if not light_flickering:
            timer = 1

    if buttons[0]:
        exit_button.button_clicked(mousepos)
    screen.blit(exit_button.surface, exit_button.coords)


def level_3(keys, buttons):
    pass


def level_4(keys, buttons):
    global laser_pointer
    global laser_dot
    screen.blit(lvl_4_bg, (0, 0))

    mousepos = pygame.mouse.get_pos()
    laser_dot_pos = [mousepos[0] - laser_dot.get_width() // 2, mousepos[1] - laser_dot.get_height() // 2]
    laser_pointer_pos = [mousepos[0] - laser_pointer.get_width() // 2, screen_size[1] - laser_pointer.get_height() // 2]

    screen.blit(laser_dot, laser_dot_pos)
    screen.blit(laser_pointer, laser_pointer_pos)

    if not music_channel.get_busy():
        music_channel.play(lvl_4_music)

    screen.blit(playful_cat.costumes[playful_cat.current_costume], [playful_cat.x, playful_cat.y])
    if abs(playful_cat.x - mousepos[0]) >= 20 and not playful_cat.parab_jumping:
        playful_cat.walk(mousepos[0])
    else:
        playful_cat.realistic_jump(5)
    playful_cat.floor = screen_size[1] - cat.costumes[cat.current_costume].get_height()
    playful_cat.update()

    if buttons[0]:
        exit_button.button_clicked(mousepos)
    screen.blit(exit_button.surface, exit_button.coords)


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)


def work_according_to_level(keys, buttons):
    global level_id
    if level_id == 0:
        level_0(keys, buttons)
    elif level_id == 1:
        level_1(keys, buttons)
    elif level_id == 2:
        level_2(keys, buttons)
    elif level_id == 3:
        level_3(keys, buttons)
    elif level_id == 4:
        level_4(keys, buttons)
    else:
        level_id = 1


# Screen creation
pygame.init()
screen = pygame.display.set_mode(screen_size)

mask = pygame.Surface(screen_size, pygame.SRCALPHA)
mask.fill((0, 0, 0, 128))

# Music and sounds setup
pygame.mixer.init()
start_menu_music = pygame.mixer.Sound("sound/music/game_enter.wav")
main_menu_music = pygame.mixer.Sound("sound/music/main_menu.wav")
music_channel = pygame.mixer.Channel(0)
sfx_channel = pygame.mixer.Channel(1)
music_channel.set_volume(0.05)
hide_n_seek_music = pygame.mixer.Sound("sound/music/scary_music.wav")
flashlight_flicker = pygame.mixer.Sound("sound/SFX/flickering_light.wav")
jumpscare = pygame.mixer.Sound("sound/SFX/jumpscare.wav")
lvl_4_music = pygame.mixer.Sound("sound/music/playful_music.wav")

# Mini-games entering buttons
box_button = Button(text="", actionOnClick=set_level, function_args=[2], icon=pygame.image.load("pictures/other_models/PNG/scaled/box.png"), coords=[563, 201])
laser_pointer_icon = Button(text="", actionOnClick=set_level, function_args=[4], icon=pygame.image.load("pictures/other_models/PNG/scaled/laser_pointer_icon.png"), coords=[563, 101])

# Level 2 setup
row_len = 6
rows = 4

boxes = [[Button(text="", actionOnClick="RT", function_args=[2], icon=pygame.image.load("pictures/other_models/PNG/scaled/box.png"), coords=[(screen_size[0] - 50) / row_len * j + 50, (screen_size[1] - 20) / rows * i + 20]) for j in range(row_len)] for i in range(rows)]
inhabited_box = random.choice(random.choice(boxes))
inhabited_box.surface = pygame.image.load("pictures/other_models/PNG/scaled/box_eyed.png")
light_flickering = False
all_eyed = False

# Level 4 setup
laser_pointer = pygame.image.load("pictures/other_models/PNG/scaled/laser_pointer.png")
laser_dot = pygame.image.load("pictures/other_models/PNG/scaled/laser_dot.png")
lvl_4_bg = pygame.image.load("pictures/bg2.png")
lvl_4_bg = pygame.transform.scale(lvl_4_bg, [screen_size[0], lvl_4_bg.get_height() * screen_size[0] / lvl_4_bg.get_width() * 0.85])

# Tayson setup
cat = Tayson(30, 150, 150)
timer = random.randint(120, 300)
timer_jumpscare = -1
jumpscare_going_on = False
time_since_disappearance = -1
playful_cat = Tayson(20, 100, screen_size[1] - 25)

# Main menu setup
start_button = Button([0, 0], [39, 69, 161], "Start", [21, 176, 78], set_level, corners=8, function_args=[1])
start_button.__center__()
exit_button = Button(actionOnClick=set_level, icon=pygame.image.load("pictures/exit.png"), function_args=[1])
exit_button.coords = [screen_size[0] - exit_button.size[0], 0]

# Main script
level_id = 0
tick_count = 0

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    click = False
    tick_count += 1
    tick_count %= 32767
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Level handler
    work_according_to_level(pygame.key.get_pressed(), pygame.mouse.get_pressed())

    # Update the display
    pygame.display.update()

pygame.quit()

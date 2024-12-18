import random
import pygame
import sys


WIDTH, HEIGHT = 400, 300
SCREEN_RATE = 2
MIN_PARTICLES_SIZE, MAX_PARTICLES_SIZE = 1, 4
MIN_INTERACT_DISTANCE, MAX_INTERACT_DISTANCE = 0, 80
VISCOSITY = 0.5
MAX_WEIGHT = 1
RULES_DICT = {}
COLORS = {'red': (255, 0, 0),
          'green': (0, 255, 0),
          'blue': (0, 0, 255),
          'white': (255, 255, 255),
          'yellow': (255, 255, 0),
          'purple': (255, 0, 255),
          'black': (0, 0, 0),
          'gray': (127, 127, 127),
          }

MENUS_LIST = list()


class Particle:
    def __init__(self, x, y, vx, vy, color, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size

    def interact(self, other_particles, weight):
        if weight == 0:
            return
        fx = 0
        fy = 0
        for other in other_particles:
            dx = self.x - other.x
            dy = self.y - other.y
            d = (dx * dx + dy * dy) ** 0.5
            if (MIN_INTERACT_DISTANCE < d <= MAX_INTERACT_DISTANCE):
                F = weight * other.size / d
                fx += F * dx
                fy += F * dy
        self.vx = (self.vx + fx) * VISCOSITY
        self.vy = (self.vy + fy) * VISCOSITY
        self.x += self.vx
        self.y += self.vy

        if self.x > WIDTH:
            self.vx = -abs(self.vx)
        if self.x < 0:
            self.vx = abs(self.vx)
        if self.y > HEIGHT:
            self.vy = -abs(self.vy)
        if self.y < 0:
            self.vy = abs(self.vy)


def random_Position():
    return random.randint(0, WIDTH), random.randint(0, HEIGHT)


def random_Size():
    return random.randint(MIN_PARTICLES_SIZE, MAX_PARTICLES_SIZE)


def random_Weight():
    if random.random() > 0.8:
        return 0
    return -MAX_WEIGHT + (random.random() * MAX_WEIGHT * 2)


def rule(group1, group2, weight):
    for this_particle in group1:
        this_particle.interact(group2, weight)


def create_particles(num, color):
    group = []
    for _ in range(num):
        group.append(Particle(*random_Position(), 0, 0,
                              COLORS[color],
                              random_Size()))
    return group


def make_Random_Rules(symetric=False):
    for g1, i1 in particles.items():
        for g2, i2 in particles.items():
            if (g1, g2) not in RULES_DICT:
                rand = round(random_Weight(), 2)
                RULES_DICT[(g1, g2)] = rand
                if symetric:
                    RULES_DICT[(g2, g1)] = rand
            rule(i1, i2, RULES_DICT[(g1, g2)])

    global MENUS_LIST
    MENUS_LIST = list(RULES_DICT.items())
    MENUS_LIST.sort()


def draw_Particles():
    for color, group in particles.items():
        for particle in group:
            pygame.draw.circle(screen,
                               color,
                               (particle.x * SCREEN_RATE,
                                particle.y * SCREEN_RATE),
                               particle.size)


def draw_All_Rules(surface):
    font = pygame.font.Font(None, 20)
    y = 0
    x = 0
    for idx, item in enumerate(MENUS_LIST):
        text = f'{idx:0d} ::   {item[0]} : {item[1]:>10}'
        text_surface = font.render(text, True,
                                   COLORS['white'], COLORS['black'])
        w, h = text_surface.get_rect().width, text_surface.get_rect().height
        y += h
        x = w if not x else x
        surface.blit(text_surface,
                     ((WIDTH * SCREEN_RATE - x) // 2,
                      (HEIGHT * SCREEN_RATE - h) // 4 + y))


def draw_menu(surface, text, value):
    text_surface = font.render('Use arrow keys to change items (h, r, *)',
                               True, COLORS['white'], COLORS['red'])
    w, h = text_surface.get_rect().width, text_surface.get_rect().height
    surface.blit(text_surface,
                 (WIDTH * SCREEN_RATE - w - 20, 20))

    text_surface = font.render(f'{text} : {value}', True,
                               COLORS['white'], COLORS['gray'])
    w2, h2 = text_surface.get_rect().width, text_surface.get_rect().height
    surface.blit(text_surface,
                 (WIDTH * SCREEN_RATE - w2 - 20, 20 + h + 10))


# init particles
red = create_particles(150, "red")
green = create_particles(150, "green")
blue = create_particles(150, "blue")
yellow = create_particles(150, "yellow")
purple = create_particles(150, "purple")
particles = {
    'red': red,
    'green': green,
    'blue': blue,
    'yellow': yellow,
    # 'purple': purple,
}


# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Font
font_size = 30
font = pygame.font.Font(None, font_size)

# Set window size and title
screen = pygame.display.set_mode((WIDTH * SCREEN_RATE, HEIGHT * SCREEN_RATE))
pygame.display.set_caption("Basic Pygame Window")

current_menu_index = 0
show_hint = False
# pyGame Running
running = True
while running:
    # Clear screen
    screen.fill(COLORS['black'])

    # Interact Particles
    make_Random_Rules(symetric=True)

    # Draw Particles
    draw_Particles()

    current_menu_text = MENUS_LIST[current_menu_index][0]
    current_menu_value = MENUS_LIST[current_menu_index][1]

    draw_menu(screen, current_menu_text, current_menu_value)

    if show_hint:
        draw_All_Rules(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle close button
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_menu_index -= 1
                if current_menu_index < 0:
                    current_menu_index = 0
            elif event.key == pygame.K_DOWN:
                current_menu_index += 1
                if current_menu_index >= len(MENUS_LIST):
                    current_menu_index = len(MENUS_LIST) - 1
            elif event.key == pygame.K_LEFT:
                RULES_DICT[current_menu_text] = round(
                    current_menu_value - 0.05, 2)
            elif event.key == pygame.K_RIGHT:
                RULES_DICT[current_menu_text] = round(
                    current_menu_value + 0.05, 2)
            elif event.unicode == '*':
                RULES_DICT[current_menu_text] = 0
            elif event.key == pygame.K_r:
                RULES_DICT.clear()
            elif event.key == pygame.K_h:
                show_hint = not show_hint
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

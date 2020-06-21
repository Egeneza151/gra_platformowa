import pygame, os, random
pygame.init()

# kolory
DARKRED = pygame.color.THECOLORS['darkred']
LIGHTRED = pygame.color.THECOLORS['palevioletred']
DARKGREEN = pygame.color.THECOLORS['darkgreen']
LIGHTBLUE = pygame.color.THECOLORS['lightblue']
BLACK = pygame.color.THECOLORS['black']
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']

# okno główne
os.environ['SDL_VIDEO_CENTERED'] = '1'    # centrowanie okna
SIZESCREEN = WIDTH, HEIGHT = 1366, 740
screen = pygame.display.set_mode(SIZESCREEN)

# grafika  - wczytywanie znaków
file_names = sorted(os.listdir('png'))
file_names.remove('background.png')
BACKGROUND = pygame.image.load(os.path.join('png', 'background.png')).convert()
for file_name in file_names:
    image_name = file_name[:-4]
    if '_L' in image_name or '_R' in image_name:
        image_name = image_name.upper()
    elif 'L' in image_name:
        image_name = image_name.replace('L', '_L').upper()
    elif 'R' in image_name:
        image_name = image_name.replace('R', '_R').upper()
    else:
       image_name = image_name.upper()
    if 'PLAYER_' in image_name:
        image_name = image_name.replace('PLAYER_', '').upper()
    globals().__setitem__(image_name, pygame.image.load(
        os.path.join('png', file_name)).convert_alpha(BACKGROUND))


# grafika postać
IMAGES_R = [WALK_R1, WALK_R2]
IMAGES_L = [WALK_L1, WALK_L2]

# grafika platformy
GRASS_LIST = [GRASS_SINGLE, GRASS_L, GRASS_C, GRASS_R]
METAL_LIST = [METAL_SINGLE, METAL_L, METAL_C, METAL_R]

# grafika ściany
WALL_LIST = [WALL, WALL_LEFT, WALL_TOP, WALL_RIGHT, WALL_BOTTOM]
WALL_CORNER_LIST = [WALL_TOP_L, WALL_TOP_R, WALL_BOTTOM_R, WALL_BOTTOM_L]


# grafika, broń i pociski

# grafika inne

# grafika enemy type 1 - zombie
ZOMBIE_WALK_R = [ZOMBIE_WALK_R1, ZOMBIE_WALK_R2]
ZOMBIE_WALK_L = [ZOMBIE_WALK_L1, ZOMBIE_WALK_L2]
ZOMBIE_DEAD_R = [ZOMBIE_DEAD_R, ZOMBIE_DEAD_R]
ZOMBIE_DEAD_L = [ZOMBIE_DEAD_L, ZOMBIE_DEAD_L]

# grafika enemy type 1 - bat
BAT_FLY_R = [BAT_FLY_R1, BAT_FLY_R2]
BAT_FLY_L = [BAT_FLY_L1, BAT_FLY_L2]
BAT_DEAD_R = [BAT_DEAD_R, BAT_DEAD_R]
BAT_DEAD_L = [BAT_DEAD_L, BAT_DEAD_L]

# grafika enemy type 1 - spider
SPIDER_WALK_R_LIST = [SPIDER_WALK_R1, SPIDER_WALK_R2]
SPIDER_WALK_L_LIST = [SPIDER_WALK_L1, SPIDER_WALK_L2]
SPIDER_DEAD_R_LIST = [SPIDER_DEAD_R, SPIDER_DEAD_R]
SPIDER_DEAD_L_LIST = [SPIDER_DEAD_L, SPIDER_DEAD_L]


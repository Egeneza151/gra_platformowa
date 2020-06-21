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

ZOMBIE_WALK1R = pygame.image.load(os.path.join('png', 'zombie_walk1R.png'))
ZOMBIE_WALK2R = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK2R.png'))
ZOMBIE_WALK3R = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK3R.png'))
ZOMBIE_WALK4R = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK4R.png'))
ZOMBIE_WALK5R = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK5R.png'))
ZOMBIE_WALK6R = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK6R.png'))

ZOMBIE_WALK1L = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK1L.png'))
ZOMBIE_WALK2L = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK2L.png'))
ZOMBIE_WALK3L = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK3L.png'))
ZOMBIE_WALK4L = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK4L.png'))
ZOMBIE_WALK5L = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK5L.png'))
ZOMBIE_WALK6L = pygame.image.load(os.path.join('png', 'ZOMBIE_WALK6L.png'))

ZOMBIE_DEAD3R = pygame.image.load(os.path.join('png', 'ZOMBIE_DEAD3R.png'))
ZOMBIE_DEAD6R = pygame.image.load(os.path.join('png', 'ZOMBIE_DEAD6R.png'))
ZOMBIE_DEAD3L = pygame.image.load(os.path.join('png', 'ZOMBIE_DEAD3L.png'))
ZOMBIE_DEAD6L = pygame.image.load(os.path.join('png', 'ZOMBIE_DEAD6L.png'))

ZOMBIE_ATTACK1R = pygame.image.load(os.path.join('png', 'ZOMBIE_ATTACK1R.png'))
ZOMBIE_ATTACK2R = pygame.image.load(os.path.join('png', 'ZOMBIE_ATTACK2R.png'))

ZOMBIE_ATTACK1L = pygame.image.load(os.path.join('png', 'ZOMBIE_ATTACK1L.png'))
ZOMBIE_ATTACK2L = pygame.image.load(os.path.join('png', 'ZOMBIE_ATTACK2L.png'))

ZOMBIE_HURT2R = pygame.image.load(os.path.join('png', 'ZOMBIE_HURT2R.png'))

ZOMBIE_HURT2L = pygame.image.load(os.path.join('png', 'ZOMBIE_HURT2L.png'))


COIN1 = pygame.image.load(os.path.join('png', 'coin1.png'))
COIN2 = pygame.image.load(os.path.join('png', 'coin2.png'))
COIN3 = pygame.image.load(os.path.join('png', 'coin3.png'))
COIN4 = pygame.image.load(os.path.join('png', 'coin4.png'))
COIN5 = pygame.image.load(os.path.join('png', 'coin5.png'))
COIN6 = pygame.image.load(os.path.join('png', 'coin6.png'))


DRZWI_CZER = pygame.image.load(os.path.join('png', 'drzwi_czerwone.png'))
DRZWI_ZIEL = pygame.image.load(os.path.join('png', 'drzwi_zielone.png'))


# grafika postać
IMAGES_R = [WALK_R1, WALK_R2, WALK_R3, WALK_R4, WALK_R5, WALK_R6, WALK_R7]
IMAGES_L = [WALK_L1, WALK_L2, WALK_L3, WALK_L4, WALK_L5, WALK_L6, WALK_L7]

IMAGES_DIE_R = [DIE_0, DIE_1, DIE_2, DIE_3, DIE_4, DIE_5, DIE_6]

# grafika platformy
GRASS_LIST = [GRASS_SINGLE, GRASS_L, GRASS_C, GRASS_R]
METAL_LIST = [METAL_SINGLE, METAL_L, METAL_C, METAL_R]

# grafika ściany
WALL_LIST = [WALL, WALL_LEFT, WALL_TOP, WALL_RIGHT, WALL_BOTTOM]
WALL_CORNER_LIST = [WALL_TOP_L, WALL_TOP_R, WALL_BOTTOM_R, WALL_BOTTOM_L]

#coiny
COINS = [COIN1, COIN2, COIN3, COIN4, COIN5, COIN6]

# grafika, broń i pociski

# grafika inne

# grafika enemy type 1 - zombie
# ZOMBIE_WALK_R = [ZOMBIE_WALK_R1, ZOMBIE_WALK_R2]
# ZOMBIE_WALK_L = [ZOMBIE_WALK_L1, ZOMBIE_WALK_L2]
# ZOMBIE_DEAD_R = [ZOMBIE_DEAD_R, ZOMBIE_DEAD_R]
# ZOMBIE_DEAD_L = [ZOMBIE_DEAD_L, ZOMBIE_DEAD_L]

ZOMBIE_WALK_R = [ZOMBIE_WALK1R,ZOMBIE_WALK2R,ZOMBIE_WALK3R,ZOMBIE_WALK4R,ZOMBIE_WALK5R,ZOMBIE_WALK6R]
ZOMBIE_WALK_L = [ZOMBIE_WALK1L,ZOMBIE_WALK2L,ZOMBIE_WALK3L,ZOMBIE_WALK4L,ZOMBIE_WALK5L,ZOMBIE_WALK6L]
ZOMBIE_DEAD_R = [ZOMBIE_DEAD3R,ZOMBIE_DEAD6R]
ZOMBIE_DEAD_L = [ZOMBIE_DEAD3L,ZOMBIE_DEAD6L]
ZOMBIE_ATTACK_R = [ZOMBIE_ATTACK1R,ZOMBIE_ATTACK2R]
ZOMBIE_ATTACK_L = [ZOMBIE_ATTACK1L,ZOMBIE_ATTACK2L]
ZOMBIE_HURT_R = [ZOMBIE_HURT2R]
ZOMBIE_HURT_L = [ZOMBIE_HURT2L]
#
# # grafika enemy type 1 - bat
# BAT_FLY_R = [BAT_FLY_R1, BAT_FLY_R2]
# BAT_FLY_L = [BAT_FLY_L1, BAT_FLY_L2]
# BAT_DEAD_R = [BAT_DEAD_R, BAT_DEAD_R]
# BAT_DEAD_L = [BAT_DEAD_L, BAT_DEAD_L]
#
# # grafika enemy type 1 - spider
# SPIDER_WALK_R_LIST = [SPIDER_WALK_R1, SPIDER_WALK_R2]
# SPIDER_WALK_L_LIST = [SPIDER_WALK_L1, SPIDER_WALK_L2]
# SPIDER_DEAD_R_LIST = [SPIDER_DEAD_R, SPIDER_DEAD_R]
# SPIDER_DEAD_L_LIST = [SPIDER_DEAD_L, SPIDER_DEAD_L]


import pygame, os
import game_module as gm

os.environ['SDL_VIDEO_CENTERED'] = '1'          # centrowanie okna
pygame.init()

## ustawienia ekranu i gry
screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption('Prosta gra platformowa...')
clock = pygame.time.Clock()


# klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.items = {}
        self.movement_x = 0
        self.movement_y = 0
        self._count = 0
        self.lifes = 3
        self.level = None
        self.direction_of_movement = 'right'

    def turn_right(self):
        self.movement_x = 6

    def turn_left(self):
        self.movement_x = -6

    def stop(self):
        self.movement_x = 0

    def update(self):
        self.rect.x += self.movement_x

        if self.movement_x > 0:
            self._move(gm.IMAGES_R)

        if self.movement_x < 0:
            self._move(gm.IMAGES_L)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.turn_right()
            if event.key == pygame.K_a:
                self.turn_left()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.movement_x > 0:
                self.stop()
                self.image = gm.STAND_R
            if event.key == pygame.K_a and self.movement_x < 0:
                self.stop()
                self.image = gm.STAND_L

    def _move(self, image_list):
        if self._count < 4:
            self.image = image_list[0]
        elif self._count < 8:
            self.image = image_list[1]

        if self._count >= 8:
            self._count = 0
        else:
            self._count += 1


# klasa platformy
class Platform(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, rect_x, rect_y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.image.fill(colour)
        self.rect.x = rect_x
        self.rect.y = rect_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


#ogólna klasa planszy
class Level:
    def __init__(self, player):
        self.set_of_platforms = set()
        self.player = player

    def update(self):
        for p in self.set_of_platforms:
            p.update()

    def draw(self, surface):
        for p in self.set_of_platforms:
            p.draw(surface)

# klasa planszy nr 1
class Level_1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.create_platforms()

    def crete_platforms(self):
        ws_platform_static = [[15 * 70, 70, 70, gm.HEIGHT - 70],
                              [4 * 70, 70, 100, 450],[4 * 70, 70, 1100, 350],
                              [3 * 70, 70, 800, 500]]

        for ws in ws_platform_static:
            platform_object = Platform(gm.DARKGREEN, *ws)
            self.set_of_platforms.add(platform_object)

# konkretyzacja obiektów
player = Player(gm.STAND_R)
current_level = Level_1(player)
player.level = current_level
player.rect.center = screen.get_rect().center

# głowna pętla gry
window_open = True
while window_open:
    screen.fill(gm.LIGHTBLUE)
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        elif event.type == pygame.QUIT:
            window_open = False

        player.get_event(event)

    # rysowanie i aktualizacja obiektów
    player.update()
    player.draw(screen)
    current_level.draw(screen)

    # aktualizacja okna pygame
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

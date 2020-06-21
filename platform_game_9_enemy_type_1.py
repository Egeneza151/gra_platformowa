import pygame, os, random
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
        if self.direction_of_movement == 'left':
            self.direction_of_movement = 'right'
        self.movement_x = 6

    def turn_left(self):
        if self.direction_of_movement == 'right':
            self.direction_of_movement = 'left'
        self.movement_x = -6

    def jump(self):
        self.rect.y += 2
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        self.rect.y -= 2
        if colliding_platforms:
            self.movement_y = -14

    def shoot(self):
        if self.items.get('shotgun', False) and len(self.level.set_of_bullets) < 2:
            if self.direction_of_movement == 'right':
                bullet = Bullet(
                    gm.BULLET_R,self.direction_of_movement,
                    self.rect.centerx, self.rect.centery+15)
            else:
                bullet = Bullet(
                    gm.BULLET_L, self.direction_of_movement,
                    self.rect.centerx, self.rect.centery+15)

            self.level.set_of_bullets.add(bullet)



    def stop(self):
        self.movement_x = 0

    def update(self):
        self._gravitation()

        # -----------------ruch w poziomie ----------------
        self.rect.x += self.movement_x

        # sparwdzanie kolizji
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)

        for p in colliding_platforms:
            if self.movement_x > 0:
                self.rect.right = p.rect.left
            if self.movement_x < 0:
                self.rect.left = p.rect.right

        # animacje
        if self.movement_x > 0:
            self._move(gm.IMAGES_R)
        if self.movement_x < 0:
            self._move(gm.IMAGES_L)

        # -----------------ruch w pionie ----------------
        self.rect.y += self.movement_y

        # sprawdzanie kolizji
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)

        for p in colliding_platforms:
            if self.movement_y > 0:
                self.rect.bottom = p.rect.top
                if self.direction_of_movement == 'left' and self.movement_x == 0:
                    self.image = gm.STAND_L
                if self.direction_of_movement == 'right' and self.movement_x == 0:
                    self.image = gm.STAND_R
            if self.movement_y < 0:
                self.rect.top = p.rect.bottom

            self.movement_y = 0

            # garcz jedzie razem z platformą
            if isinstance(p, MovingPlatform) and self.movement_x == 0:
                self.rect.x += p.movement_x


        self.rect.y += 3
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        self.rect.y -= 3

        # zmiana grafiki
        if not colliding_platforms:
            if self.movement_y > 0:
                if self.direction_of_movement == 'left':
                    self.image = gm.FALL_L
                else:
                    self.image = gm.FALL_R
            if self.movement_y < 0:
                if self.direction_of_movement == 'left':
                    self.image = gm.JUMP_L
                else:
                    self.image = gm.JUMP_R

        # sprawdzamy kolizję z przedmiotami
        colliding_items = pygame.sprite.spritecollide(
            self, self.level.set_of_items, False)
        for item in colliding_items:
            if item.name == 'shotgun':
                self.items[item.name] = 1
                item.kill()


    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.turn_right()
            if event.key == pygame.K_a:
                self.turn_left()
            if event.key == pygame.K_w:
                self.jump()
            if event.key == pygame.K_SPACE:
                self.shoot()
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

    def _gravitation(self):
        if self.movement_y == 0:
            self.movement_y = 2
        else:
            self.movement_y += 0.35

class Enemy(pygame.sprite.Sprite):
    def __init__(self, star_image, image_list_right,
                 image_list_left, image_list_right_dead, image_list_left_dead,
                 movement_x = 0, movement_y = 0):
        super().__init__()
        self.image = star_image
        self.image = self.image.get_rect()
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.image_list_right = image_list_right
        self.image_list_left = image_list_left
        self.image_list_right_dead = image_list_right_dead
        self.image_list_left_dead = image_list_left_dead
        self.direction_of_movement = 'right'
        self.lifes = 1
        self._count = 0


    def update(self):
        if not self.lifes and self._count > 7:
            self.kill()

        self.rect.x += self.movement_x

        #animacja
        if self.lifes:
            if self.movement_x > 0:
                self._move(self.image_list_right)
            if self.movement_x < 0:
                self._move(self.image_list_left)
        else:
            if self.direction_of_movement == 'right':
                self._move(self.image_list_right_dead)
            else:
                self._move(self.image_list_left_dead)


# klasa wrogra (typ 1)
class PlatformEnemy(Enemy):
    def __init__(self, star_image, image_list_right,
                 image_list_left, image_list_right_dead, image_list_left_dead, platform,
                 movement_x = 0, movement_y = 0):
        super().__init__(star_image, image_list_right,
                 image_list_left, image_list_right_dead, image_list_left_dead,
                 movement_x, movement_y)

        self.platform = platform
        self.rect.bottom = self.platform.rect.top
        self.rect.centerx = random.randint(self.platform.rect.letf + self.rect.width//2,
                                           self.platform.rect.right - self.rect.width//2,)




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
    def __init__(self, image_list, width, height, rect_x, rect_y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.image_list = image_list

    def draw(self, surface):
        if self.width == 70:
            surface.blit(self.image_list[0], self.rect)
        else:
            surface.blit(self.image_list[1], self.rect)
            for i in range(70, self.width - 70, 70):
                surface.blit(self.image_list[2], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[3], [self.rect.x + self.width - 70, self.rect.y])

# klasa reprezentująca ruchomą platformę
class MovingPlatform(Platform):
    def __init__(self,image_list ,width, height, rect_x, rect_y):
        super().__init__(image_list,width, height, rect_x, rect_y)
        self.movement_x = 0
        self.movement_y = 0
        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_right = 0
        self.boundary_left = 0
        self.player = None

    def update(self):
        # ruch prawo/lewo
        self.rect.x += self.movement_x
        # sprawdzamy kontakt z graczem
        if pygame.sprite.collide_rect(self, self.player):
            if self.movement_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        # ruch góra/dół
        self.rect.y += self.movement_y
        # sprawdzamy kontakt z graczem
        if pygame.sprite.collide_rect(self, self.player):
            if self.movement_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # sprawdzamy granice i decydujemy o zmianie kierunku
        # ruch w pionie
        if (self.rect.bottom > self.boundary_bottom
                or self.rect.top < self.boundary_top):
            self.movement_y *= -1

        # ruch w poziomie
        position = self.rect.x - self.player.level.world_shift
        if (position < self.boundary_left
                or position + self.width > self.boundary_right):
            self.movement_x *= -1


# ogólna klasa przedmiotu
class Item(pygame.sprite.Sprite):
    def __init__(self, image, name, rect_center_x, rect_center_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.center = [rect_center_x, rect_center_y]

# klasa reprezentująca pocisk
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, rect_center_x, rect_center_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [rect_center_x, rect_center_y]
        self.direction_of_movement = direction

    def update(self):
        if self.direction_of_movement == 'right':
            self.rect.x += 15
        else:
            self.rect.x -= 15




#ogólna klasa planszy
class Level:
    def __init__(self, player):
        self.set_of_platforms = set()
        self.set_of_items = pygame.sprite.Group()
        self.set_of_bullets = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0

    def update(self):
        self._delete_bullet()

        for p in self.set_of_platforms:
            p.update()

        self.set_of_bullets.update()

        # przesunięcie planszy gdy gracz jest zbliża się do prawej krawędzi
        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self._shift_world(-diff)

        # przesunięcie planszy gdy gracz jest zbliża się do lewej krawędzi
        if self.player.rect.left <= 150:
            diff = 150 - self.player.rect.left
            self.player.rect.left = 150
            self._shift_world(diff)


    def draw(self, surface):
        for p in self.set_of_platforms:
            p.draw(surface)

        self.set_of_items.draw(surface)
        self.set_of_bullets.draw(surface)

    def _shift_world(self, shift_x):
        self.world_shift += shift_x

        for p in self.set_of_platforms:
            p.rect.x += shift_x

        for item in self.set_of_items:
            item.rect.x += shift_x

        for b in self.set_of_bullets:
            b.rect.x += shift_x

    def _delete_bullet(self):
        for b in self.set_of_bullets:
            # sprwadzamy kolizje z platformami i usuwamy pocisk
            if pygame.sprite.spritecollideany(b, self.set_of_platforms):
                b.kill()
            # sprwadzamy czy pocisk wyleciał poza planszę i usuwamy pocisk
            if b.rect.left > gm.WIDTH or b.rect.right < 0:
                b.kill()



# klasa planszy nr 1
class Level_1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.create_platforms()
        self.create_moving_platforms()
        self.create_items()

    def create_platforms(self):
        ws_platform_static = [[50 * 70, 70, 70, gm.HEIGHT - 70],
                              [4 * 70, 70, 100, 350],[4 * 70, 70, 1100, 350],
                              [3 * 70, 70, 800, 500], [70, 70, 800, 250], [2*70, 70, 500, 150]]

        for ws in ws_platform_static:
            platform_object = Platform(gm.GRASS_LIST, *ws)
            self.set_of_platforms.add(platform_object)

    def create_moving_platforms(self):
        # tworzymy ruchomą platformę (ruch w poziomie)
        mp_x = MovingPlatform(gm.METAL_LIST, 3 * 70, 40, 1600, 350)
        mp_x.movement_x = -2
        mp_x.boundary_left = 1450
        mp_x.boundary_right = 2200
        mp_x.player = self.player
        self.set_of_platforms.add(mp_x)

        # tworzymy ruchomą platformę (ruch w poionie)
        mp_y = MovingPlatform(gm.METAL_LIST, 4 * 70, 40, 2350, 500)
        mp_y.movement_y = 2
        mp_y.boundary_top = 150
        mp_y.boundary_bottom = 550
        mp_y.player = self.player
        self.set_of_platforms.add(mp_y)

    def create_items(self):
        shotgun = Item(gm.SHOTGUN, 'shotgun', 100, gm.HEIGHT-120)
        self.set_of_items.add(shotgun)


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
    current_level.update()
    player.update()
    current_level.draw(screen)
    player.draw(screen)
    # aktualizacja okna pygame
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

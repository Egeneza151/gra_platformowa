import pygame, os, random
import game_module2 as gm

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
        self.hearts = {}
        self.lifes = 3
        self.number_of_lifes = self.lifes + len(self.hearts)
        self.coins = {}
        self.number_of_coins = 0 + len(self.coins)
        self.movement_x = 0
        self.movement_y = 0
        self._count = 0
        self.level = None
        self.direction_of_movement = 'right'
        self.die_count = 0
        self.door_count = 0

    #obrot w prawo
    def turn_right(self):
        if self.direction_of_movement == 'left':
            self.direction_of_movement = 'right'
        self.movement_x = 6
    #obrot w lewo
    def turn_left(self):
        if self.direction_of_movement == 'right':
            self.direction_of_movement = 'left'
        self.movement_x = -6
    #skok
    def jump(self):
        self.rect.y += 2
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        self.rect.y -= 2
        #gdy jest na platformie to moze skoczyc o 14 jednostek do gory
        if colliding_platforms:
            self.movement_y = -14
    #wykonuje strzal
    def shoot(self):
        #jezeli ma bron i pocuiskow jest mniej niz 2 to moze strzelic
        if self.items.get('weapon', False) and len(self.level.set_of_bullets) < 2:
            #strzal w prawo
            if self.direction_of_movement == 'right':
                bullet = Bullet(
                    gm.BULLET_R,self.direction_of_movement,
                    self.rect.centerx, self.rect.centery+15)
            #strzal w lewo
            else:
                bullet = Bullet(
                    gm.BULLET_L, self.direction_of_movement,
                    self.rect.centerx, self.rect.centery+15)

            self.level.set_of_bullets.add(bullet)
    #zatrzymuje sie
    def stop(self):
        self.movement_x = 0
    #glowna metoda aktualizacji gracza
    def update(self):
        #jezeli gracz ma wiecej zyc niz 0 to moze kontynuowac gre
        if self.number_of_lifes > 0:
            self._gravitation()

            # -----------------ruch w poziomie ----------------
            self.rect.x += self.movement_x

            # sparwdzanie kolizji
            colliding_platforms = pygame.sprite.spritecollide(
                self, self.level.set_of_platforms, False)

            for p in colliding_platforms:
                if self.movement_x > 0: #jezeli natrafi na kolizje(bloczek-scianka) zatrzymuje sie
                    self.rect.right = p.rect.left
                if self.movement_x < 0:
                    self.rect.left = p.rect.right

            # animacje
            if self.movement_x > 0:
                self._move(gm.IMAGES_R)   #obrazy ruchu w prawo pirata
            if self.movement_x < 0:
                self._move(gm.IMAGES_L) #obrazy ruchu w lewo

            # -----------------ruch w pionie ----------------
            self.rect.y += self.movement_y

            # sprawdzanie kolizji
            colliding_platforms = pygame.sprite.spritecollide(
                self, self.level.set_of_platforms, False)  # jezeli koliduje gracz z platforma

            for p in colliding_platforms: #dla kazdej plaformy z ktora koliduje wykonuje kod zawarty w petli
                if self.movement_y > 0:
                    self.rect.bottom = p.rect.top # kolizja platformy z dolna czescia pirata
                    if self.direction_of_movement == 'left' and self.movement_x == 0:
                        self.image = gm.STAND_L  #pod scaina koniec animiacji ruchu
                    if self.direction_of_movement == 'right' and self.movement_x == 0:
                        self.image = gm.STAND_R
                if self.movement_y < 0: # jest w powietrzu glowa z dolem platformy
                    self.rect.top = p.rect.bottom

                self.movement_y = 0

                # garcz jedzie razem z platformą
                if isinstance(p, MovingPlatform) and self.movement_x == 0: #jezeli znajduje sie na ruchomwej platformie to razem z nia
                    self.rect.x += p.movement_x


            self.rect.y += 3
            colliding_platforms = pygame.sprite.spritecollide(
                self, self.level.set_of_platforms, False)
            self.rect.y -= 3

            # zmiana grafiki
            if not colliding_platforms: # jest w powietrrzu
                if self.movement_y > 0:
                    if self.direction_of_movement == 'left':
                        self.image = gm.FALL_L # animacja spadania
                    else:
                        self.image = gm.FALL_R
                if self.movement_y < 0:
                    if self.direction_of_movement == 'left':
                        self.image = gm.JUMP_L
                    else:
                        self.image = gm.JUMP_R

            # sprawdzamy kolizję z przedmiotami
            #sprawdza kolizje z bronia
            colliding_items = pygame.sprite.spritecollide(
                self, self.level.set_of_items, False)
            for item in colliding_items:
                if item.name == 'weapon':
                    self.items[item.name] = 1
                    item.kill()
            # sprawdza kolizje z sercami
            colliding_hearts = pygame.sprite.spritecollide(
                self, self.level.set_of_hearts, False)
            for heart in colliding_hearts:
                if heart.name == 'heart':
                    self.hearts[heart.name] = 1
                    self.number_of_lifes += 1
                    heart.kill()
            # sprawdza kolizje z coinami
            colliding_coins = pygame.sprite.spritecollide(
                self, self.level.set_of_coins, False)
            for coin in colliding_coins:
                if coin.name == 'coin':
                    self.coins[coin.name] = 1
                    self.number_of_coins += 1
                    coin.kill()

            colliding_doors = pygame.sprite.spritecollide(
                self, self.level.set_of_doors, False)

            #sprawdza kolizje z drzwiami i przesuwa gracza
            print(self.door_count)
            if self.door_count == 0: # jezli nie dotknal sie drzwi
                for door in colliding_doors:
                    if door.online == True:
                        if door.name == 'door1':
                            self.rect.x += 1000
                        else:
                            self.rect.x -= 1000 # z 2 drzwi do 1  wraca 0 1000
                        self.door_count += 1 #co 40 klatek
            #operuje na liczniku drzwi, z ktorych mozna ponownie skorzystac
            else:
                self.door_count += 1
                if self.door_count == 40:
                    self.door_count = 0
                    for door in colliding_doors:
                        door.online = True
        #jezeli gracz posiada 0 lub mniej zyc to umiera
        else:
            self.game_over()

    #rysowanie animacji
    def draw(self, surface):
        surface.blit(self.image, self.rect) # jaki obraz oraz w jakim miesjcu
    #dzialanie na klawiszach
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
                self.image = gm.STAND_R # zatrzymanie postaci w prawej strony
            if event.key == pygame.K_a and self.movement_x < 0:
                self.stop()
                self.image = gm.STAND_L
    #rysowanie animacji co 4 klatki
    def _move(self, image_list):
        if self._count < 4:
            self.image = image_list[0]
        elif self._count < 8:
            self.image = image_list[1]

        if self._count >= 8:
            self._count = 0
        else:
            self._count += 1
    #grawitacja gracza
    def _gravitation(self):
        if self.movement_y == 0:
            self.movement_y = 2
        else:
            self.movement_y += 0.35
    #pobiera ilosc monet
    def get_coins(self):
        return "COINS: " + str(self.number_of_coins) #zamienia int'a na stringa
    #pobiera ilosc zyc
    def get_lifes(self):
        return "LIFES: " + str(self.number_of_lifes)
    #rysuje i przesuwa trupa co 4 klatki
    def _die(self, image_list):
        if self.die_count < 4:
            self.image = image_list[0]
            self.rect.y += 2
        elif self.die_count < 8:
            self.image = image_list[1]
            self.rect.y += 2
        elif self.die_count < 12:
            self.image = image_list[2]
            self.rect.y += 2
        elif self.die_count < 16:
            self.image = image_list[3]
            self.rect.y += 2
        elif self.die_count < 20:
            self.image = image_list[4]
            self.rect.y += 2
        elif self.die_count < 24:
            self.image = image_list[5]
            self.rect.y += 2
        elif self.die_count < 28:
            self.image = image_list[6]
            self.rect.y += 2

        self.die_count += 1
        #jezeli licznik sie skonczyl to ustawia licznik na podana liczbe
        if self.die_count >= 28: #klatki smierci
            self.door_count = 29
    #ustawia liczbe zyc na 0 i wykonuje metode smierci oraz rysuje na ekranie zakonczenie gry oraz zmienia tlo
    def game_over(self):
        self.number_of_lifes = 0
        self._die(gm.IMAGES_DIE_R)#rysuje animacje smierci
        screen.fill(gm.DARKRED) #czerwony ekran koniec gry
        myfont = pygame.font.SysFont('Comic Sans MS', 150)
        textsurface = myfont.render("GAME OVER", False, (0, 0, 0))
        screen.blit(textsurface, (300, -40)) # polozenie napisu

#klasa przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, star_image, image_list_right,
                 image_list_left, image_list_right_dead, image_list_left_dead,image_list_attack_right, image_list_attack_left, start, bound_l, bound_r,
                 movement_x = 0, movement_y = 0):
        super().__init__()
        self.image = star_image
        self.rect = self.image.get_rect()
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.image_list_right = image_list_right
        self.image_list_left = image_list_left
        self.image_list_right_dead = image_list_right_dead
        self.image_list_left_dead = image_list_left_dead
        self.image_list_attack_right = image_list_attack_right
        self.image_list_attack_left = image_list_attack_left
        self.direction_of_movement = 'right'
        self.lifes = 2
        self._count = 0

        self.boundary_left = bound_l
        self.boundary_right = bound_r
        self.player = None

        #temp ustawienia przeciwnika
        self.rect.x = start
        self.rect.y = self.movement_y

    #glowna metoda aktualizacji przeciwnika
    def update(self):
        #jezeli przeciwnik nie zyje i jego licznik jest wiekszy od zadanej liczby to umiera
        if not self.lifes and self._count > 7:
            self.kill()

        self.rect.x += self.movement_x

        #animacja
        #jezeli zyje to wykonuje
        if self.lifes:
            # zasieg ataku #-41 i 72
            distance_between_player = self.rect.x - player.rect.x
            if -241 < distance_between_player < 272:
                if self.movement_x > 0:
                    self._move(self.image_list_attack_right)
                    self.rect.x += 3
                if self.movement_x < 0:
                    self._move(self.image_list_attack_left)
                    self.rect.x += -3
            else:
                if self.movement_x > 0:
                    self._move(self.image_list_right)
                if self.movement_x < 0:
                    self._move(self.image_list_left)
        #jezeli umarl to wykonuje sie animacja smierci
        else:
            if self.direction_of_movement == 'right':
                self._move(self.image_list_right_dead)
            else:
                self._move(self.image_list_left_dead)

        #sprawdzanie kolizji
        if pygame.sprite.collide_rect(self, self.player):
            if self.player.direction_of_movement == 'left':
                self.player.rect.left = self.rect.right
                #odpychanie gracza od przeciwnika
                self.repulsion(80)
            elif self.player.direction_of_movement == 'right':
                self.player.rect.right = self.rect.left
                # odpychanie gracza od przeciwnika
                self.repulsion(-80)
            self.player.number_of_lifes -= 1

         # ruch w poziomie
        position = self.rect.x - self.player.level.world_shift
        if (position < self.boundary_left
                or position > self.boundary_right):
            self.movement_x *= -1

    # rysowanie animacji co 4 klatki
    def _move(self, image_list):
        if self._count < 4:
            self.image = image_list[0]
        elif self._count < 8:
            self.image = image_list[1]

        if self._count >= 8:
            self._count = 0
        else:
            self._count += 1

    #obrot w prawo
    def turn_right(self):
        if self.direction_of_movement == 'left':
            self.direction_of_movement = 'right'
        self.movement_x = 6
    #obrot w lewo
    def turn_left(self):
        if self.direction_of_movement == 'right':
            self.direction_of_movement = 'left'
            self.movement_x = -6

    # odpychanie gracza od przeciwnika
    def repulsion(self, distance):
        self.player.rect.x += distance

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

    # rysowanie animacji co 4 klatki
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
    def __init__(self, image_list, width, height, rect_x, rect_y, flag_position = 'left'):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.image_list = image_list
        self.flag_position = flag_position
    #rysowanie platformy
    def draw(self, surface):
        #jezeli jego szerokosc jest pojedyncza to sie wykona
        if self.width == 64:
            #jezeli jego wysokosc jest wiecej niz pojedyncza to sie wykona
            if self.height > 64:
                #strona lewa
                if self.flag_position == 'left':
                    #rysowanie
                    for i in range(64, self.height - 64, 64):
                        surface.blit(self.image_list[4], [self.rect.x, self.rect.y + i])
                #strona prawa
                elif self.flag_position == 'right':
                    # rysowanie
                    for i in range(64, self.height - 64, 64): #od 64 do podanej wysokosci -64, ze skokiem 64
                        surface.blit(self.image_list[5], [self.rect.x, self.rect.y + i]) # rysowanie w pionie
            else:
                surface.blit(self.image_list[0], self.rect)
        else:
            surface.blit(self.image_list[1], self.rect)
            for i in range(64, self.width - 64, 64):
                surface.blit(self.image_list[2], [self.rect.x + i, self.rect.y]) # w poziomie
            surface.blit(self.image_list[3], [self.rect.x + self.width - 64, self.rect.y])

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
    #glowna metoda aktualizujaca
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
    #glowna metoda aktualizacji
    def update(self):
        if self.direction_of_movement == 'right':
            self.rect.x += 15
        else:
            self.rect.x -= 15

class Heart(pygame.sprite.Sprite):
    def __init__(self, image, name, rect_center_x, rect_center_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.center = [rect_center_x, rect_center_y]

class Coin(pygame.sprite.Sprite):
    def __init__(self, image, name, rect_center_x, rect_center_y, image_list):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.center = [rect_center_x, rect_center_y]
        self.image_list = image_list

        self._count = 0
        self.draw(self.image_list)
    #rysowanie monety co 4 klatki
    def draw(self, image_list):
        if self._count < 4:
            self.image = image_list[0]
        elif self._count < 8:
            self.image = image_list[1]
        elif self._count < 12:
            self.image = image_list[2]
        elif self._count < 16:
            self.image = image_list[3]
        elif self._count < 20:
            self.image = image_list[4]
        elif self._count < 24:
            self.image = image_list[5]

        if self._count >= 24:
            self._count = 0
        else:
            self._count += 1
#klasa drzwi
class Door(pygame.sprite.Sprite):
    def __init__(self, image, name, rect_center_x, rect_center_y):
        super().__init__() # mozliwosc korzystania z biblioteki
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.center = [rect_center_x, rect_center_y]
        self.online = True

#ogólna klasa planszy
class Level:
    def __init__(self, player):
        self.set_of_platforms = set()
        self.set_of_items = pygame.sprite.Group()
        self.set_of_bullets = pygame.sprite.Group()
        self.set_of_enemies = pygame.sprite.Group()
        self.set_of_hearts = pygame.sprite.Group()
        self.set_of_coins = pygame.sprite.Group()
        self.set_of_doors = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0
    #glowna metoda aktualizacji
    def update(self):
        self._delete_bullet()
        self.die_player()
        #aktualizacja platform
        for p in self.set_of_platforms:
            p.update()
        #aktualizacja pociskow, wrogow i drzwi
        self.set_of_bullets.update()
        self.set_of_enemies.update()
        self.set_of_doors.update()
        #rysowanie monet
        for e in self.set_of_coins:
            e.draw(gm.COINS) # pobiera z module coiny

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

    #rysowanie
    def draw(self, surface):
        #rysowanie platform
        for p in self.set_of_platforms:
            p.draw(surface)
        #rysowanie broni, pociskow, wrogow, serc, monet i drzwi
        self.set_of_items.draw(surface)
        self.set_of_bullets.draw(surface)
        self.set_of_enemies.draw(surface)
        self.set_of_hearts.draw(surface)
        self.set_of_coins.draw(surface)
        self.set_of_doors.draw(surface)
    #przesuwanie swiata
    def _shift_world(self, shift_x):
        self.world_shift += shift_x
        #przesuwanie platform
        for p in self.set_of_platforms:
            p.rect.x += shift_x
        #przesuwanie broni
        for item in self.set_of_items:
            item.rect.x += shift_x
        #przesuwanie pociskow
        for b in self.set_of_bullets:
            b.rect.x += shift_x
        # przesuwanie wrogow
        for e in self.set_of_enemies:
            e.rect.x += shift_x
        # przesuwanie serc
        for heart in self.set_of_hearts:
            heart.rect.x += shift_x
        # przesuwanie monet
        for coin in self.set_of_coins:
            coin.rect.x += shift_x
        # przesuwanie drzwi
        for door in self.set_of_doors:
            door.rect.x += shift_x

    #usuwanie pociskow
    def _delete_bullet(self):
        #dla kazdego pocisku
        for b in self.set_of_bullets:
            # sprwadzamy kolizje z platformami i usuwamy pocisk
            if pygame.sprite.spritecollideany(b, self.set_of_platforms):
                b.kill()

            #sprawdzamy kolizje z przeciwnikami
            if pygame.sprite.spritecollideany(b, self.set_of_enemies):
                self._get_damage()
                b.kill()

            # sprwadzamy czy pocisk wyleciał poza planszę i usuwamy pocisk
            if b.rect.left > gm.WIDTH or b.rect.right < 0:
                b.kill()
    #metoda, w ktorej wrog otrzymuje obrazenia
    def _get_damage(self):
        for e in self.set_of_enemies:
            if pygame.sprite.spritecollideany(e, self.set_of_bullets):
                e.lifes -= 1
    #smierc gracza gry osiagnie zadana wysokosc
    def die_player(self):
        if player.rect.y > 630:
            player.game_over()

# klasa planszy nr 1
class Level_1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self.create_platforms()
        self.create_moving_platforms()
        self.create_items()
        self.create_enemies()
        self.create_hearts()
        self.create_coins()
        self.create_doors()
    #tworzenie platform
    def create_platforms(self):
        ws_platform_static = [[50 * 64, 64, 64, gm.HEIGHT - 64],
                              [4 * 64, 64, 100, 350],
                              [4 * 64, 64, 1100, 350],
                              [3 * 64, 64, 800, 500],
                              [64, 64, 800, 250],
                              [2*64, 64, 500, 150],
                              [64, 16*64, -128, -100, 'left'],
                              [64, 16*64, 3500, -100, 'right'],
                              [64, 64, 500, 500],
                              [4*64, 64, 800, 100]]
        #dodanie platform do zmiennej
        for ws in ws_platform_static:
            platform_object = Platform(gm.GRASS_LIST, *ws)
            self.set_of_platforms.add(platform_object)
    #tworzenie ruchomych platform
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
    #tworzenie broni
    def create_items(self):
        weapon = Item(gm.WEAPON, 'weapon', 100, gm.HEIGHT-120)
        self.set_of_items.add(weapon)
    #tworzenie wrogow
    def create_enemies(self):
        zombie = Enemy(gm.ZOMBIE_WALK_R[0],gm.ZOMBIE_WALK_R,gm.ZOMBIE_WALK_L,gm.ZOMBIE_DEAD_R,gm.ZOMBIE_DEAD_L,gm.ZOMBIE_ATTACK_R,gm.ZOMBIE_ATTACK_L,1000,1000,1500, movement_x=1,movement_y=600)
        zombie2 = Enemy(gm.ZOMBIE_WALK_R[0], gm.ZOMBIE_WALK_R, gm.ZOMBIE_WALK_L, gm.ZOMBIE_DEAD_R, gm.ZOMBIE_DEAD_L,gm.ZOMBIE_ATTACK_R, gm.ZOMBIE_ATTACK_L, 800, 800, 800+3*64, movement_x=2, movement_y=28)
        zombie.player = self.player
        zombie2.player = self.player
        self.set_of_enemies.add(zombie)
        self.set_of_enemies.add(zombie2)
    #tworzenie serc
    def create_hearts(self):
        heart = Heart(gm.HEART, 'heart', 200, gm.HEIGHT - 120)
        heart2 = Heart(gm.HEART, 'heart', 400, gm.HEIGHT - 120)
        self.set_of_hearts.add(heart)
        self.set_of_hearts.add(heart2)
    #tworzenie monet
    def create_coins(self):
        coin = Coin(gm.COIN1, 'coin', 300, gm.HEIGHT - 120, image_list = gm.COINS)
        coin2 = Coin(gm.COIN1, 'coin', 700, gm.HEIGHT - 120, image_list=gm.COINS)
        coin3 = Coin(gm.COIN1, 'coin', 500, gm.HEIGHT - 120, image_list=gm.COINS)
        self.set_of_coins.add(coin)
        self.set_of_coins.add(coin2)
        self.set_of_coins.add(coin3)
    #tworzenie drzwi
    def create_doors(self):
        door1 = Door(gm.DRZWI_CZER,'door1', 100+128, 350-64)
        door2 = Door(gm.DRZWI_ZIEL,'door2', 1100+128, 350-64)
        self.set_of_doors.add(door1)
        self.set_of_doors.add(door2)


# konkretyzacja obiektów
player = Player(gm.STAND_R)
current_level = Level_1(player)
player.level = current_level
player.rect.center = screen.get_rect().center

# głowna pętla gry
window_open = True
while window_open:
    #screen.fill(gm.LIGHTBLUE)
    screen.blit(gm.BACKGROUND,(0,0))

    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(player.get_coins(), False, (0, 0, 0))
    textsurface2 = myfont.render(player.get_lifes(), False, (0, 0, 0))
    screen.blit(textsurface, (0, 0))
    screen.blit(textsurface2, (1000, 0))
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

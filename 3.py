import pygame
import os
import random
##########################################################

class Settings(object):
    file_path = os.path.dirname(os.path.abspath(__file__))
    width = 700
    height = 600
    fps = 60       
    title = "Unstable Factory - Marvin G." 
    images_path = os.path.join(file_path, "bitmaps")
    music_path = os.path.join(file_path, "music")
    debug = False

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)

class Falling_Object(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "crateWood.png")).convert_alpha()
        self.tmp = random.randrange(40, 120)
        self.image = pygame.transform.scale(self.image, (self.tmp, self.tmp))
        self.rect = self.image.get_rect()
        self.rect.y = -100
        self.rect.centerx = random.randrange(40, Settings.width-40)
        self.max_speed = 6
        self.speed = random.randrange(3, self.max_speed)
        self.obj_count = 3

    def update(self):
        #Limit das nicht zu viele Blöcke spawnen.
        if len(game.all_falling_objects.sprites()) < self.obj_count + int(game.difficulty):
            game.all_falling_objects.add(Falling_Object())
        
        self.rect.y += self.speed + int(game.difficulty)

        #Objekte werden zerstört sobald y Wert erreicht wurde.
        if self.rect.y > 650:
            #Objete werden neuerstellt.
            self.kill()
            game.score += 1
            self.respawn()
        
        #Limit für die Schwierigkeit des Spiels.
        if game.difficulty < 6:
            game.difficulty += 0.0002

    def respawn(self):
        game.all_falling_objects.add(Falling_Object())

class FloatField(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "shield.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centery = game.spieler.rect.centery
        self.rect.centerx = game.spieler.rect.centerx

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.speed = 5
        self.index_idle = int(0)
        self.index_mov = 0

        #Laden der Bilder in 2 unterschiedlichen Arrays
        self.images_idle = []
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle1.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle2.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle3.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle4.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle5.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle6.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle7.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle8.png")))
        self.images_idle.append(pygame.image.load(os.path.join(Settings.images_path, "idle9.png")))

        self.images_mov = []
        self.images_mov.append(pygame.image.load(os.path.join(Settings.images_path, "mov1.png")))
        self.images_mov.append(pygame.image.load(os.path.join(Settings.images_path, "mov2.png")))
        self.images_mov.append(pygame.image.load(os.path.join(Settings.images_path, "mov3.png")))
        self.images_mov.append(pygame.image.load(os.path.join(Settings.images_path, "mov4.png")))
        self.images_mov.append(pygame.image.load(os.path.join(Settings.images_path, "mov5.png")))
        self.images_mov.append(pygame.image.load(os.path.join(Settings.images_path, "mov6.png")))
        self.images_mov.append(pygame.image.load(os.path.join(Settings.images_path, "mov8.png")))

        #Default-Image wird gesetzt und rect wird erzeugt.
        self.image = self.images_idle[self.index_idle]
        self.image = pygame.transform.scale(self.image, (48, 84))
        self.rect = self.image.get_rect()
        self.rect.bottom = Settings.height - 1

        #Variablen für die Bewegung des Spielers.
        self.direction = 0
        self.lock_left = 0
        self.lock_right = 0
        self.lock_up = 0
        self.lock_down = 0

        self.floatfield_activation = 580

    def update(self):
        #Durchlauf des Arrays "Idle" für die Animation beim stehen bleiben.
        self.index_idle += 0.2
        if self.index_idle >= len(self.images_idle):
            self.index_idle = 0
        self.image = self.images_idle[int(self.index_idle)]
        self.image = pygame.transform.scale(self.image, (48, 84))

        #Spieler kann nicht ausserhalb der Karte gehen.
        if self.rect.x <= 0:
            self.lock_left = 1
        else: self.lock_left = 0

        if self.rect.x >= Settings.width - 48:
            self.lock_right = 1
        else: self.lock_right = 0

        if self.rect.top <= 0:
            self.lock_up = 1
        else: self.lock_up = 0
        
        if self.rect.bottom >= Settings.height:
            self.lock_down = 1
        else: self.lock_down = 0

        #Bewegung von Links nach Rechts.
        keys = pygame.key.get_pressed()
        if self.lock_left == 0:
            if keys[pygame.K_LEFT]:
                self.direction = 1
                self.rect.x -= self.speed
                self.index_mov += 0.2
                if self.index_mov >= len(self.images_mov):
                    self.index_mov = 0
                self.image = self.images_mov[int(self.index_mov)]
                self.image = pygame.transform.scale(self.image, (48, 84))

        if self.lock_right == 0:
            if keys[pygame.K_RIGHT]:
                self.direction = 0
                self.rect.x += self.speed
                self.index_mov += 0.2
                if self.index_mov >= len(self.images_mov):
                    self.index_mov = 0
                self.image = self.images_mov[int(self.index_mov)]
                self.image = pygame.transform.scale(self.image, (48, 84))

        if self.lock_down == 0:
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed

        if self.lock_up == 0:
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed

        #Ändern der Spriterichtung
        if self.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.transform.flip(self.image, False, False)

        print(self.rect.bottom)

class TeleportHelper(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "teleport.jpg"))
        self.image = pygame.transform.scale(self.image, (60, 600))
        self.rect = self.image.get_rect()
        self.amount = 5
        self.pause = 0

    def check_col(self):
        #Siehe README.md für eine genauere Erklärung.
        if self.amount >= 1:
            self.rect.centery = game.spieler.rect.centery
            self.rect.centerx = random.randrange(24, Settings.width - 48)
            collision = pygame.sprite.groupcollide(game.all_tp, game.all_falling_objects, False, False)
            if bool(collision) == True:
                self.check_col()
            elif bool(collision) == False:
                game.spieler.rect.centerx = self.rect.centerx
                self.amount -= 1

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "pu.png"))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.speed = 4
        self.spawn_timer = random.randrange(0, 10000)
        self.rect.centery = -100
        self.rect.centerx = random.randrange(20, Settings.width-20)

    def update(self):
        self.rect.y += self.speed
        collision = pygame.sprite.groupcollide(game.all_pus, game.all_players, True, False)
        if bool(collision) == True:
            game.tp_help.amount += 1
            self.counter = 0

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.width, Settings.height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(os.path.join(Settings.images_path, "background.jpg")).convert_alpha()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()
        self.done = False

        self.score = 0

        #Initialisierung der fallenden Objekte.
        self.fall_obj = Falling_Object()
        self.all_falling_objects = pygame.sprite.Group()
        self.all_falling_objects.add(self.fall_obj)

        #Initialisierung des Spielers.
        self.spieler = Player()
        self.all_players = pygame.sprite.Group()
        self.all_players.add(self.spieler)

        #Initialisierung für die Teleport-Hilfe.
        self.tp_help = TeleportHelper()
        self.all_tp = pygame.sprite.Group()
        self.all_tp.add(self.tp_help)

        #Powerup
        self.pu_counter = 0
        self.all_pus = pygame.sprite.Group()

        #Float Field
        self.float_field = FloatField()
        self.all_float_fields = pygame.sprite.Group()
        self.all_float_fields.add(self.float_field)

        #Schwierigkeit wird auf 0 gesetzt am Anfang des Spiels.
        self.difficulty = 0

        #Am Anfang soll man leben.
        self.dead = 0


        pygame.font.init()

        #Initialisierung der Text-Variablen
        self.myfont = pygame.font.SysFont('Arial Black', 30)
        self.myfont_2 = pygame.font.SysFont('Arial Black', 20)
        self.score_display = self.myfont.render(str(self.score), True, (0, 0, 0))

        self.difficulty_display = self.myfont.render(str(self.difficulty), True, (0, 0, 0))

        #Initialisierung der Musikbibliothek
        pygame.mixer.init()
        pygame.mixer.music.load((os.path.join(Settings.music_path, "theme.wav")))
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(loops=-1)

        self.secret = []
        self.hint = ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a", "start"]
        self.secret_used = 0
        
    
    def run(self):
        while not self.done:             # Hauptprogrammschleife mit Abbruchkriterium   
            keys = pygame.key.get_pressed()
            self.clock.tick(Settings.fps)          # Setzt die Taktrate auf max 60fps   
            for event in pygame.event.get():    # Durchwandere alle aufgetretenen  Ereignisse
                if event.type == pygame.QUIT:   # Wenn das rechts obere X im Fenster geklicktr
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                    elif event.key == pygame.K_RETURN:
                        if self.dead == 1:
                            self.done = True
                    elif event.key == pygame.K_r:
                        if self.dead == 1:
                            self.dead = 0
                            self.fall_obj.respawn()
                            self.tp_help.amount = 5
                    elif keys[pygame.K_0]:
                        if self.secret_used == 0:
                            if event.key == pygame.K_UP:
                                self.secret.append("up")
                            elif event.key == pygame.K_DOWN:
                                self.secret.append("down")
                            elif event.key == pygame.K_LEFT:
                                self.secret.append("left")
                            elif event.key == pygame.K_RIGHT:
                                self.secret.append("right")
                            elif event.key == pygame.K_b:
                                self.secret.append("b")
                            elif event.key == pygame.K_a:
                                self.secret.append("a")
                            elif event.key == pygame.K_SPACE:
                                self.secret.append("start")

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.tp_help.check_col()
            
            if self.secret == self.hint:
                self.tp_help.amount = 101
                self.secret_used = 1
                self.secret = []
            self.screen.blit(self.background, self.background_rect)
            self.all_falling_objects.draw(self.screen)
            self.all_falling_objects.update()

            self.all_float_fields.update()
            if self.spieler.rect.bottom <= self.spieler.floatfield_activation:
                self.all_float_fields.draw(self.screen)

            self.all_pus.draw(self.screen)
            self.all_pus.update()
            if self.pu_counter == random.randrange(0, 10000):
                self.all_pus.add(PowerUp())

            #Der Spieler soll im endscreen nicht zu sehen sein.
            if self.dead == 0:
                self.all_players.draw(self.screen)
            self.all_players.update()

            #Sobald Settings.debug auf True gesetzt wird kann man die "Scan-Kiste" sehen.
            if Settings.debug == True:
                self.all_tp.draw(self.screen)
            self.all_tp.update()

            #Kollision von Spieler und Box
            collision = pygame.sprite.groupcollide(self.all_players, self.all_falling_objects, False, False, collided=pygame.sprite.collide_rect_ratio(.75))
            if bool(collision) == True:
                self.difficulty = 0
                self.score = 0
                self.dead = 1
                game.all_falling_objects.empty()
                
        
            #Wenn dead=0 dann wird er normale Text ausgegeben (Score, Difficulty).
            #Wenn dead=1 dann wird der endscreen ausgegeben.
            if self.dead == 0:
                self.screen.blit(self.score_display,(10,0))
                self.score_display = self.myfont.render(str(self.score), True, (0, 0, 0))

                self.score_text = self.myfont.render(str("Punkte"), True, (0, 0, 0))
                self.screen.blit(self.score_text,(10,30))

                self.screen.blit(self.difficulty_display,(Settings.width - 50, 0))
                self.difficulty_display = self.myfont.render(str(self.difficulty), True, (0, 0, 0))

                self.difficulty_text = self.myfont.render(str("Schwierigkeit"), True, (0, 0, 0))
                self.screen.blit(self.difficulty_text,(Settings.width-230,30))

                self.amount_left = self.myfont.render(str(game.tp_help.amount), True, (0, 0, 0))
                self.screen.blit(self.amount_left,(10, 80))

                self.amount_text = self.myfont.render(str("Teleports über"), True, (0, 0, 0))
                self.screen.blit(self.amount_text,(10, 110))
            elif self.dead == 1:
                self.death_text = self.myfont_2.render(str("Verloren! Drücke \"ENTER\" um das Spiel zu beenden."), True, (0, 0, 0))
                self.screen.blit(self.death_text,(60, Settings.height // 3))

                self.death_text_2 = self.myfont_2.render(str("Um nochmal zu spielen drücke \"R\""), True, (0, 0, 0))
                self.screen.blit(self.death_text_2,(160, Settings.height // 2.5))

            pygame.display.flip()

game = Game()
if __name__ == '__main__':
                                    
    pygame.init()               # Bereitet die Module zur Verwendung vor
    pygame.mixer.init()
    game.run()
    pygame.quit()               # beendet pygame

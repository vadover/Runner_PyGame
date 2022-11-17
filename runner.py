# ==IMPORTS==
import pygame   # Импорт модуля "pygame"
import sys
from random import randint, choice

# ==PLAYER==
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics\Player\player_walk_1.png').convert_alpha()    # Импорт изображения игрока
        player_walk_2 = pygame.image.load('graphics\Player\player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics\Player\jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio\jump.mp3')
        self.jump_sound.set_volume(0.5)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

# ==OBSTACLES==
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            # ==IMPORT IMAGE FLY==
            fly_1 = pygame.image.load('graphics\Fly\Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics\Fly\Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            # ==IMPORT IMAGE SNAIL==
            snail_1 = pygame.image.load('graphics\snail\snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics\snail\snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

# ==SCORE COUNTER==
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# ==COLLISION==
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True
    
# ==MAIN FUNCTIONS==
pygame.init()   # Инициализация
screen = pygame.display.set_mode((800, 400))    # Отрисовка дисплея
pygame.display.set_caption('Runner')    # Название окна
clock = pygame.time.Clock()
font = pygame.font.Font('font\Pixeltype.ttf', 50)  # Подключение шрифта
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound('audio\music.wav')
bg_Music.set_volume(0.5)
bg_Music.play(loops = -1)

# ==GROUPS==
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# ==BACKGROUND SPRITES==
sky_surface = pygame.image.load('graphics\Sky.png').convert()   # Импорт изображения неба
ground_surface = pygame.image.load('graphics\ground.png').convert()  # Импорт изображения земли

# ==INTRO SCREEN==
player_stand = pygame.image.load('graphics\Player\player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

name_game = font.render('RunnerGame', False, (64,64,64))
name_game_rect = name_game.get_rect(center = (400, 70))

text_over = font.render('Press the space bar to restart', False, (64,64,64))
text_over_rect = text_over.get_rect(center = (400, 330))

# ==TIMER==
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# ==MAIN PART==
while True:
    # ==INPUT USER==
    for event in pygame.event.get():
        # ==QUIT==
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        
    if game_active:
        # ==BACKGROUND==
        screen.blit(sky_surface, (0, 0))    # Отрисовка изображения неба на координатах (0, 0)
        screen.blit(ground_surface, (0, 300))   # Отрисовка изображения земли на координатах (0, 300)
        score = display_score()

        # ==PLAYER==
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()

    else:
        # ==GAME OVER SCREEN==
        screen.fill('#d0f4f7')
        screen.blit(player_stand, player_stand_rect)

        score_message = font.render(f'Your score: {score}', False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400,370))
        screen.blit(score_message, score_message_rect)
        screen.blit(name_game, name_game_rect)
        screen.blit(text_over, text_over_rect)

    pygame.display.update()
    clock.tick(60)
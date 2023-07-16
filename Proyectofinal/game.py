import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FNAF Game")
icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)

# Fuente del texto
font = pygame.font.Font(None, 36)

# Variables del juego
score = 0
game_over = False

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -10
        if keys[pygame.K_RIGHT]:
            self.speed_x = 10
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase del enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = 0.9

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)


#Clase meteoros
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("meteor.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)
# Clase del proyectil
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Cargar imágenes
background = pygame.image.load("background.png")
start_screen = pygame.image.load("start.png")
score_screen = pygame.image.load("score.png")
credits_screen = pygame.image.load("credits.png")

# Iniciar el reloj
clock = pygame.time.Clock()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


# Funciones auxiliares
def show_menu_screen():
    screen.blit(start_screen, (0, 0))
    text = font.render("Five Nights at Freddy's", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))


    text = font.render("1 - Play Game", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    text = font.render("2 - High Scores", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))

    text = font.render("3 - Credits", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 100))

    text = font.render("4 - Quit", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 150))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "scores"
                elif event.key == pygame.K_3:
                    return "credits"
                elif event.key == pygame.K_4:
                    pygame.quit()
                    exit()

def show_start_screen():
    screen.blit(start_screen, (0, 0))
    pygame.display.flip()
    wait_for_key()

def show_score_screen():
    screen.blit(score_screen, (0, 0))
    show_scores()
    pygame.display.flip()
    wait_for_key()

def show_credits_screen():
    screen.blit(credits_screen, (0, 0))
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_scores():
    scores = read_scores()
    text = font.render("Scoreboard", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
    y = 100
    for score in scores:
        text = font.render(score[0] + ": " + str(score[1]), True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50

def read_scores():
    scores = []
    with open("scores.txt", "r") as file:
        for line in file:
            name, score = line.strip().split(",")
            scores.append((name, int(score)))
    return scores

def write_score(name, score):
    with open("scores.txt", "a") as file:
        file.write(name + "," + str(score) + "\n")

# Función principal del juego
def game():
    global score
    running = True
    game_over = False
    meteor_spawn_time = 60  # Controla la frecuencia de aparición de meteoritos
    meteor_timer = 0

    enemy_speed_increment = .5  # Incremento de velocidad de los enemigos
    enemies_speed = 1  # Velocidad inicial de los enemigos
    while running:
        if game_over:
            screen.fill(BLACK)
            text = font.render("Game Over", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            write_score(player_name, score)
            wait_for_key()
            break

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Actualizar
        all_sprites.update()

        # Controlar la aparición de meteoritos
        meteor_timer += 1
        if meteor_timer >= meteor_spawn_time and score >= 30:
            meteor = Meteor()
            all_sprites.add(meteor)
            meteors.add(meteor)
            meteor_timer = 0

        # Colisiones - Jugador y Enemigo o Meteorito
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            game_over = True

        # Colisiones - Jugador y Meteorito
        hits = pygame.sprite.spritecollide(player, meteors, True)
        if hits:
            game_over = True


        # Colisiones - Enemigo y Bala
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            score += 1
            if score >= 10 and enemies_speed < 1.5:
                enemies_speed += enemy_speed_increment
            if score >= 20 and enemies_speed < 2.2:
                enemies_speed += enemy_speed_increment
            if score >= 21 and enemies_speed < 2.4:
                enemies_speed += enemy_speed_increment
            if score == 30:
                for _ in range(2):
                    meteor = Meteor()
                    all_sprites.add(meteor)
                    meteors.add(meteor)

        # Colisiones - Jugador y Enemigo o Meteorito
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            game_over = True

        # Colisiones - Jugador y Meteorito
        hits = pygame.sprite.spritecollide(player, meteors, True)
        if hits:
            game_over = True

        # Colisiones - Meteorito y Bala
        hits = pygame.sprite.groupcollide(meteors, bullets, True, True)

        # Verificar si los enemigos alcanzaron el borde inferior de la pantalla
        for enemy in enemies:
            if enemy.rect.bottom >= HEIGHT:
                game_over = True

        # Verificar si los meteoritos alcanzaron el borde inferior de la pantalla
        for meteor in meteors:
            if meteor.rect.bottom >= HEIGHT:
                game_over = True

        # Actualizar velocidad de los enemigos
        for enemy in enemies:
            enemy.speed_y = enemies_speed

        # Renderizar
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()

        # Frecuencia de actualización
        clock.tick(60)

while True:
    option = show_menu_screen()
    if option == "play":
        # Preguntar el nombre del jugador
        player_name = input("Ingresa tu nombre: ")
        score = 0
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        # Cargar meteoritos
        meteors = pygame.sprite.Group()

        # Crear jugador
        player = Player()
        all_sprites.add(player)

        # Cargar enemigos
        for _ in range(3):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Iniciar el juego
        game()

        # Pantalla de scoreboard
        show_score_screen()
    elif option == "scores":
        # Pantalla de scoreboard
        show_score_screen()

    elif option == "credits":
        #Mostrar creditos
        show_credits_screen()

# Salir del juego
pygame.quit()


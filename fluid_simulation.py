import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Parámetros del juego
width, height = 800, 600
car_width, car_height = 50, 80
car_speed = 5
enemy_speed = 5

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Clase del jugador (coche)
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - car_height)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= car_speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += car_speed

# Clase del enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - car_width)
        self.rect.y = random.randint(-height, 0)

    def update(self):
        self.rect.y += enemy_speed
        if self.rect.top > height:
            self.rect.x = random.randint(0, width - car_width)
            self.rect.y = random.randint(-height, 0)

# Inicializar la pantalla
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Racing Game")

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Crear jugador
player = Car()
all_sprites.add(player)

# Crear enemigos
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Reloj de Pygame
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar sprites
    all_sprites.update()

    # Verificar colisiones
    if pygame.sprite.spritecollide(player, enemies, False):
        print("¡Colisión!")
        # Puedes agregar aquí lógica adicional para manejar la colisión, como reiniciar el juego.

    # Limpiar la pantalla
    screen.fill(white)

    # Dibujar sprites en la pantalla
    all_sprites.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(30)

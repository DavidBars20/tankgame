import pygame
import random

pygame.init()

# Tela do jogo
Screen_Width = 600
Screen_Height = 400
win = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Tank Battle")

# Cores
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

# FPS e relógio
FPS = 60
clock = pygame.time.Clock()

# Fontes
font = pygame.font.SysFont('Arial', 30)

# Funções de renderização de texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Classe do tanque
class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.speed = 5
        self.color = color
        self.direction = 'UP'
        self.alive = True

    def draw(self, win):
        if self.alive:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
            # Desenhar o canhão
            if self.direction == 'UP':
                pygame.draw.line(win, self.color, (self.x + self.width//2, self.y), (self.x + self.width//2, self.y - 10), 4)
            elif self.direction == 'DOWN':
                pygame.draw.line(win, self.color, (self.x + self.width//2, self.y + self.height), (self.x + self.width//2, self.y + self.height + 10), 4)
            elif self.direction == 'LEFT':
                pygame.draw.line(win, self.color, (self.x, self.y + self.height//2), (self.x - 10, self.y + self.height//2), 4)
            elif self.direction == 'RIGHT':
                pygame.draw.line(win, self.color, (self.x + self.width, self.y + self.height//2), (self.x + self.width + 10, self.y + self.height//2), 4)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = 'LEFT'
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = 'RIGHT'
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = 'UP'
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = 'DOWN'

        # Limites de tela
        self.x = max(0, min(Screen_Width - self.width, self.x))
        self.y = max(0, min(Screen_Height - self.height, self.y))

# Classe do projétil
class Projectile:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.size = 5
        self.speed = 10
        self.direction = direction
        self.color = color

    def move(self):
        if self.direction == 'UP':
            self.y -= self.speed
        elif self.direction == 'DOWN':
            self.y += self.speed
        elif self.direction == 'LEFT':
            self.x -= self.speed
        elif self.direction == 'RIGHT':
            self.x += self.speed

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size)

    def off_screen(self):
        return self.x < 0 or self.x > Screen_Width or self.y < 0 or self.y > Screen_Height

    def collide(self, tank):
        return tank.x < self.x < tank.x + tank.width and tank.y < self.y < tank.y + tank.height

# Classe do inimigo
class EnemyTank(Tank):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.speed = random.randint(2, 4)

    def move_continuous(self):
        # Movimenta continuamente na direção atual
        if self.direction == 'LEFT':
            self.x -= self.speed
        elif self.direction == 'RIGHT':
            self.x += self.speed
        elif self.direction == 'UP':
            self.y -= self.speed
        elif self.direction == 'DOWN':
            self.y += self.speed

        # Troca de direção se atingir os limites da tela
        if self.x <= 0 or self.x >= Screen_Width - self.width:
            self.direction = 'RIGHT' if self.direction == 'LEFT' else 'LEFT'
        if self.y <= 0 or self.y >= Screen_Height - self.height:
            self.direction = 'DOWN' if self.direction == 'UP' else 'UP'

# Função para gerar novos tanques
def generate_enemy_tank(enemies):
    if len(enemies) < 5:  # Limite de 5 tanques inimigos na tela ao mesmo tempo
        x = random.randint(0, Screen_Width - 40)
        y = random.randint(0, Screen_Height - 40)
        new_enemy = EnemyTank(x, y, Red)
        enemies.append(new_enemy)

# Função para desenhar os menus
def main_menu():
    menu = True
    while menu:
        win.fill(Black)
        draw_text('Tank Battle', font, White, win, Screen_Width//2 - 100, Screen_Height//2 - 100)
        draw_text('Press Enter to Play', font, Green, win, Screen_Width//2 - 150, Screen_Height//2)
        draw_text('Press Q to Quit', font, Red, win, Screen_Width//2 - 100, Screen_Height//2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Função principal do jogo
def game_loop():
    player_tank = Tank(Screen_Width // 2, Screen_Height - 60, Blue)
    enemies = [EnemyTank(random.randint(0, Screen_Width-40), random.randint(0, Screen_Height-40), Red) for _ in range(3)]
    
    player_projectiles = []
    enemy_projectiles = []
    
    running = True
    spawn_timer = 0

    while running:
        clock.tick(FPS)
        win.fill(Black)
        
        # Eventos de controle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_tank.move(keys)

        # Disparar projétil do jogador
        if keys[pygame.K_SPACE]:
            if len(player_projectiles) < 5:  # Limitar projéteis simultâneos
                proj = Projectile(player_tank.x + player_tank.width//2, player_tank.y, player_tank.direction, White)
                player_projectiles.append(proj)

        # Gerar novos tanques inimigos periodicamente
        spawn_timer += 1
        if spawn_timer > FPS * 5:  # Gerar um novo tanque inimigo a cada 5 segundos
            generate_enemy_tank(enemies)
            spawn_timer = 0

        # Movimentação e desenho dos inimigos
        for enemy in enemies:
            enemy.move_continuous()
            enemy.draw(win)

        # Movimentar e desenhar projéteis do jogador
        for proj in player_projectiles:
            proj.move()
            proj.draw(win)
            if proj.off_screen():
                player_projectiles.remove(proj)
            for enemy in enemies:
                if proj.collide(enemy) and enemy.alive:
                    enemy.alive = False
                    if proj in player_projectiles:
                        player_projectiles.remove(proj)

        # Inimigos disparando projéteis
        for enemy in enemies:
            if random.random() < 0.02:  # Probabilidade de disparo
                proj = Projectile(enemy.x + enemy.width//2, enemy.y + enemy.height//2, enemy.direction, Red)
                enemy_projectiles.append(proj)

        # Movimentar e desenhar projéteis dos inimigos
        for proj in enemy_projectiles:
            proj.move()
            proj.draw(win)
            if proj.off_screen():
                enemy_projectiles.remove(proj)
            if proj.collide(player_tank):
                running = False  # Fim de jogo se o jogador for atingido

        # Desenhar o tanque do jogador
        player_tank.draw(win)

        pygame.display.update()

    pygame.quit()

# Executar o menu e iniciar o jogo
main_menu()
game_loop()

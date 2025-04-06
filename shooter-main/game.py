from pygame import *
from assets import *
from random import randint

# фонова музика
mixer.init()
mixer.music.load(GAME_MUSIC)
mixer.music.play(-1)
fire_sound = mixer.Sound(FIRE_SOUND)
damage_sound = mixer.Sound(DAMAGE_SOUND)

# необхідні зображення:
img_back = GAME_BG_IMG  # фон гри
img_hero = ROCKET_IMG  # герой
img_enemy = ENEMY_IMG  # ворог
img_bullet = BULLET_IMG 

font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font1.render("YOU LOSE", True, (100, 0, 0))

score = 0
lost = 0
max_lost = 1  # програш при одному пропущеному ворогу
best_score = 0  # Кращий результат гри
enemy_increase_interval = 0  # Лічильник для збільшення ворогів

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, 
                 size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-0.5, self.rect.top-0.5, 40, 50, -20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1  # Якщо пропущений ворог, збільшуємо лічильник втрат

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), 
                             (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
# Початково створюємо 3 ворогів
for i in range(3):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

bullets = sprite.Group()

start_time = time.get_ticks()
finish = False
run = True

def restart_game():
    global score, lost, finish, monsters, bullets, ship, start_time, best_score, enemy_increase_interval
    score = 0
    lost = 0
    start_time = time.get_ticks()
    finish = False
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
    monsters = sprite.Group()
    # Початково створюємо 3 ворогів
    for i in range(3):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
        monsters.add(monster)
    bullets = sprite.Group()
    enemy_increase_interval = 0  # Скидаємо лічильник збільшення ворогів

# головний цикл гри
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                fire_sound.play()
                ship.fire()

            elif e.key == K_RETURN and finish:
                # Оновлення кращого результату
                best_score = max(best_score, score)
                restart_game()

    if not finish:
        window.blit(background, (0, 0))
        
        # оновлення часу
        elapsed_time = (time.get_ticks() - start_time) // 1000
        timer_text = font2.render("Час: " + str(elapsed_time) + " с", 1, (255, 255, 255))
        window.blit(timer_text, timer_text.get_rect(topright=(win_width - 10, 20)))
        
        # рахунок і пропущені вороги
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # відображення кращого результату
        best_text = font2.render("Кращий: " + str(best_score), 1, (255, 255, 255))
        window.blit(best_text, (10, 80))

        ship.update()

        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            # Додаємо ворога після кожного вбивства
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
            retry_text = font2.render("Натисніть Enter для повтору", True, (255, 255, 255))
            window.blit(retry_text, (100, 300))

        # збільшення кількості ворогів через певний час
        enemy_increase_interval += 1
        if enemy_increase_interval >= 150:  # збільшуємо ворогів кожні 150 кадрів (приблизно кожні 2,5 секунди)
            new_enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(new_enemy)
            enemy_increase_interval = 0  # скидаємо лічильник

        display.update()

    time.delay(50)

from pygame import *
from assets import *
from random import randint

# фонова музика
from record import *
from time import time as timer


mixer.init()
mixer.music.load(GAME_MUSIC)
mixer.music.play(-1)
fire_sound = mixer.Sound(FIRE_SOUND)
damage_sound = mixer.Sound(DAMAGE_SOUND)


# нам потрібні такі картинки:
img_back = GAME_BG_IMG  # фон гри
img_hero = ROCKET_IMG  # герой
img_enemy = ENEMY_IMG # ворог
img_bullet = BULLET_IMG 
img_enemy2 = ENEMY2_IMG

font.init()
font2= font.Font(None, 36)

font1 = font.Font(None, 80)
win = font1.render("YOU WIN", True, (43, 255, 0))
lose = font1.render("YOU LOSE", True, (255, 0, 0))

score = 0
lost = 0
max_lost = 3
goal = 20
life = 3
record = load_record()

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
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 100:
            self.rect.y += self.speed

        
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-0.5, self.rect.top-0.5, 40, 50, -20)
        bullets.add(bullet)

class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

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
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
    monsters.add(monster)

cats = sprite.Group()
for i in range(1, 6):
    cat = Enemy(img_enemy2, randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
    cats.add(cat)

bullets = sprite.Group()

start_time = time.get_ticks()
shots_fired = 0
def restart_game():
    global score, lost, finish, monsters, bullets, ship, start_time, shots_fired, num_fire, life, cats
    score = 0
    lost = 0
    shots_fired = 0
    num_fire = 0
    life = 3
    start_time = time.get_ticks()
    finish = False
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
    monsters = sprite.Group()
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
        monsters.add(monster)
    bullets = sprite.Group()

        
    cats = sprite.Group()
    for i in range(1, 6):
        cat = Enemy(img_enemy2, randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
        cats.add(cat)



finish = False
run = True  # прапорець скидається кнопкою закриття вікна

rel_time = False
num_fire = 0
max_bullets = 5
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                if num_fire < max_bullets and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                    shots_fired += 1

                if num_fire >= max_bullets and rel_time == False:
                    last_time = timer()
                    rel_time = True

            elif e.key == K_RETURN and finish:
                restart_game()
    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

                # Обчислення таймера (у секундах)
        elapsed_time = (time.get_ticks() - start_time) // 1000
        timer_text = font2.render("Час: " + str(elapsed_time) + " с", 1, (255, 255, 255))
        window.blit(timer_text, timer_text.get_rect(topright=(win_width - 10, 20)))
        # Лічильник пострілів
        shots_text = font2.render("Постріли: " + str(shots_fired), 1, (255, 255, 255))
        window.blit(shots_text, shots_text.get_rect(topright=(win_width - 10, 50)))

        record_text = font2.render("Рекорд: " + str(record), 1, (255, 255, 0))
        window.blit(record_text, (10, 80))

        ship.update()

        monsters.update()

        cats.update()

        cats.draw(window)

        bullets.draw(window)
        if rel_time == True:
            now_time = timer() # зчитуємо час

            if now_time - last_time < 3: #поки не минуло 3 секунди виводимо інформацію про перезарядку
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки


        bullets.update()

        ship.reset()

        monsters.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
            retry_text = font2.render("Klick Enter", True, (255, 255, 255))
            window.blit(retry_text, (100, 300))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
            retry_text = font2.render("Klick Enter", True, (255, 255, 255))
            window.blit(retry_text, (100,300))


        display.update()
    time.delay(50)

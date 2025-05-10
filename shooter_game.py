#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_background = "galaxy1.jpg"
img_hero = "rocket1.png"
img_enemy = "ufo1.png"
img_asteroid = "asteroid1.png"
img_bullet = "bullet.png"

#fonts and captions NEW
font.init()
font2 = font.SysFont("Arial", 36)

font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

clock = time.Clock()
FPS = 60
win_width = 1400
win_height = 1000
display.set_caption("Shooter Game Beta v1.02")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_background), (win_width, win_height))




score = 0
lost = 0
diff = (score - lost)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y += self.speed
        else:
            self.kill()

min_speed = 2
max_speed = 5

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()

for i in range(0, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(min_speed, max_speed))
    monsters.add(monster)

for i in range(0, 3):
    asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(min_speed, max_speed))
    monsters.add(asteroid)

rel_time = False
num_fire = 0


finish = False
level = 0
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        window.blit(background, (0,0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 40))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 70))

        text_level = font2.render("Level: " + str(level), 1, (255, 255, 255))
        window.blit(text_level, (10, 100))

        diff = lost - score
        text_diff = font2.render("Diff: " + str(diff), 1, (255, 255, 255))
        window.blit(text_diff, (10, 130))


        ship.reset()
        ship.update()

        monsters.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        display.update()

        if score >= 30:
            lost = 0
            score = 0
            level += 1
            min_speed += 1
            max_speed += 1

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Reloading...', 1, (255, 0, 247))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
            



        #for collisions

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score += 1
            ranm = randint(1, 2)
            if ranm == 1:
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
                monsters.add(monster)
            elif ranm == 2:
                asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
                monsters.add(asteroid)

        if diff >= 10:
            finish = True
            window.blit(lose, (800, 800))
            time.delay(3000)
            run = False
    
    clock.tick(FPS)
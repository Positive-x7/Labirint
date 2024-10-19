from pygame import *

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class  Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, sixe_x, sixe_y, player_x_speed, player_y_speed):
            GameSprite.__init__(self, player_image, player_x, player_y, sixe_x, sixe_y)
            self.x_speed = player_x_speed
            self.y_speed = player_y_speed

    def update(self):
        if self.rect.x <= win_width-80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_toucthed = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_toucthed:
                self.rect.right = p.rect.left
        elif self.x_speed < 0:
            for p in platforms_toucthed:
                self.rect.left = p.rect.right
        if self.rect.y <= win_height-80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_toucthed = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_toucthed:
                self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in  platforms_toucthed:
                self.rect.top = 700#
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 30, 35, 15)
        bullet.add(bullet)


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = "left"

    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width-85:
            self.side == "left"
        
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, bullet_speed ):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = bullet_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

win_width = 1000#
win_height = 700#
window = display.set_mode((win_width, win_height))
display.set_caption("Лабиринт")
back = (119, 210, 223)

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

w1 = GameSprite('platform1.png', 116, 250, 300, 50)#
w2 = GameSprite('platform2.png', 370, 100, 50, 580)#
w3 = GameSprite('platform3.png', 370, 300, 250, 50)#
w4 = GameSprite('platform3.png', 200, 500, 650, 50)#
w5 = GameSprite('platform2.png', 700, 100, 50, 580)#
#w6 = GameSprite('platform2.png', 700, 80, 50, 580)#

barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
#barriers.add(w6)

packman = Player('hero.png', 5, 420, 80, 80, 0, 0)

monster = Enemy('cyborg.png', win_width - 80, 180, 80, 80, 5)#
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 100, 100)#

monsters.add(monster)
finish = False

run = True 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5

            elif e.key == K_SPACE:
                packman.fire()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    
    if finish == False:
        window.fill(back)
        #window.blit(back, (0,0))
        packman.update()
        bullets.update()
        packman.reset()
        bullets.draw(window)
        monsters.draw(window)
        monsters.update()
        barriers.draw(window)
        final_sprite.reset()

        if sprite.collide_rect(packman, monster):
            finish = True#
            img = image.load('game-over_1.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    time.delay(25)
    display.update()
import pygame
import random
import os
import time

FPS = 60
WIDTH = 1080
HEIGHT = 720
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#游戏初始化
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("坦克大战")
clock = pygame.time.Clock()
expl_anim = {}
expl_anim['enemy'] = []
for i in range(5):
    expl_img  = pygame.image.load(os.path.join(
        "img/explosion",f"expl{i}.png")).convert()
    expl_img.set_colorkey(WHITE)
    expl_anim['enemy'].append(pygame.transform.scale(expl_img,(75,75)))

start_sound = pygame.mixer.Sound(os.path.join("audios","start.wav"))
shoot_sound = pygame.mixer.Sound(os.path.join("audios","Gunfire.wav"))

def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/5)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)


def new_enemy(x):
    enemy_tank = EnemyTank(x)
    all_sprites.add(enemy_tank)
    enemy_tank_group.add(enemy_tank)


def new_brick(x):
    x = random.randint(0,45)
    # 避开坦克出生地
    y = random.randint(5,25)
    brick = Brick(x*24,y*24)
    all_sprites.add(brick)
    brick_group.add(brick)

class Player(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        # 要显示的图片
        tank_img = pygame.image.load(
            os.path.join("img/myTank", "tank_T1_0.png")).convert()
        self.tank = tank_img
        self.tank.set_colorkey(WHITE)
        self.image = self.tank.subsurface((0, 0), (48, 48))
        # 定位
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = center
        else:
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        
        self.speed = 8
        self.direction = "UP"
        self.can_move  =True
        self.rect_origin_x = self.rect.x
        self.rect_origin_y = self.rect.y
        # 移动缓冲，用于避免坦克连续移动过快导致不方便调整位置
        self.move_cache_time = 3
        self.move_cache_count = 0
        # 生命值
        self.health = 5
        self.hidden = False

    def update(self):
        if self.hidden:
            return
        # 移动缓冲
        self.move_cache_count += 1
        if self.move_cache_count < self.move_cache_time:
            return
        else:
            self.move_cache_count = 0
            wheel_index = self.move_cache_count % 2

        self.rect_origin_x = self.rect.x
        self.rect_origin_y = self.rect.y
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "RIGHT"
            if wheel_index == 1:
                self.image = self.tank.subsurface((0, 144), (48, 42))
            else:
                self.image = self.tank.subsurface((48,144),(48,42))
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "LEFT"
            if wheel_index == 1:
                self.image = self.tank.subsurface((0, 96), (48, 42))
            else:
                self.image = self.tank.subsurface((48,96),(48,42))
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = "UP"
            if wheel_index == 1:
                self.image = self.tank.subsurface((0,0), (48, 42))
            else:
                self.image = self.tank.subsurface((48,0),(48,42))
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = "DOWN"
            if wheel_index == 1:
                self.image = self.tank.subsurface((0,48), (48, 42))
            else:
                self.image = self.tank.subsurface((48,48),(48,42))

        if (self.rect.right > WIDTH):
            self.rect.right = WIDTH
        if (self.rect.left < 0):
            self.rect.left = 0
        if (self.rect.top < 0):
            self.rect.top = 0
        if (self.rect.bottom > HEIGHT):
            self.rect.bottom = HEIGHT
        # 碰到敌方坦克
        if pygame.sprite.spritecollide(self,enemy_tank_group,False,None):
            self.rect.x = self.rect_origin_x
            self.rect.y = self.rect_origin_y
        # 碰到砖块
        if pygame.sprite.spritecollide(self,brick_group,False,None):
            self.rect.x = self.rect_origin_x
            self.rect.y = self.rect_origin_y
        # 碰到河流
        if pygame.sprite.spritecollide(self,river_group,False,None):
            self.rect.x = self.rect_origin_x
            self.rect.y = self.rect_origin_y
    
    def shoot(self):
        # 有了冷却时间 也可以去除
        bullet_len = len(player_bullet_group)
        # print(bullet_len) 打印数量 进行观察
        if (bullet_len > 2):
            return
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        shoot_sound.play()
        all_sprites.add(bullet)
        player_bullet_group.add(bullet)

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+500)
class EnemyTank(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        # 要显示的图片
        tank_img = pygame.image.load(os.path.join(
            "img/enemyTank", "enemy_1_0.png")).convert()
        self.tank = tank_img
        self.tank.set_colorkey(WHITE)
        self.image = self.tank.subsurface((0, 0), (48, 48))
        # 定位
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10

        # 定义属性 跟rect相关 与rect风格一致
        # 坦克速度
        self.speed = 2
        # 方向
        self.direction = "DOWN"
        # 坦克位置
        if x is None:
            self.x = random.randint(0,2)
        else:
            self.x = x
        self.rect.left, self.rect.top = self.x*12*24,53
        #步数
        self.step = 60
        self.bullets = []
        # 上次射击时间
        self.last_shoot_time = 0
        self.cooling_time = 1000
        self.rect_oridin_x = self.rect.x
        self.rect_oridin_y = self.rect.y
        # 移动缓冲，用于避免坦克连续移动过快导致不方便调整位置
        self.move_cache_time = 3
        self.move_cache_count = 0

    def rand_direction(self):
            num = random.randint(1, 4)
            if num == 1:
                return "UP"
            if num == 2:
                return "DOWN"
            if num == 3:
                return "LEFT"
            if num == 4:
                return "RIGHT"
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if(now -self.last_shoot_time) < self.cooling_time:
            return
        for x in self.bullets:
            if (x.is_living == False):
                self.bullets.remove(x)

        bullet = Bullet(self.rect.centerx,self.rect.centery,self.direction)
        shoot_sound.play()
        all_sprites.add(bullet)
        enemy_bullet_group.add()
        self.bullets.append(bullet)
        self.last_shoot_time  = now

    def move(self):
        # 移动缓冲
        self.move_cache_count += 1
        if self.move_cache_count < self.move_cache_time:
            return
        else:
            self.move_cache_count = 0
        self.rect_origin_x = self.rect.x
        self.rect_origin_y = self.rect.y
        if (self.step <= 0):
            self.step = 120
            self.direction = self.rand_direction()
        # 方向
        if self.direction == "UP":
            self.rect.y -= self.speed
            self.image = self.tank.subsurface((0,0),(48,42))
        if self.direction == "DOWN":
            self.rect.y += self.speed
            self.image = self.tank.subsurface((0,48),(48,42))
        if self.direction == "LEFT":
            self.rect.x -= self.speed
            self.image = self.tank.subsurface((0,96),(48,42))
        if self.direction == "RIGHT":
            self.rect.x += self.speed
            self.image = self.tank.subsurface((0,144),(48,42))
        if (self.rect.right > WIDTH):
            self.rect.right = WIDTH
        if (self.rect.left < 0):
            self.rect.left = 0
        if (self.rect.top < 0):
            self.rect.top = 0
        if (self.rect.bottom > HEIGHT):
            self.rect.bottom = HEIGHT
        # 碰到玩家
        if pygame.sprite.spritecollide(self,player_tank_group,False,None):
            self.rect.x = self.rect_origin_x
            self.rect.y = self.rect_origin_y
            self.step = 120
            self.direction = self.rand_direction()
        # 碰到砖块
        if pygame.sprite.spritecollide(self,brick_group,False,None):
            self.rect.x = self.rect_origin_x
            self.rect.y = self.rect_origin_y
            self.step = 120
            self.direction = self.rand_direction()
        # 碰到河流
        if pygame.sprite.spritecollide(self,river_group,False,None):
            self.rect.x = self.rect_origin_x
            self.rect.y = self.rect_origin_y
            self.step = 120
            self.direction = self.rand_direction()

        # 步数递减
        self.step -= 1
        # 触发射击
        if random.randint(1,5) == 3:
            self.shoot()

# 爆炸
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,type):
        pygame.sprite.Sprite.__init__(self)
        # 要显示的图片
        self.type = type
        self.image = expl_anim[self.type][0]
        # 定位
        self.rect = self.image.get_rect()
        self.rect.center  =center
        self.frame = 0
        self.last_update  =pygame.time.get_ticks()
        self.frame_rect = 58

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rect:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.type]):
                self.kill()
            else:
                self.image = expl_anim[self.type][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.bullets = ['./img/bullet/bullet_up.png','./img/bullet/bullet_down.png',
                        './img/bullet/bullet_left.png',
'./img/bullet/bullet_right.png']
        self.direction = direction
        if self.direction == "UP":
            self.bullet = pygame.image.load(self.bullets[0])
        elif self.direction == "DOWN":
            self.bullet = pygame.image.load(self.bullets[1])
        elif self.direction == "LEFT":
            self.bullet = pygame.image.load(self.bullets[2])
        elif self.direction == "RIGHT":
            self.bullet = pygame.image.load(self.bullets[3])
        self.image = self.bullet
        self.image.set_colorkey(WHITE)
        # 定位
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -10
        # 是否存活
        self.is_living = True
    
    def update(self):
        if self.direction == "UP":
            self.rect.y += self.speed
        elif self.direction == "DOWN":
            self.rect.y -= self.speed
        elif self.direction == "LEFT":
            self.rect.x += self.speed
        elif self.direction == "RIGHT":
            self.rect.x -= self.speed
        
        if self.rect.bottom > HEIGHT:
            self.kill()
            self.is_living = False
        if self.rect.top < 0:
            self.kill()
            self.is_living = False
        if self.rect.left < 0:
            self.kill()
            self.is_living = False
        if self.rect.right > WIDTH:
            self.kill()
            self.is_living = False

class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # 要显示的图片
        brick_img = pygame.image.load(
            os.path.join("img/scene/","brick.png")).convert()
        self.image = brick_img
        self.image.set_colorkey(WHITE)

        # 定位
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class River(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # 要显示的图片
        river_img = pygame.Surface((24, 24))
        for i in range(2):
            for j in range(2):
                river_img.blit(pygame.image.load(
                    os.path.join("img/scene/","river1.png")).convert(),(12*i,12*j))
        self.image = river_img
        self.image.set_colorkey(WHITE)

        # 定位
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Born(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        # 要显示的图片
        appearance_img = pygame.image.load(
            os.path.join("img/others/","appear.png"))
        self.appearances = []
        self.appearances.append(appearance_img.subsurface((0,0),(48,48)))
        self.appearances.append(appearance_img.subsurface((48,0),(48,48)))
        self.appearances.append(appearance_img.subsurface((96,0),(48,48)))
        # 定位
        self.image = self.appearances[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_rate += 1
            if self.frame == 3:
                self.kill()
                player.health = 5
                player.rect.center = self.rect.center
                player.hidden = False

            else:
                self.image = self.appearances[self.frame]
                center = self.rect.center
                self.rect = self.rect.get_rect()
                self.rect.center = center

all_sprites = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_tank_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
river_group = pygame.sprite.Group()
player_tank_group = pygame.sprite.Group()
player = Player(None)
all_sprites.add(player)
player_tank_group.add(player)
river1 = River(300,300)
river2 = River(324,300)
river3 = River(348,300)
all_sprites.add(river1)
all_sprites.add(river2)
all_sprites.add(river3)
river_group.add(river1)
river_group.add(river2)
river_group.add(river3)

for i in range(30):
    new_brick(i)

for i in range(4):
    new_enemy(i)
# 游戏循环
running = True
start_sound.play()
time.sleep(5)
while running:
    # FPS:frame per second每秒执行帧数
    clock.tick(FPS)
    # 取得输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # 更新游戏
    # 执行群组中所有精灵的update方法
    all_sprites.update()
    # 敌方坦克移动逻辑
    for enemy_tank in enemy_tank_group:
        enemy_tank.move()

    # 判断玩家子弹与敌方坦克
    hits_playerbullet_enemytank = pygame.sprite.groupcollide(
        player_bullet_group,enemy_tank_group,True,True)
    for enemy in hits_playerbullet_enemytank:
        expl = Explosion(enemy.rect.center,'enemy')
        all_sprites.add(expl)
    # 判断玩家子弹与墙壁
    hits_playerbullet_brick = pygame.sprite.groupcollide(
        player_bullet_group,brick_group,True,True)
    # 判断敌方子弹与墙壁
    hits_enemybullet_brick = pygame.sprite.groupcollide(
        player_bullet_group,brick_group,True,True)
    for enemy in hits_enemybullet_brick:
        enemy.bullets = []
    # 判断敌方子弹与墙壁
    hits_playerbullet_playertank = pygame.sprite.spritecollide(
        player,enemy_bullet_group,True,pygame.sprite.collide_rect)
    for hit in hits_playerbullet_playertank:
        player.health -= 1
        if player.health <= 0:
            center = player.rect.center
            born = Born(player.rect.center)
            all_sprites.add(born)
            player.hide()

    # 画面显示
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_health(screen,player.health,10,30)
    pygame.display.update()
pygame.quit()
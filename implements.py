import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        self.alive = False
        self.color = (0,0,0)
        # 아이템 생성 (20% 확률로 빨간공 또는 파란공)
        if random.random() < 0.2:
            item_color = random.choice([config.ball_fever_color, (0, 0, 255)])
            item = Item(item_color, self.rect.centerx, self.rect.centery)
            config.ITEMS.append(item)


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list):
        for block in blocks:
            if block.alive and self.rect.colliderect(block.rect):
                if self.rect.bottom > block.rect.top or self.rect.top < block.rect.bottom:
                    self.dir = 360 - self.dir
                elif self.rect.right > block.rect.left or self.rect.left < block.rect.right:
                    self.dir = 180 - self.dir
                block.collide()

    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        if self.rect.left <= config.wall_width or self.rect.right >= config.display_dimension[0] - config.wall_width:
            self.dir = 180 - self.dir
        if self.rect.top < 1:
            self.dir = 360 - self.dir

    def alive(self):
        paddlePosition = config.paddle_pos[1]
        ballPosition = self.rect.top
        return paddlePosition > ballPosition


class Item(Basic):
    def __init__(self, color: tuple, x: int, y: int):
        super().__init__(color, 3, (x, y), config.item_size)
        self.color = color

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def move(self):
        self.rect.y += self.speed

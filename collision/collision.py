from __future__ import annotations

import sys

import pygame

if __name__ == "__main__":
    # 初始化 Pygame
    pygame.init()

    # 設定遊戲畫面大小
    screen_size = [800, 600]
    screen = pygame.display.set_mode(screen_size)

    # 設定顏色
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # 創建兩個方塊的初始位置
    block1 = pygame.Rect(300, 300, 50, 50)
    block2 = pygame.Rect(400, 300, 50, 50)

    # 設定方塊移動速度
    speed = [2, 2]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # 移動方塊
        block1 = block1.move(speed)
        if block1.left < 0 or block1.right > screen_size[0]:
            speed[0] = -speed[0]
        if block1.top < 0 or block1.bottom > screen_size[1]:
            speed[1] = -speed[1]

        # 碰撞檢測
        if block1.colliderect(block2):
            speed[0] = -speed[0]
            speed[1] = -speed[1]

        # 繪製方塊
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, block1)
        pygame.draw.rect(screen, BLUE, block2)
        pygame.display.flip()

    # 關閉 Pygame

pygame.quit()

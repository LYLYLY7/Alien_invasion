import pygame


class Ship:
    """管理飞船的类"""
    """ai_game引用AlienInvasion实例"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        # rect 矩形
        self.screen_rect = ai_game.screen.get_rect()

        # 加载⻜船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘新⻜船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 移动标志（飞船一开始不动）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """向右移动飞船"""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """在指定位置绘制⻜船"""
        self.screen.blit(self.image, self.rect)

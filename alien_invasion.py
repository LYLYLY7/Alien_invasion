import sys

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """管理游戏资源和⾏为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 计时
        self.clock = pygame.time.Clock()

        self.settings = Settings()
        # 游戏窗口大小
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 窗口标题
        pygame.display.set_caption("Alien Invasion")
        """Ship(self) self:指向的是当前的 AlienInvasion 实例"""
        self.ship = Ship(self)
        """将子弹存储到编组中"""
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 监听键盘鼠标事件
            self._check_events()
            # 更新船位置
            self.ship.update()
            # 更新子弹位置
            """self.bullets.update() 将为 bullets 编组中的每颗⼦弹调⽤ bullet.update()"""
            self.bullets.update()
            # 删除已消失的子弹
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            # 重新渲染屏幕
            self._update_screen()
            # 循环尽量保证每秒运行60次
            self.clock.tick(60)

    def _check_events(self):
        """侦听键盘和⿏标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 左右移动飞船 按下一直移动 松开停止
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按下"""
        """监听左右移动"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            """监听q键退出"""
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建新⼦弹，并将其加⼊编组 bullets """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        """填充背景色"""
        self.screen.fill(self.settings.bg_color)
        """添加子弹"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        """添加ship飞船"""
        self.ship.blitme()
        """重新渲染"""
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运⾏游戏
    ai = AlienInvasion()
    ai.run_game()

import sys
import pygame
from settings import Settings
from ship import Ship


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

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 监听键盘鼠标事件
            self._check_events()
            # 更新船向右位置
            self.ship.update()
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
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        """填充背景色"""
        self.screen.fill(self.settings.bg_color)
        """添加ship飞船"""
        self.ship.blitme()
        """重新渲染"""
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运⾏游戏
    ai = AlienInvasion()
    ai.run_game()

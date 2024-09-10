import sys
import pygame
from settings import Settings


class AlienInvasion:
    """管理游戏资源和⾏为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # 窗口标题
        pygame.display.set_caption("Alien Invasion")
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 侦听键盘和⿏标事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #  每次循环时重绘屏幕
            self.screen.fill(self.settings.bg_color)
            # 让最近绘制的屏幕可⻅，不断更新屏幕
            pygame.display.flip()
            # 循环尽量保证每秒运行60次
            self.clock.tick(60)


if __name__ == '__main__':
    # 创建游戏实例并运⾏游戏
    ai = AlienInvasion()
    ai.run_game()

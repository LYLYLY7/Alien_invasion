import sys
import pygame


class AlienInvasion:
    """管理游戏资源和⾏为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        # 绘制窗口宽1200 高800
        self.screen = pygame.display.set_mode((1200, 800))
        # 窗口标题
        pygame.display.set_caption("Alien Invasion")
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 侦听键盘和⿏标事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #  每次循环时重绘屏幕
            self.screen.fill(self.bg_color)
            # 让最近绘制的屏幕可⻅，不断更新屏幕
            pygame.display.flip()
            # 循环尽量保证每秒运行60次
            self.clock.tick(60)


if __name__ == '__main__':
    # 创建游戏实例并运⾏游戏
    ai = AlienInvasion()
    ai.run_game()

import sys
import pygame


class AlienInvasion:
    """管理游戏资源和⾏为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 绘制窗口宽1200 高800
        self.screen = pygame.display.set_mode((1200, 800))
        # 窗口标题
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 侦听键盘和⿏标事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # 让最近绘制的屏幕可⻅，不断更新屏幕
            pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运⾏游戏
    ai = AlienInvasion()
    ai.run_game()

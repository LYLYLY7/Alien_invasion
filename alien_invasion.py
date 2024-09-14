import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和⾏为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 游戏启动后处于活动状态
        self.game_active = True
        # 计时
        self.clock = pygame.time.Clock()

        self.settings = Settings()
        # 游戏窗口大小
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 窗口标题
        pygame.display.set_caption("Alien Invasion")
        # 创建⼀个⽤于存储游戏统计信息的实例
        self.stats = GameStats(self)
        """Ship(self) self:指向的是当前的 AlienInvasion 实例"""
        self.ship = Ship(self)
        """将子弹存储到编组中"""
        self.bullets = pygame.sprite.Group()
        """将外星人存储到编组中"""
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 监听键盘鼠标事件
            self._check_events()
            if self.game_active:
                # 更新船位置
                self.ship.update()
                # 更新子弹位置,删除消失子弹
                self._update_bullets()
                # 更新外星人
                self._update_aliens()
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

    def _check_fleet_edges(self):
        """在有外星⼈到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变它们的⽅向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """创建新⼦弹，并将其加⼊编组 bullets """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新⼦弹的位置并删除已消失的⼦弹"""
        # 更新⼦弹的位置
        self.bullets.update()

        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查外星人与子弹的碰撞并作处理
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应⼦弹和外星⼈的碰撞"""
        # 删除发⽣碰撞的⼦弹和外星⼈
        """检查是否有⼦弹击中了外星⼈
                   如果是，就删除相应的⼦弹和外星⼈"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 删除现有的⼦弹并创建⼀个新的外星舰队
            # # 清空屏幕上的子弹
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人，再不断添加，直到没有空间添加外星⼈为⽌
        alien = Alien(self)
        # 外星⼈的间距为外星⼈的宽度和外星⼈的⾼度
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            """余下的空间超过外星人宽度的两倍"""
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 添加⼀⾏外星⼈后，重置 x 值并递增 y 值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建⼀个外星⼈，并将其加⼊外星舰队"""
        new_alien = Alien(self)
        """新外星人的水平位置设置为第一个外星人宽度位置"""
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """检查是否有外星⼈位于屏幕边缘，并更新整个外星舰队的位置"""
        self._check_fleet_edges()
        """更新外星舰队中所有外星⼈的位置"""
        self.aliens.update()
        # 检测外星⼈和⻜船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星⼈到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        """填充背景色"""
        self.screen.fill(self.settings.bg_color)
        """添加子弹"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        """添加ship飞船"""
        self.ship.blitme()
        """添加外星人"""
        self.aliens.draw(self.screen)
        """重新渲染"""
        pygame.display.flip()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将ships_left 减1
            self.stats.ships_left -= 1
            # 清空外星⼈列表和⼦弹列表
            self.bullets.empty()
            self.aliens.empty()
            # 创建⼀个新的外星舰队，并将⻜船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """检查是否有外星⼈到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像⻜船被撞到⼀样进⾏处理
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建游戏实例并运⾏游戏
    ai = AlienInvasion()
    ai.run_game()

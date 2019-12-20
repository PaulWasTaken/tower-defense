from game_info import GameInfo


class HealingWave(GameInfo):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.ENEMY_INF["shaman"]["magic_animation"]
        self.heal_amount = self.ENEMY_INF["private"]["hp"] / 200

    def heal(self):
        for enemy in self.GameObjects.ENEMIES:
            delta_x = self.EnemyInf.WIDTH * 2
            delta_y = self.EnemyInf.WIDTH * 2
            if (self.x - delta_x < enemy.x < self.x + delta_x and
                    self.y - delta_y < enemy.y < self.y + delta_y):
                if enemy.current_hp < self.ENEMY_INF[enemy.name]["hp"] * 1.2:
                    enemy.current_hp += self.heal_amount

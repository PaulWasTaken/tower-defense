from initializer import initialize_dragon


class Dragon:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.display_inf = game.DisplayInf
        self.game_objects = game.GameObjects
        self.damage = game.MAGIC_TYPES["dragon"]["damage"]
        self.image = game.MAGIC_TYPES["dragon"]["image"]
        self.yvel = self.display_inf.HEIGHT / 30
        self.head_x = self.x + self.display_inf.WIDTH / 8
        self.head_y = self.y + self.display_inf.HEIGHT / 8
        initialize_dragon(self)

    def move(self):
        self.y += self.yvel
        self.head_y += self.yvel
        if self.y > self.display_inf.HEIGHT - self.display_inf.HEIGHT / 5:
            return None
        else:
            return self

    def deal_damage(self):
        epsilon_x = self.display_inf.WIDTH / 10
        epsilon_y = self.display_inf.HEIGHT / 6
        x = self.head_x
        y = self.head_y
        for enemy in self.game_objects.ENEMIES:
            if (enemy.x - epsilon_x < x < enemy.x + epsilon_x and
                enemy.y - epsilon_y < y < enemy.y + epsilon_y):
                enemy.current_hp -= self.damage

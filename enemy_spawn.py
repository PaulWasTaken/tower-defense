from enemy import Private, Shaman, Summoner, Ogre, Codo


class EnemySpawn:
    def __init__(self, game):
        self.game = game

        self.current_amount = 0
        self.wave_number = game.GameStatus.WAVE_COUNTER

    def spawn(self):
        if (self.wave_number % 5 == 0 and self.wave_number != 0 and
                self.current_amount < self.game.EnemyInf.MAX_AMOUNT / 2):
            self.game.GameObjects.ENEMIES.add(Codo(
                0, self.game.RoadInf.ENTRANCE - 10, self.game))
            self.current_amount += 1
            if self.current_amount >= self.game.EnemyInf.MAX_AMOUNT / 2:
                self.current_amount = self.game.EnemyInf.MAX_AMOUNT
            return
        if (self.current_amount + 1) % 4 == 0 and self.wave_number != 0:
            self.game.GameObjects.ENEMIES.add(Summoner(
                0, self.game.RoadInf.ENTRANCE - 10, self.game))
            self.current_amount += 1
            return
        if (self.current_amount + 1) % 5 == 0 and self.wave_number != 0:
            self.game.GameObjects.ENEMIES.add(Shaman(
                0, self.game.RoadInf.ENTRANCE - 10, self.game))
            self.current_amount += 1
            return
        if self.wave_number % 3 == 0 and self.wave_number != 0:
            self.game.GameObjects.ENEMIES.add(Ogre(
                0, self.game.RoadInf.ENTRANCE - 10, self.game))
            self.current_amount += 1
            return
        self.game.GameObjects.ENEMIES.add(Private(
            0, self.game.RoadInf.ENTRANCE - 10, self.game))
        self.current_amount += 1

# battle.py

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.current_turn = "player"
        self.battle_over = False

    def player_attack(self):
        damage = self.player.attack
        self.enemy.take_damage(damage)
        print(f"{self.player.name} attaque {self.enemy.name} et inflige {damage} dégâts.")
        self.next_turn()

    def enemy_attack(self):
        damage = self.enemy.attack
        self.player.take_damage(damage)
        print(f"{self.enemy.name} attaque {self.player.name} et inflige {damage} dégâts.")
        self.next_turn()

    def next_turn(self):
        if self.player.hp <= 0:
            print("Vous avez perdu...")
            self.battle_over = True
            return
        elif self.enemy.hp <= 0:
            print("Vous avez gagné !")
            self.battle_over = True
            return

        self.current_turn = "enemy" if self.current_turn == "player" else "player"

    def run(self):
        while not self.battle_over:
            print("\n---------------------------")
            print(f"{self.player.name} : {self.player.hp}/{self.player.max_hp} HP")
            print(f"{self.enemy.name} : {self.enemy.hp}/{self.enemy.max_hp} HP")
            print("---------------------------")

            if self.current_turn == "player":
                input("Appuie sur Entrée pour attaquer...")
                self.player_attack()
            else:
                self.enemy_attack()
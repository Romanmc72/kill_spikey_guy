import spikey_classes as sc


game = sc.Game()
my_player = sc.Player(game.package.player, game.package.fist)
my_enemy = sc.Enemy(game.package.enemy)

game.add_character(my_player)
game.add_character(my_enemy)

game.play()

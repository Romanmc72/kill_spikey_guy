import spikey_classes as sc


game = sc.Game(background="./images/room.png")
my_player = sc.Player(image="./images/circle.png", speed=5)
my_enemy = sc.Enemy(image="./images/sharp.png", lives=3, speed=1)

game.add_character(my_player)
game.add_character(my_enemy)

game.play()

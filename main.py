import spikey_classes as sc


game = sc.Game(background="./images/room.png")
my_player = sc.Player(image="./images/circle.png", lives=30, speed=3)
my_enemy = sc.Enemy(image="./images/sharp.png")

game.add_character(my_player)
game.add_character(my_enemy)

game.play()

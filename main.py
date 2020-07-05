#!/usr/bin/env python3
"""
This is tha actual game itself, run this file and the game should launch.
"""
import spikey_classes as sc

if __name__ == "__main__":
    game = sc.Game()
    my_player = sc.Player(game.package.player, game.package.fist)
    my_enemy = sc.Enemy(game.package.enemy)

    game.add_character(my_player)
    game.add_character(my_enemy)

    game.play()

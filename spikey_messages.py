#!/usr/bin/env python3
"""
These are the messages that are thrown upon a game over. The varying messages are thrown
depending on the cheat codes entered. The game is family friendly by default but can be
edited to be more explicit if you know the cheats.

I separated this to its own module because it was annoyingly large to keep and maintain
in the centralized classes repository.
"""
from collections import namedtuple

EndGameMessage = namedtuple('EndGameMessage', ['insult', 'meh', 'impressed', 'damn_son'])
      
normal_message = EndGameMessage(
    insult=['Maybe next time'],
    meh=['I guess that was okay'],
    impressed=['Nicely done'],
    damn_son=['Speechless', '*standing-ovation*']
)

mean_message = EndGameMessage(
    insult=[
        'You really suck at this',
        'The worst performance in the history of performances. Ever.',
        'Awful',
        'Disgraceful!',
        'You call that trying?',
        'BOOOOO YOU STINK!!!',
        'I\'ve never seen worse',
        'Nice try. NOT!',
        'ha ha',
        'Loser',
        'You gonna cry? :(',
        'It\'s like you don\'t even care...'
    ],
    meh=[
        'at least you tried this time',
        'I have see worse.',
        'Not totally disappointing',
        'I still think you could do better'
    ],
    impressed=['I have nothing negative to say'],
    damn_son=[
        'bet you feel proud of yourself',
        'Congrats on your huge waste of time',
        'Don\'t you have better things to do?'
    ]
)

explicit_message = EndGameMessage(
    insult=[
        'Eat it bitch',
        'Fuck outta here if you gonna sucka dick',
        'Choked a big one',
        'u suck ass',
        'shitty performance',
        'Bitch',
        'fuck you motherfucker',
        'u piece of shit'
    ],
    meh=[
        'Big fuckin woop',
        'Yeah you got a few points. You still a Bitch tho',
        'Not a total fucking failure',
        'almost a decent score, asshole.',
        'Choked a smaller dick this time'
    ],
    impressed=['Nice job. Bitch'],
    damn_son=[
        'Damn son, you cheatin?',
        'You probably cheated, Bitch'
    ]
)

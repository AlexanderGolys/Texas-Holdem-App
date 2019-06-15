import sys
import pygame
import random
from pygame.locals import *
import classes


FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BGCOLOR = (10, 10, 10)
cards = [i for i in range(54)]


def main(no_players):
    assert no_players > 1, 'Number of players must be min 2'
    assert no_players < 10, 'Max number of players in Texas Holdem Poker is 9'
    step = 0
    players = [classes.Player(1/no_players) for _ in range(no_players)]

    while True:
        pygame.init()
        global FPSCLOCK, DISPLAYSURF
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption("Texas Holdem No-Limit Poker")
        DISPLAYSURF.fill(BGCOLOR)

        if step == 0:
            players_cards = get_cards(no_players, cards)
            step += 1

        draw_your_hand(players_cards)



        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_your_hand(p_cards):
    table_img = pygame.image.load('./graphics/table4.png')
    DISPLAYSURF.blit(table_img, (0, 0))
    if step == 1:
        card1_img = pygame.image.load('./graphics/' + decode_cards(p_cards[0][0]) + '.png')
        card2_img = pygame.image.load('./graphics/' + decode_cards(p_cards[0][1]) + '.png')

        DISPLAYSURF.blit(card1_img, (WINDOWWIDTH / 2 - 20, WINDOWHEIGHT / 4 * 3))
        DISPLAYSURF.blit(card2_img, (WINDOWWIDTH / 2 + 20, WINDOWHEIGHT / 4 * 3))


def decode_cards(nb):
    color = (nb % 4) + 1
    value = nb // 4
    if value < 8:
        value_str = str(value + 2)
    elif value == 8:
        value_str = "T"
    elif value == 9:
        value_str = "J"
    elif value == 10:
        value_str = "Q"
    elif value == 11:
        value_str = "K"
    else:
        value_str = "A"
    return value_str + str(color)


def get_cards(no_players, c):
    random.shuffle(c)
    players_cards = []
    for i in range(no_players):
        players_cards.append([c[0], c[1]])
        del c[:2]
    return players_cards


main(1)

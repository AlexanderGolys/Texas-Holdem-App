import sys
import pygame
import random
from pygame.locals import *
from src import classes, play, draw, mechanics
from time import sleep

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
cards = [i for i in range(52)]


def main(no_players):
    pygame.init()
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Texas Holdem No-Limit Poker")
    pygame.key.set_repeat(100, 1)
    assert no_players > 1, 'Number of players must be minimum 2'
    assert no_players < 7, 'Max number of players is 6'
    players = [classes.Player(10000, i) for i in range(no_players)]
    dealer = random.randint(0, no_players)
    bb = 50
    sb = 25

    while True:
        for i, player in enumerate(players):
            if player.stack == 0:
                del players[i]
            if len(players) == 1:
                draw.end_game_animation(DISPLAYSURF, players[0])

        unfold = 0
        play.get_cards(cards, players)
        dealer = (dealer + 1) % no_players
        draw.standard_draw(players, DISPLAYSURF)
        pot = play.play_preflop(players, dealer, bb, sb, DISPLAYSURF)
        for player in players:
            player.give_to_the_pot()
            draw.draw_players_stack(player, DISPLAYSURF)
            if not player.fold:
                unfold += 1
        draw.draw_preflop_sit(players, dealer, DISPLAYSURF)
        draw.draw_pot(pot, DISPLAYSURF)

        if unfold > 1:
            flop = play.get_flop(cards)
            draw.draw_flop(flop, DISPLAYSURF)
            pot += play.play(players, dealer, bb, flop, pot, 0, DISPLAYSURF)
            unfold = 0
            for player in players:
                if not player.fold:
                    unfold += 1

        if unfold > 1:
            turn = play.get_turn(cards)
            draw.draw_turn(turn, DISPLAYSURF)
            pot += play.play(players, dealer, bb, turn, pot, 1, DISPLAYSURF)
            for player in players:
                if not player.fold:
                    unfold += 1

        unfolded_players = []
        for player in players:
            if not player.fold:
                unfolded_players.append(player)

        if unfold > 1:
            river = play.get_river(cards)
            draw.draw_river(river, DISPLAYSURF)
            pot += play.play(players, dealer, bb, river, pot, 2, DISPLAYSURF)

            draw.draw_pot(pot, DISPLAYSURF)
            for player in players:
                player.allin = False
            draw.draw_all_hands(players, DISPLAYSURF)

            winners = mechanics.winning(unfolded_players, river)

            print("\n\n\n\n\n\n")
            for player in players:
                mechanics.evaluate(river, player)
            print("")
        else:
            winners = [unfolded_players[0]]

        for winner in winners:
            winner.earn(pot / len(winners))
            print("player ", winner.number, " won this round")

        draw.draw_win_info(winners, DISPLAYSURF, pot)

        sleep(5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def faster_load():
    pygame.key.set_repeat(100, 5)


def even_faster_load():
    pygame.key.set_repeat(100, 1)


def normal_load():
    pygame.key.set_repeat(100, 10)


def all_allin(players):
    for player in players:
        if not player.allin and not player.fold:
            return False
    return True




main(6)

import random
from src import draw
import pygame
from pygame.locals import *
import sys


MINBET = 1


def get_cards(c, players):
    random.shuffle(c)
    for player in players:
        player.get_cards([c[0], c[1]])
        del c[:2]


def get_flop(cards):
    return cards[:3]


def get_turn(cards):
    return cards[:4]


def get_river(cards):
    return cards[:5]


def read_decision(surface):
    bet = 0
    while True:

        draw.draw_decision_bet(bet, surface)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    return 'allin'
                if event.key == K_c:
                    return 'check'
                if event.key == K_f:
                    return 'fold'
                if event.key == K_UP:
                    bet += MINBET
                if event.key == K_DOWN:
                    bet = max(0, bet - MINBET)
                if event.key == K_RETURN:
                    if bet == 0:
                        return 'check'
                    else:
                        return bet


def play_preflop(players, dealer, bb, sb, surface):
    pot = 0
    i = 0
    max_bet = bb
    turn = (dealer + 1) % len(players)
    players[turn].raise_(sb)
    pot += sb
    draw.draw_preflop_sit(players, turn, surface)
    for player in players:
        draw.draw_players_stack(player, surface)
    turn = (turn + 1) % len(players)
    players[turn].raise_(bb)
    pot += bb
    draw.draw_preflop_sit(players, turn, surface)
    for player in players:
        draw.draw_players_stack(player, surface)
    i += 1
    equal = False
    while not equal:
        turn = (turn + 1) % len(players)
        if players[turn].fold:
            continue
        draw.standard_draw(players, surface)
        draw.draw_preflop_sit(players, turn, surface)

        decision = read_decision(surface)
        if decision == 'check':
            if players[turn].bet < max_bet:
                pot += max_bet - players[turn].bet
                players[turn].raise_(max_bet - players[turn].bet)
        elif decision == 'fold':
            players[turn].fold_()
        else:
            pot += max(float(decision), bb)
            players[turn].raise_(max(float(decision), bb))
            if players[turn].bet < max_bet:
                pot += max_bet - players[turn].bet
                players[turn].raise_(max_bet - players[turn].bet)
            max_bet = players[turn].bet
        i += 1
        if i > len(players):
            equal = True
            for player in players:
                if player.bet != max_bet and not (player.fold or player.allin):
                    equal = False
    for player in players:
        player.give_to_the_pot()
    return pot


def play(players, dealer, bb, table_cards, table_pot, round_nb, surface):
    pot = 0
    i = 0
    max_bet = 0
    turn = (dealer + 1) % len(players)
    draw.draw_preflop_sit(players, turn, surface)
    for player in players:
        draw.draw_players_stack(player, surface)
    equal = False
    while not equal:
        i += 1
        turn = (turn + 1) % len(players)
        if players[turn].fold or players[turn].allin:
            continue
        draw.standard_draw(players, surface)
        draw.draw_preflop_sit(players, turn, surface)
        if round_nb == 0:
            draw.draw_flop(table_cards, surface)
        elif round_nb == 1:
            draw.draw_turn(table_cards, surface)
        elif round_nb == 2:
            draw.draw_river(table_cards, surface)
        draw.draw_pot(table_pot, surface)

        decision = read_decision(surface)
        if decision == 'check':
            if players[turn].bet < max_bet:
                pot += max_bet - players[turn].bet
                players[turn].raise_(max_bet - players[turn].bet)
        elif decision == 'fold':
            players[turn].fold_()
        elif decision == 'allin':
            pot += players[turn].go_allin()
        else:
            pot += max(float(decision), bb)
            players[turn].raise_(max(float(decision), bb))
            if players[turn].bet < max_bet:
                pot += max_bet - players[turn].bet
                players[turn].raise_(max_bet - players[turn].bet)
            max_bet = players[turn].bet
        if i >= len(players) - 1:
            equal = True
            for player in players:
                if player.bet != max_bet and not (player.fold or player.allin):
                    equal = False

    for player in players:
        player.give_to_the_pot()
    return pot

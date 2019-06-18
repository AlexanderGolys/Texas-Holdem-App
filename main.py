import sys
import pygame
import random
from pygame.locals import *
import classes


FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BGCOLOR = (10, 10, 60)
BLACK = (0, 0, 0)
STACKBG = (200, 200, 200, 40)
REDSTACK = (255, 200, 200)
cards = [i for i in range(52)]
PLAYER0X = WINDOWWIDTH / 2 - 100
PLAYER0Y =  WINDOWHEIGHT / 4 * 3
PLAYER1X = WINDOWWIDTH / 2 - 300
PLAYER1Y = WINDOWHEIGHT / 2 - 50
PLAYER2X = WINDOWWIDTH / 2 - 100
PLAYER2Y = WINDOWHEIGHT / 8
PLAYER3X =  WINDOWWIDTH / 2 - 20 + 50
PLAYER3Y = WINDOWHEIGHT / 8
PLAYER4X = WINDOWWIDTH / 2 - 20 + 240
PLAYER4Y = WINDOWHEIGHT / 2 - 50
PLAYER5X = WINDOWWIDTH / 2 - 20 + 50
PLAYER5Y = WINDOWHEIGHT / 4 * 3


def main(no_players):
    pygame.init()
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Texas Holdem No-Limit Poker")
    DISPLAYSURF.fill(BGCOLOR)
    assert no_players > 1, 'Number of players must be minimum 2'
    assert no_players < 7, 'Max number of players is 6'
    step = 0
    players = [classes.Player(1/no_players, i) for i in range(no_players)]
    dealer = random.randint(0, no_players)
    bb = 0.02
    sb = 0.01
    stage = 0
    pot = 0

    while True:
        if stage == 0:
            get_cards(cards, players)
        dealer = (dealer + 1) % no_players

        standard_draw(players)

        if stage == 0:
            pot = play_preflop(players, dealer, bb, sb)

            for player in players:
                player.give_to_the_pot()
                draw_players_stack(player)
            draw_preflop_sit(players, dealer)
            print(pot)
            draw_pot(pot)
            stage += 1

        flop = get_flop(cards)
        draw_flop(flop)
        draw_pot(pot)
        play_flop(players, dealer, bb, flop, pot)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_table():
    table_img = pygame.image.load('./graphics/table4.png')
    DISPLAYSURF.blit(table_img, (0, 0))


def draw_your_hand(p_cards):
    card1_img = pygame.image.load('./graphics/' + decode_cards(p_cards[0]) + '.png')
    card2_img = pygame.image.load('./graphics/' + decode_cards(p_cards[1]) + '.png')

    DISPLAYSURF.blit(card1_img, (PLAYER0X - 20, PLAYER0Y))
    DISPLAYSURF.blit(card2_img, (PLAYER0X + 20, PLAYER0Y))


def draw_players_reversed_cards(player):
    card_img = pygame.image.load('./graphics/reverse.png')
    if player.number != 0:
        DISPLAYSURF.blit(card_img, (give_players_x_coords(player.number) - 20, give_players_y_coords(player.number)))
        DISPLAYSURF.blit(card_img, (give_players_x_coords(player.number) + 20, give_players_y_coords(player.number)))


def draw_players_stack(player):
    font_obj = pygame.font.Font('freesansbold.ttf', 15)
    stack_surface = font_obj.render(str(player.stack)[:5], True, BLACK, STACKBG)
    stack_rect = stack_surface.get_rect()
    stack_rect.center = (give_players_x_coords(player.number) + 20, give_players_y_coords(player.number) + 70)
    DISPLAYSURF.blit(stack_surface, stack_rect)


def standard_draw(players):
    DISPLAYSURF.fill(BGCOLOR)
    draw_table()
    draw_your_hand(players[0].hand)
    for player in players:
        draw_players_reversed_cards(player)
        draw_players_stack(player)


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


def get_cards(c, players):
    random.shuffle(c)
    for player in players:
        player.get_cards([c[0], c[1]])
        del c[:2]


def get_flop(cards):
    return cards[:3]


def give_players_x_coords(player_nb):
    if player_nb == 0:
        return PLAYER0X
    elif player_nb == 1:
        return PLAYER1X
    elif player_nb == 2:
        return PLAYER2X
    elif player_nb == 3:
        return PLAYER3X
    elif player_nb == 4:
        return PLAYER4X
    elif player_nb == 5:
        return PLAYER5X


def give_players_y_coords(player_nb):
    if player_nb == 0:
        return PLAYER0Y
    elif player_nb == 1:
        return PLAYER1Y
    elif player_nb == 2:
        return PLAYER2Y
    elif player_nb == 3:
        return PLAYER3Y
    elif player_nb == 4:
        return PLAYER4Y
    elif player_nb == 5:
        return PLAYER5Y


def give_players_coords(player_nb):
    return give_players_x_coords(player_nb), give_players_y_coords(player_nb)


def read_decision():
    print('what you wanna do?')
    dec = input()
    if dec == 'c':  # check or call
        return 'check'
    elif dec == 'f':
        return 'fold'
    elif dec == 'b':
        bet = input()
        return bet
    else:
        print('incorrect')
        return read_decision()


def play_preflop(players, dealer, bb, sb):
    pot = 0
    i = 0
    max_bet = bb
    turn = (dealer + 1) % len(players)
    print(players[turn])
    players[turn].raise_(sb)
    pot += sb
    draw_preflop_sit(players, turn)
    for player in players:
        draw_players_stack(player)
    turn = (turn + 1) % len(players)
    i += 1
    players[turn].raise_(bb)
    pot += bb
    draw_preflop_sit(players, turn)
    for player in players:
        draw_players_stack(player)
    i += 1
    equal = False
    while not equal:
        turn = (turn + 1) % len(players)
        if players[turn].fold:
            continue
        standard_draw(players)
        draw_preflop_sit(players, turn)

        decision = read_decision()
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
                if player.bet != max_bet and not player.fold:
                    equal = False
    return pot


def play_flop(players, dealer, bb, flop, table_pot):
    pot = 0
    i = 0
    max_bet = 0
    turn = (dealer + 1) % len(players)
    draw_preflop_sit(players, turn)
    for player in players:
        draw_players_stack(player)
    equal = False
    while not equal:
        turn = (turn + 1) % len(players)
        if players[turn].fold:
            continue
        standard_draw(players)
        draw_preflop_sit(players, turn)
        draw_flop(flop)
        draw_pot(table_pot)

        decision = read_decision()
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
                if player.bet != max_bet and not player.fold:
                    equal = False
    return pot


def draw_flop(flop):
    cards_to_draw = [decode_cards(i) for i in flop]
    card1_img = pygame.image.load('./graphics/' + cards_to_draw[0] + '.png')
    card2_img = pygame.image.load('./graphics/' + cards_to_draw[1] + '.png')
    card3_img = pygame.image.load('./graphics/' + cards_to_draw[2] + '.png')
    DISPLAYSURF.blit(card1_img, (WINDOWWIDTH/2 - 40 - 50, WINDOWHEIGHT/2 - 50))
    DISPLAYSURF.blit(card2_img, (WINDOWWIDTH/2 - 50, WINDOWHEIGHT/2 - 50))
    DISPLAYSURF.blit(card3_img, (WINDOWWIDTH/2 + 40 - 50, WINDOWHEIGHT/2 - 50))
    pygame.display.update()


def draw_preflop_sit(players, turn):
    for i, player in enumerate(players):
        font_obj = pygame.font.Font('freesansbold.ttf', 15)
        if not player.fold:
            stack_surface = font_obj.render(str(player.bet)[:5], True, BLACK, STACKBG)
        else:
            stack_surface = font_obj.render('FOLD', True, BLACK, STACKBG)
        if i == turn:
            if not player.fold:
                stack_surface = font_obj.render(str(player.bet)[:5], True, BLACK, REDSTACK)
            else:
                stack_surface = font_obj.render('FOLD', True, BLACK, REDSTACK)

        stack_rect = stack_surface.get_rect()
        stack_rect.center = (give_players_x_coords(player.number) + 20, give_players_y_coords(player.number) - 20)
        DISPLAYSURF.blit(stack_surface, stack_rect)
        pygame.display.update()


def draw_pot(pot):
    font_obj = pygame.font.Font('freesansbold.ttf', 15)
    stack_surface = font_obj.render(str(pot)[:5], True, BLACK, STACKBG)
    stack_rect = stack_surface.get_rect()
    stack_rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT *3 /5)
    DISPLAYSURF.blit(stack_surface, stack_rect)
    pygame.display.update()


main(6)

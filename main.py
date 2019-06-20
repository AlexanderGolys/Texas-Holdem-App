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
        pot += play_flop(players, dealer, bb, flop, pot, 0)
        turn = get_turn(cards)
        draw_turn(turn)
        pot += play_flop(players, dealer, bb, turn, pot, 1)
        river = get_river(cards)
        draw_river(river)
        pot += play_flop(players, dealer, bb, river, pot, 2)
        draw_pot(pot)
        for player in players:
            player.allin = False

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


def get_turn(cards):
    return cards[:4]


def get_river(cards):
    return cards[:5]


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
    for player in players:
        player.give_to_the_pot()
    return pot


def play_flop(players, dealer, bb, table_cards, table_pot, round):
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
        if players[turn].fold or players[turn].allin:
            continue
        standard_draw(players)
        draw_preflop_sit(players, turn)
        if round == 0:
            draw_flop(table_cards)
        elif round == 1:
            draw_turn(table_cards)
        elif round == 2:
            draw_river(table_cards)
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
        if i >= len(players):
            equal = True
            for player in players:
                if player.bet != max_bet and not player.fold:
                    equal = False

    for player in players:
        player.give_to_the_pot()
        player.fold = False
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


def draw_turn(turn):
    flop = turn[:3]
    draw_flop(flop)
    card_img = pygame.image.load('./graphics/' + decode_cards(turn[3]) + '.png')
    DISPLAYSURF.blit(card_img, (WINDOWWIDTH/2 + 80 - 50, WINDOWHEIGHT/2 - 50))
    pygame.display.update()


def draw_river(river):
    turn = river[:4]
    draw_turn(turn)
    card_img = pygame.image.load('./graphics/' + decode_cards(river[4]) + '.png')
    DISPLAYSURF.blit(card_img, (WINDOWWIDTH / 2 + 120 - 50, WINDOWHEIGHT / 2 - 50))
    pygame.display.update()


def draw_preflop_sit(players, turn):
    for i, player in enumerate(players):
        font_obj = pygame.font.Font('freesansbold.ttf', 15)
        if not player.fold and player.stack > 0:
            stack_surface = font_obj.render(str(player.bet)[:5], True, BLACK, STACKBG)
        elif not player.fold:
            stack_surface = font_obj.render('ALL-IN', True, BLACK, STACKBG)
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


def winning(table, players):
    pass


def decode_for_winning(cards):
    decoded = [decode_cards(card) for card in cards]
    result = []
    for card in decoded:
        if card[0] == 'A':
            one_result = 13
        elif card[0] == 'K':
            one_result = 12
        elif card[0] == 'Q':
            one_result = 11
        elif card[0] == 'J':
            one_result = 10
        elif card[0] == 'T':
            one_result = 9
        else:
            one_result = int(card[0])
        result.append([one_result, int(card[1])])


def evaluate(table, player):
    pair = False
    t_pair = False
    trip = False
    streight = False
    flush = False
    full = False
    four = False
    s_flush = False

    temp = table + player
    ev_cards = [classes.Card(decode_for_winning(card)[0], decode_for_winning(card)[1]) for card in temp]
    ev_cards.sort(key=lambda c: c.value)
    for i in range(len(ev_cards) - 1):
        if pair and ev_cards[i].value == ev_cards[i + 1].value:
            t_pair = True
            c_t_pair = c_pair + [ev_cards[i], ev_cards[i+1]]
        if ev_cards[i].value == ev_cards[i + 1].value:
            pair = True
            c_pair = [ev_cards[i], ev_cards[i+1]]
    for i in range(len(ev_cards) - 2):
        if trip and ev_cards[i].value == ev_cards[i + 1].value:
            c_full = c_trip + [ev_cards[i], ev_cards[i+1]]
        if ev_cards[i].value == ev_cards[i + 2].value:
            trip = True
            c_trip = [ev_cards[i], ev_cards[i+1], ev_cards[i+2]]
    for i in range(len(ev_cards) - 3):
        if ev_cards[i].value == ev_cards[i + 3].value:
            four = True
            c_four = [ev_cards[i], ev_cards[i+1], ev_cards[i+2], ev_cards[i+3]]
    for i in range(len(ev_cards) - 4):
        if ev_cards[i].value == ev_cards[i+1].value - 1 == ev_cards[i+2].value - 2 == ev_cards[i+3].value - 3 == ev_cards[i+4].value - 4:
            streight = True
            c_streight = [ev_cards[i], ev_cards[i+1], ev_cards[i+2], ev_cards[i+3], ev_cards[i+4]]
            c_streight.sort(key=lambda c: c.color)
            if c_streight[0].color == c_streight[4].color:
                s_flush = True
                c_s_flush = c_streight
    ev_cards.sort(key=lambda c: c.color)
    for i in range(len(ev_cards) - 4):
        if flush and ev_cards[i].color == ev_cards[i+4].color:
            c_flush.append(ev_cards[i+4])
        if not flush and ev_cards[i].color == ev_cards[i+4].color:
            flush = True
            c_flush = [ev_cards[i], ev_cards[i+1], ev_cards[i+2], ev_cards[i+3], ev_cards[i+4]]


    ev_cards.sort(key=lambda c: c.value, reverse=True)

    if s_flush:
        return 8, c_s_flush
    elif four:
        for card in ev_cards:
            if card not in c_four:
                c_four.append(card)
                break
        return 7, c_four
    elif full:
        if len(c_full) == 5:
            return 6, c_full
        c_full.sort(key=lambda c: c.value)
        if c_full[0] != c_full[2]:
            return 6, c_full[2:]
        return 6, c_full[:3] + c_full[5:]
    elif flush:
        return 5, c_flush[:6]
    elif streight:
        return 4, c_streight
    elif trip:
        for card in ev_cards:
            if card not in c_trip:
                c_trip.append(card)
                break
        for card in ev_cards:
            if card not in c_trip:
                c_trip.append(card)
                break
        return 3, c_trip
    elif t_pair:
        c_t_pair.sort(key=lambda c: c.value, reverse=True)
        c_t_pair = c_t_pair[:5]
        for card in ev_cards:
            if card not in c_t_pair:
                c_t_pair.append(card)
                break
        return 2, c_t_pair
    elif pair:
        for card in ev_cards:
            if card not in c_pair:
                c_pair.append(card)
                break
        for card in ev_cards:
            if card not in c_pair:
                c_pair.append(card)
                break
        for card in ev_cards:
            if card not in c_pair:
                c_pair.append(card)
                break
        return 1, c_pair
    else:
        return 0, ev_cards[:6]

main(6)

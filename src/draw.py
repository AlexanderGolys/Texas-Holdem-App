import pygame
import random

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BGCOLOR = (10, 10, 60)
BLACK = (0, 0, 0)
STACKBG = (200, 200, 200, 40)
REDSTACK = (255, 100, 100)
GOLD = (212, 175, 55)
PLAYER0X = WINDOWWIDTH / 2 - 100
PLAYER0Y = WINDOWHEIGHT / 4 * 3
PLAYER1X = WINDOWWIDTH / 2 - 300
PLAYER1Y = WINDOWHEIGHT / 2 - 50
PLAYER2X = WINDOWWIDTH / 2 - 100
PLAYER2Y = WINDOWHEIGHT / 8
PLAYER3X = WINDOWWIDTH / 2 - 20 + 50
PLAYER3Y = WINDOWHEIGHT / 8
PLAYER4X = WINDOWWIDTH / 2 - 20 + 240
PLAYER4Y = WINDOWHEIGHT / 2 - 50
PLAYER5X = WINDOWWIDTH / 2 - 20 + 50
PLAYER5Y = WINDOWHEIGHT / 4 * 3


def draw_table(surface):
    table_img = pygame.image.load('./graphics/table4.png')
    surface.blit(table_img, (0, 0))


def draw_all_hands(players, surface):
    for player in players:
        card1_img = pygame.image.load('./graphics/' + decode_cards(player.hand[0]) + '.png')
        card2_img = pygame.image.load('./graphics/' + decode_cards(player.hand[1]) + '.png')
        surface.blit(card1_img, (give_players_x_coords(player.number) - 20, give_players_y_coords(player.number)))
        surface.blit(card2_img, (give_players_x_coords(player.number) + 20, give_players_y_coords(player.number)))
        pygame.display.update()


def draw_your_hand(p_cards, surface):
    card1_img = pygame.image.load('./graphics/' + decode_cards(p_cards[0]) + '.png')
    card2_img = pygame.image.load('./graphics/' + decode_cards(p_cards[1]) + '.png')

    surface.blit(card1_img, (PLAYER0X - 20, PLAYER0Y))
    surface.blit(card2_img, (PLAYER0X + 20, PLAYER0Y))


def draw_players_reversed_cards(player, surface):
    card_img = pygame.image.load('./graphics/reverse.png')
    if player.number != 0:
        surface.blit(card_img, (give_players_x_coords(player.number) - 20, give_players_y_coords(player.number)))
        surface.blit(card_img, (give_players_x_coords(player.number) + 20, give_players_y_coords(player.number)))


def draw_players_stack(player, surface):
    font_obj = pygame.font.Font('freesansbold.ttf', 15)
    stack_surface = font_obj.render(str(player.stack), True, BLACK, STACKBG)
    stack_rect = stack_surface.get_rect()
    stack_rect.center = (give_players_x_coords(player.number) + 20, give_players_y_coords(player.number) + 70)
    surface.blit(stack_surface, stack_rect)


def standard_draw(players, surface):
    surface.fill(BGCOLOR)
    draw_table(surface)
    draw_your_hand(players[0].hand, surface)
    for player in players:
        draw_players_reversed_cards(player, surface)
        draw_players_stack(player, surface)


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


def draw_flop(flop, surface):
    cards_to_draw = [decode_cards(i) for i in flop]
    card1_img = pygame.image.load('./graphics/' + cards_to_draw[0] + '.png')
    card2_img = pygame.image.load('./graphics/' + cards_to_draw[1] + '.png')
    card3_img = pygame.image.load('./graphics/' + cards_to_draw[2] + '.png')
    surface.blit(card1_img, (WINDOWWIDTH/2 - 40 - 50, WINDOWHEIGHT/2 - 50))
    surface.blit(card2_img, (WINDOWWIDTH/2 - 50, WINDOWHEIGHT/2 - 50))
    surface.blit(card3_img, (WINDOWWIDTH/2 + 40 - 50, WINDOWHEIGHT/2 - 50))
    pygame.display.update()


def draw_turn(turn, surface):
    flop = turn[:3]
    draw_flop(flop, surface)
    card_img = pygame.image.load('./graphics/' + decode_cards(turn[3]) + '.png')
    surface.blit(card_img, (WINDOWWIDTH/2 + 80 - 50, WINDOWHEIGHT/2 - 50))
    pygame.display.update()


def draw_river(river, surface):
    turn = river[:4]
    draw_turn(turn, surface)
    card_img = pygame.image.load('./graphics/' + decode_cards(river[4]) + '.png')
    surface.blit(card_img, (WINDOWWIDTH / 2 + 120 - 50, WINDOWHEIGHT / 2 - 50))
    pygame.display.update()


def draw_preflop_sit(players, turn, surface):
    for i, player in enumerate(players):
        font_obj = pygame.font.Font('freesansbold.ttf', 15)
        if not player.fold and player.stack > 0:
            stack_surface = font_obj.render(str(int(player.bet)), True, BLACK, STACKBG)
        elif not player.fold:
            stack_surface = font_obj.render('ALL-IN', True, BLACK, STACKBG)
        else:
            stack_surface = font_obj.render('FOLD', True, BLACK, STACKBG)
        if i == turn:
            if not player.fold:
                stack_surface = font_obj.render(str(player.bet), True, BLACK, REDSTACK)
            else:
                stack_surface = font_obj.render('FOLD', True, BLACK, REDSTACK)

        stack_rect = stack_surface.get_rect()
        stack_rect.center = (give_players_x_coords(player.number) + 20, give_players_y_coords(player.number) - 20)
        surface.blit(stack_surface, stack_rect)
        pygame.display.update()


def draw_pot(pot, surface):
    font_obj = pygame.font.Font('freesansbold.ttf', 15)
    stack_surface = font_obj.render(str(pot)[:5], True, BLACK, STACKBG)
    stack_rect = stack_surface.get_rect()
    stack_rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT * 3/5)
    surface.blit(stack_surface, stack_rect)
    pygame.display.update()


def draw_decision_bet(bet, surface):
    font_obj = pygame.font.Font('freesansbold.ttf', 22)
    stack_surface = font_obj.render('BET: ' + str(bet), True, BLACK, STACKBG)
    stack_rect = stack_surface.get_rect()
    stack_rect.center = (60, 450)
    surface.blit(stack_surface, stack_rect)
    pygame.display.update()


def draw_win_info(winners, surface, pot):
    font_obj = pygame.font.Font('freesansbold.ttf', 22)
    if len(winners) == 1:
        text = 'player ' + str(winners[0].number) + ' wins a pot (' + str(pot) + ')'
    else:
        text = 'players '
        for winner in winners[:-1]:
            text += str(winner.number) + ' and '
        text += str(winners[-1].number) + ' ties for a pot (' + str(pot) + ')'

    stack_surface = font_obj.render(text, True, BLACK, STACKBG)
    stack_rect = stack_surface.get_rect()
    stack_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT * 1/3)
    surface.blit(stack_surface, stack_rect)
    pygame.display.update()


def end_game_animation(surface, player):
    every_px = [(i, j) for i, j in (range(WINDOWWIDTH), range(WINDOWHEIGHT))]
    while every_px:
        random.shuffle(every_px)
        surface.set_at(every_px[0], GOLD)
        del every_px[0]
        pygame.display.update()

    font_obj = pygame.font.Font('freesansbold.ttf', 30)
    text = 'PLAYER ' + str(player.number) + ' WINS'
    stack_surface = font_obj.render(text, True, BLACK, GOLD)
    stack_rect = stack_surface.get_rect()
    stack_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    surface.blit(stack_surface, stack_rect)
    pygame.display.update()



from src import classes, draw


def winning(players, table):
    result = [True for _ in players]

    for i in range(len(players)):
        for player in players:
            if whos_better(table, players[i], player) == 2:
                result[i] = False
                break
    winners = []
    for i, res in enumerate(result):
        if res:
            winners.append(players[i])
    return winners


def whos_better(table, player1, player2):
    ev1 = evaluate(table, player1)
    ev2 = evaluate(table, player2)
    if ev1[0] > ev2[0]:
        return 0
    if ev1[0] < ev2[0]:
        return 2
    if ev1[0] == 8 or ev1[0] == 7 or ev1[0] == 4:  # straight flush, four of a kind, straight
        if ev1[2] > ev2[2]:
            return 0
        elif ev1[2] < ev2[2]:
            return 2
        else:
            return 1

    if ev1[0] == 6:  # full house
        if ev1[2] > ev2[2]:
            return 0
        elif ev1[2] < ev2[2]:
            return 2
        else:
            if ev1[3] > ev2[3]:
                return 0
            elif ev1[3] < ev2[3]:
                return 2
            else:
                return 1

    if ev1[0] == 5 or ev1[0] == 0:  # flush, high card
        ev1[1].sort(key=lambda c: c.value)
        ev2[1].sort(key=lambda c: c.value)
        while ev1[1]:
            if ev1[1][-1] > ev2[1][-1]:
                return 0
            if ev1[1][-1] < ev2[1][-1]:
                return 2
            del ev1[1][-1]
            del ev2[1][-1]
        return 1

    if ev1[0] == 3 or ev1[0] == 2:  # two pairs, three of a kind
        if ev1[2] > ev2[2]:
            return 0
        elif ev1[2] < ev2[2]:
            return 2
        else:
            if ev1[3] > ev2[3]:
                return 0
            elif ev1[3] < ev2[3]:
                return 2
            else:
                if ev1[4] > ev2[4]:
                    return 0
                elif ev1[4] < ev2[4]:
                    return 2
                else:
                    return 1

    if ev1[0] == 1:  # pair
        if ev1[2] > ev2[2]:
            return 0
        elif ev1[2] < ev2[2]:
            return 2
        else:
            ev1[1].sort(key=lambda c: c.value)
            ev2[1].sort(key=lambda c: c.value)
            while ev1[1]:
                if ev1[1][-1] > ev2[1][-1]:
                    return 0
                if ev1[1][-1] < ev2[1][-1]:
                    return 2
                del ev1[1][-1]
                del ev2[1][-1]
            return 1


def decode_for_winning(cards):
    if type(cards) is not list:
        g_cards = [cards]
    else:
        g_cards = cards
    decoded = [draw.decode_cards(card) for card in g_cards]
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
            one_result = int(card[0]) - 1
        return one_result, int(card[1])


def evaluate(table, player):
    pair = False
    t_pair = False
    trip = False
    straight = False
    flush = False
    full = False
    four = False
    s_flush = False

    temp = table + player.hand
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

    for i in range(len(ev_cards) - 1):
        if trip and ev_cards[i].value == ev_cards[i + 1].value != c_trip[0].value:
            c_full = c_trip + [ev_cards[i], ev_cards[i+1]]

    for i in range(len(ev_cards) - 3):
        if ev_cards[i].value == ev_cards[i + 3].value:
            four = True
            c_four = [ev_cards[i], ev_cards[i+1], ev_cards[i+2], ev_cards[i+3]]

    temp = []
    for ii in range(len(ev_cards) - 1):
        if ev_cards[ii].value != ev_cards[ii + 1].value:
            temp.append(ev_cards[ii])
    temp.append(ev_cards[-1])

    for i in range(len(temp) - 4):
        if temp[i].value == temp[i+1].value - 1 == temp[i+2].value - 2 == temp[i+3].value - 3 == temp[i+4].value - 4:
            straight = True
            c_straight = [temp[i], temp[i+1], temp[i+2], temp[i+3], temp[i+4]]

            c_straight.sort(key=lambda c: c.color)
            if c_straight[0].color == c_straight[4].color:
                s_flush = True
                c_s_flush = c_straight

    ev_cards.sort(key=lambda c: c.color)

    for i in range(len(ev_cards) - 4):
        if flush and ev_cards[i].color == ev_cards[i+4].color:
            c_flush.append(ev_cards[i+4])
        if not flush and ev_cards[i].color == ev_cards[i+4].color:
            flush = True
            c_flush = [ev_cards[i], ev_cards[i+1], ev_cards[i+2], ev_cards[i+3], ev_cards[i+4]]

    ev_cards.sort(key=lambda c: c.value, reverse=True)

    if s_flush:
        print("player ", player.number, " has a straight flush from ", c_s_flush[0].v_to_sign(), " to ",
              c_s_flush[-1].v_to_sign())
        return 8, c_s_flush, c_s_flush[-1].value
    elif four:
        for card in ev_cards:
            if card not in c_four:
                c_four.append(card)
                break
        print("player ", player.number, " has a four of ", c_four[-1].v_to_sign() + "s")
        return 7, c_four, c_four[-1]
    elif full:
        if len(c_full) == 5:
            return 6, c_full, max(set(c_full), key=c_full.count), min(set(c_full), key=c_full.count)
        c_full.sort(key=lambda c: c.value)
        if c_full[0] != c_full[2]:
            c_full = c_full[2:]
            print("player ", player.number, " has a full house, ", max(set(c_full), key=c_full.count).v_to_sign() +
                  "s full of ", min(set(c_full), key=c_full.count).v_to_sign() + "s")
            return 6, c_full, max(set(c_full), key=c_full.count), min(set(c_full), key=c_full.count)
        c_full = c_full[:3] + c_full[5:]
        print("player ", player.number, " has a full house, ", max(set(c_full), key=c_full.count).v_to_sign() +
              "s full of ", min(set(c_full), key=c_full.count).v_to_sign() + "s")
        return 6, c_full, max(set(c_full), key=c_full.count), min(set(c_full), key=c_full.count)
    elif flush:
        print("player ", player.number, " has a flush")
        return 5, c_flush[:6]
    elif straight:
        c_straight.sort(key=lambda c: c.value)
        print("player ", player.number, " has a straight from ", c_straight[0].v_to_sign(), " to ", c_straight[-1].v_to_sign())
        return 4, c_straight, c_straight[-1]
    elif trip:
        for card in ev_cards:
            if card not in c_trip:
                c_trip.append(card)
                break
        for card in ev_cards:
            if card not in c_trip:
                c_trip.append(card)
                break
        print("player ", player.number, " has a three of ", c_trip[0].v_to_sign() + "s")
        return 3, c_trip, c_trip[0], max(c_trip[3], c_trip[4]), min(c_trip[3], c_trip[4])
    elif t_pair:
        c_t_pair.sort(key=lambda c: c.value, reverse=True)
        c_t_pair = c_t_pair[:5]
        for card in ev_cards:
            if card not in c_t_pair:
                c_t_pair.append(card)
                break
        print("player ", player.number, " has a two pairs: ", max(c_t_pair[0], c_t_pair[2]).v_to_sign() + "s and ",
              min(c_t_pair[0], c_t_pair[2]).v_to_sign() + "s")
        return 2, c_t_pair, max(c_t_pair[0], c_t_pair[2]), min(c_t_pair[0], c_t_pair[2]), c_t_pair[4]
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
        print("player ", player.number, " has a pair of ", c_pair[0].v_to_sign() + "s")
        return 1, c_pair, c_pair[0]
    else:
        print("player ", player.number, "has high card ", ev_cards[0].v_to_sign())
        return 0, ev_cards[:6]
#Final Project
#Name: Isaac & Megan
#Date: 2024/1/8 - 2024/1/23
#ICS3U
#File Name: Final_Project

import random


#UNO
def uno():
    uno = input("You are going to win, enter UNO to win:")
    print("You win!")
    return ["f", "f"]


#Draw cards.
def draw_card(number, deck):
    if len(deck) == 0:
        return None, deck

    number = int(number)
    if number <= 0:
        return None, deck

    # If not enough cards, draw as many as possible (simple handling)
    if len(deck) < number:
        number = len(deck)

    # Keep it simple: return one card for 1, list of cards for >1
    if number == 1:
        card = deck[-1]
        del deck[-1]
        return card, deck
    else:
        cards = []
        for i in range(number):
            card = deck[-1]
            del deck[-1]
            cards.append(card)
        return cards, deck


#Let the player can only draw 2 cards.
def c_plus_2(player_hand, deck):
    new_cards, deck = draw_card(2, deck)
    if new_cards is None:
        return player_hand
    # draw_card returns list when number > 1
    for c in new_cards:
        player_hand.append(c)
    return player_hand


#Let the player can only draw 4 cards.
def c_plus_4(player_hand, deck):
    new_cards, deck = draw_card(4, deck)
    if new_cards is None:
        return player_hand
    for c in new_cards:
        player_hand.append(c)
    return player_hand


#Let the play skip their turn.
def skip_card(current_player):
    next_player = current_player + 1
    return next_player


#Reverse the order of players.
def reverse_card(player_direction):
    player_direction.reverse()
    return player_direction


#Player Turns
def play_card(player_hand, top_card, deck):
    card_color = top_card[0]
    card_type = top_card[1]
    while True:
        try:
            play = input("Do you want to play a card?(Yes/No) \n").strip()
            if play.lower() == "yes" or play.lower() == "y":
                play = "Yes"
            elif play.lower() == "no" or play.lower() == "n":
                play = "No"
            else:
                print("Please enter Yes or No.")
                continue

            if play == "Yes":
                if len(player_hand) == 0:
                    # already no cards, win
                    return "f", "f", player_hand

                card_number = int(input("Which card you want to play? (Enter card index) \n"))

                if card_number < 0 or card_number >= len(player_hand):
                    print("Please enter valid value.")
                    continue

                chosen_card = player_hand[card_number]
                card_color, card_type = chosen_card

                # Allow matching color, or wild cards, or first move (top_card empty)
                if card_color == top_card[0] or card_type in ["Color Change", "+4"] or top_card[0] == "":
                    del player_hand[card_number]

                    # If player used last card, they win (UNO)
                    if len(player_hand) == 0:
                        chosen_card = uno()
                        return chosen_card[0], chosen_card[1], player_hand

                    return card_color, card_type, player_hand
                else:
                    print("You can't play this card.")
                    print("This's your card:", "", player_hand)

            if play == "No":
                card_type = "None"
                card_color = top_card[0]
                new_card, deck = draw_card(1, deck)
                if new_card is not None:
                    player_hand.append(new_card)
                break
        except:
            print("Please enter valid value.")

    return card_color, card_type, player_hand


# Define the UNO deck
def create_total_cards():
    colors = ["Red", "Yellow", "Green", "Blue"]
    special_card_types = ["Skip", "Reverse", "+2", "+4", "Color Change"]
    number_range = [i for i in range(1, 9)]

    number_cards = []
    for color in colors:
        for number in number_range:
            card = [color, number]
            number_cards.append(card)

    special_cards = []
    for color in colors:
        for special in special_card_types:
            card = [color, special]
            special_cards.append(card)

    total_cards = number_cards + special_cards
    return total_cards


#Shuffle the card and give each player 7 cards.
def deal_hand(cards_per_player, deck):
    if len(deck) < cards_per_player:
        return None
    hand = deck[:cards_per_player]
    del deck[:cards_per_player]
    return hand


#Main program
deck = create_total_cards()
random.shuffle(deck)

print("Welcome to the UNO card game!")

while True:
    user = input("Do you want to start the game(Yes/No): ").strip()
    if user.lower() == "yes" or user.lower() == "y":
        user = "Yes"
        break
    elif user.lower() == "no" or user.lower() == "n":
        user = "No"
        break
    else:
        print("Please enter Yes or No.")

if user == "Yes":
    print("The game is about to start, there are 4 players and each player will be given 7 cards.\n")
    rules = """
    UNO Game Rules:
    1. Goal: The first player to play all the cards in his hand wins. 
    2. Starting Game: Each player starts with 7 cards. 
    3. Game Procedure: Players take turns to play cards in a clockwise direction. 
    4. Special card rules.
        - Skip: The next player loses his turn.
        - Reverse: Changes the direction of the game.
        - Plus Two (+2): The next player must draw two cards and lose his turn.
        - Wild: The player may change the current colour.
        - Wild +4: The next player draws four cards and loses his turn.
    5. UNO Shout: When a player has only one card left in his hand, he must shout "UNO".
    6. Winning Condition: The first player to play all cards in their hand wins.
        """
    print(rules)

    player1_hands = deal_hand(7, deck)
    player2_hands = deal_hand(7, deck)
    player3_hands = deal_hand(7, deck)
    player4_hands = deal_hand(7, deck)
    players_hands = [player1_hands, player2_hands, player3_hands, player4_hands]

    current_player = 0
    player_direction = [0, 1, 2, 3]
    top_card = ["", ""]
    game_over = False
    chosen_card = ["", ""]

    # Minimal change but fixes Skip/Reverse correctly:
    i = 0  # index in player_direction
    while not game_over:
        current_player = int(player_direction[i])

        if chosen_card != ["f", "f"]:
            print("It's player", current_player + 1, "turns")
            print(players_hands[current_player])

            current_hand = players_hands[current_player]
            chosen_card[0], chosen_card[1], players_hands[current_player] = play_card(current_hand, top_card, deck)
            top_card = chosen_card

            # If UNO() returned ["f","f"], game ends
            if chosen_card == ["f", "f"]:
                game_over = True
                break

            color, cardtype = chosen_card

            if cardtype in ["Skip", "Reverse", "+2", "+4"]:
                if cardtype == "Skip":
                    # skip next player: jump forward by 2
                    i = (i + 2) % 4
                    continue

                elif cardtype == "Reverse":
                    player_direction = reverse_card(player_direction)
                    # keep current player position, then move to next in new direction
                    i = player_direction.index(current_player)
                    i = (i + 1) % 4
                    continue

                elif cardtype == "+2":
                    next_i = (i + 1) % 4
                    next_player = player_direction[next_i]
                    players_hands[next_player] = c_plus_2(players_hands[next_player], deck)

                elif cardtype == "+4":
                    next_i = (i + 1) % 4
                    next_player = player_direction[next_i]
                    players_hands[next_player] = c_plus_4(players_hands[next_player], deck)

        # normal move to next player
        i = (i + 1) % 4

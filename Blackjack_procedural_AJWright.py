
'''
Code written by Amanda Wright for K2 Foundations program.  1/17/19

Code simulates a round of blackjack for 1-8 players using the following rules:
3 ways for a player to win:
1) Player's hand total is 21.
2) Player's hand total (if under 21) is higher than the dealer's hand total.
3) Dealer's hand total exceeds 21.
Set up:  Each player gets 2 cards face down while the dealer gets 2 cards, one
face up and one face down.
Card values:  Cards two through ten are worth their pip value, face cards are
worth 10, and aces are worth 1 or 11.
Play:  Players draw addtional cards to improve their hand. Players can win at
at this point if their hand totals 21 which is called "blackjack". If, after
all the players draw as many additional cards as they need and the players
have all busted or hit blackjack, the round ends.  If any players remain, the
Dealer shows his hidden card and must "hit" until his hand total is 17 or more
points.  If the dealer "busts" (hand total exceed 21), then any remaining
players win.  If the player and dealer totals are the same, the game is a push.
'''

# import modules
import itertools
import random

# generates a shuffled deck of cards as a list of tuples
deck = list(itertools.product(
    ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King'],
    ['Spades', 'Hearts', 'Diamonds', 'Clubs']))
random.shuffle(deck)

# returns a hand of cards as a list of tuples
def deal_cards(deck):
    hand = []
    for i in range(2):
        hand.append(deck.pop())
    return hand

# prints the face value of the cards in a player's hand
def player_hand_info(players_dict, player):
    print(player, ", your cards are: ", sep='')
    current_hand = players_dict[player]
    for card in current_hand:
        print(card[0], " of ", card[1], sep='')

# prints the face value of one of the cards in a dealer's hand
def dealer_hand_info(dealer_dict):
    print("Dealer's cards are: ", sep='')
    print ("Hidden Card")
    print(dealer_dict['Dealer'][0][0], " of ", dealer_dict['Dealer'][0][1], sep='')

# Returns the point total of a Blackjack hand.  If the hand belongs to a player
# (x=1), the player determines the value of any ace.  If the hand belongs to a
# dealer, optimal ace value is calculated.
def hand_total(dict, player, x):
    current_hand = dict[player]
    ace_check = "N"
    tot_1 = 0
    tot_2 = 0
    for card in current_hand:
        if type(card[0]) == int:
            tot_1 += card[0]
            tot_2 += card[0]
        if card[0] == "Jack" or card[0] == "Queen" or card[0] == "King":
            tot_1 += 10
            tot_2 += 10
        if card[0] == "Ace" and x == 1:
            ace = int(input("Do you want your ace to be worth 1 or 11? "))
            tot_1 += ace
        if card[0] == "Ace" and x == 2:
            ace_check = "Y"
            tot_1 += 1
            tot_2 += 11
    if x == 1:
        total = tot_1
    if x == 2 and ace_check == "N":
        total = tot_1
    if x == 2 and ace_check == "Y":
        if tot_2 <= 21 and tot_1 < 17:
            total = tot_2
        elif tot_2 > 21:
            total = tot_1
        else:
            total = tot_2
    return total

# Prints single dealer card.  Then for each player, prints player
# hand, calculates and prints the value of a player hand, and takes input
# from the player as to if they want to hit or stand.  Play proceeds based
# on hand value and further player input as dictated by Blackjack rules.
def player_round(players_dict, deck, results_dict):
    for player in players_dict:
        player_hand_info(players_dict, player)
        total = hand_total(players_dict, player, x=1)
        print(player, ", your hand totals: ", total, sep='')
        if total == 21:
            print("BlACKJACK! You win!")
            results_dict[player] = total
            break
        choice = input("Do you want to hit or stand? ")
        while choice != "hit" and choice != "stand":
            print ("Please enter the words hit or stand only. ")
            choice = input("Do you want to hit or stand? ")
        while choice == "hit":
            print("Dealing one card.")
            players_dict[player].append(deck.pop())
            player_hand_info(players_dict, player)
            total = hand_total(players_dict, player, x=1)
            print("Your new hand totals: ", total, sep='')
            if total == 21:
                print("BlACKJACK! You win! ")
                results_dict[player] = total
                choice = "end"
                break
            if total > 21:
                print("BUSTED! You lose.")
                results_dict[player] = total
                choice = "end"
            else:
                choice = input("Do you want to hit or stand? ")
                while choice != "hit" and choice != "stand":
                    print ("Please enter the words hit or stand only. ")
                    choice = input("Do you want to hit or stand? ")
        if choice == "stand":
            print("Okay, you choose to stand.  We'll see what the dealer has.")
            results_dict[player] = total

# If players remain who have not hit Blackjack or busted, evaluates dealer's
# hand and hits or stands as dictated by Blackjack rules.
def dealer_round(dealer_dict, deck, player_dict, results_dict):
    counter = 0
    for player in player_dict:
        if results_dict[player] >= 21:
            counter += 1
    if counter == len(player_dict):
        print("Since all players hit blackjack or busted, the game is over!")
        exit()

    player_hand_info(dealer_dict, "Dealer")
    total = hand_total(dealer_dict, "Dealer", x=2)
    print("Dealer's hand totals:", total)
    results_dict["Dealer"] = total
    while total < 17:
        print("Dealer hits.")
        dealer_dict["Dealer"].append(deck.pop())
        player_hand_info(dealer_dict, "Dealer")
        total = hand_total(dealer_dict, "Dealer", x=2)
        print("Dealer's hand totals:", total)
        results_dict["Dealer"] = total
    if total == 21:
        print("BLACKJACK!  Dealer wins")
    elif total > 21:
        print("Dealer busted! All remaining players win!")
    else:
        print("Dealer stands.")

# Prints final results of the current Blackjack round.
def game_results(results_dict, player_dict):
    print("Here are the results of this round of Blackjack.")
    if results_dict['Dealer'] == 21:
        print('Dealer got blackjack.')
        for player in player_dict:
            if results_dict[player] == 21:
                print(player, ", you also got blackjack, so you WIN!", sep='')
            if results_dict[player] > 21:
                print(player, ", you busted. You lose!", sep='')
            if results_dict[player] < 21:
                print(player, ", the dealer got blackjack.  You lose!", sep='')
    if results_dict['Dealer'] > 21:
        print("Dealer busted.")
        for player in player_dict:
            if results_dict[player] == 21:
                print(player, ", you got blackjack!  You win.", sep='')
            if results_dict[player] > 21:
                print(player, ", you busted. You lose!", sep='')
            if results_dict[player] < 21:
                print(player, ", you WIN!", sep='')
    if results_dict['Dealer'] < 21:
        for player in player_dict:
            if results_dict[player] == 21:
                print(player, ", you got blackjack!  You WIN!", sep='')
            if results_dict[player] < results_dict['Dealer']:
                print(player, ", dealer wins and you lose!", sep='')
            if results_dict[player] > results_dict['Dealer'] and results_dict[player] > 21:
                print(player, ", you busted.  Dealer wins and you lose!", sep='')
            if results_dict[player] > results_dict['Dealer'] and results_dict[player] < 21:
                print(player, ", you beat the dealer.  You WIN!", sep='')
            if results_dict[player] == results_dict['Dealer']:
                print(player, ", you have the same total as the dealer.  Push.", sep='')

# Following code mplememnts a round of blackjack using the functions defined above
print("Welcome to Blackjack!")
players = {}   #stores player names and hands
dealer = {}    #stores dealer hand
results = {}   #stores player and dealer hand totals
num_play = (int(input("How many players? Max number is 8. ")))
while num_play > 8:
    print("Too many players!  Try again.")
    num_play = (int(input("How many players? Max number is 8. ")))
print("Shuffling cards for", num_play, "players.")
print("Dealing cards.")
for i in range(0, num_play):   # adds player name and card info to players_dict
    player = input("Player, what is your name? ")
    players[player] = deal_cards(deck)
    results[player] = 0    # adds player name to results_dict
dealer["Dealer"] = deal_cards(deck)  #adds dealer name and card info to dealers_dict
results["Dealer"] = 0  #adds the dealer to the results_dict
dealer_hand_info(dealer)
player_round(players, deck, results)
dealer_round(dealer, deck, players, results)
game_results(results, players)

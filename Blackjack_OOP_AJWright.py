
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
at this point if their hand totals 21 which is called "blackjack". If after
all the players draw as many additional cards as they need and the players
have all busted or hit blackjack, the round ends.  If any players remain, the
Dealer shows his hidden card and must "hit" until his hand total is 17 or more
points.  If the dealer "busts" (hand total exceed 21), then any remaining
players win.  If the player and dealer totals are the same, the game is a push.
'''

# import modules
import itertools
import random

class Hand(object):
    """Abstract class for holding information relavent to a Blackjack card hand."""
    def __init__(self,deck):
        """Assumes deck is a list of tuples.  Creates a hand of 2 cards. """
        self.cards = []
        for i in range(2):
            self.cards.append(deck.pop())

    def show_hand(self):
        """Prints the face value of the cards in a hand."""
        for x in self.cards:
            print(x[0], " of ", x[1])

    def deal_card(self, deck):
        """Adds one card from the deck to a hand."""
        self.cards.append(deck.pop())

    def cal_total(self, x):
        """Returns the point total of a Blackjack hand.  If the hand belongs
        to a player (x=1), player determines the value of any ace.  If the hand
        belongs to a dealer(x=2), optimal ace value is calculated."""
        self.hand_total = 0
        ace_check = "N"
        tot_1 = 0
        tot_2 = 0
        for card in self.cards:
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
            self.hand_total = tot_1
        if x == 2 and ace_check == "N":
            self.hand_total = tot_1
        if x == 2 and ace_check == "Y":
            if tot_2 <= 21 and tot_1 < 17:
                self.hand_total = tot_2
            elif tot_2 > 21:
                self.hand_total = tot_1
            else:
                self.hand_total = tot_2
        return self.hand_total

class Player(Hand):
    """Subclass of Hand; card hand belongs to a player."""

    def __init__(self,deck):
        """Assumes deck is a list of tuples.  Creates a hand of 2 cards and
        associates it with a player inputed name. """
        Hand.__init__(self,deck)
        self.name = input("Player, what is your name? ")

    def get_name(self):
        """Returns player name."""
        return self.name

class Dealer(Hand):
    """Subclass of Hand; card hand belongs to the dealer."""

    def __init__(self, deck):
        Hand.__init__(self, deck)

    def first_reveal(self):
        """Prints the face value of one of the cards in the dealer's hand."""
        print("Dealer's cards are: ")
        print("Hidden Card")
        print(self.cards[0][0], " of ", self.cards[0][1])

class BJround(object):
    """Abstract class that implements a single round of Blackjack."""

    def __init__(self,deck):
        """Prints introductory remarks, determines number of players, and creates
        Player instances to represent each player and a Dealer instance to
        represent the dealer."""
        print("Welcome to Blackjack!")
        self.game_players = []
        num_play = (int(input("How many players? Max number is 8. ")))
        while num_play > 8:
            print("Too many players!  Try again.")
            num_play = (int(input("How many players? Max number is 8. ")))
        print("Shuffling cards.")
        print("Dealing cards to", num_play, "players.")
        for i in range(0, num_play):
            player = Player(deck)
            self.game_players.append(player)
        self.dealer1 = Dealer(deck)

    def number_of_players(self):
        """Returns the number of players in the game."""
        return len(self.game_players)

    def player_round(self):
        """Prints single dealer card.  Then for each player, prints player
        hand, calculates and prints the value of a player hand, and takes input
        from the player as to if they want to hit or stand.  Play proceeds based
        on hand value and further player input as dictated by Blackjack rules."""
        self.dealer1.first_reveal()
        for player in self.game_players:
            print(player.get_name() + ",")
            print("Your cards are: ")
            player.show_hand()
            player.cal_total(x=1)
            print(player.get_name(), ", your total is: ", player.hand_total, sep='')
            if player.hand_total == 21:
                print("BlACKJACK! You win!")
                break
            choice = input("Do you want to hit or stand? ")
            while choice != "hit" and choice != "stand":
                print ("Please enter the words hit or stand only. ")
                choice = input("Do you want to hit or stand? ")
            while choice == "hit":
                print("Dealing one card.")
                player.deal_card(deck)
                player.show_hand()
                player.cal_total(x=1)
                print("Your new hand totals: ", player.hand_total, sep='')
                if player.hand_total == 21:
                    print("BlACKJACK! You win!")
                    choice = "end"
                    break
                if player.hand_total > 21:
                    print("BUSTED! You lose.")
                    choice = "end"
                else:
                    choice = input("Do you want to hit or stand? ")
                    while choice != "hit" and choice != "stand":
                        print ("Please enter the words hit or stand only. ")
                        choice = input("Do you want to hit or stand? ")
            if choice == "stand":
                print("Okay, you choose to stand.  We'll see what the dealer has.")

    def dealer_round(self):
        """If players remain who have not hit Blackjack or busted, evaluates
        dealer's hand and hits or stands as dictated by Blackjack rules. """
        counter = 0
        for player in self.game_players:
            if player.hand_total >= 21:
                counter += 1
        if counter == self.number_of_players():
            print("Since all players hit blackjack or busted, the game is over!")
            exit()

        self.dealer1.cal_total(x=2)
        self.dealer1.show_hand()
        print("Dealer's hand totals: ", self.dealer1.hand_total, sep='')
        while self.dealer1.hand_total < 17:
            print("Dealing one card.")
            self.dealer1.deal_card(deck)
            self.dealer1.show_hand()
            self.dealer1.cal_total(x=2)
            print("Dealer's new hand totals: ", self.dealer1.hand_total, sep='')
        if self.dealer1.hand_total == 21:
            print("BLACKJACK!  Dealer wins")
        elif self.dealer1.hand_total > 21:
            print("Dealer busted! All remaining players win!")
        else:
            print("Dealer stands.")

    def results(self):
        """Prints final results of the current Blackjack round."""
        print("Here are the results of this round of Blackjack.")
        if self.dealer1.hand_total == 21:
            print('Dealer got blackjack.')
            for player in self.game_players:
                if player.hand_total == 21:
                    print(player.get_name(), ", you also got blackjack, so you WIN!", sep='')
                if player.hand_total > 21:
                    print(player.get_name(), ", you busted. You lose!", sep='')
                if player.hand_total < 21:
                    print(player.get_name(), ", the dealer got blackjack.  You lose!", sep='')
        if self.dealer1.hand_total > 21:
            print("Dealer busted.")
            for player in self.game_players:
                if player.hand_total == 21:
                    print(player.get_name(), ", you got blackjack!  You win.", sep='')
                if player.hand_total > 21:
                    print(player.get_name(), ", you busted. You lose!", sep='')
                if player.hand_total < 21:
                    print(player.get_name(), ", you WIN!", sep='')
        if self.dealer1.hand_total < 21:
            for player in self.game_players:
                if player.hand_total == 21:
                    print(player.get_name(), ", you got blackjack!  You WIN!", sep='')
                if player.hand_total < self.dealer1.hand_total:
                    print(player.get_name(), ", dealer wins and you lose!", sep='')
                if player.hand_total > self.dealer1.hand_total and player.hand_total > 21:
                    print(player.get_name(), ", you busted.  Dealer wins and you lose!", sep='')
                if player.hand_total > self.dealer1.hand_total and player.hand_total < 21:
                    print(player.get_name(), ", you beat the dealer.  You WIN!", sep='')
                if player.hand_total == self.dealer1.hand_total:
                    print(player.get_name(), ", you have the same total as the dealer.  Push.", sep='')

"""The following code generates a deck of shuffled cards then implements
a single round of Blackjack using the methods within the BJround class. """

# generates shuffled deck of cards
deck = list(itertools.product(
    ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King'],
    ['Spades', 'Hearts', 'Diamonds', 'Clubs']))
random.shuffle(deck)

# plays a round of Blackjack
round1 = BJround(deck)
round1.player_round()
round1.dealer_round()
round1.results()

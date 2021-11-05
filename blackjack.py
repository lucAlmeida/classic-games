import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

in_play = False
outcome = ""
question = 'Hit or stand?'
score = 0

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        return 'Hand contains ' + ' '.join([str(card) for card in self.cards])

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        aces = [ card.get_rank() == 'A' for card in self.cards ]
        hand_value = sum([ VALUES[card.get_rank()] for card in self.cards ])
        has_ace = any(aces)
        if not has_ace:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            return hand_value
        
    def draw(self, canvas, pos):
        first_five = self.cards[:5]
        for i in range(len(first_five)):
            card_pos = [i * CARD_SIZE[0] + pos[0], pos[1]]
            self.cards[i].draw(canvas, card_pos)
            
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
        
    def __str__(self):
        return 'Deck contains ' + ' '.join([str(card) for card in self.cards])
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]

def deal():
    global outcome, question, score, in_play, deck, player_hand, dealer_hand
    
    if in_play:
        outcome = 'Player loses!'
        question = 'New deal?'
        score -= 1
        in_play = False
        return

    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    outcome = ''
    question = 'Hit or stand?'
    in_play = True

def hit():
    global in_play, score, question, outcome
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = 'You have busted'
            in_play = False
            score -= 1
            question = 'New deal?'
            
def stand():
    global in_play, score, question, outcome
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

        if dealer_hand.get_value() > 21:
            outcome = 'Dealer has busted'
            score += 1
        elif player_hand.get_value() <= dealer_hand.get_value():
            outcome = 'Dealer wins!'
            score -= 1
        else:
            outcome = 'Player wins!'
            score += 1
        in_play = False
        question = 'New deal?'

def draw(canvas):    
    canvas.draw_text("Blackjack", [80, 100], 42, "Yellow")
    canvas.draw_text("Score " + str(score), [380, 100], 32, "Black")
    
    canvas.draw_text("Dealer", [70, 150], 24, "White")
    canvas.draw_text(outcome, [350, 150], 24, "Orange")
    canvas.draw_text("Player", [70, 350], 24, "White")
    canvas.draw_text(question, [350, 350], 24, "Orange")
    
    dealer_hand.draw(canvas, [70, 200])
    if in_play:
        canvas.draw_image(card_back, (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0] * 1, CARD_BACK_CENTER[1] + CARD_BACK_SIZE[1] * 0), CARD_BACK_SIZE, [70 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

    player_hand.draw(canvas, [70, 400])

frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Blue")

frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()


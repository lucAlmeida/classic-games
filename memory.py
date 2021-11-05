import simplegui
import random

NUM_PAIRS = 8

def new_game():
    global deck, exposed, to_shuffle, prev_card1, prev_card2, state, turns
    deck = [n % NUM_PAIRS for n in range(NUM_PAIRS * 2)]
    exposed = [False] * NUM_PAIRS * 2
    random.shuffle(deck)
    prev_card1 = None
    prev_card2 = None
    state = 0
    turns = 0
    label.set_text("Turns = " + str(turns))

def mouseclick(pos):
    global exposed, state, prev_card1, prev_card2, turns
    for i in range(len(deck)):
        if pos[0] > (i + 1) * 50 - 50 and pos[0] <= (i + 1) * 50:
            if not exposed[i] and state == 0:
                exposed[i] = True
                state = 1
                turns += 1
                prev_card1 = i
                label.set_text("Turns = " + str(turns))
            elif not exposed[i] and state == 1:
                exposed[i] = True
                state = 2
                prev_card2 = i
            elif not exposed[i] and state == 2:
                exposed[i] = True
                if deck[prev_card1] != deck[prev_card2]:
                    exposed[prev_card1] = False
                    exposed[prev_card2] = False
                state = 1
                turns += 1
                prev_card1 = i
                prev_card2 = None
                label.set_text("Turns = " + str(turns))

def draw(canvas):
    for i in range(len(deck)):
        card_size = i * 50
        if exposed[i]:
            canvas.draw_text(str(deck[i]), [card_size + 14, 60], 32, "White")
        else:
            canvas.draw_polygon([[card_size, 100], 
                                 [card_size + 50, 100], 
                                 [card_size + 50, 0], 
                                 [card_size, 0]], 1, 'White', 'Green')

frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()


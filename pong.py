import simplegui
import random

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [0, 0]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240) // 30
    else:
        ball_vel[0] = -random.randrange(120, 240) // 30
    ball_vel[1] = -random.randrange(60, 180) // 30
    
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    global game_start
    
    paddle1_pos = HEIGHT // 2 + HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT // 2 + HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(random.choice([RIGHT, LEFT]))

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    if ball_pos[0] < PAD_WIDTH:
        spawn_ball(RIGHT)
        score2 += 1
    elif ball_pos[0] > WIDTH - PAD_WIDTH:
        spawn_ball(LEFT)
        score1 += 1
    
    ball_pos[0] += ball_vel[0]
    if ball_pos[1] < BALL_RADIUS or ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    ball_pos[1] += ball_vel[1]

    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, 'Blue', 'Blue')
    
    if paddle1_pos + paddle1_vel > PAD_HEIGHT and paddle1_pos + paddle1_vel < HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel > PAD_HEIGHT and paddle2_pos + paddle2_vel < HEIGHT:
        paddle2_pos += paddle2_vel

    canvas.draw_polygon([[0, paddle1_pos], [0, paddle1_pos - PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos - PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos]], 10, 'Grey')
    canvas.draw_polygon([[WIDTH, paddle2_pos], [WIDTH, paddle2_pos - PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos - PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos]], 10, 'Grey')
    
    if (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and \
        ball_pos[1] <= paddle1_pos + BALL_RADIUS and \
        ball_pos[1] >= paddle1_pos - PAD_HEIGHT - BALL_RADIUS) or \
        (ball_pos[0] + BALL_RADIUS >= WIDTH and \
         ball_pos[1] <= paddle2_pos + BALL_RADIUS and \
         ball_pos[1] >= paddle2_pos - PAD_HEIGHT - BALL_RADIUS):
            ball_vel[0] = -ball_vel[0] * 1.1
        
    canvas.draw_text(str(score1), [WIDTH // 4, HEIGHT // 4 - 30], 32, "White")
    canvas.draw_text(str(score2), [WIDTH - WIDTH // 4, HEIGHT // 4 - 30], 32, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 7
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc

def keyup(key):
    global paddle1_vel, paddle2_vel
    acc = 7
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel += acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= acc
    elif key == simplegui.KEY_MAP["space"]:
        new_game()

def restart_handler():
    new_game()

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart_handler)

new_game()
frame.start()


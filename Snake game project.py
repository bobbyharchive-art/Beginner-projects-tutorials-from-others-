import turtle
import time
import random 

delay = 0.1

# Score
score = 0
high_score = 0
current_game_apples = 0

wn = turtle.Screen()
wn.title("Snake Game by @BobbyQ")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0) # Turns off the screen updates 

# Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

# Golden apple (appears every 3rd apple)
apples_eaten = 0
golden_food = turtle.Turtle()
golden_food.speed(0)
golden_food.shape("circle")
golden_food.color("gold")
golden_food.penup()
golden_food.hideturtle()

segments = []

# Pen 
pen = turtle.Turtle ()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0 High Score 0", align="center", font=("Courier", 24, "normal"))

#functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
        
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
   
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
  
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20) 

def get_valid_position():
    while True:
            x = random.randint (-280,280)
            y = random.randint (-280, 280)
            
            # Check if position is far enough from head and all segments
            if head.distance (x,y) > 40 and all(segment.distance(x, y) > 20 for segment in segments): 
                return (x, y)
            
def spawn_golden_apple():
        while True:
            gx = random.randint(-280, 280)
            gy = random.randint(-280, 280)
            # Ensure Golden apple is far from the head and all segments
            if head.distance(gx, gy) > 40 and all(segment.distance(gx, gy) > 20 for segment in segments):
                golden_food.goto(gx, gy)
                golden_food.showturtle()
                break

def place_food():
    x, y = get_valid_position()
    food.goto(x,y)

def reset_game():
    global score, delay, current_game_apples
    time.sleep(1)
    head.goto(0,0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000,1000)
    segments.clear()
    
    score = 0
    delay = 0.1
    current_game_apples = 0
    golden_food.hideturtle()
    current_game_apples = 0
    pen.clear()
    pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor() <-290 or head.ycor()>290 or head.ycor()<-290:
        reset_game()   

    # Check for collision with food
    if head.distance(food) < 20:
        # Move food to random spot (radomly)
        while True:
            x = random.randint(-280,280)
            y = random.randint (-280,280)
            if head.distance (x, y) > 40 and all (segment.distance (x, y) > 20 for segment in segments):
                food.goto(x, y)
                break

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("purple")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay (red apple)
        delay = max (delay - 0.001, 0.05)

        # Increase the score
        score += 10

        if score > high_score: 
            high_score = score

        # Update the score display (red apple)
        pen.clear()
        pen.write(f"Score: {score} High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

        # Track apples eaten (golden apple)
        current_game_apples += 1

        # Show golden apple every 3 red apples (not at start)
        if current_game_apples > 0 and current_game_apples % 3 == 0 and not golden_food.isvisible():
            spawn_golden_apple()
                    
    # Check collision with golden apple
    if head.distance(golden_food) < 20:
        golden_food.hideturtle()
        delay *= 0.95

        # Add yellow segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("yellow")
        new_segment.penup()
        segments.append(new_segment)

        # Score for golden apple
        score += 30
        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {} High Score: {}". format(score, high_score), align="center", font=("Courier", 24, "normal"))

    #Move the end segments first in reverse
    for index in range(len(segments) -1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments [0].goto(x,y)

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) <20:
            reset_game()
            break
    
    time.sleep(delay)

wn.mainloop()
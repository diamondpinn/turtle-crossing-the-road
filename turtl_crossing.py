import time
from turtle import Screen, Turtle
import random

STARTING_POSITION = (0, -280)
FINISH_LINE_Y = 280
FONT = ("Courier", 24, "normal")
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 10
MOVE_INCREMENT = 2

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.penup()
        self.goto(STARTING_POSITION)
        self.setheading(90)  # Face the turtle upwards

    def move_forward(self):
        self.forward(STARTING_MOVE_DISTANCE)

    def move_backward(self):
        self.backward(STARTING_MOVE_DISTANCE)

    def go_to_start(self):
        self.goto(STARTING_POSITION)

class Car(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color(random.choice(COLORS))
        self.penup()
        self.setheading(180)  # Face the car to the left
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.speed("fastest")
        self.speed_factor = random.uniform(0.5, 2.0)  # Random speed factor for each car
        self.refresh()

    def refresh(self):
        self.goto(300, random.randint(-250, 250))

    def move(self):
        self.forward(STARTING_MOVE_DISTANCE * self.speed_factor)

class CarManager:
    def __init__(self):
        self.cars = []
        self.generate_initial_cars()

    def generate_initial_cars(self):
        for _ in range(10):
            self.create_car()

    def create_car(self):
        new_car = Car()
        self.cars.append(new_car)

    def move_cars(self):
        for car in self.cars:
            car.move()
            # Check if the car has passed the left edge
            if car.xcor() < -320:
                car.refresh()

    def increase_speed(self):
        global STARTING_MOVE_DISTANCE
        STARTING_MOVE_DISTANCE += MOVE_INCREMENT

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(-220, 260)
        self.level = 1
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def level_up(self):
        self.level += 1
        self.update_scoreboard()

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

screen.listen()
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.onkey(player.move_forward, "Up")
screen.onkey(player.move_backward, "Down")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.move_cars()

    # Check if the turtle has reached the top edge
    if player.ycor() > FINISH_LINE_Y:
        player.go_to_start()
        car_manager.increase_speed()
        scoreboard.level_up()

    # Detect collision with cars
    for car in car_manager.cars:
        if player.distance(car) < 20:
            scoreboard.clear()
            scoreboard.goto(0, 0)
            scoreboard.write("Game Over", align="center", font=FONT)
            game_is_on = False

screen.exitonclick()

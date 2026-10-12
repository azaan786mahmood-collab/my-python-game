import tkinter as tk  # Import tkinter so we can make the game window
import random  # Import random so enemies and stars can appear randomly

WIDTH = 600  # Set the width of the game screen
HEIGHT = 700  # Set the height of the game screen

root = tk.Tk()  # Create the main game window
root.title("Space Shooter")  # Give the window the name Space Shooter
root.resizable(False, False)  # Stop the player from resizing the window

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")  # Create the black game screen
canvas.pack()  # Put the game screen inside the window

player = canvas.create_rectangle(280, 620, 320, 660, fill="cyan")  # Create the cyan player spaceship

bullets = []  # Create an empty list to store bullets
enemies = []  # Create an empty list to store enemies
score = 0  # Set the starting score to zero
game_over = False  # Tell the game that it has not ended

score_text = canvas.create_text(50, 30, text="Score: 0", fill="white", font=("Arial", 18))  # Create the score display

stars = []  # Create an empty list to store the stars

for _ in range(80):  # Repeat this 80 times to create 80 stars
    x = random.randint(0, WIDTH)  # Choose a random horizontal position
    y = random.randint(0, HEIGHT)  # Choose a random vertical position
    star = canvas.create_oval(x, y, x+2, y+2, fill="white")  # Create a small white star
    stars.append(star)  # Add the star to the stars list


def move_player(event):  # Create a function that moves the player

    if game_over:  # Check if the game has ended
        return  # Stop the function if the game is over

    x1, y1, x2, y2 = canvas.coords(player)  # Get the player's current position

    if event.keysym == "Left" and x1 > 0:  # Check if Left Arrow was pressed and the player is on screen
        canvas.move(player, -20, 0)  # Move the player 20 pixels to the left

    if event.keysym == "Right" and x2 < WIDTH:  # Check if Right Arrow was pressed and the player is on screen
        canvas.move(player, 20, 0)  # Move the player 20 pixels to the right


def shoot(event=None):  # Create a function for shooting bullets

    if game_over:  # Check if the game has ended
        return  # Stop shooting if the game is over

    x1, y1, x2, y2 = canvas.coords(player)  # Get the player's current position

    bullet = canvas.create_rectangle((x1+x2)//2-3, y1-10, (x1+x2)//2+3, y1, fill="yellow")  # Create a yellow bullet

    bullets.append(bullet)  # Add the bullet to the bullets list


def create_enemy():  # Create a function for making enemies

    if game_over:  # Check if the game has ended
        return  # Stop making enemies if the game is over

    for _ in range(2):  # Create two enemies each time this function runs

        x = random.randint(20, WIDTH-40)  # Choose a random horizontal position

        enemy = canvas.create_rectangle(x, 0, x+30, 30, fill="red")  # Create a red enemy at the top

        enemies.append(enemy)  # Add the enemy to the enemies list

    root.after(3000, create_enemy)  # Wait 3 seconds and then create two more enemies


def update():  # Create the main game loop

    global score, game_over  # Allow this function to change score and game_over

    if game_over:  # Check if the game has ended
        return  # Stop updating everything if the game is over

    for bullet in bullets[:]:  # Go through every bullet in the game

        canvas.move(bullet, 0, -15)  # Move each bullet upwards

        if canvas.coords(bullet)[1] < 0:  # Check if the bullet has left the top of the screen
            canvas.delete(bullet)  # Delete the bullet from the screen
            bullets.remove(bullet)  # Remove the bullet from the bullets list

    for enemy in enemies[:]:  # Go through every enemy in the game

        canvas.move(enemy, 0, 2)  # Move each enemy down slowly

        if canvas.coords(enemy)[3] > HEIGHT:  # Check if an enemy reaches the bottom
            end_game()  # End the game if an enemy reaches the bottom

        for bullet in bullets[:]:  # Check every bullet against the enemy

            if hit(bullet, enemy):  # Check if the bullet hits the enemy

                canvas.delete(enemy)  # Delete the enemy from the screen
                canvas.delete(bullet)  # Delete the bullet from the screen

                enemies.remove(enemy)  # Remove the enemy from the enemies list
                bullets.remove(bullet)  # Remove the bullet from the bullets list

                score += 1  # Add one point to the score

                canvas.itemconfig(score_text, text=f"Score: {score}")  # Update the score on the screen

                break  # Stop checking bullets for this enemy

    for star in stars:  # Go through every star

        canvas.move(star, 0, 3)  # Move each star down

        x1, y1, x2, y2 = canvas.coords(star)  # Get the star's current position

        if y1 > HEIGHT:  # Check if the star has reached the bottom
            canvas.move(star, 0, -HEIGHT)  # Move the star back to the top

    root.after(30, update)  # Run the game loop again after 30 milliseconds


def hit(a, b):  # Create a function to check if two objects collide

    ax1, ay1, ax2, ay2 = canvas.coords(a)  # Get the position of object A
    bx1, by1, bx2, by2 = canvas.coords(b)  # Get the position of object B

    return (  # Return True if the two objects are touching
        ax1 < bx2 and  # Check the left side of object A
        ax2 > bx1 and  # Check the right side of object A
        ay1 < by2 and  # Check the top of object A
        ay2 > by1  # Check the bottom of object A
    )


def end_game():  # Create a function for ending the game

    global game_over  # Allow this function to change game_over

    game_over = True  # Tell the game that the game is over

    canvas.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER", fill="red", font=("Arial", 40))  # Show GAME OVER

    canvas.create_text(WIDTH/2, HEIGHT/2+50, text=f"Final Score: {score}", fill="white", font=("Arial", 20))  # Show the final score


root.bind("<Left>", move_player)  # Make the Left Arrow move the player
root.bind("<Right>", move_player)  # Make the Right Arrow move the player
root.bind("<space>", shoot)  # Make the Space key shoot

create_enemy()  # Start creating enemies
update()  # Start the game loop
root.mainloop()  # Keep the game window open
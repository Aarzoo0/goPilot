import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game Window Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GoPilot👨‍✈️")

# Colors
WHITE = (255, 255, 255)
DARK_BLUE =  (135, 206, 235) 
LIGHT_BLUE = (0, 51, 102)  
GREEN = (34, 139, 34)  # Plane color
YELLOW = (255, 255, 102)  # Message text color

# Game Clock
clock = pygame.time.Clock()

# Plane Settings
plane_width = 50
plane_height = 50
plane_x = 100
plane_y = HEIGHT // 2
plane_speed = 5

# Fonts for Messages
font = pygame.font.SysFont("Comic Sans MS", 36)  # Reduced font size for welcome message
small_font = pygame.font.SysFont("Comic Sans MS", 24)  # Strong, bold font for small messages

# Load Images
plane_img = pygame.image.load('assets/plane.png')  # Plane image
plane_img = pygame.transform.scale(plane_img, (50, 50))

bird_img = pygame.image.load('assets/bird.png')  # Bird image for obstacles
bird_img = pygame.transform.scale(bird_img, (50, 50))

star_img = pygame.image.load('assets/star.png')  # Star image for luck points
star_img = pygame.transform.scale(star_img, (50, 50))

# Obstacle Settings
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Luck Point Settings
luck_point_width = 50  # Same size as star
luck_point_height = 50  # Same size as star
luck_points = []

# Message Display Duration
message_duration = 3  # seconds
message_start_time = None  # Time when the message started
message_text = ""
is_message_displaying = False

# Create an obstacle (bird image)
def create_obstacle():
    x_pos = WIDTH
    y_pos = random.randint(0, HEIGHT - obstacle_height)
    obstacles.append([x_pos, y_pos])

# Move obstacles
def move_obstacles():
    for obstacle in obstacles:
        obstacle[0] -= obstacle_speed  # Move obstacles left

# Draw obstacles (bird image)
def draw_obstacles():
    for obstacle in obstacles:
        screen.blit(bird_img, (obstacle[0], obstacle[1]))

# Create a luck point (star image)
def create_luck_point():
    x_pos = WIDTH
    y_pos = random.randint(0, HEIGHT - luck_point_height)
    luck_points.append([x_pos, y_pos])

# Move luck points
def move_luck_points():
    for luck_point in luck_points:
        luck_point[0] -= obstacle_speed  # Move luck points left

# Draw luck points (star image)
def draw_luck_points():
    for luck_point in luck_points:
        screen.blit(star_img, (luck_point[0], luck_point[1]))

# Check if luck point is collected
def check_luck_point_collection():
    global plane_x, plane_y
    for luck_point in luck_points:
        if plane_x < luck_point[0] + luck_point_width and plane_x + plane_width > luck_point[0]:
            if plane_y < luck_point[1] + luck_point_height and plane_y + plane_height > luck_point[1]:
                luck_points.remove(luck_point)  # Remove collected luck point
                display_message("Keep flying high!")

# Display a message
def display_message(message):
    global message_start_time, message_text, is_message_displaying
    message_text = message
    message_start_time = time.time()  # Record the time when the message started
    is_message_displaying = True

# Display a welcome message (Start page)
def display_start_page():
    start_text = font.render("Welcome to the Game Adill Ibrahim!", True, YELLOW)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 3))
    instructions_text = small_font.render("Press any key to start", True, YELLOW)
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

# Display the "Game Over" message and then the final message
def display_game_over_page():
    game_over_text = font.render("Game Over, but not exams!", True, (231, 207, 129))  # Red-orange color
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    pygame.display.update()
    time.sleep(2)  # Display for 2 seconds

    # Final message after game over
    final_msg = small_font.render("All the best Adil, go give your best, phod dena!", True, (164, 230, 194))
    screen.blit(final_msg, (WIDTH // 2 - final_msg.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    time.sleep(4)  # Display for 4 seconds

# Main Game Loop
def game_loop():
    global plane_y, is_message_displaying, message_text
    running = True
    while running:
        # Background color gradient
        for y in range(0, HEIGHT):
            color = [
                int(LIGHT_BLUE[0] * (1 - y / HEIGHT) + DARK_BLUE[0] * (y / HEIGHT)),
                int(LIGHT_BLUE[1] * (1 - y / HEIGHT) + DARK_BLUE[1] * (y / HEIGHT)),
                int(LIGHT_BLUE[2] * (1 - y / HEIGHT) + DARK_BLUE[2] * (y / HEIGHT)),
            ]
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

        # Event handling (quit game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False  # Start the game after pressing Enter key

        # Display the start page
        display_start_page()

        # Wait for a key press to start the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            break  # Exit the start page and start the game

    # Game logic after the start page
    running = True
    while running:
        screen.fill(DARK_BLUE)  # Background color

        # Event handling (quit game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Control plane movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and plane_y > 0:
            plane_y -= plane_speed
        if keys[pygame.K_DOWN] and plane_y < HEIGHT - plane_height:
            plane_y += plane_speed

        # Create obstacles and luck points randomly
        if random.randint(1, 100) == 1:
            create_obstacle()
        if random.randint(1, 100) == 1:
            create_luck_point()

        # Move and draw obstacles and luck points
        move_obstacles()
        draw_obstacles()
        move_luck_points()
        draw_luck_points()

        # Check for collision and collection of luck points
        check_luck_point_collection()

        for obstacle in obstacles:
            if plane_x < obstacle[0] + obstacle_width and plane_x + plane_width > obstacle[0]:
                if plane_y < obstacle[1] + obstacle_height and plane_y + plane_height > obstacle[1]:
                    display_game_over_page()  # Show game over and final message
                    running = False  # End the game after showing final message

        # Draw the plane
        screen.blit(plane_img, (plane_x, plane_y))

        # Display the message if it's being shown
        if is_message_displaying:
            # Show message
            text = font.render(message_text, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

            # Check if message time has expired
            if time.time() - message_start_time >= message_duration:
                is_message_displaying = False

        # Update the display
        pygame.display.update()

        # Frame rate (60 FPS)
        clock.tick(60)

# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()

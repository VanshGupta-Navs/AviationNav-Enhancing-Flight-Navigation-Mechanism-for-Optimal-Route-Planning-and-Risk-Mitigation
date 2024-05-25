import pygame
import ofApp
import ofApp2

# Initialize pygame
pygame.init()

# Set up the window
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Your App Name")

# Create an instance of your app
app = ofApp()

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    app.update()

    # Render
    screen.fill((0, 0, 0))  # Clear the screen
    app.render(screen)      # Render your app
    pygame.display.flip()   # Update the display

    # Cap the frame rate
    clock.tick(60)  # Limit to 60 frames per second

# Quit pygame
pygame.quit()

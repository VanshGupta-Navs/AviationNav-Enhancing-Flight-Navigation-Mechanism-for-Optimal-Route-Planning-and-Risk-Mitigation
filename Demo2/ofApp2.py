import pygame
import Environment
import Robot

class ofApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Your App Name")
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.Font(None, 30)
        self.updateFlag = True
        self.map = Environment()
        self.car = Robot()
        self.obst = []
        self.OBST = movingObst()
        self.wall = maze()
        self.updateTime = 0
        self.drawTime = 0

    def setup(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def keyPressed(self, key):
        pass

    def keyReleased(self, key):
        pass

    def mouseMoved(self, x, y):
        pass

    def mouseDragged(self, x, y, button):
        pass

    def mousePressed(self, x, y, button):
        pass

    def mouseReleased(self, x, y, button):
        pass

    def mouseEntered(self, x, y):
        pass

    def mouseExited(self, x, y):
        pass

    def windowResized(self, w, h):
        pass

    def dragEvent(self, dragInfo):
        pass

    def gotMessage(self, msg):
        pass

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # Clear the screen

            # Call your update and draw methods
            self.update()
            self.draw()

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Cap the frame rate

        pygame.quit()

if __name__ == "__main__":
    app = ofApp()
    app.run()

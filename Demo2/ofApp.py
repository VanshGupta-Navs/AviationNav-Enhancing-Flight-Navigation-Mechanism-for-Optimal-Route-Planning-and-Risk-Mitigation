import time
import random
import pygame
from pygame.locals import *
import sys
import ofApp2

class ofApp:
    def __init__(self):
        self.updateFlag = True
        self.numberOfobst = 10
        self.obst = []
        self.map = None
        self.car = None
        self.OBST = None
        self.updateTime = 0
        self.drawTime = 0
        self.myfont = pygame.font.Font("Roboto-Regular.ttf", 10)
        self.setup()

    def setup(self):
        randomSeed = None
        CLK = True

        if randomSeed:
            random.seed(randomSeed)

        if CLK:
            start = time.time()

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dynamic-obstacles")
        self.screen.fill((200, 200, 200))

        w = pygame.Vector2(pygame.display.get_surface().get_width() / 2, 0)
        wall = maze(w)
        ob = wall
        self.obst.append(ob)

        w = pygame.Vector2(pygame.display.get_surface().get_width() / 2, 0.6 * pygame.display.get_surface().get_height())
        wall = maze(w)
        ob = wall
        self.obst.append(ob)

        w = pygame.Vector2(pygame.display.get_surface().get_width() / 4, 0.4 * pygame.display.get_surface().get_height())
        wall = maze(w, 60, 0.2 * pygame.display.get_surface().get_height())
        ob = wall
        self.obst.append(ob)

        w = pygame.Vector2(0.75 * pygame.display.get_surface().get_width(), 0.4 * pygame.display.get_surface().get_height())
        wall = maze(w, 60, 0.2 * pygame.display.get_surface().get_height())
        ob = wall
        self.obst.append(ob)

        for i in range(self.numberOfobst):
            ob = obstacles()
            self.obst.append(ob)

        self.OBST = movingObst()
        ob = self.OBST
        self.obst.append(ob)

        print("Obst size:", len(self.obst))

        if randomSeed:
            print("RandomSeed:", randomSeed)

        if CLK:
            end = time.time()
            print("\nSetup:", (end - start) * 1000, "ms")

    def update(self):
        if not self.updateFlag:
            return

        CLK = True

        if CLK:
            start = time.time()

        automatic = True

        if automatic:
            for i in self.obst:
                i.move(self.obst)

        if self.map is not None:
            self.map.update(self.car, self.obst)

        if CLK:
            end = time.time()
            self.updateTime = (end - start) * 1000

    def draw(self):
        CLK = True

        if CLK:
            start = time.time()

        for i in self.obst:
            i.render(self.screen)

        if self.map is not None:
            self.map.render(self.screen)

        if self.car is not None:
            self.car.render(self.screen)

        fpsStr = f"Frame rate: {int(pygame.time.Clock().get_fps())}"
        fps_surface = self.myfont.render(fpsStr, True, (255, 0, 0))
        self.screen.blit(fps_surface, (pygame.display.get_surface().get_width() - 100, pygame.display.get_surface().get_height() - 25))

        if self.map is not None:
            numNode = f"Number of nodes: {int(self.map.numofnode())}"
            numNode_surface = self.myfont.render(numNode, True, (255, 0, 0))
            self.screen.blit(numNode_surface, (pygame.display.get_surface().get_width() - 140, pygame.display.get_surface().get_height() - 10))

        if CLK:
            end = time.time()
            self.drawTime = (end - start) * 1000

            timeStr = f"Update rate: {self.updateTime}"
            time_surface = self.myfont.render(timeStr, True, (255, 0, 0))
            self.screen.blit(time_surface, (pygame.display.get_surface().get_width() - 140, pygame.display.get_surface().get_height() - 755))

            timeStr = f"Draw rate: {self.drawTime}"
            time_surface = self.myfont.render(timeStr, True, (255, 0, 0))
            self.screen.blit(time_surface, (pygame.display.get_surface().get_width() - 140, pygame.display.get_surface().get_height() - 740))

    def keyPressed(self, key):
        if key == K_p:
            self.updateFlag = not self.updateFlag
        elif key == K_g:
            self.map.grid = not self.map.grid
        elif key == K_x:
            pygame.image.save(self.screen, "screenshot.png")

        manual = True

        if manual:
            self.OBST.move(key)

    def keyReleased(self, key):
        pass

    def mouseMoved(self, x, y):
        pass

    def mouseDragged(self, x, y, button):
        pass

    def mousePressed(self, x, y, button):
        loc = pygame.Vector2(x, y)
        if button == 1:
            if self.car is not None:
                self.map.targetSet(loc)
        elif button == 3:
            self.car = Robot(loc)
            self.map = Enviroment(self.car.getLocation())

    def mouseReleased(self, x, y, button):
        pass

    def mouseEntered(self, x, y):
        pass

    def mouseExited(self, x, y):
        pass

    def windowResized(self, w, h):
        pass

    def gotMessage(self, msg):
        pass

    def dragEvent(self, dragInfo):
        pass

if __name__ == "__main__":
    app = ofApp()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                app.keyPressed(event.key)
            elif event.type == KEYUP:
                app.keyReleased(event.key)
            elif event.type == MOUSEMOTION:
                app.mouseMoved(event.pos[0], event.pos[1])
            elif event.type == MOUSEBUTTONDOWN:
                app.mousePressed(event.pos[0], event.pos[1], event.button)
            elif event.type == MOUSEBUTTONUP:
                app.mouseReleased(event.pos[0], event.pos[1], event.button)

        app.update()
        app.draw()
        pygame.display.flip()
        clock.tick(30)



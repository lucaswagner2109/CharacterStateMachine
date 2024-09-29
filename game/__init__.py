import pygame, sys

class Game:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Title")
        self.screen = pygame.display.set_mode((640, 320))
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill((252,252,252))
            pygame.display.update()
                    
game = Game()
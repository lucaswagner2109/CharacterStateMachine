from .config import Config

class Game():
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Title")
        self.screen = pygame.display.set_mode(Config.WINDOW_SIZE)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill(Config.BLACK)
            pygame.display.update()
import pygame
import grove_ultrasonic as ultrasonic

def main():
    pygame.init()

    # Nastavení velikosti okna
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 600

    # Vytvoření okna
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Dynamicky se měnící text")
    pygame.mouse.set_visible(False)


    # Nastavení výchozího textu
    font = pygame.font.SysFont(None, 48)
    new_text = "Výchozí text".encode('utf-8')
    text = font.render(new_text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    # Hlavní smyčka
    running = True
    new_text = 0
    while running:

        ultrason = ultrasonic.GroveUltrasonicRanger(18)
        new_text = ultrason.get_distance()
        
        #ultrasonic = UltrasonicRanger(5)
        #new_text = ultrasonic.get_distance()
        
        print(new_text)
        pygame.time.delay(100)
        

        # Procházení událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                        pygame.display.quit()
                        pygame.quit()
                        running = False
                        return 0

        # Změna textu
        #new_text += 1
        new_text_surface = font.render(str(new_text), True, (255, 255, 255))
        text_rect = new_text_surface.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Kreslení
        screen.fill((0, 0, 0))
        screen.blit(new_text_surface, text_rect)
        pygame.display.update()

    # Ukončení Pygame
    pygame.quit()
    pygame.display.quit()
    


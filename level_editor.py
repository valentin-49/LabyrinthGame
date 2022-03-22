import pygame


pygame.init()



#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 200
SIDE_MARGIN = 200

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


#game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21



#background image
background_image = pygame.image.load('img/Background/background_color_violet.png').convert_alpha()
background_image = pygame.transform.scale(background_image,(SCREEN_WIDTH,SCREEN_HEIGHT))





#couleurs
lower_bar= (0, 0, 60)
WHITE = (255, 255, 255)
RED = (200, 25, 25)




#fonction background
def draw_background():
    width = background_image.get_width()
screen.blit(background_image, [0, 0])






run = True
while run:



	draw_background()
	
	

	#lower bar bleu
	pygame.draw.rect(screen, lower_bar, (0, 630, 800, 500))

	

	





	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False



	pygame.display.update()

pygame.quit()


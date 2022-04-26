import pygame
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#fenêtre de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 150
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Editeur')


#variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 4
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


#background
background_image = pygame.image.load('img/Background/Q0yP6.png').convert_alpha()
background_image = pygame.transform.scale(background_image,(SCREEN_WIDTH,SCREEN_HEIGHT))


#tuiles
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()


#couleurs
lower_bar= (0, 0, 60)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
GREEN = (144, 201, 120)
side_bar = (85, 123, 131)


#font
font = pygame.font.SysFont('Futura', 30)

#liste tuiles vide
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)




#fonction pour les textes
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#background
def draw_background():
	width = background_image.get_width()
	screen.blit(background_image, [0, 0])

#grille
def draw_grid():
	#lignes vertical
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	#lignes horizontal
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#tuiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))



#créations boutons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0


run = True
while run:

	clock.tick(FPS)

	draw_background()
	draw_grid()
	draw_world()

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	#########################################################draw_text('FLECHE HAUT ET BAS POUR CHANGER DE LEVEL', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	#save and load data
	if save_button.draw(screen):
		#save level data
		with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				writer.writerow(row)
		#alternative pickle method
		#pickle_out = open(f'level{level}_data', 'wb')
		#pickle.dump(world_data, pickle_out)
		#pickle_out.close()
	if load_button.draw(screen):
		#load in level data
		#reset scroll back to the start of the level
		scroll = 0
		with open(f'level{level}_data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)
		#alternative pickle method
		#world_data = []
		#pickle_in = open(f'level{level}_data', 'rb')
		#world_data = pickle.load(pickle_in)
				

	#panel tuiles
	pygame.draw.rect(screen, side_bar, (SCREEN_WIDTH, 0, SIDE_MARGIN, 645))

	#selection tuile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#highlight tuile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	#scroll map
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#ajout tuile
	#postion souris
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	#check tuile
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tuile
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#keyboard
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()


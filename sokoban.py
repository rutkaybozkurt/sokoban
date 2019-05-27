import pygame
import sys
import os
from level import Level
from menu import *

pygame.init()
pygame.display.init()
pygame.display.set_caption("Sokoboi")
size = (800, 600)
screen = pygame.display.set_mode(size)


def draw_level(level_matrix):
	# Load images
	wall = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/wall.png').convert()
	box = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/box.png').convert()
	box_on_target = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/box_on_target.png').convert()
	floor = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/floor.png').convert()
	target = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/target.png').convert()
	player = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/player.png').convert()

	# Dictionary to map images to characters in level matrix
	images = {'#': wall, ' ': floor, '$': box, '.': target, '@': player, '*': box_on_target}

	# Get image size to print on screen
	box_size = wall.get_width()


	# Print images for matrix
	for i in range(0, len(level_matrix)):
		for c in range(0, len(level_matrix[i])):
			screen.blit(images[level_matrix[i][c]], (c * box_size, i * box_size))

	pygame.display.update()


def move(direction, active_level):

	matrix = active_level.get_matrix()

	active_level.save_history(matrix)

	x = active_level.get_pos()[0]
	y = active_level.get_pos()[1]

	global target_found

	#Print boxes
	print(active_level.get_boxes())

	if direction == "L":
		print("######### Moving Left #########")
		i = 0
		j = -1
	elif direction == "R":
		print("######### Moving Right #########") 
		i = 0
		j = 1
	elif direction == "U":
		print("######### Moving Up #########")
		i = -1
		j = 0
	elif direction == "D":
		print("######### Moving Down #########")
		i = 1
		j = 0
	

	# Next square is empty space
	if matrix[x + i][y + j] == " ":
		print("Empty Space Found")
		matrix[x + i][y + j] = "@"
		if target_found is True:
			matrix[x][y] = "."
			target_found = False
		else:
			matrix[x][y] = " "

	# Next square is a_box
	elif matrix[x + i][y + j] == "$":
		print("Box Found")
		if matrix[x + 2 * i][y + 2 * j] == " ":
			matrix[x + 2 * i][y + 2 * j] = "$"
			matrix[x + i][y + j] = "@"
			if target_found == True:
				matrix[x][y] = "."
				target_found = False
			else:
				matrix[x][y] = " "

		elif matrix[x + 2 * i][y + 2 * j] == ".":
			matrix[x+ 2 * i][y + 2 * j] = "*"
			matrix[x + i][y + j] = "@"
			if target_found == True:
				matrix[x][y] = "."
				target_found = False
			else:
				matrix[x][y] = " "


	# Next square is a_box on target
	elif matrix[x + i][y + j] == "*":
		print("Box on target Found")
		if matrix[x + 2 * i][y + 2*j] == " ":
			matrix[x + 2 * i][y + 2 * j] = "$"
			matrix[x + 2 * i][y + 2 * j] = "@"
			if target_found is True:
				matrix[x][y] = "."
			else:
				matrix[x][y] = " "
			target_found = True

		elif matrix[x + 2 * i][y + 2 * j] == ".":
			matrix[x + 2 * i][y + 2 * j] = "*"
			matrix[x + i][y + j] = "@"
			if target_found is True:
				matrix[x][y] = "."
			else:
				matrix[x][y] = " "
			target_found = True

	# Next square is a target
	elif matrix[x + i][y + j] == ".":
		print("Target Found")
		matrix[x + i][y + j] = "@"
		if target_found == True:
			matrix[x][y] = "."
		else:
			matrix[x][y] = " "
		target_found = True

	# Else
	else:
		print("There is a wall here")


	draw_level(matrix)

	print("Boxes remaining: " + str(len(active_level.get_boxes())))

	if len(active_level.get_boxes()) == 0 :
		screen.fill((0, 0, 0))
		print("Level Completed")
		global current_level
		print("Current_level is:" + str(current_level))
		current_level += 1
		init_level(current_level)


def init_level(level):
	global active_level
	active_level = Level(level)

	draw_level(active_level.get_matrix())

	global target_found
	target_found = False

#Hazır menü classı ile yapılmış menü, kendi menümüz de yapılabilir
def game_menu():
	main_menu = cMenu(50,50,20,5,'vertical',100,screen,
	[('Start Game',1,None),
	('Quit Game',5,None)])
	
	main_menu.set_center(True, True)
	main_menu.set_alignment('center', 'center')

	state = 0
	prev_state = 1

	rect_list = []

	pygame.event.set_blocked(pygame.MOUSEMOTION)

	while 1: 

		if prev_state != state:
			pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
			prev_state = state
		
		e = pygame.event.wait()

		if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
			if state == 0:
				rect_list, state = main_menu.update(e, state)
			elif state == 1:
				game_loop()
				state = 0
			elif state == 3:
				break
			else:
				print('Exit!')
				pygame.quit()
				sys.exit()

		# Quit if the user presses the exit button
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Update the screen
		pygame.display.update(rect_list)

# Current_level'ın gösterildiği ve değiştirebildiği bir ekran eklenecek
def level_select():
	current_level = 1

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			current_level -= 1
		elif event.key == pygame.K_RIGHT:
			current_level += 1
		elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
			game_menu()



def game_loop():
	init_level(current_level)

	target_found = False

	menu = False

	while True:

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					move("L", active_level)
				elif event.key == pygame.K_RIGHT:
					move("R", active_level)
				elif event.key == pygame.K_UP:
					move("U", active_level)
				elif event.key == pygame.K_DOWN:
					move("D", active_level)
				elif event.key == pygame.K_u:
					draw_level(active_level.undo())
				elif event.key == pygame.K_r:
					init_level(current_level)
				elif event.key == pygame.K_ESCAPE:
					menu = True
					break
			elif event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		if menu:
			screen.fill((0,0,0))
			pygame.display.update()
			break

if __name__ == "__main__":
	current_level = 1
	game_menu()

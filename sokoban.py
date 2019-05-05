

import pygame,sys,os
from level import Level

pygame.display.init()
pygame.display.set_caption("Sokoboi")
size = (800,600)
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
		print "######### Moving Left #########"
		i = 0
		j = -1
	elif direction == "R":
		print "######### Moving Right #########" 
		i = 0
		j = 1
	elif direction == "U":
		print "######### Moving Up #########"
		i = -1
		j = 0
	elif direction == "D":
		print "######### Moving Down #########"
		i = 1
		j = 0
	

	# Next square is empty space
	if matrix[x + i][y + j] == " ":
		print "Empty Space Found"
		matrix[x + i][y + j] = "@"
		if target_found == True:
			matrix[x][y] = "."
			target_found = False
		else:
			matrix[x][y] = " "

	# Next square is a_box
	elif matrix[x + i][y + j] == "$":
		print "Box Found"
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
		print "Box on target Found"
		if matrix[x + 2 * i][y + 2*j] == " ":
			matrix[x + 2 * i][y + 2 * j] = "$"
			matrix[x + 2 * i][y + 2 * j] = "@"
			if target_found == True:
				matrix[x][y] = "."
			else:
				matrix[x][y] = " "
			target_found = True

		elif matrix[x + 2 * i][y + 2 * j] == ".":
			matrix[x + 2 * i][y + 2 * j] = "*"
			matrix[x + i][y + j] = "@"
			if target_found == True:
				matrix[x][y] = "."
			else:
				matrix[x][y] = " "
			target_found = True

	# Next square is a target
	elif matrix[x + i][y + j] == ".":
		print "Target Found"
		matrix[x + i][y + j] = "@"
		if target_found == True:
			matrix[x][y] = "."
		else:
			matrix[x][y] = " "
		target_found = True

	# Else
	else:
		print "There is a wall here"


	draw_level(matrix)

    	print "Boxes remaining: " + str(len(active_level.get_boxes()))

    	if len(active_level.get_boxes()) == 0:
		screen.fill((0, 0, 0))
		print("Level Completed")
		global current_level
		current_level += 1
		init_level(current_level)


def init_level(level):
	global active_level
	active_level = Level(level)

	draw_level(active_level.get_matrix())

	global target_found
	target_found = False


current_level = 1

# Initialize Level
init_level(current_level)

target_found = False

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
				pygame.quit()
				sys.exit()
		elif event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

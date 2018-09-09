# imports needed for program
import sys
import pygame

from pygame.locals import *

# iniitilize pygame content
pygame.init()

# Set up window dimensions and title
DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello Wolrd!')

# color constants in RGB formats
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# create a font object with the font and size of the text as the two parameters
fontObj = pygame.font.Font('freesansbold.ttf', 32)
# create a text box with the text 'Hello world!' in green and a background of blue
# the true means there will be anti-aliasing (smooth lines), false means aliased lines (blocky lines)
textSurfaceObj = fontObj.render('Hello world!', True, GREEN, BLUE)
# sets a rectangle object equal to the rectangle of the text box cfreated above
textRectObj = textSurfaceObj.get_rect()
# Sets the center of the object at pixel x = 200 and pixel y = 150, change this in order to change where
# the text will display on screen
textRectObj.center = (200, 150)

# main game loop
while True:
	DISPLAYSURF.fill(WHITE)
	# draw the text object on the board, exact coordinates come from the rect obj
	DISPLAYSURF.blit(textSurfaceObj, textRectObj) 
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	# actually update the display window
	pygame.display.update()

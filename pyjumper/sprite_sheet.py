# This class handles sprite sheets
# This was taken from http://programarcadegames.com/python_examples/en/sprite_sheets/

import pygame

 
class SpriteSheet:
    """ Class used to grab images out of a sprite sheet. """
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
 
 
    def get_image(self, x, y, width, height, colorkey=None):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
 
        # Create a new blank image
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Assuming black works as the transparent color
        if colorkey is None:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
 
        # Return the image
        return image


import pygame

from sprite_sheet import SpriteSheet


screen_width = 532
screen_height = 850

pygame.init()
pygame.display.set_mode((screen_width, screen_height))


background_image = 'images/background.png'
menu_background_image = 'images/menu_background.png'
player_background_image = 'images/likright_X.png'
player_shooting_background_image = 'images/likpuca_X.png'
btn_background_image = 'images/consent_button.png'
btn_hover_background_image = 'images/consent_button_on.png'

frame_rate = 30

font_name = 'sans'
font_size = 35

platform_w = 100
platform_h = 25

player_w = 100
player_h = 100

menu_button_w = 200
menu_button_h = 70

screen_scroll_player_top = 350

platforms_generate_interval = (100, 400)

sounds_effects = {
        'jump': 'sound_effects/jump.ogg',
        'pada': 'sound_effects/pada.ogg',
        'spring': 'sound_effects/springshoes.ogg',
        'broken': 'sound_effects/lomise.ogg',
        }


game_sprite_sheet_filename='images/gametiles_X.png' 
game_ss = SpriteSheet(game_sprite_sheet_filename)

spring_image = game_ss.get_image(808, 198, 34, 23)
opened_spring_image = game_ss.get_image(808, 230, 34, 55)
basic_platform = game_ss.get_image(2, 2, 114, 30)
platform_moving_horizontal = game_ss.get_image(2, 36, 114, 30)
platform_moving_vertical = game_ss.get_image(2, 73, 114, 30)
one_hit_platform = game_ss.get_image(2, 109, 114, 30)
broken_platform = game_ss.get_image(2, 146, 120, 30)
broken_platform_2 = game_ss.get_image(2, 182, 121, 40)
broken_platform_3 = game_ss.get_image(4, 232, 113, 55)
broken_platform_4 = game_ss.get_image(3, 298, 115, 64)


menu_sprite_sheet_filename='images/screens_X.png' 
menu_ss = SpriteSheet(menu_sprite_sheet_filename)

ufo_image = menu_ss.get_image(696, 483, 155, 68)
ray_image = menu_ss.get_image(733, 2, 158, 181)

import pygame
import math
from info import *

#kolidraat fanaar glucose gladiatoren
def achtergrond_functie(achtergrond_path):
    global scherm
    achtergrond = pygame.image.load("tracks/" + achtergrond_path)
    scherm.blit(achtergrond, (0, 0))
    # scherm.fill((255, 255, 255))
    
def krijg_muis_positie():
    return pygame.mouse.get_pos()

def teken(autos):
    global scherm
    for auto in autos:
        pygame.draw.rect(auto.auto_oppervlak, auto.kleur, (0, 0, auto.breete, auto.lengte))
        auto.gedraaide_oppervlak = pygame.transform.rotate(auto.auto_oppervlak, auto.richting)
        auto.gedraaid_rechthoek = auto.gedraaide_oppervlak.get_rect(center=(auto.positie_x, auto.positie_y))
        scherm.blit(auto.gedraaide_oppervlak, auto.gedraaid_rechthoek.topleft)
    return scherm
    
def teken_pixel(pixel_x, pixel_y):
    global scherm
    if 0 <= pixel_x < scherm.get_width() and 0 <= pixel_y < scherm.get_height():
        scherm.set_at((round(pixel_x), round(pixel_y)), RAY_KLEUR)

def frame():
    global scherm
    pygame.display.update()

def scherm_maken(scherm_breete, scherm_hoogte):
    global scherm
    pygame.init()
    scherm = pygame.display.set_mode((scherm_breete, scherm_hoogte))

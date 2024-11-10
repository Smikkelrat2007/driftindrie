import pygame
from car import *
from display import *
from info import *
from track import mask_de_track
autos = []

def verwerk_input(game_on, autos):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        keys = pygame.key.get_pressed()
        for auto in [auto for auto in autos if auto.speler]:
            auto.links_rechts = 0
            if keys[auto.links_toets]:
                auto.links_rechts += 1
            if keys[auto.rechts_toets]:
                auto.links_rechts -= 1
            auto.voor_achter = 0
            if keys[auto.gas_toets]:
                auto.voor_achter += 1
            if keys[auto.rem_toets]:
                auto.voor_achter -= 1
                
        if keys[pygame.K_1]:
            autos = maak_test_auto(90, RAY_LIJST, autos)
        if keys[pygame.K_2]:
            autos = []
        if keys[pygame.K_3]:
            for auto in autos:
                auto.snelheid = 0
    return game_on, autos

def game(autos):
    dict, hoogste_waarde, achtergrond, gras_pixels = mask_de_track(track_info)
    scherm_maken(scherm_breete, scherm_hoogte)
    # autos = maak_test_auto(track_info[achtergrond][0], track_info[achtergrond][1], 90, 0, autos)
    
    game_on = True
    while game_on:
        pass
        pygame.time.Clock().tick(MAX_FPS)
        game_on, autos = verwerk_input(game_on, autos)
        achtergrond_functie(achtergrond)
        run_autos(autos, dict, gras_pixels)
        teken(autos)
        frame()

if __name__ == "__main__":
    game(autos)
    pygame.quit()
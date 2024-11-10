import math
import pygame
from ray import *
# from track import punten_checken
from display import krijg_muis_positie
from track import punten_checken
import neat

def maak_test_auto(richting, stralen_lijst, autos):
    muis_x, muis_y = krijg_muis_positie()
    print(muis_x, muis_y)
    autos.append(Auto(muis_x, muis_y, richting, 0, 3, 0.1, 0.05, 0.2, 10, 0.0001, 0.02, 1, (255,0,255), 20, 40, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, stralen_lijst, 100, 0, ""))
    return autos

def maak_ai_auto(positie_x, positie_y, richting, stralen_lijst, tijd, net):
    return Auto(positie_x, positie_y, richting, 2.5, 3, 0.1, 0.05, 0.2, 10, 0.0001, 0.02, 1, (255,0,255), 20, 40, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, stralen_lijst, MAX_LENGTE_RAYS, tijd, net)

def krijg_ai_info(auto, punten_dict, gras_pixels):
    auto.spawn_rays(gras_pixels)
    punten = punten_checken(round(auto.positie_x), round(auto.positie_y), punten_dict)
    if not punten == "error":
        auto.punten = punten
    
    input_lijst = auto.lengte_lijst
    for positie in auto.positie_lijst:
        try:
            input_lijst.append(punten_dict[positie] - auto.punten)
        except:
            input_lijst.append(0)
            
    return input_lijst, auto.punten

def apply_ai_outputs(auto, controls):
    auto.links_rechts = controls[0]
    auto.voor_achter = controls[1]

def run_ai_auto(auto, gras_pixels):
    auto.mechanica_toepassen()
    auto.positie_veranderen()
    if auto.positie_checken(gras_pixels):
        auto.dood = True

def run_autos(autos, punten_dict, gras_pixels):
    verwijder_auto = []
    for auto in autos:
        if not auto.dood:
            auto.mechanica_toepassen()
            auto.positie_veranderen()

            auto.spawn_rays(gras_pixels)
            if auto.positie_checken(gras_pixels):
                auto.dood = True

class Auto:
    def __init__(self, positie_x, positie_y, richting, snelheid, maximale_draai_snelheid, gas_sterkte, achteruit_gas_sterkte, rem_sterkte, grip_sterkte, luchtfrictie, rolfrictie, speler, kleur, breete, lengte, gas_toets, rem_toets, links_toets, rechts_toets, stralen_lijst, max_lengte_rays, tijd, net):
            self.positie_x = positie_x
            self.positie_y = positie_y
            self.richting = richting
            self.snelheid = snelheid
            self.maximale_draai_snelheid = maximale_draai_snelheid
            self.gas_sterkte = gas_sterkte
            self.achteruit_gas_sterkte = achteruit_gas_sterkte
            self.rem_sterkte = rem_sterkte
            self.grip_sterkte = grip_sterkte
            self.luchtfrictie = luchtfrictie
            self.rolfrictie = rolfrictie
            self.speler = speler
            self.kleur = kleur
            self.breete = breete
            self.lengte = lengte
            self.gas_toets = gas_toets
            self.rem_toets = rem_toets
            self.links_toets = links_toets
            self.rechts_toets = rechts_toets
            self.stralen_lijst = stralen_lijst
            self.max_lengte_rays = max_lengte_rays
            self.geboorte = tijd

            self.dood = False
            self.lengte_lijst = []
            self.positie_lijst = []
            self.auto_oppervlak = pygame.Surface((self.breete, self.lengte), pygame.SRCALPHA)
            self.voor_achter = 0 # Geeft aan wat de input is van de speler/AI, 1 betekend 100% gassen, -1 betekend, 100% remmen
            self.links_rechts = 0 # Geeft aan wat de input is van de speler/AI, -1 betekend 100% naar links sturen, 1 betekend helemaal naar rechts sturen
            self.snelheid_x = 0
            self.snelheid_y = 0
            self.neural_net = net
            self.punten = 0
            self.fitness = 0

    def mechanica_toepassen(self):
        if self.snelheid >= 0:
            if self.voor_achter <= 0:
                self.acceleratie = self.rem_sterkte * self.voor_achter
            if self.voor_achter >= 0:
                self.acceleratie = self.gas_sterkte * self.voor_achter
        if self.snelheid <= 0:
            if self.voor_achter >= 0:
                self.acceleratie = self.rem_sterkte * self.voor_achter
            elif self.voor_achter <= 0:
                self.acceleratie = self.achteruit_gas_sterkte * self.voor_achter

        if self.snelheid > 0:
            self.snelheid -= self.luchtfrictie * self.snelheid ** 2
            self.snelheid -= self.rolfrictie
            max(self.snelheid, 0)
        elif self.snelheid < 0:
            self.snelheid += self.luchtfrictie * self.snelheid ** 2
            self.snelheid += self.rolfrictie
            min(self.snelheid, 0)

        self.snelheid += self.acceleratie
        self.richting += self.links_rechts * self.grip_sterkte / max(self.maximale_draai_snelheid, self.snelheid)
        
        self.snelheid_x = math.sin(math.radians(self.richting)) * self.snelheid
        self.snelheid_y = math.cos(math.radians(self.richting)) * self.snelheid
        
    def positie_veranderen(self):
        self.positie_x += self.snelheid_x
        self.positie_y += self.snelheid_y

    def spawn_rays(self, gras_pixels):
        self.lengte_lijst, self.positie_lijst = spawn_stralen(self.stralen_lijst, self.positie_x, self.positie_y ,self.richting, [], gras_pixels, [])

    def positie_checken(self, gras_pixels):
        if (round(self.positie_x), round(self.positie_y)) in gras_pixels:
            return True
        return False

    # def punten(self, dict):
    #     punten_checken(self.positie_x, self.positie_y, dict)
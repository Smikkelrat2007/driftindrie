import math
import pygame
from info import *
from display import teken_pixel

def spawn_stralen(stralen_lijst, x, y, hoek, lengte_lijst, gras_pixels, posities):
    for straal in stralen_lijst:
        positie_opslaan = False
        if isinstance(straal, list):
            lengte_lijst, posities = spawn_stralen(straal, eind_x, eind_y, hoek, lengte_lijst, gras_pixels, posities)
        else:
            if isinstance(straal, str):
                
                straal = int(straal)
                positie_opslaan = True

            straal_object = Straal(x, y, hoek + straal)
            while straal_object.check_pixel(gras_pixels):
                straal_object.zet_stap()
            straal_object.zet_stap_terug()
            
            eind_x, eind_y, lengte = straal_object.geef_informatie()
            if positie_opslaan:
                
                posities.append((eind_x, eind_y))
                
            lengte_lijst.append(lengte)
    return lengte_lijst, posities

class Straal:
    def __init__(self, positie_x, positie_y, richting, max_lengte=MAX_LENGTE_RAYS):
        self.positie_x = positie_x
        self.positie_y = positie_y
        self.richting = richting
        self.stapgroote_x = math.sin(math.radians(self.richting)) * SKIPPING_FACTOR
        self.stapgroote_y = math.cos(math.radians(self.richting)) * SKIPPING_FACTOR

        self.max_lengte = max_lengte
        self.i = 0

    def zet_stap(self):
        self.positie_x += self.stapgroote_x
        self.positie_y += self.stapgroote_y
        
        teken_pixel(self.positie_x, self.positie_y)
        self.i += 1
        
    def zet_stap_terug(self):
        self.positie_x -= self.stapgroote_x
        self.positie_y -= self.stapgroote_y

    def check_pixel(self, gras_pixels):
        if (round(self.positie_x), round(self.positie_y)) in gras_pixels:
            return False
        if self.i > self.max_lengte:
            return False
        return True
        

    def geef_informatie(self):
        return round(self.positie_x), round(self.positie_y), SKIPPING_FACTOR * self.i
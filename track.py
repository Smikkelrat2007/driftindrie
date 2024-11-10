from pathlib import Path

from info import image_extensies, mask_sprijdings_lijst, track_info_deluxe_max_ultra
import random
from collections import deque
from tkinter import Tk, PhotoImage
import os
from display import teken_pixel
pad = Path("/Users/Zeno/School/Coderclass/bullshit/driftindrie/tracks")

def vind_alle_tracks_in_folder():
    bestanden_in_folder = []
    for bestand in pad.rglob("*"):
        if bestand.suffix.lower() in image_extensies:
            bestanden_in_folder.append(bestand.name)
    return bestanden_in_folder

def kies_een_random_track(bestanden_in_folder, track_info):
    import info
    beschikbare_tracks = []
    for key in track_info.keys():
        if key in bestanden_in_folder:
            beschikbare_tracks.append(key)
    return random.choice(beschikbare_tracks)

def gras_pixels_checken(positie_x, positie_y, gras_pixels):
    if (positie_x, positie_y) in gras_pixels:
        return True
    return False

def punten_checken(positie_x, positie_y, punten_dict):
    try:
        return punten_dict[(positie_x, positie_y)]
    except:
        return "error"

def mask_track_positie(x, y, gras_pixels):
    rij = deque([(x,y,0)])
    geweest_set = set([(x,y)])
    geweest_dict = {}
    hoogste_waarde = 0
    if (x, y) in gras_pixels:
        print(f"waarde: {x}, {y} niet op de baan :(")
    while rij:
        x, y, i = rij.popleft()
        hoogste_waarde = max(hoogste_waarde, i)
        if (x, y) in gras_pixels:
            continue
        for dx, dy in mask_sprijdings_lijst:
            nieuw_x, nieuw_y = x+dx, y+dy
            if not (nieuw_x, nieuw_y) in geweest_set:
                if not (nieuw_x, nieuw_y) in gras_pixels:
                    rij.append((nieuw_x, nieuw_y, i+1))
                    geweest_set.add((nieuw_x, nieuw_y))
                    geweest_dict[(nieuw_x, nieuw_y)] = i+1
    return geweest_dict, hoogste_waarde

def zoek_gras_pixels(achtergrond_plaatje):
    root = Tk()
    root.withdraw()

    image_path = os.path.join('tracks', achtergrond_plaatje)
    plaatje = PhotoImage(file=image_path)

    gras_pixels = set()
    for x in range(plaatje.width()):
        for y in range(plaatje.height()):
            
            if plaatje.get(x, y) == (255, 255, 255):
                gras_pixels.add((x, y))

    root.destroy()
    return gras_pixels

def mask_de_track(track_info):
    track = kies_een_random_track(vind_alle_tracks_in_folder(), track_info)
    if track in track_info_deluxe_max_ultra.keys():
        gras_pixels, dict, hoogste_waarde = track_info_deluxe_max_ultra[track]
    else:
        gras_pixels = zoek_gras_pixels(track)
        dict, hoogste_waarde = mask_track_positie(track_info[track][0], track_info[track][1], gras_pixels)
        track_info_deluxe_max_ultra[track] = (gras_pixels, dict, hoogste_waarde)
    return dict, hoogste_waarde, track, gras_pixels
import pygame
scherm_breete = 1200
scherm_hoogte = 800

image_extensies = [".png", ".jpg", ".jpeg"]
# track_info = {"goofyahhtrack.png":[220, 100, 90]}
# "goofyahhtrack.png":[220, 100, 140],"untitled-2.png":[222, 101, 140],"track.png":[400, 300, 90],"track2.png":[200, 100, 90],"lukeenbastrack.png": [630, 574, 210],"zeno.png":[200, 100, 90], "luketrackss.png":[255,205,135], 
#,"goofyahhtrack.png":[220, 100, 140],"untitled-2.png":[222, 101, 140],"track.png":[400, 300, 90],"track2.png":[200, 100, 90],"lukeenbastrack.png": [630, 574, 210],"zeno.png":[200, 100, 90], "luketrackss.png":[255,205,135], 
track_info = {"goofyahhtrack.png":[220, 100, 110], "oval.png":[300,50,90],"sigma_face.png":[268, 163 ,80], "sigma_face_mirror.png":[742, 159, 290], "real_oval.png":[600,113,90], "mirror_real_oval.png":[820,113,270], "scherpere oval.png":[377,200,90]}          
#"
# , "circel.png":[400,65,90]
#track_info = {"untitled.png":[246, 66,90]}
track_info_deluxe_max_ultra = {}

#track_info = {"test.png": [500, 50, 90]}

#track_info = {"goofyahhtrack.png":[220, 100, 140], "untitled-2.png":[222, 101, 140], "lukeenbastrack.png": [630, 574, 270], "untitled.png":[246, 66,90], "oval.png":[300,50,90]}

mask_sprijdings_lijst = [(1, 0), (0, 1), (-1, 0), (0, -1)]
MAX_FPS = 60

SKIPPING_FACTOR = 5

rays_laten_zien = True
RAY_KLEUR = (100, 255, 0)
AUTO_KLEUR = (100,100,100)

MAX_LENGTE_RAYS = 1000

RUNTIMEFRAMES = 60*20

RAY_LIJST = [-110, -90, -35, "0", [-90,[-135, -180], -120, -150, 90,[135, 180], 120, 150], 35, 90, 110, "180"]

VERDER_OP_DE_BAAN_WEIGHT = 1
OVERLEEF_TIJD_WEIGHT = 0
CRASH_PENALTY = 800
GEMIDDELDE_DELTA_V_WEIGHT = 0.0001
LAZERED_PENALTY = 10000000000000

LAAT_ZIEN_TOETS = pygame.K_1
KILL_MYSELF_TOETS = pygame.K_2
SAVE_GENOME_TOETS = pygame.K_0
LOAD_GENOME_TOETS = pygame.K_9
ITS_TIME = pygame.K_6
IT_IS_NOT_TIME = pygame.K_5

AANTAL_GENERATIES = 10000000

LENGTE_RAYS_MULTIPLYER = 0.1

def its_time_for_a_upgrade():
    global track_info
    from ai import track_info
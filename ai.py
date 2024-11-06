import neat
import neat.activations

import pygame
from track import mask_de_track  # Function that sets up the track
import time
from car import *
from display import *
from info import *
import pickle

def save_genome(genome, filename="best_genome.pkl"):
    """Save a NEAT genome to a file."""
    with open(filename, "wb") as f:
        pickle.dump(genome, f)
    print(f"Genome saved to {filename}")

def bereken_fitness(track_progress, time_alive, crashed, lazered):
    VERDER_OP_DE_BAAN_WEIGHT = 1
    OVERLEEF_TIJD_WEIGHT = 0
    CRASH_PENALTY = 1000
    GEMIDDELDE_DELTA_V_WEIGHT = 5
    LAZERED_PENALTY = 10000

    punten = 0
    punten += track_progress * VERDER_OP_DE_BAAN_WEIGHT
    punten += time_alive * OVERLEEF_TIJD_WEIGHT

    if crashed:
        punten -= CRASH_PENALTY
        punten += (track_progress / time_alive) * GEMIDDELDE_DELTA_V_WEIGHT
        
    if lazered:
        punten -= LAZERED_PENALTY
    return punten

def fitness_function(genomes, config):
    global track_info
    dict, hoogste_waarde, achtergrond, gras_pixels = mask_de_track()
    scherm_maken(scherm_breete, scherm_hoogte)

    ais = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        car = maak_ai_auto(track_info[achtergrond][0], track_info[achtergrond][1], track_info[achtergrond][2], RAY_LIJST, 0, net)
        genome.fitness = 0
        ais.append((car, genome))
    simulate(ais, dict, hoogste_waarde, achtergrond, gras_pixels)

def laat_simulatie_zien(achtergrond, autos):
    meeste_punten = 0
    meeste_punten_auto = None

    for auto in autos:
        if not auto.dood:
            auto.kleur = (255, 0, max(min(auto.punten * 0.1, 255), 0))
        if auto.punten > meeste_punten:
            meeste_punten = auto.punten
            meeste_punten_auto = auto
    if meeste_punten_auto:
        meeste_punten_auto.kleur = (255, 255, 0)

    achtergrond_functie(achtergrond)
    teken(autos)
    frame()

def simulate(ais, punten_dict, hoogste_waarde, achtergrond, gras_pixels):
    global track_info
    running = True
    i = 0
    laat_zien_toets = pygame.K_1
    kill_myself_toets = pygame.K_2
    while running:
        i += 1
        keys = pygame.key.get_pressed()

        if keys[laat_zien_toets]:
            autos = [car for car, genome in ais]
            laat_simulatie_zien(achtergrond, autos)

        if keys[kill_myself_toets]:
            running = False
        for car, genome in ais:
            if not car.dood:
                
                lengte_lijst, punten = krijg_ai_info(car, punten_dict, gras_pixels)
                aangepaste_lengte_lijst = []
                for lengte in lengte_lijst:
                    aangepaste_lengte_lijst.append(lengte*0.1)
                aangepaste_lengte_lijst.append(car.snelheid)
                apply_ai_outputs(car, car.neural_net.activate(aangepaste_lengte_lijst))
                zou_ik_nu_fitness_moeten_calculaten = run_ai_auto(car, gras_pixels)
                if zou_ik_nu_fitness_moeten_calculaten:
                    punten = bereken_fitness(car.punten, i, car.dood, False)
                    genome.fitness = round(punten)
                    print("genome.fitness: ", genome.fitness)
                if car.punten > hoogste_waarde - 100:
                    running = False

                if car.punten + 100 < i * 2:
                    car.kleur = (0,255,0)
                    punten = bereken_fitness(car.punten, i, False, True)
                    genome.fitness = round(punten)
                    car.dood = True
                if RUNTIMEFRAMES - i < 0:
                    running = False

        autos = [car for car, genome in ais] # checken of alle mfers dood zijn type shit
        if all(auto.dood for auto in autos):
            running = False

    for car, genome in ais:
        if genome.fitness == 0:
            punten = bereken_fitness(car.punten, i, car.dood, False)
            genome.fitness = round(punten)
            print("genome.fitness: ", genome.fitness)

def init_neat():
    config_path = "neat-config/neat-config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    #population.add_reporter(neat.StatisticsReporter())

    population.run(fitness_function, 10000000)

if __name__ == "__main__":
    init_neat()
    pygame.quit()




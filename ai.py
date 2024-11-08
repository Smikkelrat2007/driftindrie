import neat
import neat.activations
from neat.checkpoint import Checkpointer





import random
import pygame
from track import mask_de_track  # Function that sets up the track
import time
from car import *
from display import *
from info import *
import pickle

import neat
import pickle

class BestGenomeSaver(neat.reporting.BaseReporter):
    def __init__(self, filename="best_genome.pkl"):
        self.filename = filename
        self.best_genome = None
        self.best_fitness = float('-inf')
        self.previous_generations_fitness = 0
    def post_evaluate(self, config, population, species, best_genome):
        if best_genome.fitness > self.best_fitness:
            self.best_genome = best_genome
            self.best_fitness = best_genome.fitness
            print(self.best_fitness)
            save_genome(self.best_genome, self.filename)
        self.previous_generations_fitness = (best_genome.fitness)
    def get_previous_generations_fitness(self):
        return self.previous_generations_fitness
    
def save_genome(genome, filename="best_genome.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(genome, f)
    print(len(f"|Genome saved to: {filename}|") * "-", f"\n|Genome saved to: {filename}|\n", len(f"|Genome saved to: {filename}|") * "-")
    
def load_genome(filename="best_genome.pkl"):
    with open(filename, "rb") as f:
        genome = pickle.load(f)
    print(len(f"|Genome loaded from: {filename}|") * "-", f"\n|Genome loaded from: {filename}|\n", len(f"|Genome loaded from: {filename}|") * "-")
    return genome

def bereken_fitness(track_progress, time_alive, crashed, lazered, hoogste_waarde):
    punten = ((track_progress/10) ** 1.1) * VERDER_OP_DE_BAAN_WEIGHT
    punten += time_alive * OVERLEEF_TIJD_WEIGHT
    if crashed:
        punten -= CRASH_PENALTY
    if lazered:
        punten -= LAZERED_PENALTY
    if not crashed and not lazered:
        punten += ((track_progress / time_alive) ** 5)  * GEMIDDELDE_DELTA_V_WEIGHT * hoogste_waarde
    return round(punten)

def simulatie_prep(genomes, config):
    dict, hoogste_waarde, achtergrond, gras_pixels = mask_de_track()
    scherm_maken(scherm_breete, scherm_hoogte)
    ais = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        car = maak_ai_auto(track_info[achtergrond][0], track_info[achtergrond][1], track_info[achtergrond][2], RAY_LIJST, 0, net)
        genome.fitness = 0
        ais.append((car, genome))
    simulate(ais, dict, hoogste_waarde, achtergrond, gras_pixels)

def simulate(ais, punten_dict, hoogste_waarde, achtergrond, gras_pixels):
    
    running = True
    i = 0
    saver = BestGenomeSaver(filename="best_genome.pkl")
    print(f"gen runned on: {achtergrond}")
    while running:
        i += 1
        running = inputs_kijken(pygame.key.get_pressed(), achtergrond, ais)
        for car, genome in ais:
            if not car.dood:
                lengte_lijst, punten = krijg_ai_info(car, punten_dict, gras_pixels)
                aangepaste_lengte_lijst = []
                for lengte in lengte_lijst:
                    aangepaste_lengte_lijst.append(lengte*0.1)
                aangepaste_lengte_lijst.append(car.snelheid * 5)
                
                
                apply_ai_outputs(car, car.neural_net.activate(aangepaste_lengte_lijst), 1)
                zou_ik_nu_fitness_moeten_calculaten = run_ai_auto(car, gras_pixels)
                if zou_ik_nu_fitness_moeten_calculaten:
                    punten = bereken_fitness(car.punten, i, car.dood, False, hoogste_waarde)
                    genome.fitness = round(punten)

                if car.punten > hoogste_waarde - 500:
                    running = False

                if car.punten + 100 < i * 2:
                    car.kleur = (0,255,0)
                    punten = bereken_fitness(car.punten, i, False, True, hoogste_waarde)
                    genome.fitness = round(punten)
                    car.dood = True
                    
                if (i * 2) - 100 > hoogste_waarde:
                    running = False
    
        autos = [car for car, genome in ais] # checken of alle mfers dood zijn type shit
        if all(auto.dood for auto in autos):
            running = False
    

    for car, genome in ais:
        if genome.fitness == 0:
            punten = bereken_fitness(car.punten, i, car.dood, False, hoogste_waarde)
            genome.fitness = round(punten)

def inputs_kijken(keys, achtergrond, ais):
    if keys[LAAT_ZIEN_TOETS]:
        laat_simulatie_zien(achtergrond, [car for car, genome in ais])

    if keys[KILL_MYSELF_TOETS]:
        return False
    return True

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

def init_neat():
    config_path = "neat-config/neat-config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    population = neat.Population(config)
    population.add_reporter(BestGenomeSaver(filename="best_genome.pkl"))

    winner = population.run(simulatie_prep, 10000000)

if __name__ == "__main__":
    init_neat()
    pygame.quit()




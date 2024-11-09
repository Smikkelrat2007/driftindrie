import neat
import neat.activations
from neat.checkpoint import Checkpointer

import pygame
from track import mask_de_track  # Function that sets up the track
from car import *
from display import *
from info import *
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
    punten = track_progress * VERDER_OP_DE_BAAN_WEIGHT
    punten += time_alive * OVERLEEF_TIJD_WEIGHT
    if crashed:
        punten -= CRASH_PENALTY
    if lazered:
        punten -= LAZERED_PENALTY
    if not crashed and not lazered:
        punten += ((track_progress / time_alive) ** 5)  * GEMIDDELDE_DELTA_V_WEIGHT * hoogste_waarde
    return round(punten)

def simulatie_prep(genomes, config):
    global track_info
    
    dict, hoogste_waarde, achtergrond, gras_pixels = mask_de_track(track_info)
    scherm_maken(scherm_breete, scherm_hoogte)
    ais = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        car = maak_ai_auto(track_info[achtergrond][0], track_info[achtergrond][1], track_info[achtergrond][2], RAY_LIJST, 0, net)
        genome.fitness = 0
        ais.append((car, genome))
    simulate(ais, dict, hoogste_waarde, achtergrond, gras_pixels)

def simulate(ais, punten_dict, hoogste_waarde, achtergrond, gras_pixels):
    global track_info
    
    running = True
    i = 0
    print(f"track: {achtergrond}")
    while running:
        i += 1
        running = inputs_kijken(pygame.key.get_pressed(), achtergrond, ais)
        for car, genome in ais:
            if not car.dood:

                aangepaste_lengte_lijst = [lengte * 0.1 for lengte in krijg_ai_info(car, punten_dict, gras_pixels)[0]] + [car.snelheid]

                apply_ai_outputs(car, car.neural_net.activate(aangepaste_lengte_lijst), 1)
                zou_ik_nu_fitness_moeten_calculaten = run_ai_auto(car, gras_pixels)

                if zou_ik_nu_fitness_moeten_calculaten:
                    genome.fitness = round(bereken_fitness(car.punten, i, car.dood, False, hoogste_waarde))

                if car.punten + 100 < i * 2:
                    car.kleur = (0,255,0)
                    genome.fitness = round(bereken_fitness(car.punten, i, False, True, hoogste_waarde))
                    car.dood = True
                    
                if (i * 2) - 100 > hoogste_waarde or car.punten > hoogste_waarde - 500:
                    running = False
    
        autos = [car for car, genome in ais] # checken of alle mfers dood zijn type shit
        if all(auto.dood for auto in autos):
            running = False
    

    for car, genome in ais:
        if genome.fitness == 0:
            punten = bereken_fitness(car.punten, i, car.dood, False, hoogste_waarde)
            genome.fitness = round(punten)

def inputs_kijken(keys, achtergrond, ais):
    global track_info
    if keys[LAAT_ZIEN_TOETS]:
        laat_simulatie_zien(achtergrond, [car for car, genome in ais])

    if keys[KILL_MYSELF_TOETS]:
        return False
    if keys[ITS_TIME]:
        track_info = {"goofyahhtrack.png":[220, 100, 140], "untitled-2.png":[222, 101, 140], "lukeenbastrack.png": [630, 574, 210], "untitled.png":[246, 66,90]}
        its_time_for_a_upgrade()
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




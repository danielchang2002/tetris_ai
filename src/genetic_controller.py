from os import pardir
import numpy as np
from game import Game
from genetic import Genetic_AI
import random
import pandas as pd


def cross(a1, a2, aggregate="lin"):
    """
    Compute crossover of two agents, returning a new agent
    """
    new_genotype = []
    a1_prop = a1.fit_rel / a2.fit_rel
    for i in range(len(a1.genotype)):
        rand = random.uniform(0, 1)
        if rand > a1_prop:
            new_genotype.append(a1.genotype[i])
        else:
            new_genotype.append(a2.genotype[i])

    return Genetic_AI(genotype=np.array(new_genotype), aggregate=aggregate, mutate=True)


def compute_fitness(agent, num_trials):
    """
    Given an agent and a number of trials, computes fitness as
    arithmetic mean of lines cleared over the trials
    """
    fitness = []
    for _ in range(num_trials):
        game = Game('genetic', agent=agent)
        peices_dropped, rows_cleared = game.run_no_visual()
        fitness.append(peices_dropped)
        print(f"    Trial: {_}/{num_trials}")

    # NOTE: consider dropping outliers for smoother performance
    return np.average(np.array(fitness))



def run_X_epochs(num_epochs=10, num_trials=5, pop_size=100, aggregate='lin', num_elite=5, survival_rate=.35, logging_file='default.csv'):

    # data collection over epochs
    data=[[1, np.ones(9), 1, np.ones(9),  1, np.ones(9)]]
    headers = ['avg_fit','avg_gene', 'top_fit', 'top_gene', 'elite_fit', 'elite_gene']
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(f'data/{logging_file}.csv', index=False)

    # create inital population
    population = [Genetic_AI(aggregate=aggregate) for _ in range(pop_size)]

    for epoch in range(num_epochs):
        """
        Fitness
        """

        # data collection within epochs
        total_fitness = 0
        top_agent = 0
        gene = np.zeros(9)

        for n in range(pop_size):
            # compute fitness, add to total
            print(f"Agent: {n}/{pop_size}")
            agent = population[n]
            agent.fit_score = compute_fitness(agent, num_trials=num_trials)
            total_fitness += agent.fit_score 
            gene+=agent.genotype


        # compute % of fitness accounted for by each agent
        for agent in population:
            agent.fit_rel = agent.fit_score / total_fitness

        """
        Selection
        """

        next_gen = []

        # sort population by descending fitness
        sorted_pop = sorted(population, reverse=True)

        # elite selection: copy over genotypes from top preforming agents
        elite_fit_score = 0
        elite_genes = np.zeros(9)
        top_agent=sorted_pop[0]

        for i in range(num_elite):
            elite_fit_score +=sorted_pop[i].fit_score
            elite_genes += sorted_pop[i].genotype
            next_gen.append(Genetic_AI(genotype=sorted_pop[i].genotype, mutate=False))

        # selection: select top agents as parents base on survival rate
        num_parents = round(pop_size * survival_rate)
        parents = sorted_pop[:num_parents]

        # crossover: randomly select 2 parents and cross genotypes
        for _ in range(pop_size-(num_elite)):
            # randomly select parents, apply crossover, and add to the next generation
            # the cross functions automatically applies mutation to the new agent
            parents = random.sample(parents, 2)
            next_gen.append(cross(parents[0], parents[1], aggregate=aggregate))


        avg_fit = (total_fitness/pop_size)
        avg_gene = (gene/pop_size)
        top_fit = (top_agent.fit_score)
        top_gene = (top_agent.genotype)
        elite_fit = (elite_fit_score/num_elite)
        elite_gene = (elite_genes/num_elite)

        data = [[avg_fit, avg_gene, top_fit, top_gene, elite_fit, elite_gene]]
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(f'data/{logging_file}.csv', mode='a', index=False, header=False)


        print(f'\nEpoch {epoch}: \n    total fitness: {total_fitness/pop_size}\n    best agent: {top_agent.fit_score}\n')

        population = next_gen

    return data


        


if __name__ == '__main__':
    run_X_epochs(num_epochs=15, num_trials=5, pop_size=50, num_elite=5)

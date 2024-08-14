"""
GA Optimization 

This module provides a simple implementation of a Genetic Algorithm (GA) for optimization problems.

@ Author            Reda Ghanem
@ Version           0.1.1
@ Last update       26/04/2024
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #


import numpy as np

class SimpleGA:
    def __init__(self, population_size, gene_length, fitness_function, mutation_rate=0.01, generations=100):
        self.population_size = population_size
        self.gene_length = gene_length
        self.fitness_function = fitness_function  # Custom fitness function
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = np.random.randint(2, size=(population_size, gene_length))

    def select(self):
        # Tournament selection
        selected = []
        for _ in range(self.population_size):
            tournament = np.random.choice(self.population_size, size=3)
            best = max(tournament, key=lambda idx: self.fitness_function(self.population[idx]))
            selected.append(self.population[best])
        return np.array(selected)

    def crossover(self, parent1, parent2):
        point = np.random.randint(1, self.gene_length - 1)
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2

    def mutate(self, individual):
        for i in range(self.gene_length):
            if np.random.rand() < self.mutation_rate:
                individual[i] = 1 - individual[i]

    def run(self):
        for generation in range(self.generations):
            fitness = np.array([self.fitness_function(ind) for ind in self.population])
            print(f'Generation {generation} - Best Fitness: {max(fitness)}')
            
            # Selection
            selected_population = self.select()

            # Crossover
            new_population = []
            for i in range(0, self.population_size, 2):
                parent1, parent2 = selected_population[i], selected_population[i+1]
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(child1)
                new_population.append(child2)
            
            # Mutation
            new_population = np.array(new_population)
            for i in range(self.population_size):
                self.mutate(new_population[i])

            self.population = new_population

# Example usage
# if __name__ == "__main__":
#     # Define a custom fitness function
#     def custom_fitness(individual):
#         return np.sum(individual)  # Example: Sum of all genes

#     ga = SimpleGA(population_size=10, gene_length=5, fitness_function=custom_fitness, mutation_rate=0.01, generations=20)
#     ga.run()

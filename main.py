import random
import matplotlib.pyplot as plt
import networkx as nx


def create_solutions(population_size=2):
    if population_size < 2:
        raise ValueError("Population size must be at least 2.")
    return [[random.choice(COLORS) for x in range(len(NEIGHBOURING_NODES))] for y in range(population_size)]


# Based on dictionary get each individuals colors and search neighbours for similar color. Then update fitness by 1 if colors dont match
def calculate_fitness(population):
    fitness_scores = []
    for individual in population:
        fitness = 0
        for index, color in enumerate(individual):
            neighbours = NEIGHBOURING_NODES[index + 1]
            for neighbour in neighbours:
                if individual[neighbour - 1] != color:
                    fitness += 1
        fitness_scores.append(fitness)
    return fitness_scores


def choose_parents(population, fitness_list):
    roulette = create_roulette(fitness_list)
    parent1 = population[random.choice(roulette)]
    parent2 = population[random.choice(roulette)]
    while parent1 is parent2:  # make sure parents are not the same individual
        parent2 = population[random.choice(roulette)]
    return [parent1, parent2]


# Creates a list with n * fitness enum elements so eg if there are 2 fitnesses with 12 and 20 the list will have 12; 0 elements and 20; 1 elements
def create_roulette(fitness_list):
    roulette = []
    for index, value in enumerate(fitness_list):
        roulette += [index] * value
    return roulette


# Using 1 point crossover (the middle point)
def reproduce(parent1, parent2):
    middle = len(parent1)//2
    child1 = parent1[:middle] + parent2[middle:]
    child2 = parent2[:middle] + parent1[middle:]
    return [child1, child2]


def next_gen(population, mutation_probability=0, elite_count=0):
    fitnesses = calculate_fitness(population)
    best_fit_pos = fitnesses.index(max(fitnesses))
    best_fitness = fitnesses[best_fit_pos] / MAX_FITNESS
    best_sequence = population[best_fit_pos]
    gen_mutations = 0

    sorted_population = [x for _, x in sorted(
        zip(fitnesses, population), reverse=True)]

    # Elitism keep elite_count of best performing individuals from current gen
    next_generation = sorted_population[:elite_count]

    # Fill the rest of the next generation
    while len(next_generation) < len(population):
        parents = choose_parents(population, fitnesses)
        children = reproduce(parents[0], parents[1])
        for child in children:
            if len(next_generation) < len(population):
                next_generation.append(child)

    for individual in next_generation:
        gen_mutations += mutate(individual, mutation_probability)

    return next_generation, best_fitness, best_sequence, gen_mutations


def mutate(individual, mutation_probability=0):
    mutated = False
    for i in range(len(individual)):
        if (random.random() < mutation_probability):
            individual[i] = random.choice(COLORS)
            mutated = True
    return 1 if mutated else 0


def plot_graph(neighbour_nodes, node_colors, title, ax):
    G = nx.Graph()

    for node, neighbours in neighbour_nodes.items():
        for neighbour in neighbours:
            G.add_edge(node, neighbour)
    pos = nx.spring_layout(G, seed=100)
    nx.draw_networkx_nodes(
        G, pos, node_color=[node_colors[node-1] for node in G.nodes()],
        node_size=500, cmap=plt.cm.viridis, ax=ax, edgecolors='black'
    )

    nx.draw_networkx_edges(G, pos, ax=ax, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_color='black')
    ax.set_title(title)
    ax.axis('on')


COLORS = ['r', 'g', 'b', 'y']
NEIGHBOURING_NODES = {
    1: [2, 3, 12], 2: [1, 3, 4, 11, 12], 3: [1, 2, 4, 5, 6, 7],
    4: [2, 3, 7, 9], 5: [3, 6], 6: [3, 5, 7], 7: [3, 4, 6, 8, 9],
    8: [7, 9, 10], 9: [4, 7, 8, 10, 11], 10: [8, 9, 11, 13],
    11: [2, 9, 10, 12, 13], 12: [1, 2, 11, 13], 13: [10, 11, 12]
}

NUMBER_OF_SOLUTIONS = 100
GENERATIONS = 1000
MUTATION_CHANCE = 0.002  # 0.2%
NUMBER_OF_ELITES = max(1, NUMBER_OF_SOLUTIONS // 100) # 1% of the population with the best stats(fitness) move on as elites, or at least 1
MAX_FITNESS = sum(len(values) for values in NEIGHBOURING_NODES.values()) # The max fitness is the maximum achievable fitness when all neighbours have different colors

population = create_solutions(NUMBER_OF_SOLUTIONS)
for g in range(GENERATIONS):
    population, best_current_fitness, best_current_sequence, current_mutations = next_gen(population, MUTATION_CHANCE, NUMBER_OF_ELITES)
    # Keep the first gen sequence for plotting later
    if g == 0:
        first_gen = best_current_sequence
    print(f"Generation: {g} | Mutations: {current_mutations} / {len(population)} | Current fitness: {format(best_current_fitness, '.3f')} | Solution: {population[1]}")

# Plotting the graph
fig, ax = plt.subplots(1, 2, figsize=(14, 7))
plot_graph(NEIGHBOURING_NODES, first_gen, "Start Generation", ax[0])
plot_graph(NEIGHBOURING_NODES, best_current_sequence, "End Generation", ax[1])
plt.show()

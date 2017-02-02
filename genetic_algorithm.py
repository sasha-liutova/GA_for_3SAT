import random
import copy
import matplotlib.pyplot as plt


def run_and_set_bonuses(instance, n_individuals, n_iterations, crossover_probability, mutation_probability, satisfied_clause_bonus, satisfied_formula_bonus):
    """
    runs genetic algorithm with certain values of bonuses
    :return: solution. None if no solution found.
    """
    n_var, n_clauses, clauses, weights = instance['n_var'], instance['n_clauses'], instance['clauses'], instance[
        'weights']

    population = inicialize_population(n_individuals=n_individuals, individual_size=n_var)
    for iteration in range(n_iterations):
        population = selection_by_tournament(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus)
        population = crossover_population(population, crossover_probability)
        population = mutation_population(population, mutation_probability)

    solution = get_best_individual(population, weights, clauses)
    return solution


def run(instance, n_individuals, n_iterations, crossover_probability, mutation_probability):
    """
    runs genetic algorithm for input instance of problem
    :return: solution. None if no solution found.
    """
    n_var, n_clauses, clauses, weights = instance['n_var'], instance['n_clauses'], instance['clauses'], instance['weights']
    satisfied_clause_bonus, satisfied_formula_bonus = 500, 1100

    population = inicialize_population(n_individuals=n_individuals, individual_size=n_var)
    # statistics = [get_statistics(population, weights, clauses, n_clauses)]
    for iteration in range(n_iterations):
        population = selection_by_tournament(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus)
        population = crossover_population(population, crossover_probability)
        population = mutation_population(population, mutation_probability)

        # optional for investigation
        # current_statistics = get_statistics(population, weights, clauses, n_clauses)
        # statistics.append(current_statistics)

    # optional
    # plot_statistics(statistics)

    solution = get_best_individual(population, weights, clauses)
    return solution


def get_statistics(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus):
    """
    returns statistics: min, max and avg fitness for input population
    """
    fitnesses = [fitness(individual, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus) for individual in population]
    return {'min': min(fitnesses), 'max': max(fitnesses), 'avg': sum(fitnesses) / float(len(fitnesses))}


def plot_statistics(statistics):
    """
    plots input statistics
    """

    values_max = [x['max'] for x in statistics]
    values_min = [x['min'] for x in statistics]

    maximum = max(values_max)
    minimum = min(values_min)
    step = (maximum-minimum)/5

    counter = 0
    for item in statistics:
        plt.scatter(counter, item['max'], color='green', s=2)
        plt.scatter(counter, item['min'], color='red', s=2)
        plt.scatter(counter, item['avg'], color='yellow', s=2)
        counter += 1

    plt.ylim(minimum-step, maximum+step)

    plt.xlabel('# population')
    plt.ylabel('optimization criterion')
    plt.show()


def get_weights_sum(individual, weights):
    """
    return sum of weights of variables set to True for input individual
    """
    index, fitness = 0, 0

    for i in individual:
        if i == 1:
            fitness += weights[index]
        index += 1

    return fitness


def is_valid(individual, clauses):
    """
    returns True if formula with given evaluation is satisfied. Otherwise returns False
    """
    for clause in clauses:
        satisfied = False
        for var in clause:
            negation = False
            if var < 0:
                negation = True
                var *= (-1)
            index = var - 1
            value = individual[index]
            if (value == 1 and not negation) or (value == 0 and negation):
                satisfied = True
        if not satisfied:
            return False

    return True


def get_best_individual(population, weights, clauses):
    """
    returns best (valid and with highest sum of weights) individual from population
    """
    valid_individuals = []
    for individual in population:
        if is_valid(individual, clauses):
            valid_individuals.append(individual)
    if len(valid_individuals) == 0:
        return None
    weights_sums = [get_weights_sum(valid_individual, weights) for valid_individual in valid_individuals]
    best_sum = max(weights_sums)
    index = weights_sums.index(best_sum)
    best_individual = valid_individuals[index]
    return {'individual': best_individual, 'weights_sum': best_sum}


def flip(n):
    if n == 0:
        return 1
    else:
        return 0


def mutation_individual(individual):
    """
    returns mutated individual
    """
    index = random.randint(0, len(individual) - 1)
    individual_new = copy.deepcopy(individual)
    individual_new[index] = flip(individual_new[index])
    return individual_new


def mutation_population(population, probability):
    """
    returns population with performed mutation
    """
    for index in range(len(population)):
        number = random.random()
        if number < probability:
            population[index] = mutation_individual(population[index])
    return population


def uniform_crossover_pair(individual1, individual2):
    """
    for 2 input individuals performs uniform crossover and returns new pair
    """
    individual1_new, individual2_new = [], []
    for i in range(len(individual1)):
        check = random.randint(0,1)
        if check == 1:
            individual1_new.append(individual2[i])
            individual2_new.append(individual1[i])
        else:
            individual1_new.append(individual1[i])
            individual2_new.append(individual2[i])
    return [individual1_new, individual2_new]


def crossover_pair(individual1, individual2):
    """
    for 2 input individuals performs one point crossover and returns new pair
    """
    point = random.randint(0,len(individual1)-1)
    individual1_new = individual1[:point] + individual2[point:]
    individual2_new = individual2[:point] + individual1[point:]
    return [individual1_new, individual2_new]


def crossover_population(population, probability):
    """
    returns population with performed crossover
    """
    population_new = []
    for i in range(int(len(population)/2)):
        number = random.random()
        if number < probability:
            population_new.extend(crossover_pair(population[2*i], population[2*i+1]))
        else:
            population_new.extend([population[2*i], population[2*i + 1]])
    if len(population_new) < len(population):
        population_new.append(population[-1])
    return population_new


def selection(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus):
    """
    returns new selected population, using roulette selection and linear scaling
    """

    # calculating fitness function for each individual, now with linear scaling
    fitnesses = linear_scaling(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus)

    # generating roulette based on fitness values
    roulette, index = [], 0
    for f in fitnesses:
        for i in range(f):
            roulette.append(index)
        index += 1

    # selecting individuals
    population_new = []
    for i in range(len(population)):
        value = random.randint(0, len(roulette) - 1)
        number_of_individual = roulette[value]
        individual = population[number_of_individual]
        population_new.append(individual)

    return population_new


def selection_by_tournament(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus):
    """
    returns new selected population, using tournament selection and linear scaling
    """

    # calculating fitness function for each individual, now with linear scaling
    fitnesses = linear_scaling(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus)

    # selecting individuals
    population_new = []
    for i in range(len(population)):
        tournament = []
        for j in range(int(len(population)/5)):
            index = random.randint(0, len(population) - 1)
            tournament.append(index)
        max_fitness = max([fitnesses[index] for index in tournament])
        best_index = fitnesses.index(max_fitness)
        population_new.append(population[best_index])

    return population_new


def linear_scaling(population, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus):
    """
    for given population returns list of fitness function values, linearly scaled
    """
    fitnesses = [fitness(individual, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus) for
                 individual in population]
    z_max, z_min = max(fitnesses), min(fitnesses)
    if z_min == z_max:
        return [1 for x in range(len(population))]
    z1, z2 = 100, 200
    fitnesses_new = []
    for z in fitnesses:
        z_new = int(z1 + (z - z_min)*(z2 - z1)/(z_max - z_min))
        fitnesses_new.append(z_new)
    return fitnesses_new


def fitness(individual, weights, clauses, n_clauses, satisfied_clause_bonus, satisfied_formula_bonus):
    """
    calculates fitness function of individual
    """
    index, fitness = 0, 0

    for i in individual:
        if i==1:
            fitness += weights[index]
        index += 1

    satisfied_clauses = 0
    for clause in clauses:
        satisfied = False
        for var in clause:
            negation = False
            if var < 0:
                negation = True
                var *= (-1)
            index = var - 1
            value = individual[index]
            if (value == 1 and not negation) or (value == 0 and negation):
                satisfied = True
        if satisfied:
            satisfied_clauses += 1

    fitness += satisfied_clauses*satisfied_clause_bonus
    if satisfied_clauses == n_clauses:
        fitness += satisfied_formula_bonus

    return fitness


def inicialize_population(n_individuals, individual_size):
    """
    returns randomly filled n individuals
    """
    population = []
    while len(population) < n_individuals:
        individual = []
        for j in range(individual_size):
            individual.append(random.getrandbits(1))
        population.append(individual)
    return population



# if __name__ == "__main__":
#     import instance_generator
#     instance = instance_generator.generate_instance(3, 10)
#     print(instance)
#     solution = run(instance, 50, 500, 0.7, 0.06)
#     print(solution)
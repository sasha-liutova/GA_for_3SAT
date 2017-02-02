import os
import genetic_algorithm
from time import time

def load_instance(filename):
    """
    loads data from file and processes it into a problem instance accepted by GA
    :param filename: filename
    :return: a dictionary, which represents an instance of problem
    """
    if not os.path.exists(filename):
        print('Invalid input: file ', filename, ' does not exist.')
        return
    with open(filename, mode='r', encoding='utf-8') as a_file:
        content = a_file.read()
        clauses_str = content.split(' 0 ')
        weights_str = clauses_str[-1].replace('%', '').replace('#', '')
        del clauses_str[-1]
        nums_str = clauses_str[0]
        del clauses_str[0]
        weights = [int(x) for x in weights_str.rstrip().split(' ') if x!= '']
        clauses = [[int(x) for x in clause.replace('%', '').replace('#', '').split(' ') if x!= ''] for clause in clauses_str]
        nums = [int(x) for x in nums_str.rstrip().split(' ') if x!= '']
        n_var, n_clauses = nums[0], nums[1]
        return {'n_var': n_var, 'n_clauses': n_clauses, 'clauses': clauses, 'weights': weights}


def solve_from_file(filename, n_individuals, n_iterations, crossover_probability, mutation_probability):
    """
    get solution of problem from file
    :param filename: filename
    :param n_individuals: number of individuals for GA
    :param n_iterations: number of iterations for GA
    :param crossover_probability: crossover probability for GA
    :param mutation_probability: mutation probability for GA
    :return:
    """
    instance = load_instance(filename)
    if instance is not None:
        solution = genetic_algorithm.run(instance, n_individuals, n_iterations, crossover_probability, mutation_probability)
    else:
        solution = None
    return solution


def solve_from_file_with_bonuses(filename, n_individuals, n_iterations, crossover_probability, mutation_probability, satisfied_clause_bonus, satisfied_formula_bonus):
    """
    get solution of problem from file with certain values of bonuses
    :param filename: filename
    :param n_individuals: number of individuals for GA
    :param n_iterations: number of iterations for GA
    :param crossover_probability: crossover probability for GA
    :param mutation_probability: mutation probability for GA
    :param satisfied_clause_bonus: bonus for satisfied clause
    :param satisfied_formula_bonus: bonus for satisfied formula
    :return:
    """
    instance = load_instance(filename)
    if instance is not None:
        solution = genetic_algorithm.run_and_set_bonuses(instance, n_individuals, n_iterations, crossover_probability, mutation_probability, satisfied_clause_bonus, satisfied_formula_bonus)
    else:
        solution = None
    return solution


def measure_time(filenames_all, n_individuals, n_iterations, crossover_probability, mutation_probability):
    """
    measures runtime for solving instances of different sizes
    :param filenames_all: structured array of sizes of instances and filenames
    :param n_individuals: number of individuals for GA
    :param n_iterations: number of iterations for GA
    :param crossover_probability: crossover probability for GA
    :param mutation_probability: mutation probability for GA
    :return: structured array with sizes of instances (number of clauses in formula) and corresponding runtime
    """
    time_array=[]
    for pair in filenames_all:
        n, filenames = pair[0], pair[1]
        execution_time = 0
        for filename in filenames:
            t0 = time()
            # for i in range(100):
            solution = solve_from_file(filename, n_individuals, n_iterations, crossover_probability, mutation_probability)
            # execution_time=(time() - t0)/100
            execution_time += (time() - t0)/len(filenames)
        print(n, ": ", execution_time, "s")
        time_array.append((n, execution_time))

    print(time_array)
    return time_array


def set_parameters(filenames, n_individuals, n_iterations, crossover_probability, mutation_probability):
    """
    calculates performance of algorithm for different values of parameters
    :param filenames: list of filenames
    :param n_individuals: number of individuals for GA
    :param n_iterations: number of iterations for GA
    :param crossover_probability: crossover probability for GA
    :param mutation_probability: mutation probability for GA
    :return: array of parameters values and corresponding performance (solved instances ratio)
    """
    result = []
    for p in [30, 40, 50, 60, 70, 80, 90, 100]:
        n_solutions = 0
        for filename in filenames:
            solution = solve_from_file(filename=filename, n_individuals=n_individuals, n_iterations=n_iterations,
                                       crossover_probability=crossover_probability, mutation_probability=mutation_probability)
            if solution is not None:
                n_solutions += 1
        print([p, n_solutions/len(filenames)])
        result.append([p, n_solutions/len(filenames)])
    print(result)


def set_bonuses(filenames, n_individuals, n_iterations, crossover_probability, mutation_probability):
    """
    for different values of bonuses calculate performance
    :param filenames: list of filenames
    :param n_individuals: number of individuals for GA
    :param n_iterations: number of iterations for GA
    :param crossover_probability: crossover probability for GA
    :param mutation_probability: mutation probability for GA
    :return: array of values of bonuses and corresponding performance (solved instances ratio)
    """
    result = []
    for clause_bonus in [100 * x for x in range(1, 10)]:
        for formula_bonus in range(clause_bonus + 600, clause_bonus + 1000, 100):
            n_solutions = 0
            for filename in filenames:
                solution = solve_from_file_with_bonuses(filename, n_individuals, n_iterations, crossover_probability,
                                                        mutation_probability, clause_bonus, formula_bonus)
                if solution is not None:
                    n_solutions += 1
            print([clause_bonus, formula_bonus, n_solutions / len(filenames)])
            result.append([clause_bonus, formula_bonus, n_solutions / len(filenames)])
    print(result)


def meassure_performance(filenames_all, n_individuals, n_iterations, crossover_probability, mutation_probability):
    """
    calculates for how many instances algorithm finds solution
    :param filenames_all: structured array of sizes of instances and filenames
    :param n_individuals: number of individuals for GA
    :param n_iterations: number of iterations for GA
    :param crossover_probability: crossover probability for GA
    :param mutation_probability: mutation probability for GA
    :return: array of sizes of instances and corresponding performance (solved instances ratio)
    """
    time_array=[]
    for pair in filenames_all:
        n_solutions = 0
        for i in range(10):
            n, filenames = pair[0], pair[1]
            for filename in filenames:
                solution = solve_from_file(filename, n_individuals, n_iterations, crossover_probability, mutation_probability)
                if solution is not None:
                    n_solutions += 1

        print(n, ": ", n_solutions/len(filenames)/10)
        time_array.append((n, n_solutions/len(filenames)/10))

    print(time_array)
    return time_array


if __name__ == "__main__":
    n_individuals = 50
    n_iterations = 500
    crossover_probability = 0.7
    mutation_probability = 0.06
    filenames = ['./instances/3_SAT_50_4.5_0.txt', './instances/3_SAT_50_4.5_1.txt', './instances/3_SAT_50_4.5_2.txt',
                 './instances/3_SAT_50_4.5_3.txt', './instances/3_SAT_50_4.5_4.txt', './instances/3_SAT_50_4.5_5.txt',
                 './instances/3_SAT_50_4.5_6.txt', './instances/3_SAT_50_4.5_7.txt', './instances/3_SAT_50_4.5_8.txt',
                 './instances/3_SAT_50_4.5_9.txt', './instances/3_SAT_50_4.5_10.txt', './instances/3_SAT_50_4.5_11.txt',
                 './instances/3_SAT_50_4.5_12.txt', './instances/3_SAT_50_4.5_13.txt', './instances/3_SAT_50_4.5_14.txt',
                 './instances/3_SAT_50_4.5_15.txt', './instances/3_SAT_50_4.5_16.txt', './instances/3_SAT_50_4.5_17.txt',
                 './instances/3_SAT_50_4.5_18.txt', './instances/3_SAT_50_4.5_19.txt', './instances/3_SAT_50_4.5_20.txt',
                 './instances/3_SAT_50_4.5_21.txt', './instances/3_SAT_50_4.5_22.txt', './instances/3_SAT_50_4.5_23.txt',
                 './instances/3_SAT_50_4.5_24.txt', './instances/3_SAT_50_4.5_25.txt', './instances/3_SAT_50_4.5_26.txt',
                 './instances/3_SAT_50_4.5_27.txt', './instances/3_SAT_50_4.5_28.txt', './instances/3_SAT_50_4.5_29.txt',
                 './instances/3_SAT_50_4.5_30.txt', './instances/3_SAT_50_4.5_31.txt', './instances/3_SAT_50_4.5_32.txt',
                 './instances/3_SAT_50_4.5_33.txt', './instances/3_SAT_50_4.5_34.txt', './instances/3_SAT_50_4.5_35.txt',
                 './instances/3_SAT_50_4.5_36.txt', './instances/3_SAT_50_4.5_37.txt', './instances/3_SAT_50_4.5_38.txt',
                 './instances/3_SAT_50_4.5_39.txt', './instances/3_SAT_50_4.5_40.txt', './instances/3_SAT_50_4.5_41.txt',
                 './instances/3_SAT_50_4.5_42.txt', './instances/3_SAT_50_4.5_43.txt', './instances/3_SAT_50_4.5_44.txt',
                 './instances/3_SAT_50_4.5_45.txt', './instances/3_SAT_50_4.5_46.txt', './instances/3_SAT_50_4.5_47.txt',
                 './instances/3_SAT_50_4.5_48.txt', './instances/3_SAT_50_4.5_49.txt']
    filenames_all = [ (30, ['./instances/3_SAT_30_4.5_0.txt', './instances/3_SAT_30_4.5_1.txt', './instances/3_SAT_30_4.5_2.txt', './instances/3_SAT_30_4.5_3.txt', './instances/3_SAT_30_4.5_4.txt', './instances/3_SAT_30_4.5_5.txt', './instances/3_SAT_30_4.5_6.txt', './instances/3_SAT_30_4.5_7.txt', './instances/3_SAT_30_4.5_8.txt', './instances/3_SAT_30_4.5_9.txt', './instances/3_SAT_30_4.5_10.txt', './instances/3_SAT_30_4.5_11.txt', './instances/3_SAT_30_4.5_12.txt', './instances/3_SAT_30_4.5_13.txt', './instances/3_SAT_30_4.5_14.txt', './instances/3_SAT_30_4.5_15.txt', './instances/3_SAT_30_4.5_16.txt', './instances/3_SAT_30_4.5_17.txt', './instances/3_SAT_30_4.5_18.txt', './instances/3_SAT_30_4.5_19.txt', './instances/3_SAT_30_4.5_20.txt', './instances/3_SAT_30_4.5_21.txt', './instances/3_SAT_30_4.5_22.txt', './instances/3_SAT_30_4.5_23.txt', './instances/3_SAT_30_4.5_24.txt', './instances/3_SAT_30_4.5_25.txt', './instances/3_SAT_30_4.5_26.txt', './instances/3_SAT_30_4.5_27.txt', './instances/3_SAT_30_4.5_28.txt', './instances/3_SAT_30_4.5_29.txt']),
                      (40, ['./instances/3_SAT_40_4.5_0.txt', './instances/3_SAT_40_4.5_1.txt', './instances/3_SAT_40_4.5_2.txt', './instances/3_SAT_40_4.5_3.txt', './instances/3_SAT_40_4.5_4.txt', './instances/3_SAT_40_4.5_5.txt', './instances/3_SAT_40_4.5_6.txt', './instances/3_SAT_40_4.5_7.txt', './instances/3_SAT_40_4.5_8.txt', './instances/3_SAT_40_4.5_9.txt', './instances/3_SAT_40_4.5_10.txt', './instances/3_SAT_40_4.5_11.txt', './instances/3_SAT_40_4.5_12.txt', './instances/3_SAT_40_4.5_13.txt', './instances/3_SAT_40_4.5_14.txt', './instances/3_SAT_40_4.5_15.txt', './instances/3_SAT_40_4.5_16.txt', './instances/3_SAT_40_4.5_17.txt', './instances/3_SAT_40_4.5_18.txt', './instances/3_SAT_40_4.5_19.txt', './instances/3_SAT_40_4.5_20.txt', './instances/3_SAT_40_4.5_21.txt', './instances/3_SAT_40_4.5_22.txt', './instances/3_SAT_40_4.5_23.txt', './instances/3_SAT_40_4.5_24.txt', './instances/3_SAT_40_4.5_25.txt', './instances/3_SAT_40_4.5_26.txt', './instances/3_SAT_40_4.5_27.txt', './instances/3_SAT_40_4.5_28.txt', './instances/3_SAT_40_4.5_29.txt']),
                      (50, ['./instances/3_SAT_50_4.5_0.txt', './instances/3_SAT_50_4.5_1.txt', './instances/3_SAT_50_4.5_2.txt', './instances/3_SAT_50_4.5_3.txt', './instances/3_SAT_50_4.5_4.txt', './instances/3_SAT_50_4.5_5.txt', './instances/3_SAT_50_4.5_6.txt', './instances/3_SAT_50_4.5_7.txt', './instances/3_SAT_50_4.5_8.txt', './instances/3_SAT_50_4.5_9.txt', './instances/3_SAT_50_4.5_10.txt', './instances/3_SAT_50_4.5_11.txt', './instances/3_SAT_50_4.5_12.txt', './instances/3_SAT_50_4.5_13.txt', './instances/3_SAT_50_4.5_14.txt', './instances/3_SAT_50_4.5_15.txt', './instances/3_SAT_50_4.5_16.txt', './instances/3_SAT_50_4.5_17.txt', './instances/3_SAT_50_4.5_18.txt', './instances/3_SAT_50_4.5_19.txt', './instances/3_SAT_50_4.5_20.txt', './instances/3_SAT_50_4.5_21.txt', './instances/3_SAT_50_4.5_22.txt', './instances/3_SAT_50_4.5_23.txt', './instances/3_SAT_50_4.5_24.txt', './instances/3_SAT_50_4.5_25.txt', './instances/3_SAT_50_4.5_26.txt', './instances/3_SAT_50_4.5_27.txt', './instances/3_SAT_50_4.5_28.txt', './instances/3_SAT_50_4.5_29.txt']),
                      (60, ['./instances/3_SAT_60_4.5_0.txt', './instances/3_SAT_60_4.5_1.txt', './instances/3_SAT_60_4.5_2.txt', './instances/3_SAT_60_4.5_3.txt', './instances/3_SAT_60_4.5_4.txt', './instances/3_SAT_60_4.5_5.txt', './instances/3_SAT_60_4.5_6.txt', './instances/3_SAT_60_4.5_7.txt', './instances/3_SAT_60_4.5_8.txt', './instances/3_SAT_60_4.5_9.txt', './instances/3_SAT_60_4.5_10.txt', './instances/3_SAT_60_4.5_11.txt', './instances/3_SAT_60_4.5_12.txt', './instances/3_SAT_60_4.5_13.txt', './instances/3_SAT_60_4.5_14.txt', './instances/3_SAT_60_4.5_15.txt', './instances/3_SAT_60_4.5_16.txt', './instances/3_SAT_60_4.5_17.txt', './instances/3_SAT_60_4.5_18.txt', './instances/3_SAT_60_4.5_19.txt', './instances/3_SAT_60_4.5_20.txt', './instances/3_SAT_60_4.5_21.txt', './instances/3_SAT_60_4.5_22.txt', './instances/3_SAT_60_4.5_23.txt', './instances/3_SAT_60_4.5_24.txt', './instances/3_SAT_60_4.5_25.txt', './instances/3_SAT_60_4.5_26.txt', './instances/3_SAT_60_4.5_27.txt', './instances/3_SAT_60_4.5_28.txt', './instances/3_SAT_60_4.5_29.txt']),
                      (70, ['./instances/3_SAT_70_4.5_0.txt', './instances/3_SAT_70_4.5_1.txt', './instances/3_SAT_70_4.5_2.txt', './instances/3_SAT_70_4.5_3.txt', './instances/3_SAT_70_4.5_4.txt', './instances/3_SAT_70_4.5_5.txt', './instances/3_SAT_70_4.5_6.txt', './instances/3_SAT_70_4.5_7.txt', './instances/3_SAT_70_4.5_8.txt', './instances/3_SAT_70_4.5_9.txt', './instances/3_SAT_70_4.5_10.txt', './instances/3_SAT_70_4.5_11.txt', './instances/3_SAT_70_4.5_12.txt', './instances/3_SAT_70_4.5_13.txt', './instances/3_SAT_70_4.5_14.txt', './instances/3_SAT_70_4.5_15.txt', './instances/3_SAT_70_4.5_16.txt', './instances/3_SAT_70_4.5_17.txt', './instances/3_SAT_70_4.5_18.txt', './instances/3_SAT_70_4.5_19.txt', './instances/3_SAT_70_4.5_20.txt', './instances/3_SAT_70_4.5_21.txt', './instances/3_SAT_70_4.5_22.txt', './instances/3_SAT_70_4.5_23.txt', './instances/3_SAT_70_4.5_24.txt', './instances/3_SAT_70_4.5_25.txt', './instances/3_SAT_70_4.5_26.txt', './instances/3_SAT_70_4.5_27.txt', './instances/3_SAT_70_4.5_28.txt', './instances/3_SAT_70_4.5_29.txt'])]

    results_per_crossover_prob = [[0.1, 0.22], [0.2, 0.18], [0.3, 0.18], [0.4, 0.2], [0.5, 0.2], [0.6, 0.22],
                                  [0.7, 0.24], [0.8, 0.2], [0.9, 0.2]]
    results_per_mutation_prob = [[0.0, 0.167], [0.02, 0.3], [0.04, 0.2], [0.06, 0.3], [0.08, 0.3], [0.1, 0.1],
                                 [0.12, 0.267], [0.14, 0.1], [0.16, 0.167], [0.18, 0.167]]
    results_per_iteration_size = [[300, 0.2], [400, 0.267], [500, 0.3], [600, 0.33]]
    results_per_population_size = [[30, 0.2], [40, 0.267], [50, 0.33], [60, 0.233], [70, 0.433],
                                   [80, 0.433], [90, 0.367], [100, 0.4]]
    times = [(30, 15.570753757158917), (40, 22.641078138351443), (50, 28.278427457809446), (60, 32.22328717708587), (70, 37.51513407230377)]
    performance_per_instances_sizes = [(30, 0.5333333333333333), (40, 0.26666666666666666), (50, 0.4), (60, 0.3), (70, 0.06666666666666667)]
    performance_per_instances_sizes_with_uniform_crossover = [(30, 0.5), (40, 0.3), (50, 0.2), (60, 0.16666666666666666), (70, 0.03333333333333333)]
    performance_per_instances_sizes_with_tournament_selection = [(30, 0.5333333333333333), (40, 0.3), (50, 0.4), (60, 0.4), (70, 0.26666666666666666)]
    performance_per_instances_sizes_with_linear_scaling = [(30, 0.5333333333333333), (40, 0.3), (50, 0.43333333333333335), (60, 0.5333333333333333), (70, 0.3)]
    performance_per_instances_sizes_with_tournament_selection_and_linear_scaling = [(30, 0.4666666666666667), (40, 0.3333333333333333), (50, 0.5), (60, 0.5), (70, 0.3)]
    performance_per_bonuses = [[100, 200, 0.3], [100, 300, 0.25], [100, 400, 0.3], [100, 500, 0.325], [100, 600, 0.25], [200, 300, 0.3], [200, 400, 0.325], [200, 500, 0.375], [200, 600, 0.4], [200, 700, 0.3], [300, 400, 0.425], [300, 500, 0.3], [300, 600, 0.35], [300, 700, 0.375], [300, 800, 0.375], [400, 500, 0.375], [400, 600, 0.425], [400, 700, 0.375], [400, 800, 0.425], [400, 900, 0.375]]
    performance_final = [(30, 0.4966666666666667), (40, 0.2866666666666667), (50, 0.37333333333333335), (60, 0.38666666666666666), (70, 0.22999999999999998)]



    # measure_time(filenames_all, n_individuals, n_iterations, crossover_probability, mutation_probability)

    # for filename in filenames:
    #     solution = solve_from_file(filename=filename, n_individuals=n_individuals, n_iterations=n_iterations,
    #                                crossover_probability=crossover_probability,
    #                                mutation_probability=mutation_probability)
    #     print(filename, solution)

    # set_bonuses(filenames, n_individuals, n_iterations, crossover_probability, mutation_probability)

    meassure_performance(filenames_all, n_individuals, n_iterations, crossover_probability, mutation_probability)
import matplotlib.pyplot as plt


def plot_time(time_list):
    """
    plots list of times
    :param time_list: data
    """
    maximum = max([x[1] for x in time_list])
    minimum = min([x[1] for x in time_list])
    step = (maximum-minimum)/5

    for pair in time_list:
        n, time = pair[0], pair[1]
        plt.scatter(n, time)

    plt.ylim(minimum-step, maximum+step)

    plt.xlabel('Number of clauses (clauses to variables ratio is 4.5)')
    plt.ylabel('time [s]')
    plt.show()


def plot_any(data, label_x, label_y):
    """
    plots any list of 2-dimensional data
    :param data:
    :param label_x: label for x axes
    :param label_y: label for y axes
    """
    maximum = max([x[1] for x in data])
    minimum = min([x[1] for x in data])
    step = (maximum-minimum)/5

    for pair in data:
        x, y = pair[0], pair[1]
        plt.scatter(x, y)

    plt.ylim(minimum-step, maximum+step)

    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()


def plot_comparison(data1, data2, label_x, label_y):
    """
    plots 2 sets of data in different colors for comparison
    :param data1: 1st set of data
    :param data2: 2nd set of data
    :param label_x: label for x axes
    :param label_y: label for y axes
    """
    maximum = max(max([x[1] for x in data1]), max([x[1] for x in data2]))
    minimum = min(min([x[1] for x in data1]), min([x[1] for x in data2]))
    step = (maximum-minimum)/5

    for pair in data1:
        x, y = pair[0], pair[1]
        plt.scatter(x, y, color='blue')

    for pair in data2:
        x, y = pair[0], pair[1]
        plt.scatter(x, y, color='red')

    plt.ylim(minimum-step, maximum+step)

    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()


if __name__ == "__main__":
    results_per_crossover_prob = [[0.1, 0.2], [0.2, 0.18], [0.3, 0.18], [0.4, 0.2], [0.5, 0.2], [0.6, 0.22],
                                  [0.7, 0.24], [0.8, 0.2], [0.9, 0.2]]
    results_per_mutation_prob = [[0.0, 0.167], [0.02, 0.3], [0.04, 0.2], [0.06, 0.3], [0.08, 0.3], [0.1, 0.1],
                                 [0.12, 0.267], [0.14, 0.1], [0.16, 0.167], [0.18, 0.167]]
    results_per_iteration_size = [[300, 0.2], [400, 0.267], [500, 0.3], [600, 0.33]]
    results_per_population_size = [[30, 0.2], [40, 0.267], [50, 0.33], [60, 0.3], [70, 0.433],
                                   [80, 0.433], [90, 0.367], [100, 0.4]]
    times = [(30, 15.570753757158917), (40, 22.641078138351443), (50, 28.278427457809446), (60, 32.22328717708587),
             (70, 37.51513407230377)]
    performance_per_instances_sizes = [(30, 0.5333333333333333), (40, 0.26666666666666666), (50, 0.4), (60, 0.3),
                                       (70, 0.06666666666666667)]
    performance_per_instances_sizes_with_uniform_crossover = [(30, 0.5), (40, 0.3), (50, 0.2),
                                                              (60, 0.16666666666666666), (70, 0.03333333333333333)]
    performance_per_instances_sizes_with_tournament_selection = [(30, 0.5333333333333333), (40, 0.3), (50, 0.4),
                                                                 (60, 0.4), (70, 0.26666666666666666)]
    performance_per_instances_sizes_with_linear_scaling = [(30, 0.5333333333333333), (40, 0.3),
                                                           (50, 0.43333333333333335), (60, 0.5333333333333333),
                                                           (70, 0.3)]
    performance_per_instances_sizes_with_tournament_selection_and_linear_scaling = [(30, 0.4666666666666667),
                                                                                    (40, 0.3333333333333333), (50, 0.5),
                                                                                    (60, 0.5), (70, 0.3)]
    performance_per_bonuses = [[100, 200, 0.3], [100, 300, 0.25], [100, 400, 0.3], [100, 500, 0.325], [100, 600, 0.25],
                               [200, 300, 0.3], [200, 400, 0.325], [200, 500, 0.375], [200, 600, 0.4], [200, 700, 0.3],
                               [300, 400, 0.425], [300, 500, 0.3], [300, 600, 0.35], [300, 700, 0.375],
                               [300, 800, 0.375], [400, 500, 0.375], [400, 600, 0.425], [400, 700, 0.375],
                               [400, 800, 0.425], [400, 900, 0.375]]
    performance_final = [(30, 0.4966666666666667), (40, 0.2866666666666667), (50, 0.37333333333333335),
                         (60, 0.38666666666666666), (70, 0.22999999999999998)]


    # plot_any(results_per_crossover_prob, 'Crossover probability', 'Ratio of solved instances')
    # plot_any(results_per_mutation_prob, 'Mutation probability', 'Ratio of solved instances')
    # plot_any(results_per_iteration_size, 'Number of iterations', 'Ratio of solved instances')
    # plot_any(results_per_population_size, 'Population size', 'Ratio of solved instances')
    # plot_any(performance_per_instances_sizes, 'Number of clauses in instance (clauses to variables ratio is 4.5)', 'Ratio of solved instances')
    # plot_comparison(performance_per_instances_sizes, performance_per_instances_sizes_with_tournament_selection_and_linear_scaling,
    #                 'Number of clauses in instance (clauses to variables ratio is 4.5)', 'Ratio of solved instances')
    plot_any(performance_final, 'Number of clauses in instance (clauses to variables ratio is 4.5)', 'Ratio of solved instances')

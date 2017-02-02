import random
import os

def generate_instance(clauses_to_variables_ratio, n_clauses):
    """
    generates an instance of 3 SAT problem in format accepted by genetic_algorithm
    :param clauses_to_variables_ratio:
    :param n_clauses: number of clauses
    :return: a dictionary, which represents an instance of problem
    """
    clauses = []
    n_var = int (n_clauses/clauses_to_variables_ratio)
    for clause_index in range(n_clauses):
        clause = []
        for var_index in range(3):
            var = random.randint(1, n_var)
            if(random.randint(0,1) == 1):
                var *= -1
            clause.append(var)
        clauses.append(clause)
    weights = []
    for var_index in range(n_var):
        weights.append(random.randint(1,100))
    return {'n_var': n_var, 'n_clauses': n_clauses, 'clauses': clauses, 'weights': weights}


def generate_instance_str(clauses_to_variables_ratio, n_clauses):
    """
    generates an instance of 3 SAT problem in string format for saving it to file
    :param clauses_to_variables_ratio:
    :param n_clauses: number of clauses
    :return: a string, which represents an instance of problem
    """
    output = ''
    n_var = int (n_clauses/clauses_to_variables_ratio)
    output += str(n_var) + ' ' + str(n_clauses) + ' 0 '
    for clause_index in range(n_clauses):
        for var_index in range(3):
            var = random.randint(1, n_var)
            if(random.randint(0,1) == 1):
                var *= -1
            output += str(var) + ' '
        output += '0 '
    output += '% '
    for var_index in range(n_var):
        output += str(random.randint(1,100)) + ' '
    output += '#'
    return output


def generate_instances_to_files (clauses_to_variables_ratio, n_clauses, n_instances, folder):
    """
    generates specified number of instances of 3 SAT problem and saves them to specified folder
    :param clauses_to_variables_ratio:
    :param n_clauses: number of clauses
    :param n_instances: number of instances
    :param folder: name of folder where to save generated instances
    :return:
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    filenames = []
    for i in range(n_instances):
        instance = generate_instance_str(clauses_to_variables_ratio, n_clauses)
        filename = folder + '/3_SAT_' + str(n_clauses) + '_' + str(clauses_to_variables_ratio) + '_' + str(i) + '.txt'
        filenames.append(filename)
        with open(filename, mode='w', encoding='utf-8') as a_file:
            a_file.write(instance)
    print('Files ', filenames, ' generated.')


if __name__ == "__main__":
    clauses_to_variables_ratio = 4.5
    n_clauses = 70
    n_instances = 30
    folder = './instances'

    generate_instances_to_files(clauses_to_variables_ratio, n_clauses, n_instances, folder)
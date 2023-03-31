import csv
import math
# from flights import Country


def compute_num_infections(country_name: str) -> int:
    """ Computes the number of infections for each country.

    >>> compute_num_infections('France')
    170995

    >>> compute_num_infections('Canada')
    58713

    >>> compute_num_infections('Japan')
    851190

    """

    cases_so_far = 0

    with open('data/COVID-19-data-from-2023-02-01.csv') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            if row[2] == country_name:
                cases_so_far += int(row[4])

    return cases_so_far


def compute_population(country_name: str) -> int:
    """ Computes the population of each country.

    >>> compute_population('France')
    64626628

    >>> compute_population('Canada')
    38454327

    >>> compute_population('Japan')
    123951692
    """

    population = 0

    with open('data/filter_un_populations.csv') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            if row[0] == country_name:
                population = int(row[1])
                assert population > 0
                break

    return population


def compute_num_deaths(country_name: str) -> int:
    """ Computes the number of deaths for each country.

    >>> compute_num_deaths('France')
    1061

    >>> compute_num_deaths('Canada')
    1060

    >>> compute_num_deaths('Japan')
    5428
    """

    deaths_so_far = 0

    with open('data/COVID-19-data-from-2023-02-01.csv') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            if row[2] == country_name:
                deaths_so_far += int(row[6])

    return deaths_so_far


def compute_infection_rate_per_1000_people(country_name: str) -> float:
    """ Computes the infection rate per 1000 people for each country.

    >>> compute_infection_rate_per_1000_people('France')
    2.64589079287875

    >>> compute_infection_rate_per_1000_people('Canada')
    1.5268242764981947

    >>> compute_infection_rate_per_1000_people('Japan')
    6.86711077731799

    >>> compute_infection_rate_per_1000_people('Bangladesh')
    0.002284060322278458

    >>> compute_infection_rate_per_1000_people('Albania')
    0.14037823314115472
    """

    cases = compute_num_infections(country_name)
    population = compute_population(country_name)

    assert population > 0

    return (cases / population) * 1000


def compute_death_rate_per_100_cases(country_name: str) -> float:
    """ Computes the death rate per 1000 people for each country.

    >>> compute_death_rate_per_100_cases('France')
    0.6204859791221966

    >>> compute_death_rate_per_100_cases('Canada')
    1.8053923321921892

    >>> compute_death_rate_per_100_cases('Japan')
    0.6376954616478107

    >>> compute_death_rate_per_100_cases('Bangladesh')
    0.7672634271099744

    >>> compute_death_rate_per_100_cases('Albania')
    1.0025062656641603
    """

    cases = compute_num_infections(country_name)
    deaths = compute_num_deaths(country_name)

    if cases == 0:
        return 0.0
    else:
        return (deaths / cases) * 100


def compute_danger_index(country_name: str) -> float:
    """ Computes the 'danger index' for each country by averaging out the infection rate and the death rate.

    >>> compute_danger_index('France')
    1.6331883860004732

    >>> compute_danger_index('Canada')
    1.666108304345192

    >>> compute_danger_index('Japan')
    3.7524031194829

    >>> compute_danger_index('Bangladesh')
    0.38477374371612644

    >>> compute_danger_index('Albania')
    0.5714422494026575
    """

    infection_rate = compute_infection_rate_per_1000_people(country_name)
    death_rate = compute_death_rate_per_100_cases(country_name)

    return (infection_rate + death_rate) / 2


def compute_safest_neighbour(neighbours: set[str]) -> list[(str, float)]:
    """ Computes the danger index for each country in the set of neighbours returned by find_paths and returns
     a dictionary containing the Top 3 'safest' neighbours and their associated danger indexes.

    >>> compute_safest_neighbour({'Canada', 'France', 'Japan'})
    [('France', 1.6331883860004732), ('Canada', 1.666108304345192), ('Japan', 3.7524031194829)]

    >>> compute_safest_neighbour({'Canada', 'Japan'})
    [('Canada', 1.666108304345192), ('Japan', 3.7524031194829)]

    >>> compute_safest_neighbour({'Albania', 'Afghanistan', 'Italy', 'Canada', 'Morocco'})
    [('Morocco', 0.003964443242267447), ('Albania', 0.5714422494026575), ('Afghanistan', 0.5924590111707589)]

    >>> compute_safest_neighbour({'Algeria', 'Belarus', 'Burundi', 'The United Kingdom', 'Uruguay'})
    [('Belarus', 0.0), ('Algeria', 0.0016257184200021268), ('Burundi', 0.006555684996930854)]
    """

    top_three_so_far = []
    lowest_index_so_far = math.inf
    neighbour_so_far = ''
    set_neighbours = neighbours

    while len(top_three_so_far) < 3 and set_neighbours != set():
        for neighbour in set_neighbours:
            neighbour_index = compute_danger_index(neighbour)
            if neighbour_index < lowest_index_so_far:
                lowest_index_so_far = neighbour_index
                neighbour_so_far = neighbour

        top_three_so_far.append((neighbour_so_far, lowest_index_so_far))
        set.remove(set_neighbours, neighbour_so_far)
        lowest_index_so_far = math.inf
        neighbour_so_far = ''

    return top_three_so_far


def write_danger_index(output_file='data/country-danger-index.csv') -> None:
    """Compute the danger_index for each country in filter_un_populations.csv and write each country
    and its corresponding index in the given output_file."""
    with open('data/filter_un_populations.csv') as main_file:
        reader = csv.reader(main_file)
        next(reader)

        with open(output_file, mode='w') as file:
            writer = csv.writer(file, delimiter=',', lineterminator="\n")
            for row in reader:
                country = row[0]
                danger_index = compute_danger_index(country)
                writer.writerow([country, danger_index])


if __name__ == '__main__':
    write_danger_index()

from utils import average
import random

MUTATION_RATE = 0.4

MUTATION_RANGE_FACTOR = 0.25


def mutate_number(num):
    adjustment = 0
    if random.random() <= MUTATION_RATE:
        # Pick mutation adjustment - not including 0 - with a step of 1/50 of the whole mutation range
        mutation_range = num * MUTATION_RANGE_FACTOR
        mutation_range_step = num * MUTATION_RANGE_FACTOR * 0.02
        adjustments = list(set(range(num - mutation_range, num + mutation_range + mutation_range_step, mutation_range_step)) - {0})
        adjustment = random.choice(adjustments)
    return num + adjustment


GENE_SETTINGS = {
    "outer_vision_rad": {
        "crossover": average,
        "mutate": mutate_number
    },
    "inner_vision_rad": {
        "crossover": average,
        "mutate": mutate_number
    },
    "max_speed": {
        "crossover": average,
        "mutate": mutate_number
    },
    # "color": {
    #     "crossover": lambda a, b: random.choice([a, b]),
    #     "mutate": mutate_number
    # },
    "food_pref": {
        "crossover": average,
        "mutate": mutate_number
    },
    "poison_pref": {
        "crossover": average,
        "mutate": mutate_number
    }
}


class Genome:
    def __init__(self, **genes):
        self.genes = genes if genes else {}

    def get(self, key):
        return self.genes.get(key)

    def get_subset(self, keys):
        return [(k, self.genes[k]) for k in keys if k in self.genes]

    def crossover(self, other_genome):
        new_genes = {}
        own_keys = self.genes.keys()
        zipped_genes = zip(self.get_subset(own_keys), other_genome.get_subset(own_keys))
        for (own_gene_name, own_gene_val), (other_gene_name, other_gene_val) in zipped_genes:
            new_genes[own_gene_name] = GENE_SETTINGS[own_gene_name]["crossover"](own_gene_val, other_gene_val)
        return Genome(**new_genes)

    def mutate(self):
        new_genes = {}
        for gene_name, gene_val in self.genes.items():
            new_genes[gene_name] = GENE_SETTINGS[gene_name]["mutate"](gene_val)
        return Genome(**new_genes)


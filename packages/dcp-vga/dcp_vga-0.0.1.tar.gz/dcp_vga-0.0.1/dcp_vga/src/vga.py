class VGA:
    def __init__(self,population_size, num_generations, crossover_probability, mutation_probability, selection_type, lip_estimation_method='naive', elitism=True):
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism = elitism
        self.lip_estimation_method = lip_estimation_method
        self.selection_type = selection_type
        
        #default number of elites is 1.
        if self.elitism:
            self.number_of_elites = 1


    def run_algorithm(self):
        pass
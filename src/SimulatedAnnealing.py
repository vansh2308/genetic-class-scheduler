from model.Schedule import Schedule
import math
import random

class SimulatedAnnealing:
    def __init__(self, configuration, temperature=1000, cooling_rate=0.003, max_iterations=5000):
        self._configuration = configuration
        self._temperature = temperature
        self._cooling_rate = cooling_rate
        self._max_iterations = max_iterations
        self._prototype = Schedule(configuration)
        self.result = None

    def run(self):
        # Create an initial solution
        current_solution = self._prototype.makeNewFromPrototype()
        current_solution.calculateFitness()
        
        best_solution = current_solution

        for i in range(self._max_iterations):
            # Create a new neighbor solution by mutating the current one
            new_solution = current_solution.copy(current_solution, False)
            new_solution.mutation(2, 100)  # Using mutation to create a neighbor. mutationSize=2, mutationProbability=100%
            new_solution.calculateFitness()

            # Get energy of solutions (we want to maximize fitness, so we use its inverse as energy)
            current_energy = 1 / current_solution.fitness
            new_energy = 1 / new_solution.fitness

            # Decide if we should accept the new solution
            if self.acceptance_probability(current_energy, new_energy, self._temperature) > random.random():
                current_solution = new_solution

            # Keep track of the best solution found so far
            if new_solution.fitness > best_solution.fitness:
                best_solution = new_solution

            # Cool down the temperature
            self._temperature *= 1 - self._cooling_rate
            
            print("Fitness:", "{:f}\t".format(best_solution.fitness), "Iteration:", i, "Temperature:", "{:f}".format(self._temperature), end="\r")

        self.result = best_solution

    def acceptance_probability(self, old_energy, new_energy, temperature):
        if new_energy < old_energy:
            return 1.0
        return math.exp((old_energy - new_energy) / temperature)

    def __str__(self):
        return "Simulated Annealing" 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import optimizer
from individual import GeneType
from numpy import power as pw

class ExampleProblem:
    """
    Example problem class to be minimized.

    This class implements a simple sum of squares function with a global minimum value of 0,
    achieved when all elements of the chromosome are equal to 0.
    """
    
    def __init__(self):
        pass
    
    def f(self, x):
        """
        Compute the objective function value.

        This method implements the sum of squares function.

        Parameters
        ----------
        x : list or numpy.ndarray
            The input chromosome represented as a list or array of real values.

        Returns
        -------
        float
            The computed value of the function given the input x.
        """
        return sum(pw(xi, 2) for xi in x)

def run_cga_example():
    """
    Run the Cellular Genetic Algorithm (cga) using the optimizer module.

    The cga is configured with a 5x5 grid, 100 generations, and a chromosome size of 5.
    The problem being solved is an instance of the ExampleProblem class, 
    with real-valued genes, constrained by specified mins and maxs.
    
    Returns
    -------
    tuple
        A tuple containing the best solution chromosome and its corresponding value.
    """
    # Create an instance of the problem
    problem_instance = ExampleProblem()

    result = optimizer.cga(
        n_cols=5,
        n_rows=5,
        n_gen=100,
        ch_size=5,
        gen_type=GeneType.REAL,
        p_crossover=0.9,
        p_mutation=0.2,
        problem=problem_instance,  # Pass the ExampleProblem instance
        selection=optimizer.TournamentSelection,
        recombination=optimizer.ByteOnePointCrossover,
        mutation=optimizer.ByteMutationRandom,
        mins=[-32.768] * 5,  # Minimum values for each gene
        maxs=[32.768] * 5    # Maximum values for each gene
    )

    # Print the results
    print("Best solution:", result[1], "\nBest solution chromosome:", result[0])

if __name__ == "__main__":
    run_cga_example()

# Implementation of Evolutionary Strategy Algorithm for Solving a continuous optimization problem.

ES is mainly efficient for solving continuous problems. Unlike genetic algorithm the main operator in ES is mutation. 
As specified by the constraint boundaries, it does not take too long to get the solution close to the global optima.  
I used the children to the population ratio of 1/6 as suggested in the literature for most of the experiment and 
changed the ratio to see the variations. As ES is metaheauristic algorithm it is imperative to perform several experiments 
by changing the global parameters. The dual and global recombinations also better be eperimented separately to observe the
significance of each approaches on the performance and final solution.

For a large number of population and generation, the algorithm is not sensitive to changes to parameters and gets to the 
optimal solution. However, since the problem has more than one optimal solution, the solution appears to change for multiple
runs of the same instances. The most noticeable observation from the experimental result is that having a higher number of 
population is the most significant factor. The solution appears to be affected more by the increase in the size of the population.
And the one-fifth success rule appears to work efficiently for the given problem. There is no significant difference between the 
approaches for certain parameter configuration.

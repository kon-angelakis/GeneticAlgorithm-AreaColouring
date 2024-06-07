# Area Colouring Genetic algorithm  
### Given a graph with nodes and neighbours(edges) and a selection of colors find the best possible solution so that no neighbours share the same color, with the use of a genetic algorithm.  

----

#### The problem given is below:  
![image](https://github.com/kon-angelakis/GeneticAlgorithm-AreaColouring/assets/56235553/6b65ebe9-9f5d-455f-8605-18dacc0dc051)  
#### Colors = Red, Blue, Green, Yellow

#### A solution:  
![image](https://github.com/kon-angelakis/GeneticAlgorithm-AreaColouring/assets/56235553/32c9ab19-2dcc-4e9a-a7ee-b67e0cb29fe3)

----

In the base version of the code the crossover going to be used is single point. Elitism will also be used for the next generation of solutions with the number of elites being at least 1 or 1% of the population.
The algorithm will also run with the below parameters:
- NUMBER_OF_SOLUTIONS = 100
- GENERATIONS = 1000
- MUTATION_CHANCE = 0.2%

----

To run you are going to need the following libraries:  
- Matplotlib


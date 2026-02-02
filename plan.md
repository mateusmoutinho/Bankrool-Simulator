create the "simulation.ipynb" file that will be a jupyter notebook that will be used to simulate the games, it must start with: (after the imports)
```python
from src import *
TOTAL_SIMULATIONS = 100000
SEED = 42,
SIMULATION_DIR = "simulations-data"
ESPECIF_SIMULATION_VIEW = 3
``` 
folow these steps:


1 generate all simulations, and save into SIMULATION_DIR, with the name of simulation <simulation>.json if the SIMULATION_DIR alread exists, it dont make the simulations

2 show all the game evs using the get_all_games_ev functions,

3 shows a "avarage simulations results", including the total times the bank was destroyed, the avarage profit, the avarage loss, the avarge total money, the min bankroww, and the max bankroww, (and other general informations, you think its important),
also, plot some graphics of the simulations results, including the bankroww evolution over the simulations, and the distribution of the results, 

4 plot 3 simulations, the most lost simulation, the most profitable simulation, and the "avarage" simulation, showing the bankroww evolution over the simulations, and the distribution of the results, 

 
5. if is ESPECIF_SIMULATION_VIEW ,show that simulation number ,excalty.
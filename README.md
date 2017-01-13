# Big Valley 
## Play God, in Python

created by Seth Green, based on an exercise in Eloquent Javascript by Marijn Haverbeke

Big Valley is a little simulated ecosystem with three kinds of critters: grass, rabbits, and wolves. Grass grows on debris, and then is eaten by rabbits. Rabbits, in turn, are eaten by wolves. As each year passes, each critter does one of three things:

1. reproduces, if she has enough energy
2. eats food, if it's next to her, increasing her energy
3. moves, if there's no food next to her, decreasing her energy

Running `bigValleySimScript.py` will run simulations of the world, for your viewing pleasure. By default, the world runs until either rabbits or wolves go extinct, and then restarts. It takes three arguments:

1. the max number of years to run before restarting (if there has not been an extinction)
2. the number of times to restart the world before quitting the program
3. whether or not to show a plot visualizing each year (`plot` for showing or `no` for only printing text output)

A quick starting default is `python bigValleySimScript.py 100 3 plot`

The parameters which determine the fate of your critters and your world are set in the `bigValleySimScript.py` file. These parameters are discussed below. You can open it and manually change them to attempt to make your ecosystem more stable. Or...

### Learning
The real point of this exercise is to design a process whereby the world could itself learn the ideal parameters which would lead to the most stable ecosystem. A first attempt at this is contained in 'bigValleySimLearning-RF1.py`. 

Each time `...-RF1.py` iterates, it randomly generates 20 sets of parameters (from a normal distribution, centered on the starting parameters that are hard coded). It then builds a Random Forest model on *all* past runs (saved in the `...-SIMS-RF1.csv` file corresponding to your input parameters) and then uses the model to predict which of the 20 parameter sets will result in the most stable ecosystem. It then simulates the world with those parameters and logs the results in the `...SIMS.csv` file for use in future iterations.

This approach has shown some promise. More stable ecosystems are produced after several hundred iterations. However, the improvement levels off around 1000 iterations, as it is still tied to the distributions centered on the original hard coded parameters. Development is under way to automatically optimize these every hundred iterations or so in attempt to create a perpetually stabilizing universe. 

### Parameters
Each new critter is generated with some small random variation (encoded in the `bigValley...` file) centered on the hard-coded parameter for that critter. Then, when critters reproduce, the variation of the new critter is centered on the value of it's parent. This creates some degree of "inheritance" or "evolution" as the world ages.

**Energy** is the starting energy for that critter. 
**Repro** is the threshold of energy that must be reached for that critter to reproduce. 
**Fatigue** is the amount of energy that critter loses each turn it moves (without eating). 

*Note:* Grass and debris don't have meaningful fatigue values because they don't move. They gain a little energy each turn until they reproduce or, in the case of grass, get eaten.

### Customize
For those adventurous souls, feel free to open `bvLife.py` and create some creatures of your own. A ruminant who gets double energy from each plant eaten? A super predator to thin out the wolf pack? A carniverous plant that eats low-energy foragers? All fair game...

#brief documentation:

`bvSim.py` and `bvSimLearning.py` set up each simulation and save it's output appropriately.

`bvWorldEvo.py` contains all the code to run each year (mostly contained in `silentTime()`). It also contains many helper functions for reproduction and eating, etc.

`bvWorldEvoPlotting.py` is an exact copy of `bvWorldEvo.py` but with some (somewhat messy) code added to visualize the world each year.

`bvLife.py` contains definitions of all the critters and the methods they use to act and live.


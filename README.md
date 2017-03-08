# Big Valley 
## Play God, in Python

created by Seth Green, based on an exercise in Eloquent Javascript by Marijn Haverbeke

Big Valley is a little simulated ecosystem with three kinds of critters: grass, rabbits, and wolves. Grass grows on rocks, and then is eaten by rabbits. Rabbits, in turn, are eaten by wolves. As each year passes, each critter does one of three things:
    1) reproduces, if she has enough energy
    2) eats food, if it's next to her, increasing her energy
    3) moves, if there's no food next to her, decreasing her energy

**You can view a visualization of this exercise (in `d3.js`) at [seth127.github.io/bigValley](https://seth127.github.io/bigValley/).** The following README details the code for developing the simulations from scratch. 

Running `bigValleySimScript.py` will run simulations of the world. By default, the world runs until either rabbits or wolves go extinct, and then restarts. The arguments and parameters are discussed at the bottom of this README in **Brief Documentation**.

A quick starting default to try is `python bigValleySimScript.py 100 3 noPlot`

The parameters which determine the fate of your critters and your world are set in the `bigValleySimScript.py` file. These parameters are discussed below. You can open it and manually change them to attempt to make your ecosystem more stable. Or...

## Learning
The real point of this exercise is to design a process whereby the world could itself learn the ideal parameters which would lead to the most stable ecosystem. This is an example of what is generally called [Agent-based modeling](https://en.wikipedia.org/wiki/Agent-based_model). There are several languages and libraries designed for doing this kind of simulation and modeling, notably [NetLogo](https://ccl.northwestern.edu/netlogo/) and [Arena](https://www.arenasimulation.com/support/entry/solving-agent-based-problems-with-arena). However, in order to have maximum control over how the parameters were set and then reset through the learning process, bigValley was built from scratch in Python.

Two approaches were tested for learning the optimal parameters. The first is a more tradition [Response Surface Methodology](https://en.wikipedia.org/wiki/Response_surface_methodology) approach, fitting a first-degree polynomial linear model, and then adjusting each parameter by a fixed learning rate in the direction of the relevant coefficient. The second utilized a Random Forest model, which selected an optimal set of parameters from a set of randomly generated options. More about both methods and the results are below. But first, a brief overview of the parameters that we are optimizing.

### Parameters
Each new critter is generated with some small random variation (encoded in the `bigValley...` file) centered on the hard-coded parameter for that critter. Then, when critters reproduce, the variation of the new critter is centered on the value of it's parent. This creates some degree of "inheritance" or "evolution" as the world ages.

**Energy** is the starting energy for that critter

**Repro** is the threshold of energy that must be reached for that critter to reproduce

**Fatigue** is the amount of energy that critter loses each turn it moves (without eating)

*Note:* Grass and rocks don't have meaningful fatigue values because they don't move. They gain a little energy each turn until they reproduce or, in the case of grass, get eaten. The number of rocks does not change within each iteration (i.e. rocks don't reproduce *or* get eaten).

There were **a total of ten parameters** which were set at the beginning of each iteration. The first six were *Energy*, *Repro*, and *Fatigue* for both wolves and rabbits (referred to below as *wolfEn*, *wolfRe*, *wolfFa*, etc.). The other four were the number of wolves, rabbits, grass, and rocks that exist at the start of that iteration.

*Note:* Several learning rates and modeling hyperparameter settings were tried until an optimal setting was found for both the Linear Model and Random Forest. For brevity's sake, only the results of the optimal models are discussed below.

###Initial Training Runs
Before each test run, 500 iterations of the world were run with parameters centered around the starting statistics noted in the appendix. These parameters had random normal noise added to them each iteration, so that some semblance of a "normal distribution" of training simulations could be generated. Additionally, the starting placement of each critter was random each time, so this added another stochastic element to each iteration. 

Once 500 iterations were run, the first *modeling iteration* began by training its model on those 500 and setting its parameters accordingly.

###Stabilization Threshold
Each iteration was set to run until either rabbits or wolves went extinct **or** until it had run for 500 years. Once a test run produced ten consecutive iterations that reached the max of 500 years without an extinction, the environment was deemed "stable" and those parameters were deemed "optimal." In the plots below, each test run is identified with a 3-character alpha-numeric ID, for purposes of easier comparison between plots.

##Response Surface Linear Model
After the initial 500 training iterations an OLS linear model was fit with the ten parameters discussed above as the explanatory variables, and the year of the first extinction for that iteration as the response. Thus, the response was bounded, with 1 (an extinction in the first year, very unlikely) on the lower endm and 500 (the max years allowed before restart) on the upper.

The default starting parameters (listed in the appendix), were then adjusted in the direction of the coefficient for that parameter. 

This process was repeated with each iteration, so that a model was fit on all 500 training iterations, *and all the previous learning iterations*, and then the starting parameters were adjusted accordingly for the next iteration. Below is a chart showing the four testing runs that were performed. The x-axis shows the iteration count (note that the parameters do not begin to "learn" until iteration 501). The y-axis shows the starting value of the parameters for that iteration.

###Critter Stats: Linear Model
![LM2-critters-w-legend](markdown-and-plotting/LM2-critters-w-legend.png)

Though the traces are far from identical, some patterns emerge. For instance, in all four tests, *Fatigue* for both rabbits and wolves immediately moved towards zero until it hit the minimum allowed value (set to 5 for these simulations). 

Most interestingly, in three of the four tests (`GP5`, `BMQ` and `JQ3`), rabbits and wolves followed opposite patterns. In these tests, *rabbitEn* moved sharply up while *rabbitFa* attempted to move down and stayed at its minimum allowed value (*Fatigue* for both critters was constrained to be at least *Energy* multiplied by 1.1, to avoid critters that could spontaneously reproduce without having to eat). On the other hand, *wolfRe* sky-rocketed while *wolfEn* moved steadily downward, in some cases levelling off at it's minimum allowed value of 100. This indicates that the optimal world has large herbivores that reproduce very quickly, and relatively small predators that reproduce very infrequently.

###Critter Counts: Linear Model
![LM2-counts-w-legend](markdown-and-plotting/LM2-counts-w-legend.png)

In all fours tests, the optimal world had drastically increased numbers of grass and rocks, indicating that starting the world a plethora of plants at the bottom of the food chain is necessary for stability. Likewise, having plenty of rocks to keep up the food supply is necessary. None of tests levelled out for either of these counts. It would be interesting to let it continue ad nauseum and see if more plant life is ever *not* better.

The critters were a different story. All four models definitely said that starting with only one wolf was ideal. This is counter to my pre-conception, but you can't argue with evidence. The starting count of rabbits was mixed. All four models reached "stability" with a different pattern for the rabbit count.


##Random Forest Model
The Random Forest Model took an entirely different approach. Again, each test run began with 500 training iterations. Then, on *each learning iteration* a Random Forest Regressor was fit to the training data (which again included the initial 500, and *all* previous learning iterations).  At this point 100 sets of parameters were generated with random normal variation around a "center value"" for each parameter. The newly trained Regressor then predicts the year of first extinction for each of those 100 parameter sets, and chooses the one with the best predicted outcome (i.e. most years until an extinction). This "best parameter set" is then used to run the current iteration.

*Note:* These "center values" for generating the 100 options are initially set to the default values in the appendix, but once the algorithm begins learning, they are set to the values of the "best parameter set" predicted in the previous iteration. This provides for a slower movement of the parameters that explores more of the feaure space, as compared to the Linear Model approach.

###Critter Stats: Random Forest
![RF2-critters-w-legend](markdown-and-plotting/RF2-critters-w-legend.png)

Right off the bat, we see a similar pattern with the wolves. Their *Repro* shoots up while the their *Energy* moves down. However, the movement is somewhat less dramatic than in the Linear Model, as it seems to level out at an optimal value relatively quickly. 

The rabbits, on the other hand, show a different pattern than we saw in the Linear approach. Where before *rabbitEn* skyrocketed upwards, here we see it stabilize at a very low number. In two of the four (`MFU` and `L1X`), *rabbitRe* hugs that bottom, creating herbivores that reproduce quickly (as in the Linear Model), but are fairly small. However, in the other two test runs (`IU7` and `OL2`), *rabbitRe* moved up, while *rabbitEn* stayed low. This is actually mirrored in one of the Linear Model test runs (`3V7`), and appears to correspond to cases where *wolfEn* and *wolfRe* stay relatively close together.

###Critter Counts: Random Forest
![RF2-counts-w-legend](markdown-and-plotting/RF2-counts-w-legend.png)

The counts show interesting differences too. While some patterns are consistent with the Linear Model--notably, lots of rocks are necessary--there are some interesting differences. For example, in the two runs noted above where *rabbitRe* is notably high (`IU7` and `OL2`), *rabbitNum* stays low, while *grassNum* moves higher. This simulates an herbivore that is slower to reproduce and thus needs a more plentiful food source. However, in the other two runs (`MFU` and `L1X`), where rabbits reproduce very quickly, *rabbitNum* is high while *grassNum* stays very low, at times bottoming out at 1. It makes sense that less grass would be necessary to control the population of quicker-reproducing rabbits (notice that *wolfNum* is also higher in these runs), while the slower-to-reproduce rabbits would need more food. However, it is a bit counterintuitive that the slower-reproducing rabbits start with a *low* population, while the especially fertile rabbits begin with a larger population.


##Conclusions and Next Steps

###Which is best?
Given our test runs, can we conclude that one method is objectively better than the other? To do so, some objective metric must be established. One such metric could be *the number of iterations that are necessary for the ecosystem to stabilize* (using our definition of "stable" from above). The plot below shows this metric for each of the test runs.

![Iterations To Stabilize](markdown-and-plotting/iterations-to-stabilize.png)

It is clear that the Linear Model finds an optimal set of parameters faster. Some, in fact, take just over 100 learning iterations (after the initial 500 training iterations) to reach "stability."

Alternatively, we could look at some measure of "how stable" these ecosystems were. To get some sense of this, once each run reached ten iterations in a row that survived to 500 years, a final iteration was run with the max number of years set to 5,000. This would test whether the ecosystem had indeed stabilized, or was still struggling to find a balance.

![Final Iterations](markdown-and-plotting/final-runs.png)

Again, the Linear Model approach is the clear winner. While one (`BMQ`) sputtered out almost immediately, the other three runs reached 5,000 years still in good health. Of those using the Random Forest approach, only one (`L1X`) reached 5,000 years, while `OL2` also sputtered out almost immediately.

This is interesting, but perhaps more interesting is to consider the parameters of each run in light of these metrics. A brief synopsis of lessons learned includes:

**Failures**
- `BMQ` had only one wolf, and with *wolfEn* at the lower threshold and *wolfRe* very high. Despite a very high *rabbitNum* this runs a high risk of quick burnout if our lonely wolf cannot find enough food quickly.
- `OL2` was on of the few with a high *rabbitRe*/*rabbitEn* ratio, and also had a relatively low *rabbitNum* and *grassNum*. It is somewhat surprising that this combination reached "stability" in the first place. Howver, it is interesting to note that `IU7`, which similar critter stats but high *grassNum* survived for over 1,000 years. Ultimately though, it also failed.

**Successes*
- `3V7`, a Linear Model, had a similar set up to `OL2` and yet it thrived. A notable difference was that, while rabbits were slow to reproduce and also not plentiful, `3V7` had a very high *grassNum*, whereas `OL2` did not.
- There is some diversity within the three successful Linear Models, though two principles that seem consistent are to keep *wolfEn* from getting *too* low and keep *rabbitNum* from getting *too* high. A *wolfRe*/*wolfEn* ratio of around 2.5 to 3 seems ideal.
- `L1X` demonstates an interesting and unique strategy of fast-reproducing rabbits and high *rabbitNum* with high *rockNum*, but very low *grassNum* and *wolfNum*. This indicates that, so long as the rabbits have to wait a few years to eat and reproduce, the ecosystem will stabilize.

These are just a few of lessons we can glean from these eight runs. We can see how, in more meaningful simulations, the interpretibility of this approach would be ideal for understanding the complicated relationships between independently varying factors.

###Looking beyond "best"
While the Linear Model approach did score superior marks on both metrics that we looked at, as we noted, the interpretation of the interactions is the primary gain from an Agent-based Model such as this. In this light, the Random Forest approach brings much to the table. Consider a real-world situation where certain parameters cannot simply be "turned up or down" without some great cost. Sure, it would be "better" if *grassNum* was higher, but imagine that this represents something like "the number of Red Cross food drops in a disaster area". It may not be practical to simply quadruple the number of food drop sites. 

However, as noted earlier, the Random Forest provides a wider range of possible optimizations and may demonstrate several successful example where, by adjusting other more easily influenced parameters, an optimal balance may be achieved. This can be attempted with the Linear Model approach as well, but the majority of successful runs seem to converge towards very similar parameters.

###Next steps
There are many directions that this research could go. One obvious example would be to introduce entirely new agents (for instance "super predators" to eat wolves; or perhaps a large, slower-to-reproduce herbivore to coexist with the smaller, faster rabbits). However, if there is to be any real-world gain from this kind of modeling, we must be sure not to introduce too many variables that are beyond our control.

Another interesting approach would be to set up different "continents." This would entail simulating four ecosystems simultaneously, but *far away* from each other on the grid. Eventually, the populations would expand enough to interact with each other. Observing the interactions on these borders of differently-evolved populations would be fascinating. 

The limit of 500 years per iteration could also be increased. This is perhaps the easiest, and most informative, extension. The limit was imposed partially to control for outliers, but mainly to control computation time. The examples presented here took several weeks to simulate on a fairly small AWS EC2 instance. With more computing power, that limit could be significantly relaxed and more varied and interesting interactions might be observed.

There is a logging system (which is currently *only* turned on for the "max 5,000" runs) which logs the average value of each parameter for *each year of an iteration* as opposed to just the starting value. This could be interesting to examine, in either of the previously mentioned contexts, to see how the creatures "evolve" througout an iteration to see if the parameters actually converge towards an ideal value once the ecosystem truly does become stable. An exploratory example of this is contained in `markdown-and-plotting/bvBigRunPlots.R`.

### Customize
For those adventurous souls, feel free to open up the bvLife.py and create some creatures of your own. A ruminant who gets double energy from each plant eaten? A predator that hunts in packs? A carniverous plant that eats low-energy foragers? The only limit is your own imagination...

#Brief Documentation:
###Simulation Functions
`bigValleySimScript.py`: runs simulations of the world, for your viewing pleasure. By default, the world runs until either rabbits or wolves go extinct, and then restarts. It takes three arguments:
    1) the max number of years to run before restarting (if there has not been an extinction)
    2) the number of times to restart the world before quitting the program
    3) whether or not to show a plot visualizing each year ('plot' for showing or 'no' for only printing text output)

`bigValleyLearningLM2.py`: runs simulations of the world and learns the optimal parameters with the Linear Model approach, discussed above. It takes three arguments:
    1) the max number of years to run before restarting (if there has not been an extinction)
    2) the number of learning iterations to run (after the initial 500 training iterations) before quitting the program. Note, if "stability" (defined above) is reached before this number, a final iteration with max years set to 5,000 will run, and then the program will quit.
    3) either `new` to start a new test run (with 500 training iterations) or the three-character alpha-numeric of a previous test run, if you'd like to pick up where you left off. *Note:* if the previous test run has already reached "stability" then it will automatically run the 5,000 iteration and then quit.

`bigValleyLearningRF2.py`: runs simulations of the world and learns the optimal parameters with the Random Forest approach, discussed above. Takes the same arguments as `bigValleyLearningLM2.py`.

###Helper Functions
`bvSim.py` and `bvSimLearning.py` set up each simulation and save it's output appropriately.

`bvLife.py` contains definitions of all the critters and the methods they use to act and live.

`bvWorldEvo.py` contains all the code to run each year (mostly contained in `silentTime()`). It also contains many helper functions for reproduction and eating, etc.

`bvWorldEvoPlotting.py` is an exact copy of `bvWorldEvo.py` but with some (somewhat messy) code added to visualize the world each year. Again, a superior visualization can be found at [seth127.github.io/bigValley](https://seth127.github.io/bigValley/).

###Appendix

####Default Starting Parameters
*wolf stats*
Energy = 300
Repro = 400
Fatigue = 20

*rabbit stats*
Energy = 70
Repro = 100
Fatigue = 10

*Note:* one run was done with each model where the stats above were doubled. 

*numbers of each critter*
Wolves = 3
Rabbits = 16
Grass = 25
Rocks = 10

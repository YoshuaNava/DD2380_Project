Readme for running tetris

##### Required python packages
numpy
pygame

##### Game execution
run tetris.py

##### Choise of algorithm
1) open 'tetris/game.py' in a text editor
2) in the play(self) method, it's possible to choose
   between MCTS, one depth max search and two depth max search.

MCTS:
uncomment the lines;
        mcts = MonteCarloTreeSearch(root)
        best_child = mcts.run()

One depth max search:
uncomment the line;
	best_child = shallowMaxSearch(root)

Two depth max search:
uncomment the line;
	best_child = DEEPMaxSearch(root)

Note: make sure to comment the algorithms that are not supposed to run.

##### Heuristics configuration
1) open 'tetris/heuristic.py' in a text editor
2) tune the weights'a' and 'b' which corresponds to the number of holes
   and aggregated height respectively.

##### notes
The rotations and translations are done immediately when the algorithm
has returned the chosen action. Therefore it is not possible to see 
the animations for rotating and translating the bricks.


# Connect 4 Game with AI
This project is a digital version of the classic Connect 4 game built with Python, NumPy, and Pygame.
It allows a human player to compete against an AI opponent while comparing the performance of two search algorithms: Minimax and Alpha-Beta Pruning.
The main goal of this project is to demonstrate and compare the efficiency and computation times of these two algorithms in a turn-based game scenario.

## How to Run the Game

    1. Install pygame library
    pip install pygame numpy
    
    3. Clone the repository
    git clone https://github.com/maramahg/Connect4Game
    cd Connect4Game
    
    4. Run the game
    python connect4.py


## Once the game starts:
You’ll see a welcome screen.
Enter your nickname.
Choose your preferred color.
The AI will randomly select a different color and start the game.
Click within the board columns to drop your piece and compete against the AI.

## Game Description
The game follows the classic Connect 4 rules:
Players take turns dropping colored pieces into a 7×6 grid.
The first player to connect four pieces in a row, either horizontally, vertically, or diagonally, wins.
If the grid fills with no winner, the game ends in a draw.

## After each match:
The program displays the computation time of both Minimax and Alpha-Beta Pruning algorithms for each round.
A scoreboard keeps track of total wins for the player and the AI.

## AI Algorithms Explained

### 1. Minimax Algorithm
The Minimax algorithm is a classic decision-making algorithm used in turn-based games.
It explores all possible future moves recursively to determine the best one.
The AI assumes the opponent will always play optimally.
It alternates between maximizing its own score and minimizing the opponent’s.
The deeper the search depth, the stronger (but slower) the AI becomes.

#### Pros:
Simple and guarantees optimal decisions if search space is small.

#### Cons:
Computationally expensive — explores every possible move.

### 2. Alpha-Beta Pruning
The Alpha-Beta Pruning algorithm is an optimized version of Minimax.
It eliminates branches in the decision tree that don’t need to be explored because they cannot affect the final decision.
Alpha represents the best value the maximizing player can guarantee.
Beta represents the best value the minimizing player can guarantee.
When Alpha ≥ Beta, further exploration of that branch is stopped (pruned).

#### Pros:
Produces the same result as Minimax.
Significantly faster due to reduced search space.

#### Cons:
Still limited by depth and board complexity.

## Comparison Goal
The main purpose of this project is to compare Minimax and Alpha-Beta Pruning in terms of:

Execution time per move
Efficiency in reaching the optimal decision
Performance difference over multiple game rounds

## After each game:
The program displays a timing screen showing how long each algorithm took to compute its moves.
This allows users to visually compare the performance and speed difference between the two algorithms in identical game conditions.

## How It Works Internally
The game initializes a 6×7 board as a NumPy array.
The player and AI take turns dropping tokens into columns.

#### Each AI move triggers:
A Minimax calculation (without pruning)
An Alpha-Beta Pruning calculation
Both timings are recorded and compared.
The board updates visually, showing the results in real time.

After a win or draw, the game displays the performance comparison and overall scoreboard:

    Example Output (in-game)
    Round | Minimax (s) | Alpha-Beta (s)
    ------------------------------------
      1    |   0.54213   |    0.03729
      2    |   0.61347   |    0.04118
      3    |   0.55591   |    0.03806

This illustrates how Alpha-Beta Pruning drastically reduces computation time while maintaining identical AI decisions.

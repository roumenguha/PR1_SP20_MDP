# ECE276B_PR1_SP20
 Project 1: Markov Processes and Dynamic Programming/Deterministic Shortest Path Applied to Motion Planning in a Maze. For ECE 276B at UCSD. 
 
 Consult my [Project Report](https://github.com/roumenguha/ECE276B_PR1_SP20_MDP/blob/master/ECE276B_PR1_Report_RoumenGuha.pdf) in the code folder for more background. 

 We did not solve the problem of the shortest path from START to GOAL, but instead solved two simpler sub-problems: START to KEY, and KEY to GOAL. The logic here is is that once the agent has the key, the door is traversable, and hence once we are at the KEY we simply need to focus on getting to the GOAL. This leads to sub-optimal solutions, but in most situations not *much* worse (except for the 'doorkey-8x8-normal' environment).
 
 Maze Traversal            |  Value Iteration (S-to-K) |  Value Iteration (K-to-G)
:-------------------------:|:-------------------------:|:-------------------------:
![5x5-normal](starter_code/gif/doorkey-5x5-normal.gif) |  ![5x5-normal-s-k](starter_code/gif/doorkey-5x5-normal-VI-StartToKey.gif) | ![5x5-normal-k-g](https://github.com/roumenguha/ECE276B_PR1_SP20_MDP/blob/master/starter_code/gif/doorkey-5x5-normal-VI-KeyToGoal.gif)

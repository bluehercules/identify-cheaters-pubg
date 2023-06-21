## Open final_assign.ipynb to view and run the code

The final assignment asks you to use the computational thinking and programming skills you learned in the course to answer an empirical social science question using digital trace data.

**You are expected to complete the final assignment entirely on your own. You are not allowed to discuss the assignment with others!**

### 1. Do cheaters team up?

Use the files `cheaters.txt` and `team_ids.txt` to estimate how often cheaters (regardless of when exactly they started cheating) end up on the same team. Your output should say how many teams have 0, 1, 2, 3, or 4 cheaters.

Now, randomly shuffle the team ids among the players in a match. Repeat this 20 times and estimate the expected counts as before. Output the mean and the 95% confidence intervals for the expected counts. 

### 2. Do victims of cheating start cheating?

Use the files `cheaters.txt` and `kills.txt` to count how many players got killed by an active cheater on at least one occasion and then started cheating. Specifically, we are interested in situations where:

1. Player B has started cheating but player A is not cheating.
2. Player B kills player A.
3. At some point afterwards, player A starts cheating.

Output the count in the data. 

Then, simulate alternative worlds in which everything is the same but the events took somewhat different sequence. To do so, randomize within a game, keeping the timing and structure of interactions but shuffling the player ids. Generate 20 randomizations like this and estimate the expected count of victims of cheating who start cheating as before. Output the mean and the 95% confidence interval for the expected count in these randomized worlds.

### 3. Do observers of cheating start cheating?

Use the files `cheaters.txt` and `kills.txt` to count how many players observed an active cheater on at least one occasion and then started cheating. Cheating players can be recognized because they exhibit abnormal killing patterns. We will assume that player A realizes that player B cheats if:

1. Player B has started cheating but player A is not cheating.
2. Player B kills at least 3 other players before player A gets killed in the game.
3. At some point afterwards, player A starts cheating.

Output the count in the data.

Then, use the 20 randomizations from Part 2 to estimate the expected count of observers of cheating who start cheating. Output the mean and the 95% confidence interval for the expected count in these randomized worlds.
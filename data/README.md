
### Data for project-code

---

This repository contains the data required to complete the final assignment. Your code should refer to the data files here but not modify them in any way.

The repository contains the following files:

* `cheaters.txt` – contains cheaters who played between March 1 and March 10, 2019
    1. player account id
    2. estimated date when the player started cheating
    3. date when the player's account was banned due to cheating


* `kills.txt` – contains the killings done in 6,000 randomly selected matches played between March 1 and March 10, 2019
    1. match id 
    2. account id of the killer
    3. account id of the player who got killed
    4. time when the kill happened
 
 
* `team_ids.txt` – contains the team ids for players in 5,419 team-play matches in the same period. If a match from the kills.txt file does not appear in these data, we will assume that it was in single-player mode.  
    1. match id 
    2. player account id
    3. team id in match
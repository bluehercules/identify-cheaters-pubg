from collections import Counter
import random
from itertools import cycle
from dictionary_methods import add_dictionary_items, add_cheaters_dictionary


def cheaters_per_team(teams_data, cheater_teams):
    ''' Takes two dictionaries as arguments. The first dictionary
    acts as a directory and the second dictionary is a subset of
    the first. If the key of the second exists in the first then
    the values of the second dictionary will be counted and 
    added to a list.
    There are two outputs: first, the list which tracks number of 
    cheaters, second, a total count of the number of teams in the  
    directory.
    '''
    # List where number of cheaters will be stored
    cheater_ls = []
    # Count keeps track of total number of teams
    count = 0

    for key in teams_data:
        teams_len = len(teams_data[key])
        count += teams_len
        # First check to see if there are any cheaters in match
        if key in cheater_teams:
            # When there are, add the teams they are on to a list
            teams = cheater_teams[key]
            cheaters_per_team = list(Counter(teams).values())
            # Extend new values to the list
            cheater_ls.extend(cheaters_per_team)
    
    return cheater_ls, count


def team_counter(count_ls, total_count):
    ''' Function takes two arguments - the first is a
    list of counts data, the second argument is a simple
    count. The number of observations is count_ls is a
    subset of the total number of observations in
    total_count.
    The function returns a Counter dictionary and uses
    the difference in the length of count_ls and total_count
    to calculate the number of groups who are not represented
    in count_ls and thus have a value of 0.
    '''
        
    summary_counter = Counter(count_ls)
    
    # Calculating how many teams have no cheaters by
    # considering difference in teams with cheaters 
    # and the count for total number of teams.
    for key, value in summary_counter.items():
        total_count -= value
    summary_counter[0] = total_count
    
    return summary_counter


def victims_start_cheating(match_directory, cheaters_directory):
    ''' Takes three arguments as inputs. Two of them being the
    kills and cheaters data and a third being a simple list of 
    player ids who are within the cheaters data list.
    Looks for scenarios where the player killed is also on cheating
    list and the start date of cheating is after match kill date.
    Output set of player ids who fit this criteria.
    '''
    
    sets = set()

    for value in match_directory.values():
        cheaters = value[0]

        # Only considering matches where there is an active cheater
        if len(cheaters) > 0:
            events = value[1]
            match_d = value[2][0]

            for e in events:
                killer = e[0]
                victim = e[1]

                # Where killer and killed are both cheaters (at some point)
                if killer in cheaters_directory and victim in cheaters_directory:
                    cheater_start_d = cheaters_directory[killer][0]
                    victim_start_d = cheaters_directory[victim][0]

                    # Finding real count of victims of cheating
                    if cheater_start_d <= match_d and victim_start_d > match_d:
                        sets.add(victim)
    
    return len(sets)


def find_killed_observers(match_directory):
    ''' Takes one argument - a match directory which holds
    various elements about each matches (key) characteristics.
    This function searches parent id (key in match_directory)
    for victims of the game who have observed abnormal killing
    behaviour. When abnormal killing behaviour is displayed by
    an active cheater then whoever is left in the match, but later
    killed, is added to a list for further analysis along with
    the date of parent id occurrence. 
    A list of lists is returned. Each inner element is a observer
    record with their date.
    '''
    
    all_players = []

    # For each match create an observers list
    for key, value in match_directory.items():
        cheaters = list(value[0])

        if len(cheaters) > 0:
            events = value[1]
            match_d = value[2][0]
            match_victims = list(value[3])

            # Temporary variables to track observers and cheater kills
            observers = match_victims[:]
            cheaters_kills = [0 for n in range(len(cheaters))]

            for e in events:
                killer = e[0]
                victim = e[1]

                observers.remove(victim)

                if killer in cheaters:
                    index = cheaters.index(killer)
                    cheaters_kills[index] += 1

                    # When cheater has 3 or more kills break loop
                    if any(i >= 3 for i in cheaters_kills):

                        # Remove active cheaters from observers list
                        for c in cheaters:
                            if c in observers:
                                observers.remove(c)

                        observers_d = [[b, match_d] for b in observers]
                        all_players.extend(observers_d)
                        break
    
    return all_players


def count_active_victims(ls_ls, cheaters_directory):
    ''' Takes a list of lists and a directory of ids as keys
    with a start and a stop date within the values.
    Assumes that within this list of lists the first element
    is an id that may be within the directory.
    If the id is within the directory, the second element of
    the inner list is checked to see that it is smaller than
    the id's start date, referenced from within the 
    directory.
    The ids which match the conditions are added to a set.
    The length of this set is returned.  
    '''
    
    first_exposure = keep_minimum(ls_ls)
    victim_tracking = set()
    
    for victim, min_match_d in first_exposure.items():
        
        # Checking id is in the directory
        if victim in cheaters_directory:
            cheater_start_d = cheaters_directory[victim][0]
            
            # Checking the exposure date is before cheating date
            if cheater_start_d > min_match_d:
                victim_tracking.add(victim)
    
    # Count of ids who match conditions is returned
    return len(victim_tracking)
 
    
def keep_minimum(ls_ls):
    ''' Takes one argument, a list of lists. The
    element's first index should be an ID which may
    occur multiples throughout the list of lists.
    The second index will be compared to lists with the
    same first index and assessed for its minimum.
    The function returns a dictionary with the id as
    key and the minimum comparable element as the value.
    '''
    
    dic = {}
    for id_key, comparable in ls_ls:
        if id_key not in dic:
            dic[id_key] = comparable
        else:
            
            # Reassign value when new object is
            # 'smaller' than current dictionary value
            if comparable < dic[id_key]:
                dic[id_key] = comparable
    
def create_shuffle_swap(players_dic):
    ''' Takes a dictionary where an ID is the key
    and there is a list of sub-ids as the value.
    Requires the use of the random package.
    Assumes that sub-ids list is holding unique values.
    The function returns a new dictionary with the
    sub-ids list in index 0 and the same sub-ids 
    but just shuffled in index 1.
    ''' 
    
    swap_dic = {}
    for key, value in players_dic.items():
        acc = list(value)
        shuffled_acc = random.sample(acc, len(acc))
        # Reassign unshuffled and shuffled sub-ids list
        swap_dic[key] = [acc, shuffled_acc] 
    return swap_dic


def shuffle_swap(swap_dic):
    ''' Takes a dictionary which holds a shuffled
    and an unshuffled list of sub-ids in its values
    as a list of lists. 
    The function takes the second list (which it assumes
    is being used in events data) and shuffles it.
    The original list and new shuffled list are assigned
    back to the dictionary it came from under the same
    key. Changes dicitonary in-place.
    '''
    
    for key, value in swap_dic.items():
        acc = value[1]
        shuffled_acc = random.sample(acc, len(acc))
        swap_dic[key] = [acc, shuffled_acc]
    return swap_dic


def players_shuffle_dic(match_players_dic):
    ''' Takes a dictionary as the only argument.
    Takes the values from each dictionary's key, 
    and shuffles the values using the random package 
    then reformats it into an iterator using cycle() 
    from itertools which is a necessary package.
    This function returns a new dictionary with the
    identical keys to the inputted dictionary but
    with the new iterator object in its values.
    '''

    new_dic = {}
    for key, value in match_players_dic.items():
        # Shuffling of values
        new_values = random.sample(value, len(value))
        # New iterator object from shuffled values
        new_dic[key] = cycle(new_values)
    return new_dic

        
def team_players_shfl(teams_data, match_players_dic):
    ''' Takes two arguments; data in a similar format to
    teams.txt, i.e. a list of lists, and a dictionary
    which holds sub-ids in the values of keys which are
    belonging to a parent id group. 
    The function returns the data object with a different
    assignment of teams to players (in the example of
    teams.txt data).
    This function changes in place - be sure to make a 
    copy of original data if this will cause inconvenience.
    '''
    
    dic = players_shuffle_dic(match_players_dic)
    
    for t in range(len(teams_data)):
        match = teams_data[t][0]
        player = teams_data[t][1]
        
        # Assignment of new player to teams_data
        replace_player = next(dic[match])
        teams_data[t][1] = replace_player  
    
    return teams_data
             


def indexing_shuffle(match_directory, events_swap_dic, swap_dic):
    ''' This function works to retain the order of events but 
    changes the sub-ids who were involved in those events under a 
    larger parent id. 
    The first argument is a match_directory, the second is a
    dictionary with key as parent id and values as a list of lists
    of observations. The second argument will change in place
    so a copy must be made before running this function to avoid 
    inconveniences. The third argument is the dictionary holding
    a list of list in values of shuffled sub-ids which will
    inform the reassignment process.
    The return of this function is the same match directory that was
    inputted. Only the second element (at index 1) is altered with 
    the new assignment process.
    '''
    
    for key, value in match_directory.items():
        events = value[1]
        
        for i, e in enumerate(events):
            killer = e[0]
            victim = e[1]
            
            # Reassign killer ids
            idx_killer = swap_dic[key][0].index(killer)
            events_swap_dic[key][i][0] = swap_dic[key][1][idx_killer]
            
            # Reassign victim ids
            idx_victim = swap_dic[key][0].index(victim)
            events_swap_dic[key][i][1] = swap_dic[key][1][idx_victim]
        
        # Setting reassigned events record to pre-existing
        # match_directory object.
        match_directory[key][1] = events_swap_dic[key]
    
    return match_directory


def reset_cheaters_observers(match_directory, cheaters_dic):
    ''' This function works to reset various elements
    of the match_directory object after changes to its 
    events observations.
    The first argument is a directory with information about
    each match in it - the cheaters set (first element) and the
    victims list (fourth element) are updated.
    The match_directory is returned changed. Make a copy of 
    the original match_directory before running the function
    to avoid any inconveniences from the changes.''' 
    
    # New dictionaries that will be inputted into directory
    cheaters_updated = {}
    victims_updated = {}
    
    for key, value in match_directory.items():
        cheaters_curent = value[0]
        events = value[1]
        match_d = value[2][0]
        observers_current = value[3]
        
        # Runnning through events to capture new data on
        # cheaters and victims in each match.
        for e in events:
            killer = e[0]
            victim = e[1]
            
            # Use of dictionary methods
            add_cheaters_dictionary(cheaters_updated, key, killer,
                                    match_d, cheaters_dic)
            add_dictionary_items(victims_updated, key, victim, sets=True)
        
        # Reassignment of new dictionaries to original argument
        match_directory[key][0] = cheaters_updated[key]
        match_directory[key][3] = victims_updated[key]

    return match_directory


    return dic

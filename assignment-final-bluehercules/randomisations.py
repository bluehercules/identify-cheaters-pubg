import random
from itertools import cycle
from dictionary_methods import add_dictionary_items, add_cheaters_dictionary
    
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



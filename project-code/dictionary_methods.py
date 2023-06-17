import datetime


def add_cheaters_dictionary(dictionary, key, value, match_date, cheaters_directory):
    ''' A specific function to add active cheaters
    to a pre-existing dictionary. The function takes 
    five arguments.
    If the key is not in the dictionary, it will create
    that key with an empty set as the value. If the key
    is in the dictionary then the value will be added
    to the set only if the value (ie. the player) is
    actively cheating. We can cross-check the player's
    start cheating date by referencing the cheaters_directory.
    This function changes the dictionary in place.
    '''
    
    # Creating dictionary with key and value as an empty set
    if key not in dictionary:
        dictionary[key] = set()
    
    # Adding killer if they are an active cheater
    if value in cheaters_directory:
        cheater_start_d = cheaters_directory[value][0]
        
        if cheater_start_d <= match_date:
            if value not in dictionary[key]:
                dictionary[key].add(value)
    
    # We do not check cheating stop date on the assumption that 
    # the player was banned from the game and is no longer
    # actively playing on PUBG.


def add_dictionary_items(dictionary, key, value, sets=False):
    ''' Adds a value to a pre-existing dictionary.
    If the key where the value is to be inputted does
    not exist then the key is also create within the 
    dictionary. If sets is set to True then the value is
    not added to the key if it is already there.
    The function returns the dictionary but
    it is important for the user to know that this
    function changes the dictionary in place and does
    not create a copy.
    '''
    
    if key in dictionary:
        if sets == False:
            dictionary[key].append(value)
        else:
            if value not in dictionary[key]:
                dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def slicing_teams(teams_data, cheaters_directory):
    ''' The purpose of this funciton is to slice the 
    teams data into three dictionaries'''
    
    match_teams_cheaters = {}
    match_teams = {}
    match_players = {}

    for r in range(len(teams_data)):
        match = teams_data[r][0]
        player = teams_data[r][1]
        team = teams_data[r][2]

        if player in cheaters_directory:
            add_dictionary_items(match_teams_cheaters, match, team)

        add_dictionary_items(match_teams, match, team, sets=True)
        add_dictionary_items(match_players, match, player)
    
    return match_teams_cheaters, match_teams, match_players

def create_directory(data, cheaters_directory):
    ''' Take data as a list of lists similar to the 
    makeup of the kills.txt dataset. This function
    creates a directory from the various objects in 
    the dataset provided. The second argument is a
    directory pertaining to cheating behaviour.
    Match date must be meticulously calculated:
    There are few scenarios where the date from
    the kill datetime will be different from the min
    to max kills of that match. We only deepdive into 
    matches that have a kill on or before 1am since
    these are the matches which could potentially
    begin the previous day.
    The function returns five dictionary objects, each
    pertaining to a different characteristic of the data.
    '''
    
    cheaters = {}
    events = {}
    date = {}
    victims = {}
    players = {}
    
    # This date is out of range of observations
    # so will always work as biggest
    min_d = datetime.date(2019, 3, 11)

    for r in range(len(data)):
        match = data[r][0]
        killer = data[r][1]
        victim = data[r][2]
        kill_dt = data[r][3]

        # Setting default match date as the date of a kill time
        kill_d = kill_dt.date()
        data[r].append(kill_d)
        # Any kills on or after 1am must be from a match of that same
        # day; it is not feasible that the match began the day before
        # assuming matches have a max duration of approx. 50 mins.
        # Reference: https://theglobalgaming.com/gaming/average-match-time-length-pubg
        if kill_dt.hour <= 1:
            data[r][4] = min_d 
            if kill_d < min_d:
                data[r][4] = kill_d 
        match_d = data[r][4]

        add_cheaters_dictionary(cheaters, match, killer,
                                match_d, cheaters_directory)
        add_dictionary_items(events, match, [killer, victim, kill_dt])
        add_dictionary_items(date, match, match_d, sets=True)
        add_dictionary_items(victims, match, victim, sets=True)
        add_dictionary_items(players, match, killer, sets=True)
        add_dictionary_items(players, match, victim, sets=True)

    return cheaters, events, date, victims, players
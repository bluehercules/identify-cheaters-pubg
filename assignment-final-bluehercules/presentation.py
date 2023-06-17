import numpy as np
import statsmodels.stats.api as sms


def print_counter(counter):
    ''' Takes a Counter dictionary as the only argument.
    Iterates through the key and value of the Counter and
    prints each specifically assuming that it is for the
    actual count of [key] number of cheaters on [value]
    number of teams.
    '''

    for i, j in counter:
        if i != 1:
            print('Teams with', i, 'cheaters')
        else:
            print('Teams with', i, 'cheater')
        print('Actual:', j, end='\n\n')


def print_counter_expected(ls_ls):
    ''' Iterates over a list of lists. Assumes that
    the index of each inner list is the same number 
    as how many cheaters are on that team. 
    Calculates the mean and 95% confidence interval
    for each inner list. 
    Requires use of numpy and statsmodels packages.
    Returns multiple print statements.'''
    
    for i, e in enumerate(ls_ls):
        
        # Prints output for teams with cheaters
        if len(e) > 0:
            mean = round(np.mean(e), 1)
            ci = sms.DescrStatsW(e).tconfint_mean()
            tup = ()

            # Rounding confidence interval values
            for c in ci:
                val = (round(c, 1),)
                tup = tup + val
            
            # Print statements
            if i != 1:
                print('Teams with', i, 'cheaters')
            else:
                print('Teams with', i, 'cheater')
            print('Expected (mean) (rounded):', mean)
            print('95% Confidence Interval (rounded):', tup, end='\n\n')

        # Prints output where there are no teams with cheaters 
        if len(e) == 0:
            print('There are no teams with', i, 'cheaters.')
        
        
def print_actual_expected(actual, expected_ls):
    ''' Formatting manipulation for a series of numbers.
    Two arguments are recieved - the first should be a
    figure for the actual count, the second should be
    a list of expected counts.
    Requires use of numpy and statsmodels packages.
    We use the second argument to calculate the mean and 
    95% confidence interval that are printed.
    Created values are placed into print statements 
    before being returned. The user should ensure correct
    ordering (or name assignment) of arguments to avoid
    a mixup with the presentation of values.''' 
    
    # Calculating mean and confidence intervals for raw data
    expected_mean = np.mean(expected_ls)
    expected_ci = sms.DescrStatsW(expected_ls).tconfint_mean()
    
    tup = ()
    # Rounding confidence interval values
    for i in expected_ci:
        val = (round(i, 2),)
        tup = tup + val
    
    print('Actual: ', actual)
    print('Expected: ', expected_mean)
    print('95% Confidence Interval (rounded): ', tup)
    

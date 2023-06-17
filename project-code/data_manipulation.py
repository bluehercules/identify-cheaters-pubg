from datetime import datetime, date


def open_txt(path, date_idx=None, dt=False, date_idx_2=None, dt2=False, intg=None):
    ''' Functions accesses and reads a txt file using the 
    for...open method. Each line is stripped and split
    for \t values. The only mandatory argument is the path
    argument which directs the function to the relative 
    path of where the txt file is stored.
    There are five optional arguments. date_idx and date_idx_2
    are by default None. If there is an element in the
    list that should be converted to a date object then the
    index should be inputted here. The str_to_date function
    is applied to the date_string with the default output
    as 'date'. If dt (or dt2) is set to True then the 
    format will be a 'datetime' object. intg asks for 
    the index of any elements that should be converted to
    an integer datatype.
    date_idx, date_idx_2 and intg only take integers as input.
    A list of lists is returned.
    '''

    ls = []

    for line in open(path, 'r'):
        strip_split = line.strip().split('\t')
        
        # Formatting date objects for first position
        if date_idx != None:
            if dt == True:
                strip_split[date_idx] = str_to_date(strip_split[date_idx],
                                                    'datetime')
            else:
                strip_split[date_idx] = str_to_date(strip_split[date_idx],
                                                    'date')

        # Formatting date objects for second position
        if date_idx_2 != None:
            if dt == True:
                strip_split[date_idx_2] = str_to_date(strip_split[date_idx_2],
                                                      'datetime')
            else:
                strip_split[date_idx_2] = str_to_date(strip_split[date_idx_2],
                                                      'date')
        
        # Formatting integer objects for index specified
        if intg != None:
            strip_split[intg] = int(strip_split[intg])

        ls.append(strip_split)
    
    return ls
        

def index_set(ls_ls, idx):
    ''' Function creates and returns a set from the 
    indexed element of a list of lists.
    '''
    
    ls = [i[idx] for i in ls_ls]
    return set(ls)


def str_to_date(date_string, formatting):
    ''' The first argument takes a string and uses
    the second argument which is a indicator of the
    format which should be returned. The second argument
    is limited to 'date' (which outputs '%Y-%m-%d')
    or 'datetime' (which outputs '%Y-%m-%d %H:%M:%S.%f')
    objects. 
    The function returns a new object in date/datetime
    format.
    '''
    
    if formatting == 'date':
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_string, date_format)
        return date_obj.date()
    
    else:
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        dt_obj = datetime.strptime(date_string, date_format)
        return dt_obj  

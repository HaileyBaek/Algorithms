# Your name, Cornell NetID
# Haomiao Han (hh696)
# Your Partner's name, Cornell NetID
# Hyein Baek (hb437)

# DO NOT CHANGE THIS CLASS
class RespaceTableCell:
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.validate()

    # This function allows Python to print a representation of a RespaceTableCell
    def __repr__(self):
        return "(%s,%s)"%(str(self.value), str(self.index))

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.value) == bool), "Values in the respacing table should be booleans."
        assert(self.index == None or type(self.index) == int), "Indices in the respacing table should be None or int"

# Inputs: the dynamic programming table, indices i, j into the dynamic programming table, the string being respaced, and an "is_word" function.
# Returns a RespaceTableCell to put at position (i,j)
def fill_cell(T, i, j, string, is_word):
    #TODO: YOUR CODE HERE
    curr_word = string[i:j+1]
    next_idx = None
    result = False
    
    if is_word(curr_word):
        if j < len(string) - 1:
            if T.get(j+1, len(string)-1).value == True:
                result = True
                next_idx = j+1
        else:
            result = True
            next_idx = j+1
    elif j == len(string) - 1:
        found = False
        for col in range(i, j):
            if T.get(i, col).value == True:
                found = True
                break

        if found:
            result = True

    #print i, j, result, next_idx
    return RespaceTableCell(result, next_idx)
                  
# Inputs: N, the size of the list being respaced
# Outputs: a list of (i,j) tuples indicating the order in which the table should be filled.
def cell_ordering(N):
    #YOUR CODE HERE
    cell_order = []
    if (N == 0):
        raise ValueError('input string length is 0')

    for i in range(N, -1, -1):
        for j in range(i, N):
            cell_order.append((i, j))

    return cell_order

# Input: a filled dynamic programming table.
# (See instructions.pdf for more on the dynamic programming skeleton)
# Return the respaced string, or None if there is no respacing.
def respace_from_table(s, table):
    result = ''
    unformatted_result = ''
    
    i = 0
    while i < len(s):
        found = False
        for j in range(i, len(s)):
            if table.get(i, j).value is True:
                result = result + s[i:j+1] + ' '
                unformatted_result += s[i:j+1]
                found = True
                break
                
        if found:
            i = table.get(i, j).index
        else:
            i += 1

    if len(unformatted_result) != len(s):   ##make sure that the result string has same 
                                            ##length as the original input string
        return None
    else:
        return result[:-1]                  ##getting rid of the final space

if __name__ == "__main__":
    # Example usage.
    from dynamic_programming import DynamicProgramTable
    s = "itwasthebestoftimes"
    wordlist = ["of", "it", "the", "best", "times", "was"]
    D = DynamicProgramTable(len(s) + 1, len(s) + 1, cell_ordering(len(s)), fill_cell)
    D.fill(string=s, is_word=lambda w:w in wordlist)
    print respace_from_table(s, D)

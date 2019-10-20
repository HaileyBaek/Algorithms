# Your name, Cornell NetID
# Haomiao Han (hh696)
# Your Partner's name, Cornell NetID
# Hyein Baek (hb437)

import dynamic_programming

# DO NOT CHANGE THIS CLASS
class DiffingCell:
    def __init__(self, s_char, t_char, cost):
        self.cost = cost
        self.s_char = s_char
        self.t_char = t_char
        self.validate()

    # Helper function so Python can print out objects of this type.
    def __repr__(self):
        return "(%d,%s,%s)"%(self.cost, self.s_char, self.t_char)

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.cost) == int), "cost should be an integer"
        assert(type(self.s_char) == str), "s_char should be a string"
        assert(type(self.t_char) == str), "t_char should be a string"
        assert(len(self.s_char) == 1), "s_char should be length 1"
        assert(len(self.t_char) == 1), "t_char should be length 1"

# Input: a dynamic programming table,  cell index i and j, the input strings s and t, and a cost function cost.
# Should return a DiffingCell which we will place at (i,j) for you.
def fill_cell(table, i, j, s, t, cost):
    # YOUR CODE HERE
    char_si = '-'
    if i != 0:
        char_si = s[i-1]
        
    char_tj = '-'
    if j != 0:
        char_tj = t[j-1]

    char_put_l = '-'
    char_put_r = '-'
    
    if (i != 0) and (j != 0):
        cost_from_upper_left = table.get(i-1, j-1).cost + cost(char_si, char_tj)
        cost_from_left = table.get(i, j-1).cost + cost('-', char_tj)
        cost_from_up = table.get(i-1, j).cost + cost(char_si, '-') 

        current_cell_cost = min(cost_from_upper_left, cost_from_left, cost_from_up)
        if cost_from_upper_left == current_cell_cost:
            char_put_l = char_si
            char_put_r = char_tj
        elif cost_from_left == current_cell_cost:
            char_put_r = char_tj
        else:
            char_put_l = char_si
    elif (i == 0) and (j == 0):
        current_cell_cost = 0
    elif i == 0:
        current_cell_cost = table.get(i, j-1).cost + cost('-', char_tj)
        char_put_r = char_tj
    else:
        current_cell_cost = table.get(i-1, j).cost + cost(char_si, '-')
        char_put_l = char_si

    #print char_si, char_tj, current_cell_cost
    #print char_put_l, char_put_r
    return DiffingCell(char_put_l, char_put_r, current_cell_cost)

# Input: n and m, represents the sizes of s and t respectively.
# Should return a list of (i,j) tuples, in the order you would like fill_cell to be called
def cell_ordering(n,m):
    # YOUR CODE HERE
    order_list = []

    if (n == 0) and (m == 0):
        raise ValueError('Both of the input strings are empty')

    if (n == 0) or (m == 0):
        print "WARNING: one of the input string is empty"
        
    for i in range(0, n+1):
        order_list.append((i, 0))
    for j in range(1, m+1):
        order_list.append((0, j))

    for i in range(1, n+1):
        for j in range(1, m+1):
            order_list.append((i, j))

    #print order_list          
    return order_list

# Returns a size-3 tuple (cost, align_s, align_t).
# cost is an integer cost.
# align_s and align_t are strings of the same length demonstrating the alignment.
# See instructions.pdf for more information on align_s and align_t.
def diff_from_table(s, t, table):
    # YOUR CODE HERE
    path_s = ''
    path_t = ''
    
    i = len(s)
    j = len(t)
    cost = table.get(i, j).cost
    
    while i >= 0 and j >= 0:
        current_cell = table.get(i, j)
        path_s = current_cell.s_char + path_s
        path_t = current_cell.t_char + path_t

        if current_cell.s_char == '-':
            j -= 1
        elif current_cell.t_char == '-':
            i -= 1
        else:
            i -= 1
            j -= 1
    
    return (cost, path_s[1:], path_t[1:])

# Example usage
if __name__ == "__main__":
    # Example cost function from instructions.pdf
    def costfunc(s_char, t_char):
        if s_char == t_char: return 0
        if s_char == 'a':
            if t_char == 'b': return 5
            if t_char == 'c': return 3
            if t_char == '-': return 2
        if s_char == 'b':
            if t_char == 'a': return 1
            if t_char == 'c': return 4
            if t_char == '-': return 2
        if s_char == 'c':
            if t_char == 'a': return 5
            if t_char == 'b': return 5
            if t_char == '-': return 1
        if s_char == '-':
            if t_char == 'a': return 3
            if t_char == 'b': return 3
            if t_char == 'c': return 3

    import dynamic_programming
    s = "acb"
    t = "baa"
    D = dynamic_programming.DynamicProgramTable(len(s) + 1, len(t) + 1, cell_ordering(len(s), len(t)), fill_cell)
    D.fill(s = s, t = t, cost=costfunc)
    (cost, align_s, align_t) = diff_from_table(s,t, D)
    print align_s
    print align_t
    print "cost was %d"%cost

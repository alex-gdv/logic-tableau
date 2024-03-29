#No import statements.

MAX_CONSTANTS = 10
PROP = ["q", "r", "p", "s"]
CON = ["^", "v", ">"]

def split_main_con(fmla):
    _neg = False    
    if fmla[0] == "-" and fmla[1] == "-":
        _neg = False
        fmla = fmla[2:]
    if fmla[0] == "-":
        _neg = True
        fmla = fmla[1:]
    brackets = 0
    for i in range(len(fmla)):
        if fmla[i] == "(":
            brackets+=1
        elif fmla[i] == ")":
            brackets-=1
        if fmla[i] in CON and brackets == 1:
            _lhs = fmla[1:i]
            _rhs = fmla[i+1:-1]
            _con = fmla[i]
        elif fmla[i] in PROP and brackets == 0:
            _lhs = fmla[i]
            _rhs = None
            _con = None
    return [_neg, _lhs, _con, _rhs]

# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    negation = False
    if fmla[0] == "-":
        negation = True
        fmla = fmla[1:]
    if fmla in PROP and negation:
        return 7
    elif fmla in PROP:
        return 6
    output = 0
    brackets = 0
    for i in range(len(fmla)):
        if fmla[i] == "(":
            brackets+=1
        elif fmla[i] == ")":
            brackets-=1
        if fmla[i] in CON and brackets == 1:
            lhs = fmla[1:i]
            rhs = fmla[i+1:-1]
            output_lhs = parse(lhs)
            output_rhs = parse(rhs)
            nums = [6,7,8]
            if output_lhs in nums and output_rhs in nums:
                output = 8
    if output != 0 and negation:
        output = 7
    return output

# Return the LHS of a binary connective formula
def lhs(fmla):
    return ''

# Return the connective symbol of a binary connective formula
def con(fmla):
    return ''

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    return ''

def add_neg(fmla):
    return "-" + fmla

def is_contradictory(lst):
    for elem in lst:
        if elem in PROP:
            neg_elem = add_neg(elem)
            if neg_elem in lst:
                return True
    return False

# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    tab = [[fmla]]
    branch_index = 0
    elem_index = 0
    while len(tab) != 0:
        neg, lhs, con, rhs = split_main_con(tab[branch_index][elem_index])
        if False:
            pass
        else:#alpha
            if not neg and con == "^":
                tab[branch_index].append(lhs)
                tab[branch_index].append(rhs)
            elif neg and con == "v":
                tab[branch_index].append(add_neg(lhs))
                tab[branch_index].append(add_neg(rhs))
            elif neg and con == ">":
                tab[branch_index].append(lhs)
                tab[branch_index].append(add_neg(rhs))
            elif not neg and con is None:
                tab[branch_index].append(lhs)
            # beta
            if not neg and con == "v":
                tab[branch_index].append(lhs)
                tab.append([rhs])
            elif not neg and con == ">":
                tab[branch_index].append(add_neg(lhs))
                tab.append([rhs])
            elif neg and con == "^":
                tab[branch_index].append(add_neg(lhs))
                tab.append([add_neg(rhs)])
    return None

#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    return 0

#DO NOT MODIFY THE CODE BELOW
f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)

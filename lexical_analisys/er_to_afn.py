"""
Thompson Algorithm
Andreina Mendes - 485306
"""

import json

# Global variables to increase the specified states for every conective processing
index_states = 1
index_or = 0
index_and = 0
index_asterisk = 0
index_plus = 0

"""
I make this code and when i was make a unique automaton using all tokens, a had a lot problems, because the symbols used to represent the operators, was used in my tokens, so a i have to change the symbol for every operator and now i can use the old siymbols in the RE's.
So now, i have this operators:
    + -> @
    * -> #
    | -> ~
    . -> .
"""

"""
create_AFN()
    -> Function to model an NFA in a dict format.
    -> The variables states and transitions is defined as lists and accept_states is defined as dict
    -> The transitions were defined as dictionaries, and each dictionary has the state in question as the key and another dictionary as the result, which contains the symbols as the key and the set of states that are the path passing that particular symbol.
"""

def create_AFN(states, transitions, initial_state, accept_states):
    AFN = {}

    AFN.update({'states': states})
    AFN.update({'transitions': transitions})
    AFN.update({'initial_state': initial_state})
    AFN.update({'accept_states': accept_states})

    return AFN

"""
kleene_lock()
    -> Function to make the processing '#' and '@' operators from a NFA param.
    -> From a boolean variable, the function choose if the conection to the new start state to the new last state will be maked.
    -> Case that will be maked, the processing will be relation to '#' operator, else, the processing will be relation to '@' operator.
    -> The conection to the new start state to the new last state is the unique diference betwen '#' and '@' operators processing.
    -> For every operator processed the global variable assosiated to the operator will be increase in 2, because two new states was created.
"""

def kleene_lock(AFN1, just_kleene):
    transitions = {}

    if just_kleene:
        global index_asterisk

        initial_state = f'k{index_asterisk}'
        accept_state = f'k{index_asterisk+1}'
        
        transitions[initial_state] = {}
        transitions[initial_state][''] = []
        transitions[initial_state][''].append(accept_state)

        index_asterisk += 2
    else:
        global index_plus

        initial_state = f'p{index_plus}'
        accept_state = f'p{index_plus+1}'

        index_plus += 2

    transitions[initial_state] = {}
    transitions[initial_state][''] = []
    transitions[initial_state][''].append(AFN1['initial_state'])
    transitions.update(AFN1['transitions'])

    for final in AFN1['accept_states']:
        transitions[final] = {}
        transitions[final][''] = []
        transitions[final][''].append(accept_state)

    transitions[accept_state] = {}
    transitions[accept_state][''] = []
    transitions[accept_state][''].append(AFN1['initial_state'])

    states = [initial_state] + AFN1['states'] + [accept_state]

    return create_AFN(states, transitions, initial_state, {accept_state:''})

"""
union()
    -> Function to make the operator processing '~'.
    -> Creates a new initial and final states and makes the transition betwen the new initial state to the initial states from both automatons passing epsilon.
    -> Adds the transitions of both automata in the transitions dictionary.
    -> Creates a new transition from the final states to the both automatons to the new final state  passing epsilon.
    -> The global variable  to the operator '~' will be increase in 2, because two new states was created.
"""

def union(AFN1, AFN2):
    global index_or
    
    transitions = {}
    initial_state = f'u{index_or}'
    accept_state = f'u{index_or+1}'
    
    transitions[initial_state] = {}
    transitions[initial_state][''] = []
    transitions[initial_state][''].append(AFN1['initial_state'])
    transitions[initial_state][''].append(AFN2['initial_state'])

    transitions.update(AFN1['transitions'])
    transitions.update(AFN2['transitions'])
    
    finals = {}
    finals.update(AFN1['accept_states'])
    finals.update(AFN2['accept_states'])

    for final in finals.keys():
        transitions[final] = {}
        transitions[final][''] = []
        transitions[final][''].append(accept_state)

    states = [initial_state] + AFN1['states'] + AFN2['states'] + [accept_state]

    index_or += 2

    return create_AFN(states, transitions, initial_state, {accept_state:''})

"""
concat()
    -> Function to make the operator processing '.'.
    -> Creates a mid state in the meadle of the two automatons and makes the transition betwen the final of the first automaton to the initial of the new state passing epsilon.
    -> Adds the transitions of the two automata in the transitions dictionary.
    -> Creates a new transition from the final of the new state to the initial state of the second automaton passing epsilon.
    -> The global variable  to the operator '.' will be increase in 2, because two new states was created.
"""

def concat(AFN1, AFN2):
    global index_and
    c_state = f'c{index_and}'

    transitions = {}
    transitions.update(AFN1['transitions'])

    for state in AFN1['accept_states']:
        transitions[state] = {}
        transitions[state][''] = []
        transitions[state][''].append(c_state)

    transitions[c_state] = {}
    transitions[c_state][''] = []
    transitions[c_state][''].append(AFN2['initial_state'])
    transitions.update(AFN2['transitions'])

    new_states = AFN1['states'] + [c_state] + AFN2['states']

    index_and += 1

    return create_AFN(new_states, transitions, AFN1['initial_state'], AFN2['accept_states'])


"""
make_operation()
    -> Function to see witch operator will be processed.
    -> The funcion gets a stack containing a automaton for every alphanumeric symbol and the operator betwen then, returned of prepare_list() function.
    -> The stack will be splited in two stacks, a stack to letters, and a stack to operators, and the stacks will be removed all elements when the operator will be discovered, to send for the specified functon of this operator.
"""

def make_operation(stack):
    AFN = {}
    symbol = [x for x in stack if type(x) == dict]
    conectives = [x for x in stack if x in ['~', '#', '@', '.']]
    
    if len(conectives) == 0:
        return symbol.pop()

    while (len(conectives) != 0):
        con = conectives.pop()

        if con == '.':
            AFN1 = symbol.pop()
            AFN2 = symbol.pop()
            AFN = concat(AFN2, AFN1)
            symbol.append(AFN)
        elif con == '~':
            AFN1 = symbol.pop()
            AFN2 = symbol.pop()
            AFN = union(AFN2, AFN1)
            symbol.append(AFN)
        elif con == '#':
            AFN1 = symbol.pop()
            AFN = kleene_lock(AFN1, True)
            symbol.append(AFN)
        elif con == '@':
            AFN1 = symbol.pop()
            AFN = kleene_lock(AFN1, False)
            symbol.append(AFN)

    return AFN

"""
prepare_list()
    -> Function to create a automaton for every alphanumeric symbol in the RE, and make a list with the  automatons generateds having the specify operator in the RE betwen then. 
"""

def prepare_list(er):
    list_ER = []
    global index_states
    symbols = ['{', '}', ',', '\'', '"', ';', '[', ']', '+', '=', '-', '*', '/', '%', '!', '>', '<', '&', '|']

    for symbol in er:
        if symbol.isalnum() or symbol in symbols:
            transition = {}
            initial_state = f'q{index_states}'
            accept_state = f'q{index_states+1}'
            
            transition[initial_state] = {}
            transition[initial_state][symbol] = []
            transition[initial_state][symbol].append(accept_state)
            states = [initial_state] + [accept_state]

            AFN = create_AFN(states, transition, initial_state, {accept_state:''})

            list_ER.append(AFN)
            index_states += 2
        else:
            list_ER.append(symbol)

    return list_ER

"""
convert_ER_to_AFN()
    -> Function to receive the RE inputed and get the result of prepare_list().
    -> Send every element in this result to the function make_operation() using the symbols '(' and ')' to make a precedency order and process the Re correctly.
"""

def convert_er_to_afn(er):
    stack = []
    AFN = {}
    list_ER = prepare_list(er)

    for symbol in list_ER:
        if symbol != ')':
            stack.append(symbol)
        elif symbol == ')':
            aux_stack = []

            while len(stack) > 0:
                verify = stack.pop()

                if verify != '(':
                    aux_stack.append(verify)
                else:
                    break
                
            aux_stack.reverse()
            AFN = make_operation(aux_stack)
            stack.append(AFN)

    return AFN

"""
join_afns()
    -> Creates a noto 'root' state and creates a transition from it to the beginning of each automaton passed as parameter.
    -> Adds the states of each automaton in a variable to compose the states of a single final automaton.
    -> Adds each automata's final state in a variable to compose the set of final states of the final automaton.
"""

def join_afns(afns):
    initial_state = 'q0'
    accept_states = {}
    states = [initial_state]
    
    transitions = {}
    transitions[initial_state] = {}
    transitions[initial_state][''] = []
    
    for afn in afns:
        transitions[initial_state][''].append(afn['initial_state'])
        transitions.update(afn['transitions'])
        
        states += afn['states']
        accept_states.update(afn['accept_states'])
        
    return create_AFN(states, transitions, initial_state, accept_states)

"""
main
    -> Converts the json file from tokens and converts it to a python dictionary.
    -> For each token, generates an automaton that has the indexing of this token in the final state value.
    -> Sends all automata from each re to the join_afns() function to join them all into the same initial state and have only one nfa.
"""

if __name__ == "__main__":
    with open('tokens.json') as json_file:
        tokens = json.load(json_file)
    
    afns = []
    
    for token, er in tokens.items():
        afn = convert_er_to_afn(er)
        accept_state = list(afn['accept_states'].keys())[0]
        afn['accept_states'][accept_state] = token
        afns.append(afn)
        
    with open("afn.json", "w") as file:
        json.dump(join_afns(afns), file, indent=4)
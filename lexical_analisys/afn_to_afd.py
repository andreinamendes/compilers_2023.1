"""
Conversão de AFN para AFD
Andreina Mendes - 485206
"""

import json

# Global variables
afn_transitions = {}
afn_initial_state = ''
afn_accept_states = {}
afn_states = []

"""
create_afd()
    -> Function to model an DFA in a dict format.
    -> The variables states and transitions is defined as lists and accept_states is defined as dict
    -> The transitions were defined as dictionaries, and each dictionary has the state in question as the key and another dictionary as the result, which contains the symbols as the key and the set of states that are the path passing that particular symbol.
"""

def create_afd(states, transitions, initial_state, accept_states):
    AFD = {}

    AFD.update({'states': states})
    AFD.update({'transitions': transitions})
    AFD.update({'initial_state': initial_state})
    AFD.update({'accept_states': accept_states})

    return AFD

"""
edge()
    -> Takes all transitions from a state and a symbol and returns as edges of this transition
    -> If the symbol is ' ', it means that it is a closure operation, so the state passed in must be added to the result
"""

def edge(s, symbol):
    edge_states = []
    
    if symbol == '':
        edge_states += [s]

    if s in list(afn_transitions.keys()) and symbol in list(afn_transitions[s].keys()):
        edge_states += afn_transitions[s][symbol]

    return edge_states

"""
DFAedge()
    -> Gets the edges for a specific transition function
    -> Gets the closure of edges to eliminate epsilon transitions
"""

def DFAedge(d, symbol):
    edges = []    
    
    for s in d:
        edges += edge(s, symbol)
    
    for s in edges:
        edges += edge(s, '')
        edges = list(set(edges))

    return edges

"""
convert_afn_to_afd()
    -> Initializes DFA variables
    -> Generates the initial DFA state with a closure of the initial NFA state and closes these to eliminate epsilon transitions
    -> Generate all DFA states by mapping each transition from each NFA state to each symbol of the alphabet
    -> Adds all states into the DFA states
    -> Generates all DFA transitions 
using all the NFA states present in each DFA state and merging them
    ->Generate all final states by checking that for each added state at least one is a final state in the NFA
"""

def convert_afn_to_afd():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '{', '}', ',', '\'', '"', ';', '%', '=', '[', ']', '+', '-', '*', '/', '!', '>', '<', '&', '|']
    
    states = []
    transitions = {}
    accept_states = {}
    initial_state = edge(afn_states[0], '')
    
    for i in initial_state:
        initial_state += edge(i, '')
        initial_state = list(set(initial_state))
    
    states.append(initial_state)

    for state in afn_states:
        for char in alphabet:
            states.append(DFAedge([state], char))
            
    states = [a for a in states if a != []]
    
    for state in states:
        for c in alphabet:
                afd_edge = DFAedge(state, c)
                
                if afd_edge != []:
                    transitions.update({str(state):{c:afd_edge}})
                    
    for state in states:
        for s in state:
            if s in list(afn_accept_states.keys()):
                accept_states.update({s:afn_accept_states[s]})

    return create_afd(states, transitions, initial_state, accept_states)

"""
start_afn()
    -> Starts a NFA with all the information contained in the input json
    -> Assigns the data in global variables to each key in the NFA json file
"""

def start_afn():
    with open('afn.json') as json_file:
        afn = json.load(json_file)

    global afn_transitions, afn_states, afn_initial_state, afn_accept_states

    afn_initial_state = afn['initial_state']
    afn_accept_states = afn['accept_states']
    afn_transitions = afn['transitions']
    afn_states = afn['states']


"""
main
    -> Initializes the NFA data and generates a json file for the DFA resulting from the convert_afn_to_dfa() function call
"""

if __name__ == '__main__':
    start_afn()

    with open("afd.json", "w") as file:
        json.dump(convert_afn_to_afd(), file, indent=4)
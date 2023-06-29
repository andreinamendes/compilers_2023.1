"""
Andreina Mendes - 485306
"""

import json

# Global variables
afd_transitions = {}
afd_initial_state = ''
afd_accept_states = {}
afd_states = []

"""
processing()
    -> Create a current state and initialize it with the initial DFA state
    -> For each symbol, get the next state by passing that symbol until you run out of symbols
    -> At the end, check if the current state is part of the group of final DFA states, if so, return the token associated to this state
"""

def processing(inp):
    current_state = afd_initial_state
    
    for c in inp:
        if current_state in afd_transitions.keys() and c in afd_transitions[current_state]:
            current_state = afd_transitions[current_state][c]

    if current_state in afd_accept_states.keys():
        return afd_accept_states[current_state]
    else:
        return 'ERROR'

"""
start_afd()
    -> Starts a DFA with all the information contained in the input json
    -> Assigns the data in global variables to each key in the DFA json file
"""

def start_afd():
    with open('test.json') as json_file:
        afd = json.load(json_file)
        
    global afd_transitions, afd_states, afd_initial_state, afd_accept_states

    afd_initial_state = afd['initial_state']
    afd_accept_states = afd['accept_states']
    afd_transitions = afd['transitions']
    afd_states = afd['states']
    
"""
main
    -> Take the whole input and do a split using the space as parameter generating a vector
    -> For each element of the array, call the processing() function and get the return token for that word
    -> If the processing() function returns 'ERROR', the word was not recognized by the automaton
    -> Show all generated tokens
"""

if __name__ == "__main__":
    # Test
    # int a = 0
    
    start_afd()
    
    inp = []
    
    for x in range(3):
        inp += input().split(' ')
        inp += ['\n']
    
    output = []
    
    for i in inp:
        if i != '\n':
            verify = processing(i)
            
            if verify != 'ERROR':
                output.append(verify)
            else:
                print(verify)
        else:
            output.append(i)

    for out in output:
        print(out, end='')
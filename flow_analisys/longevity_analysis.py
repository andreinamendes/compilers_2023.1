import pprint

def def_use_block(blocks):
  for _, block in blocks.items():
    prev_expressions = []

    for instruction in block['instructions']:
      if 'if' not in instruction and 'return' not in instruction and 'goto' not in instruction:
        possible_var_defined = instruction[0]
        possible_vars_used = [char for char in instruction[2:] if char.isalpha()]
        
        if possible_var_defined not in instruction[2:] and possible_var_defined not in prev_expressions:
          prev_expressions = instruction[2:]
          block['DEF'].add(possible_var_defined)
        
        block['USE'].update(var for var in possible_vars_used if var not in block['DEF'])

  return blocks

def analysis_in(blocks, id):
  out = blocks[id]['OUT']
  
  for elem in blocks[id]['DEF']:
    out.discard(elem)
    
  return blocks[id]['USE'].union(out)

def analysis_out(blocks, id):
  success_in = set()
  
  for succ in blocks[id]['successors']:
    if succ != 0:
      success_in.update(blocks[succ]['IN'])
  
  return success_in

def longevity_analysis(blocks):
  changes = True

  while changes:
    prevs_in, prevs_out = [blocks[i]['IN'] for i in blocks], [blocks[i]['OUT'] for i in blocks]
    
    for id in reversed(blocks):
      blocks[id]['OUT'].update(analysis_out(blocks, id))
      blocks[id]['IN'].update(analysis_in(blocks, id))
      
    if prevs_in == [blocks[i]['IN'] for i in blocks] and prevs_out == [blocks[i]['OUT'] for i in blocks]:
      changes = False
    
  return blocks

def create_block(num_block, instructions, predecessors, successors):
  block = {
    num_block: {
      'instructions': instructions,
      'predecessors': predecessors,
      'successors': successors,
      'DEF': set(),
      'USE': set(),
      'IN': set(),
      'OUT': set()
    }
  }

  return block

def get_entry():
  blocks = {}
  predecessors = None

  while True:
    num_block, num_inst = [int(x) for x in input().split(' ')]
    instructions = [input().replace(' ', '') for _ in range(num_inst)]
    successors = input()
    
    if len(successors) > 1:
      successors = [int(x) for x in successors.split(' ')]
    else:
      successors = [int(successors)]
      
    blocks.update(create_block(num_block, instructions, predecessors, successors))
    predecessors = [num_block]

    if successors == [0]:
      break

  return blocks

if __name__ == '__main__':
  blocks = get_entry()
  blocks = def_use_block(blocks)
  blocks = longevity_analysis(blocks)
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(blocks)

''' Entrada
1 2
a= a+c
b= 4-a
2
2 1
b=20*c
3
3 2
d = a+b
b = 0
0

Bloco |  DEF |  USE
1     |  b   |  a, c
2     |  b   |  c
3     |  d   |  a, b

Bloco |  IN  |  OUT
1     | a, c | a, c 
2     | a, c | a, b
3     | a, b | {}

1 1
a=0
2
2 4
b=a+1
c=c+b
a=b+2
if a < N goto 2
3 2
3 1
return c
0

Bloco |  DEF |  USE
1     |      |  
2     |      | 
3     |      |  

Bloco |  IN  |  OUT
1     |      | 
2     |      | 
3     |      | 
'''
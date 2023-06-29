import pprint
import re

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
        
        block['USE'].update({var for var in possible_vars_used if var not in block['DEF']})
      else:
        instruction = re.sub(r'[A-Z|if|return|goto|0-9]', '', instruction)
        block['USE'].update({var for var in instruction if var.isalpha() and var not in block['DEF']})

  return blocks

def analysis_out(blocks, id):
  successors_in = set()
  
  if 0 not in blocks[id]['successors']:
    for succ in blocks[id]['successors']:
      successors_in.update(blocks[succ]['IN'])

  return successors_in

def longevity_analysis(blocks):
  changes = True

  while changes:
    prevs_in, prevs_out = [blocks[i]['IN'].copy() for i in blocks], [blocks[i]['OUT'].copy() for i in blocks]
    
    for id in reversed(blocks):
      blocks[id]['OUT'].update(analysis_out(blocks, id))
      blocks[id]['IN'].update(blocks[id]['USE'].union(set([x for x in blocks[id]['OUT'] if x not in blocks[id]['DEF']])))
      
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
  predecessors = []

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
    
    for succ in successors:
      if succ <= num_block and succ != 0:
        blocks[succ]['predecessors'].append(num_block)

    if successors == [0]:
      break

  return blocks

if __name__ == '__main__':
  blocks = get_entry()
  blocks = def_use_block(blocks)
  blocks = longevity_analysis(blocks)
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(blocks)
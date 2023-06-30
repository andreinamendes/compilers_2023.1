import pprint

def gen_kill_block(blocks, definitions):
  for _, block in blocks.items():
    block['GEN'] = set(block['instructions'].keys())
    
    for gen in block['GEN']:
      block['KILL'].update(set([x for x in definitions[block['instructions'][gen][0]] if x != gen]))

  return blocks

def analysis_out(blocks, id):
  entry = blocks[id]['IN']
  
  for elem in blocks[id]['KILL']:
    entry.discard(elem)
  
  return blocks[id]['GEN'].union(entry)

def analysis_in(blocks, id):
  pre_in = set()
  
  for pre in blocks[id]['predecessors']:
    pre_in.update(blocks[pre]['OUT'])
    
  return pre_in

def reaching_definitions(blocks):
  changes = True

  while changes:
    prevs_in, prevs_out = [blocks[i]['IN'].copy() for i in blocks], [blocks[i]['OUT'].copy() for i in blocks]
    
    for id in blocks:
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
      'GEN': set(),
      'KILL': set(),
      'IN': set(),
      'OUT': set()
    }
  }

  return block

def get_entry():
  blocks = {}
  predecessors = []
  definitions = dict()
  num_blocks = int(input())

  for _ in range(num_blocks):
    num_block, num_inst = [int(x) for x in input().split(' ')]
    
    instructions = {}
    
    for _ in range(num_inst):
      key, instruction = input().replace(' ', '').split(':')
      
      if instruction[0] not in definitions.keys():
        definitions.update({instruction[0]: [key]})
      else:
        definitions[instruction[0]].append(key)
        
      instructions.update({key:instruction})
      
    successors = input()
    
    if len(successors) > 1:
      successors = [int(x) for x in successors.split(' ')]
    else:
      successors = [int(successors)]
      
    blocks.update(create_block(num_block, instructions, predecessors, successors))
    predecessors = [num_block]
    
    for succ in successors:
      if succ != 0 and succ <= num_block:
        blocks[succ]['predecessors'].append(num_block)
        
  return blocks, definitions

if __name__ == '__main__':
  blocks, definitions = get_entry()
  blocks = gen_kill_block(blocks, definitions)
  blocks = reaching_definitions(blocks)
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(blocks)
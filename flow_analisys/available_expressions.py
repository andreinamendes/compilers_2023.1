import pprint

def gen_block(blocks):
  for _, block in blocks.items():
    for key, expression in block['instructions'].items():
      aux = block['instructions'].copy()
      variables = [x for x in expression if x.isalpha()]
    
      for x in block['instructions']:
        aux.pop(x)
        if x == key:
          break

      verify_gen = True

      for _, ex in aux.items(): 
        for var in variables:
          if var in ex:
            verify_gen = False

      if verify_gen:
        block['GEN'].update({key})
        
  return blocks

def kill_block(blocks):
  for _, block in blocks.items():
    for key, expression in block['instructions'].items():
      copy = block['instructions'].copy()
      variables = [x for x in expression if x.isalpha()]
      
      for x in block['instructions']:
        copy.pop(x)
        if x == key:
          break
      
      verify_kill = False
      aux = copy.copy()
      
      for k, ex in copy.items():
        aux.pop(k)
        if ex[0] in variables:
          verify_kill = True
          for x in aux:
            if aux[x] == ex[2:]:
              verify_kill = False
                
      if verify_kill:
        block['KILL'].update({key})
        
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

def available_expressions(blocks):
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
  blocks, predecessors = {}, []
  index_e, index_d = 1, 1
  expressions, definitions = dict(), dict()
  num_blocks = int(input())

  for _ in range(num_blocks):
    num_block, num_inst = [int(x) for x in input().split(' ')]
    
    instructions = {}
    
    for _ in range(num_inst):
      instruction = input().replace(' ', '')
      id_e = f'e{index_e}'
      id_d = f'd{index_d}'
      
      expression = instruction[2:]
      verify_expression = False
      
      for x in expression:
        if x.isalpha():
          verify_expression = True
      
      if verify_expression:
        expressions.update({id_e: expression})
        instructions.update({id_e:instruction})
        
      if instruction[0] not in definitions.keys():
        definitions.update({instruction[0]: [id_d]})
      else:
        definitions[instruction[0]].append(id_d)
      
      index_e += 1
      index_d += 1

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
        
  return blocks, expressions, definitions

if __name__ == '__main__':
  blocks, expressions, definitions = get_entry()
  blocks = gen_block(blocks)
  blocks = kill_block(blocks)
  # blocks = available_expressions(blocks)
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(expressions)
  pp.pprint(definitions)
  pp.pprint(blocks)
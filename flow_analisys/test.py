import pprint


def def_use_block(blocks):
    for _, block in blocks.items():
        prev_expressions = []

        for instruction in block['instructions']:
            if 'if' not in instruction and 'return' not in instruction and 'goto' not in instruction:
                possible_var_defined = instruction[0]
                possible_vars_used = [
                    char for char in instruction[2:] if char.isalpha()]

                if possible_var_defined not in instruction[2:] and possible_var_defined not in prev_expressions:
                    prev_expressions.append(possible_var_defined)
                    block['DEF'].add(possible_var_defined)

                block['USE'].update(
                    var for var in possible_vars_used if var not in block['DEF'])

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
        prevs_in, prevs_out = [blocks[i]['IN']
                               for i in blocks], [blocks[i]['OUT'] for i in blocks]

        for id in reversed(blocks):
            blocks[id]['OUT'].update(analysis_out(blocks, id))
            blocks[id]['IN'].update(analysis_in(blocks, id))

        if prevs_in == [blocks[i]['IN'] for i in blocks] and prevs_out == [blocks[i]['OUT'] for i in blocks]:
            changes = False

    return blocks


def create_block(num_block, instructions, predecessors, successors):
    block = {
        'instructions': instructions,
        'predecessors': predecessors,
        'successors': successors,
        'DEF': set(),
        'USE': set(),
        'IN': set(),
        'OUT': set()
    }

    return {num_block: block}


def get_entry():
    blocks = {}
    predecessors = None

    while True:
        num_block, num_inst = [int(x) for x in input().split(' ')]

        if num_block == 0:
            break

        instructions = [input().replace(' ', '') for _ in range(num_inst)]
        successors = input()

        if len(successors) > 1:
            successors = [int(x) for x in successors.split(' ')]
        else:
            successors = [int(successors)]

        blocks.update(create_block(
            num_block, instructions, predecessors, successors))
        predecessors = [num_block]

    return blocks


if __name__ == '__main__':
    blocks = get_entry()
    blocks = def_use_block(blocks)
    blocks = longevity_analysis

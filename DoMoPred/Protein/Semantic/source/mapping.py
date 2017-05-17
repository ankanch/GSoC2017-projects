def mapper(mapping_file):
    '''
    Read mapping_file into a dictionary
    '''

    data = {}
    file = open(mapping_file)
    for line in file:
        if line.startswith("#"):
            continue
        line = line.strip().split("\t")
        if line[0] not in data:
            data[line[0]] = set()
        data[line[0]].add(line[1])
    return data


def map_to(query, mapping_data):
    '''
    Return the mapped value
    '''
    return mapping_data.get(query, [])




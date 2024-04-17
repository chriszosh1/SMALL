def chop_into_pairs(lst):
    pairs = []
    for i in range(0, len(lst), 2):
        pairs.append(lst[i:i+2])
    return pairs

# Example usage:
input_list = [1, 2, 3, 4, 5, 6, 7, 8]
pairs = chop_into_pairs(input_list)
print(pairs)
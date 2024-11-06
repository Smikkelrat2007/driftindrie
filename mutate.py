import random

def mutate_item(item, weights):
    mutation_type = random.choice(["int_str_swap", "int_to_list", "str_to_list", "list_to_int", "list_to_str", "list_add_item", "list_reduce"])
    if mutation_type == "int_str_swap":
        if isinstance(item, int):
            return str(item)  # int --> str
        elif isinstance(item, str):
            return int(item)  # str --> int
    elif mutation_type == "int_to_list":
        if isinstance(item, int):
            return [item]  # int --> [int]
    elif mutation_type == "str_to_list":
        if isinstance(item, str):
            return [item]  # str --> [str]
    elif mutation_type == "list_to_int":
        if isinstance(item, list) and all(isinstance(i, int) for i in item):
            return item[0]  # [int] --> int
    elif mutation_type == "list_to_str":
        if isinstance(item, list) and all(isinstance(i, str) for i in item):
            return item[0]  # [str] --> str
    elif mutation_type == "list_add_item":
        if isinstance(item, list) and len(item) == 1:
            return item + [random.randint(-180, 180)]  # [item] --> [item, str/int]
    elif mutation_type == "list_reduce":
        if isinstance(item, list) and len(item) == 2:
            return [item[0]]  # [item, item] --> [item]
    return item

my_list = [1, "hello", [2, 3], "world", [4], 5]
weights = [2, 1, 1, 1, 2, 1, 1]

while True:

    index_to_mutate = random.randint(0, len(my_list) - 1)

    mutated_item = mutate_item(my_list[index_to_mutate], weights)

    my_list[index_to_mutate] = mutated_item
    mutated_list = mutate_item(my_list, weights)
    print(mutated_list)
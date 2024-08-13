def find_string_index(arr, target):
    try:
        return arr.index(target)
    except ValueError:
        return -1
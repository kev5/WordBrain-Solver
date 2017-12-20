# Copyright 2017 Keval Khara kevalk@bu.edu
# Copyright 2017 Harish N Sathishchandra harishns@bu.edu
# Copyright 2017 Junchen Cai cairnedx@bu.edu

from sys import argv
import numpy as np


def puzz_read():
    line_1 = []
    rows = []
    blank_space = []
    blank_space_rows = []
    column_out_line = []
    while 1:
        try:
            in_puzz = input()
            if '*' not in in_puzz and ' ' not in in_puzz:
                for i in in_puzz:
                    rows.append(i)
                line_1.append(rows)
                rows = []
            else:
                column_out = 0
                for i in in_puzz + ' ':
                    if i == ' ':
                        column_out_line.append(column_out)
                        column_out = 0
                        blank_space_rows.append(blank_space)
                        blank_space = []
                    else:
                        column_out += 1
                        blank_space.append(i)
                break
        except EOFError:
            break
    if line_1 != [] and column_out_line != [] and blank_space_rows != []:
        
        return (np.array(line_1), column_out_line, blank_space_rows)
#    else:
#        return False


def trie(words):
    word_1 = dict()
    for word in words:
        new_word = word_1
        for letter in word:
            new_word = new_word.setdefault(letter, {})
        new_word[0] = {}
    return word_1


def find_neighbour(index, exist, matrix):
    locations = []
    x, y = index
    nrows, ncols = np.shape(matrix)
    for i in range(-1, 2):
        for j in range(-1, 2):
            index = (x + i, y + j)
            if index[0] >= 0 and index[1] >= 0 and index[0] < nrows:
                if index[1] < ncols and index not in exist and matrix[index]:
                    locations.append(index)
    
    return locations


def extend(paths, neighbours):
    result = []
    for i in neighbours:
        result.append(paths + [i])
    
    return result


def valid_path(path, matrix, word_1):
    char = ''
    tmp = word_1
    for index in path:
        char = matrix[index]
        if char not in tmp:
            return 0
        tmp = tmp[char]
    return 1


def find_combinations(index, size, matrix, word_1):
    exist = [index]
    neibour = find_neighbour(exist[0], exist, matrix)
    exist = extend(exist, neibour)
    i = 2
    if size == 2:
        combo = exist
    while i < size:
        combo = []
        for path in exist:
            if valid_path(path, matrix, word_1):
                co1 = extend(path, find_neighbour(path[-1], path, matrix))
                combo += co1
        exist = combo
        i += 1
    
    return combo


def matrix_indices(size):
    result = []
    for i in range(size):
        for j in range(size):
            result.append((i, j))
            
    return result


def word_path(path, matrix, word_1):
    word = ''
    for index in path:
        word += matrix[index]
    if not search_word([word], word_1):
        return 0
    return word


def search_word(key_word_list, word_1):
    for word in key_word_list:
        tmp = word_1
        for i in word:
            if i not in tmp:
                return 0
            else:
                tmp = tmp[i]
        if 0 in tmp:
            return 1
#        else:
#            return 0


def remove_word(path, matrix):
    temporary_mat_1 = np.copy(matrix)
    if len(path) == 1:
        return matrix
    num = np.shape(temporary_mat_1)[0]
    newmatrix1 = []
    for index in path:
        temporary_mat_1[index] = '0'
    for column in np.transpose(temporary_mat_1).tolist():
        newcolumn1 = list(filter(('0').__ne__, column))
        while len(newcolumn1) < num:
            newcolumn1.insert(0, 0)
        newmatrix1.append(newcolumn1)
    return np.transpose(np.array(newmatrix1, dtype=object).reshape(num, num))


def mat_str(matrix, length, word_1, blank_spacein):
    allmatrix1 = []
    if blank_spacein == []:
        fullindex = matrix_indices(np.shape(matrix)[0])
    else:
        fullindex = blank_spacein
    for index in fullindex:
        if matrix[index]:
            for path in find_combinations(index, length, matrix, word_1):
                if word_path(path, matrix, word_1):
                    allmatrix1.append((remove_word(path, matrix),
                                       word_path(path, matrix, word_1)))
    return allmatrix1


def index_search(blank_space, sindex_1, matrix):
    ind = []
    for k in blank_space:
        if k != '*':
            for i in range(sindex_1):
                for j in range(sindex_1):
                    if matrix[i][j] == k:
                        ind.append((i, j))
    return ind


def window_slide(matrix, windows, word_1, blank_space_rows):
    sindex_1 = np.shape(matrix)[0]
    result = []
    tmp = []
    ind = []
    blank_space = blank_space_rows[0]
    ind = index_search(blank_space, sindex_1, matrix)
    for mtx, wrd in mat_str(matrix, windows[0], word_1, ind):
        result.append(([wrd], mtx))
    blank_space_rows.pop(0)
    windows.pop(0)
    if windows:
        for length in windows:
            blank_space = blank_space_rows[windows.index(length)]
            ind = index_search(blank_space, sindex_1, matrix)
            tmp = result
            result = []
            for i in tmp:
                for mtx, wrd in mat_str(i[1], length, word_1, ind):
                    result.append((i[0] + [wrd], mtx))
    return result


def get_result(matrix, word_1, column_out_line, blank_space):
    windows = []
    blank_space_rows = []
    for j in blank_space:
        blank_space_rows.append(j)
    for i in column_out_line:
        windows.append(i)
    answers = []
    result = window_slide(matrix, windows, word_1, blank_space_rows)
    for i in result:
        if i[0] not in answers:
            answers.append(i[0])
    for i in sorted(answers):
        print(' '.join(i))
    return answers


def final_word(line_1, short_word_1, long_word_1, column_out_line, blank_space):
    answer = []
    answer = get_result(line_1, short_word_1, column_out_line, blank_space)
    if answer == []:
        answer = get_result(line_1, long_word_1, column_out_line, blank_space)
    print('.')


def main():
    with open(argv[1], 'r') as word_list1:
        words1 = word_list1.read().split()
    with open(argv[2], 'r') as word_list2:
        words2 = word_list2.read().split()
    while 1:
        try:
            line_1, column_out_line, blank_space = puzz_read()
            final_word(line_1, trie(words1), trie(words2), column_out_line, blank_space)
        except TypeError:
            break

if __name__ == '__main__':
    main()

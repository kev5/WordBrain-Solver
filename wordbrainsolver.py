# Copyright 2017 Keval Khara kevalk@bu.edu
# Copyright 2017 Harish N Sathishchandra harishns@bu.edu
# Copyright 2017 Junchen Cai cairnedx@bu.edu

'''WordBrain Solver'''
from sys import argv
import numpy as np


def trie(words):
    '''Retrieval Data Structure'''
    word_1 = dict()
    for word in words:
        new_word = word_1
        for letter in word:
            new_word = new_word.setdefault(letter, {})
        new_word[0] = {}
    return word_1


def routes(paths, neighbors):
    '''Different Routes'''
    result = []
    for neighbor in neighbors:
        result.append(paths + [neighbor])
    return result


def find_neighbor(index, exist, matrix):
    '''Finding Neighboring Letters'''
    locations = []
    x, y = index
    nrows, ncols = np.shape(matrix)
    for i in range(-1, 2):
        for j in range(-1, 2):
            index = (x + i, y + j)
            if (index[0] >= 0 and index[1] >= 0
                and index[0] < nrows):
                if (index[1] < ncols and index not in exist 
                    and matrix[index]):
                    locations.append(index)
    return locations


def valid_path(path, matrix, word_1):
    '''Valid Path'''
    char = ''
    tmp = word_1
    for index in path:
        char = matrix[index]
        if char not in tmp:
            return 0
        tmp = tmp[char]
    return 1


def find_combinations(index, size, matrix, word_1):
    '''Finding Combinations'''
    exist = [index]
    neibour = find_neighbor(exist[0], exist, matrix)
    exist = routes(exist, neibour)
    i = 2
    if size == 2:
        combo = exist
    while i < size:
        combo = []
        for path in exist:
            if valid_path(path, matrix, word_1):
                co1 = routes(path, find_neighbor(
                    path[-1], path, matrix))
                combo += co1
        exist = combo
        i += 1
    return combo


def create_word(path, matrix, word_1):
    '''Create Word from the Path'''
    word = ''
    for index in path:
        word += matrix[index]
    if not search_word([word], word_1):
        return 0
    return word


def search_word(key_word_list, word_1):
    '''Searching for Words'''
    for word in key_word_list:
        tmp = word_1
        for val in word:
            if val not in tmp:
                return 0
            else:
                tmp = tmp[val]
        if 0 in tmp:
            return 1


def remove_word(path, matrix):
    '''Removing Unwanted Words'''
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
    return np.transpose(np.array(
        newmatrix1, dtype=object).reshape(num, num))


def matrix_words(matrix, length, word_1, blank_space):
    '''All possible matrices and words'''
    full_matrix = []
    all_indices = []
    if blank_space == []:
        for i in range(np.shape(matrix)[0]):
            for j in range(np.shape(matrix)[0]):
                all_indices.append((i, j))
    else:
        all_indices = blank_space
    for index in all_indices:
        if matrix[index]:
            for path in find_combinations(
                index, length, matrix, word_1):
                if create_word(path, matrix, word_1):
                    full_matrix.append((remove_word(path, matrix),
                                       create_word(
                                        path, matrix, word_1)))
    return full_matrix


def index_search(blank, sindex_1, matrix):
    '''Getting indices of blanks'''
    ind = []
    for star in blank:
        if star != '*':
            for i in range(sindex_1):
                for j in range(sindex_1):
                    if matrix[i][j] == star:
                        ind.append((i, j))
    return ind


def window_slide(matrix, windows, word_1, blank_rows):
    '''Sliding the window'''
    sindex_1 = np.shape(matrix)[0]
    result = []
    tmp = []
    ind = []
    if blank_rows:
        blank = blank_rows[0]
        ind = index_search(blank, sindex_1, matrix)
        for mtx, wrd in matrix_words(matrix, windows[0], word_1, ind):
            result.append(([wrd], mtx))
        blank_rows.pop(0)
        windows.pop(0)
        if windows:
            for length in windows:
                blank = blank_rows[windows.index(length)]
                ind = index_search(blank, sindex_1, matrix)
                tmp = result
                result = []
                for val in tmp:
                    for mtx, wrd in matrix_words(val[1], length, 
                                                 word_1, ind):
                        result.append((val[0] + [wrd], mtx))
        return result


def get_result(matrix, word_1, column_out_line, blank):
    '''Getting all Results'''
    windows = []
    blank_rows = []
    for star in blank:
        blank_rows.append(star)
    for col in column_out_line:
        windows.append(col)
    answers = []
    result = window_slide(matrix, windows, word_1, blank_rows)
    for val in result:
        if val[0] not in answers:
            answers.append(val[0])
    for ans in sorted(answers):
        print(' '.join(ans))
    return answers


def final(line_1, short_word_1, long_word_1, 
               column_out_line, blank):
    '''Final Answer'''
    answer = []
    answer = get_result(line_1, short_word_1, column_out_line, 
                        blank)
    if answer == []:
        answer = get_result(line_1, long_word_1, column_out_line, 
                            blank)
    print('.')


def main():
    '''Readind Puzzles and Computing'''
    with open(argv[1], 'r') as word_list1:
        words1 = word_list1.read().split()
    with open(argv[2], 'r') as word_list2:
        words2 = word_list2.read().split()
    while 1:
        try:
            line_1 = []
            rows = []
            blank = []
            blank_rows = []
            column_out_line = []
            while 1:
                try:
                    in_puzz = input()
                    if '*' and ' ' not in in_puzz:
                        for puzz in in_puzz:
                            rows.append(puzz)
                        line_1.append(rows)
                        rows = []
                    else:
                        column_out = 0
                        for puzz in in_puzz + ' ':
                            if puzz == ' ':
                                column_out_line.append(column_out)
                                column_out = 0
                                blank_rows.append(blank)
                                blank = []
                            else:
                                column_out += 1
                                blank.append(puzz)
                        break
                except EOFError:
                    break        
            line_1, column_out_line, blank = np.array(
                  line_1), column_out_line, blank_rows
            final(line_1, trie(words1), trie(words2), 
                       column_out_line, blank)
        except TypeError:
            break

if __name__ == '__main__':
    main()

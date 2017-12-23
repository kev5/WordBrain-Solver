# Copyright 2017 Keval Khara kevalk@bu.edu

'''WordBrain Solver'''
from sys import argv
import numpy as np


class Trie:
    '''Retrieval Data Structure'''

    def __init__(self):
        '''Initialize'''
        self.head = Node()

    def add(self, word):
        '''Adding a new string'''
        curr_node = self.head
        for letter in word:
            ind = ord(letter) - 97
            if curr_node.children[ind]:
                curr_node = curr_node.children[ind]
            else:
                curr_node.add_child(ind)
                curr_node = curr_node.children[ind]
        curr_node.data = True

    def check_word(self, word):
        '''Checks if the word is present'''
        curr_node = self.head
        for letter in word:
            ind = ord(letter) - 97
            if curr_node.children[ind]:
                curr_node = curr_node.children[ind]
        return curr_node.data

    def search(self, letters):
        '''Checks for the previous letters in the list'''
        top_node = self.head
        for letter in letters:
            ind = ord(letter) - 97
            if top_node.children[ind]:
                top_node = top_node.children[ind]
            else:
                return False
        return True


class Node:
    '''Class for each Node in the Trie'''

    def __init__(self):
        '''Initializing'''
        self.data, self.children = None, np.empty(26, dtype=Node)

    def add_child(self, key):
        '''Adding a child for each Node'''
        self.children[key] = Node()


def neighbors(matrix, pos):
    '''Finding Neighbors'''
    adj = []
    for i in range(pos[0] - 1, pos[0] + 2):
        for j in range(pos[1] - 1, pos[1] + 2):
            if 0 <= i < matrix.shape[0] and 0 <= j < matrix.shape[1]:
                if matrix[i][j] != '#':
                    adj.append((i, j))
    return adj


def find_word(prob, pos):
    '''Search for the word'''
    for i in range(pos, -1, -1):
        if prob[i] == ' ':
            return "".join(prob[i + 1:pos + 1])
    return "".join(prob[0:pos + 1])


def find_pos(matrix, char):
    '''Find the position of the Letter'''
    result = []
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] == char:
                result.append((i, j))
    return result


def drop_letters(matrix):
    '''Drop the used letters in the matrix'''
    result = np.copy(matrix)
    previous = ['#'] * matrix.shape[0]
    for j in range(0, matrix.shape[1]):
        temp_mat = np.array(previous)
        index = matrix.shape[0] - 1
        for i in range(matrix.shape[0] - 1, -1, -1):
            if result[i][j] != '#':
                temp_mat[index] = result[i][j]
                index = index - 1
        result[:, j] = temp_mat
    return result


SMALL_LIST = Trie()
LARGE_LIST = Trie()
FINAL = set()


class Puzzle:
    '''Class to represent the puzzles'''

    def __init__(self, matrix, puzzle, matrix_pos, puzz_pos, trie):
        '''Initialize'''
        self.matrix, self.puzzle, self.curr_pos, self.puzz_pos, self.trie = \
            matrix, puzzle, matrix_pos, puzz_pos, trie

    def solve_puzzle(self):
        '''Solving the Input Text File'''
        if self.puzz_pos == len(self.puzzle):
            word = find_word(self.puzzle, self.puzz_pos - 1)
            if self.trie.check_word(word):
                FINAL.add("".join(self.puzzle))
            return 0
        if self.puzzle[self.puzz_pos] == ' ':
            word = find_word(self.puzzle, self.puzz_pos - 1)
            if self.trie.check_word(word):
                rmatrix = drop_letters(self.matrix)
                Puzzle(rmatrix, self.puzzle, (), self.puzz_pos + 1,
                       self.trie).solve_puzzle()
        if self.puzzle[self.puzz_pos] == '*':
            if self.curr_pos:
                adj_curr_pos = neighbors(self.matrix, self.curr_pos)
                if adj_curr_pos:
                    for pos in adj_curr_pos:
                        new_puzz = self.puzzle[:]
                        new_puzz[self.puzz_pos] = self.matrix[pos[0]][pos[1]]
                        word = find_word(new_puzz, self.puzz_pos)
                        if self.trie.search(word):
                            new_matrix = np.copy(self.matrix)
                            new_matrix[pos[0]][pos[1]] = '#'
                            Puzzle(new_matrix, new_puzz, (pos[0], pos[1]),
                                   self.puzz_pos + 1, self.trie).solve_puzzle()
            else:
                for i in range(0, self.matrix.shape[0]):
                    for j in range(0, self.matrix.shape[1]):
                        if self.matrix[i][j] != '#':
                            new_puzz = self.puzzle[:]
                            new_puzz[self.puzz_pos] = self.matrix[i][j]
                            word = find_word(new_puzz, self.puzz_pos)
                            if self.trie.search(word):
                                new_matrix = np.copy(self.matrix)
                                new_matrix[i][j] = '#'
                                Puzzle(new_matrix, new_puzz, (i, j),
                                       self.puzz_pos + 1,
                                       self.trie).solve_puzzle()
        else:
            if self.curr_pos:
                adj_curr_pos1 = set(neighbors(self.matrix, self.curr_pos))
                tmp_pos = set(find_pos(self.matrix,
                                       self.puzzle[self.puzz_pos]))
                if adj_curr_pos1 and tmp_pos:
                    moves = adj_curr_pos1 & tmp_pos
                    for pos in moves:
                        new_matrix = np.copy(self.matrix)
                        new_matrix[pos[0]][pos[1]] = '#'
                        Puzzle(new_matrix, self.puzzle, (pos[0], pos[1]),
                               self.puzz_pos + 1, self.trie).solve_puzzle()
            else:
                tmp_pos1 = find_pos(self.matrix, self.puzzle[self.puzz_pos])
                if tmp_pos1:
                    for pos in tmp_pos1:
                        new_matrix = np.copy(self.matrix)
                        new_matrix[pos[0]][pos[1]] = '#'
                        Puzzle(new_matrix, self.puzzle, (pos[0], pos[1]),
                               self.puzz_pos + 1, self.trie).solve_puzzle()


def main():
    '''Reading the Input files and Computing Answers'''
    for line in open(argv[1], 'r'):
        SMALL_LIST.add(line.rstrip())
    for line in open(argv[2], 'r'):
        LARGE_LIST.add(line.rstrip())
    inputs = []
    while 1:
        try:
            text = input("")
        except EOFError:
            break
        if "*" in text:
            puzzle = list(text)
            matrix = np.array(inputs)
            Puzzle(matrix, puzzle, (), 0, SMALL_LIST).solve_puzzle()
            if not FINAL:
                Puzzle(matrix, puzzle, (), 0, LARGE_LIST).solve_puzzle()
            if FINAL:
                word_list = list(FINAL)
                word_list.sort()
                try:
                    for string in word_list:
                        print(string)
                except ValueError:
                    pass
            print(".")
            FINAL.clear()
            inputs = []
        else:
            inputs.append(list(text))


if __name__ == '__main__':
    main()

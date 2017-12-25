// Copyright 2017 Keval Khara kevalk@bu.edu

// WordBrain Solver
#include <stdlib.h>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <vector>
#define LETTERS 26

typedef std::vector <std::vector <char>> wordlist;


struct node {
 public:
  char path;
  struct node *path_0;
  struct node *letter[LETTERS];
  std::string w = "";
  bool F = false;
};


struct balance {
 public:
  int d = 0;
  wordlist wordlist_0;
  void wordlist_1(int dd);
  void display(int n);
};


void balance::wordlist_1(int dd) {
  d = dd;
  wordlist_0.clear();
  wordlist_0.resize(d, std::vector <char> (dd, 0));
}


int attribute(std::vector <std::string> tree, balance *point,
              node *word_trie,
              std::vector <int> len,
              std::map <int, char> Map,
              std::vector <std::string> *words,
              std::set <std::string> *Map_set);
node * head;


int trie(std::vector <std::string> tree, balance *point,
         std::vector <int> len,
         node *word_trie,
         std::map <int, char> *Map,
         int unit0, int unit1,
         std::vector <std::string> *words,
         std::set <std::string> *Map_set
        ) {
  if (!word_trie) return false;
  std::map <int, char> Map_trie;
  Map_trie.insert(Map->begin(), Map->end());
  (Map_trie)[unit0 + unit1 * point->d] = word_trie->path;

  for (const auto &pointer : (*Map))
    if (word_trie->F) {
      std::vector <int> trie_len = len;
      trie_len.erase(trie_len.begin());
      std::vector <std::string> words_trie = *words;
      words_trie.push_back(word_trie->w);
      for (const auto &pointer : (words_trie))
        if (attribute(tree, point, head, trie_len,
                      Map_trie, &words_trie, Map_set)) {
          *words = words_trie;
          *Map = Map_trie;
          return true;
        } else {
          return false;
        }
    }

  int begin_0 = (unit0 - 1 > 0) ? unit0 - 1 : 0;
  int end_0 = (unit1 - 1 > 0) ? unit1 - 1 : 0;
  int begin_1 = (unit0 + 1 < point->d) ? unit0 + 1 : point->d - 1;
  int end_1 = (unit1 + 1 < point->d) ? unit1 + 1 : point->d - 1;
  for (int i = begin_0; i <= begin_1; i++) {
    for (int j = end_0; j <= end_1; j++) {
      if (Map_trie.count(i + j * point->d))
        continue;
      char target;
      try {
        target = point->wordlist_0.at(i).at(j);
      } catch(std::out_of_range) {
        continue;
      }
      if (word_trie->letter[target - 'a']) {
        if (trie(tree, point, len,
                 word_trie->letter[point->wordlist_0.at(i).at(j) - 'a'], &
                 Map_trie, i, j, words, Map_set)) {
          Map->insert(Map_trie.begin(), Map_trie.end());
          return true;
        }
      }
    }
  }
  return false;
}


int inputs(std::string ss, node *word_trie) {
  std::ifstream infile(ss);
  std::string word_file;
  int count;
  while (infile >> word_file) {
    if (word_file.length() > LETTERS)
      continue;
    count++;
    if (word_trie->letter[word_file.length()] == NULL) {
      word_trie->letter[word_file.length()] = new node;
      word_trie->letter[word_file.length()]->path_0 = word_trie;
      word_trie->letter[word_file.length()]->path = '0' + word_file.length();
    }
    node * traverse = word_trie->letter[word_file.length()];
    for (auto target : word_file) {
      if (traverse->letter[target - 'a'] == NULL) {
        traverse->letter[target - 'a'] = new node;
        traverse->letter[target - 'a']->path_0 = traverse;
        traverse->letter[target - 'a']->path = target;
      }
      traverse = traverse->letter[target - 'a'];
    }
    traverse->F = true;
    traverse->w = word_file;
  }
  return count;
}


int attribute(std::vector <std::string> tree, balance *point,
              node *word_trie,
              std::vector <int> len,
              std::map <int, char> Map,
              std::vector <std::string> *words,
              std::set <std::string> *Map_set) {
  if (len.size() == 0) {
    std::string str_tmp = "";
    for (const auto &pointer : *words)
      str_tmp += pointer + " ";
    Map_set->insert(str_tmp);
    return false;
  }
  balance unit_trie = *point;
  for (std::map <int, char>::reverse_iterator Map_new = Map.rbegin();
       Map_new != Map.rend(); ++Map_new) {
    unit_trie.wordlist_0[Map_new->first % unit_trie.d].erase(
      unit_trie.wordlist_0[Map_new->first % unit_trie.d].begin()
      + Map_new->first / unit_trie.d);
  }
  for (int i = 0; i < unit_trie.wordlist_0.size(); i++) {
    for (int j = 0; j < unit_trie.wordlist_0.at(i).size(); j++) {
      std::map <int, char> Map_trie;
      std::vector <std::string> words_trie = *words;
      std::string str_0, str_1;
      if (words_trie.size() != 0) {
        for (int x = 0; x < words_trie.size(); x++) {
          str_0 = words_trie[x];
          str_1 = tree[x];
          int count = 0;
          for (int y = 0; y < str_0.size(); y++) {
            if (str_1[y] != '*') {
              if (str_0[y] == str_1[y])
                count++;
            } else {
              count++;
            }
          }
          if (count != str_0.size())
            return false;
        }
      }
      if (word_trie->letter[len.front()]) {
        if (trie(tree, &unit_trie, len,
                 word_trie->letter[len.front()]->letter[unit_trie.
                     wordlist_0.at(i).at(j) - 'a'],
                 &Map_trie, i, j, &words_trie, Map_set)) {
          *words = words_trie;
          return true;
        }
      }
    }
  }
  return false;
}


std::vector <std::string> split_answer(const std::string& word_file,
                                       const std::string& target) {
  std::vector <std::string> word_s;
  std::string::size_type tmp, mark;
  mark = word_file.find(target);
  tmp = 0;
  while (std::string::npos != mark) {
    word_s.push_back(word_file.substr(tmp, mark - tmp));
    tmp = mark + target.size();
    mark = word_file.find(target, tmp);
  }
  if (tmp != word_file.length())
    word_s.push_back(word_file.substr(tmp));
  return word_s;
}


bool status(const int& tree_len,
            const std::vector<std::vector <char>>& result,
            const std::vector <std::string>& tree,
            std::vector <int> *len, balance *point) {
  point->wordlist_1(tree_len);
  for (int i = 0; i < point->d; i++) {
    for (int j = 0; j < result.size(); j++)
      point->wordlist_0[i][j] = result[result.size() - 1 - j][i];
  }
  for (auto &k : tree)
    len->push_back(k.length());
  if (len->size() == 0 || point->d == 0)
    return false;
  return true;
}


int main(int argc, char **argv) {
  node word_trie = node();
  node word_trie_len = node();
  inputs(argv[1], &word_trie);
  inputs(argv[2], &word_trie_len);
  while (true) {
    int flag = 0;
    balance point = balance();
    std::string str;
    wordlist result;
    std::string units;
    std::string line = "";
    while (std::cin) {
      if (std::cin.eof()) exit(0);
      getline(std::cin, line);
      if (line == "") exit(0);
      if (line.find("*") == std::string::npos) {
        std::vector<char> data(line.begin(), line.end());
        result.push_back(data);
      } else {
        units = line;
        break;
      }
    }
    int tree_len = result[0].size();
    std::vector <std::string> tree = split_answer(units, " ");
    head = &word_trie;
    std::map <int, char> Map;
    std::vector <int> len;
    if (!status(tree_len, result, tree, &len, &point))
      return false;
    std::vector<std::string> words;
    std::set<std::string> Map_set;
    attribute(tree, &point, &word_trie, len, Map, &words, &Map_set);
    if (Map_set.size() == 0) {
      head = &word_trie_len;
      attribute(tree,
                &point, &word_trie_len, len, Map, &words, &Map_set);
    }
    for (const auto &pointer : Map_set)
      std::cout << pointer << std::endl;
    std::cout << "." << std::endl;
  }
}

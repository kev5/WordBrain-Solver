# WordBrain Solver

C++ and Python Programs for solving the puzzles in the WordBrain App on Android and iOS.

The inputs to the C++ and Python programs are given by a text file called [puzzles.txt](https://github.com/kev5/WordBrain-Solver/blob/master/puzzles.txt) which has the puzzles in the following format-
```
hee
oqr
sua
*** ******
yson
elnn
hnca
olab
***** ***** ******
nchn
iaaw
bpom
atsn
**** ***** *** ****
vanmo
ipveo
toarr
tsmed
miipb
**** ******* ******* *******
vanmo
ipveo
toarr
tsmed
miipb
p*** ******* ******* *******
yson
elnn
hnca
olab
***** holly ******
```

The output of both the programs gives all the possible solutions of a given puzzle. For example, all possible solutions to the above puzzles will be printed in the following format-
```
hoe square
.
banes holly cannon
hones bally cannon
honey balls cannon
.
snow panic man bath
.
opts bedroom vampire vitamin
post bedroom vampire vitamin
pots bedroom vampire vitamin
stop bedroom vampire vitamin
.
post bedroom vampire vitamin
pots bedroom vampire vitamin
.
banes holly cannon
.
```

The programs take the [small_word_list.txt](https://github.com/kev5/WordBrain-Solver/blob/master/small_word_list.txt) and the [large_word_list.txt](https://github.com/kev5/WordBrain-Solver/blob/master/large_word_list.txt) files as arguments to look upto valid words that can be formed.

You can run the Python program in the following way-
```
~> python wordbrainsolver.py small_word_list.txt large_word_list.txt <puzzles.txt >solutions.txt
```
And the C++ program in the following way-
```
~> g++ wordbrainsolver.cpp -o wb
~> ./wb small_word_list.txt large_word_list.txt <puzzles.txt >solutions.txt
```

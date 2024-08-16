# tictactoc

A simple library to be able to control the time that certain parts of the code take

## Installation and use

To install this module use:

```sh
pip install tictactoc
```

Run tests to validate:

```sh
tictactoc-tests
```

## Usage

Basic use, start and end.

```py
from tictactoc import tictactoc

tictactoc.tic() # Start
print(tictactoc.toc()) # Finish
```

Using tac in loops.
We can do a tac in each iteration. When we finnish the loop, we do a toc skipping this time.

```py
from time import sleep
from tictactoc import tictactoc

tictactoc.tic("my loop")

my_loop=[1,2]

for element in my_loop:
    sleep(0.1)
    tictactoc.tac("my loop")

result = tictactoc.toc("my loop", skip_toc=True)

print(f"total: {result["total"]}, each iteration: {', '.join(map(str,result["steps"]))}")
```

## Credits

Developed and maintained by felipem775. [Contributions](CONTRIBUTING.md) are welcomed.

# Tugas Besar II Manajemen Basis Data 2022 - Concurrency Control

Concurrency control simulation is a simulation of how DBMS works. There are consist of two protocls, Optimistic Concurrency Control and Simple locking using only exclusive locks.

Made with love by

|              Name              |   NIM    |
| :----------------------------: | :------: |
|     Petrus Elison Manurung     | 13518110 |
| Muhammad Akyas David Al Aleey  | 13520011 |
| Muhammad Garebaldhie ER Rahman | 13520029 |
|   Fawwaz Anugrah Wiradhika D   | 13520086 |
|          Farrel Ahmad          | 13520110 |

## Requirement list and Installation

1. Install python [here](https://www.python.org/)
2. clone the repository using `git clone https://github.com/IloveNooodles/concurrency-control`

## Usage

This program uses argparse so you can read the full command here

```
usage: main.py [-h] {simple,optimistic} [pathfile]

Concurrency Control Protocol Implementation

positional arguments:
  {simple,optimistic}  choose concurrency control protocol, s[imple] and o[ptimistic]
  [pathfile]           path file for the testcase or input

options:
  -h, --help           show this help message and exit
```

To run the program you can specify the path and protocol you want to use for example `python main.py simple test/tc1.txt` to run `tc1.txt` with simple locking

In simple mode The program will ask prompt if you want to enable the deadlock prevention

```
>> Starting simple locking protocol
>> Do you want to activate deadlock prevention? (y/n)
```

## Valid input

Valid input are

- `C[number]`
- `R[number](alphabet)`
- `W[number](alphabet)`

Here are example of valid input
`R1(X); R2(Y); R1(Y); C1; C2`

After each action must be separated with ; and but no ; in the EOF

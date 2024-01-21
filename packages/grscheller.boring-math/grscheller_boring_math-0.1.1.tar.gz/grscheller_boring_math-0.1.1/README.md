# PyPI grscheller.boring-math

Daddy's boring math library.

* Functions of a mathematical nature
* Project name suggested by my then 13 year old daughter Mary
* Example of a Python package with both libraries and executables

## Overview

Here are the modules which make up the grscheller.boring_math package.

* [Integer Math Module](#integer-math-module)
  * [Fibonacci Sequences](#fibonacci-sequences)
  * [Number Theory](#number-theory)
  * [Pythagorean Triples](#pythagorean-triples)
  * [Recursive Functions](#recursive-functions)

* [Integer Math CLI Module](#integer-math-cli-module)
  * [Ackermann's Function](#ackermanns-function)
  * [Pythagorean Triples](#pythagorean-triple-function)

---

### Integer Math Module

#### Fibonacci Sequences

* Function **fibonacci**(f0: int=0, f1: int=1) -> Iterator
  * Return an iterator for a Fibonacci sequence
  * Defaults to `0, 1, 1, 2, 3, 5, 8, ...`

#### Number theory 

* Function **gcd**(fst: int, snd: int) -> int
  * takes two integers, returns greatest common divisor (gcd)
  * where `gcd >= 0`
  * `gcd(0,0)` returns `0` but in this case the gcd does not exist

* Function **lcm**(fst: int, snd: int) -> int
  * takes two integers, returns least common multiple (lcm)

* Function **primes**(start: int=2, end_before: int=100) -> Iterator
  * takes two integers, returns least common multiple (lcm)

#### Pythagorean Triples

The values `a, b, c > 0` represent integer sides of a right triangle.

* Function **pythag3**(a_max: int=3, all_max: int|None=None) -> Iterator
  * Return an interator of tuples of Pythagorean Tiples
  * Side `a <= a_max` and sides `a, b, c <= all_max`
  * Iterator finds all primative pythagorean triples up to a given a_max

#### Recursive Functions

* Function **ackermann**(m: int, n: int) -> int
  * Ackermann's function is a doublely recursively defined function
  * An example of a computable but not primitive recursive function
  * Becomes numerically intractable after m=4

---

### Integer Math CLI Module

#### Ackermann's Function

* Function **ackerman_cli**(fst: int, snd: int) -> None
  * entry point for program ackermann 
  * Ackermann's function is defined recursively by
    * `ackermann(0,n) = n+1`
    * `ackermann(m,0) = ackermann(m-1,1)`
    * `ackermann(m,n) = ackermann(m-1,ackermann(m, n-1))` for `n,m > 0`
  * Usage: `ackerman m n`

#### Pythagorean Triple Function

  * entry point for program pythag3 
  * A Pythagorean triple is a 3-tuple of integers `(a, b, c)` such that
    * `a*a + b*b = c*c` where `a,b,c > 0` and `gcd(a,b,c) = 1`
  * The integers `a, b, c` represent the sides of a right triangle
  * Usage: `pythag3 m [n]`
    * one argument outputs all triples with `a <= n`
    * two arguments outputs all triples with `a <= n` and `a, b, c <= m`

---

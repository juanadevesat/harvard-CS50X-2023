# Debug

## Learning Goals

- Become familiar with C syntax
- Learn what C compiler error messages mean
- Get practice debugging

![Alt text](img/first_bug.jpg)

## Background

There are two kinds of errors that can occur when writing a program. The first errors you are likely to encounter are **syntactical** errors. In addition to syntactical errors, there can also be logical errors, which we’ll take a look at soon.

In computer science, syntax is important for a computer to understand what you are telling it to do. Each programming language has its own syntactical rules, which include the combination of both words and punctuation.

This lab starts with distribution code which has several syntactical errors. The idea is for you to try to compile (``make``) the program, learn to interpret the rather cryptic error messages output by the compiler, and **debug** the program.

> **Hints**
>
> You’ll probably see the first error after trying to compile debug.c will be debug.c:9:5: error: use of undeclared identifier 'name'. The 9 after debug.c: means there is a problem on line 9. Why do you think is says undeclared identifier?
>
> You may want to look for errors such as missing symbols, missing libraries, missing variable declarations.
>
> If you are still stuck, try typing into the terminal help50 make debug.

## Demo

![Alt text](img/debugDemo.gif)

## How to Test Your Code

Your program should behave per the examples below.

```
debug/ $ ./debug
What is your name? Carter
Where do you live? Cambridge
Hello, Carter, from Cambridge!
```

```
debug/ $ ./debug
What is your name? Margaret
Where do you live? New York
Hello, Margaret, from New York!
```

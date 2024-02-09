# Max

### Learning Goals+

- Pass an array into a function
- Create a helper function that finds a maximum value

### Background

There are many situations where you’ll find it helpful to have a function that finds the maximum (and minimum) value in an array. Since there is no built-in ``max`` function in ``C``, you’ll create one in this practice problem. You can then use it in upcoming problem sets where it may be helpful!

> **Hints**
>
> Start out with a variable that keeps track of your max value. There are two ways to initialize this. You can start out using the lowest possible value (be careful you don’t start with zero, as the max value could be a negative number!) or you can start with the first element in the array.
>
> Loop through the array and reset this max value every time you find a value that’s larger.

### Implementation Details

The ``main`` function initializes the array, asks the user to enter values, and then passes the array and the number of items to the ``max`` function. Complete the ``max`` function by iterating through every element in the array, and return the maximum value.

### How to Test Your Code

Your program should behave per the examples below.

```
max/ $ ./max
Number of elements: 3
Element 0: 2
Element 1: 10
Element 2: -1
The max value is 10.
```

```
max/ $ ./max
Number of elements: 4
Element 0: -100
Element 1: -200
Element 2: -3
Element 3: -5000
The max value is -3.
```
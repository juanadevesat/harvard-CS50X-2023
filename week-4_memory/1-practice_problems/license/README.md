# License

## Learning Goals

- Practice working with files and file pointers
- More work with strings and arrays
- Debugging with debug50
- Use valgrind to check for memory leaks

## Background

Suppose you work for a company that develops AI-enhanced license plate recognition technology. As you develop your technology, you may want to use actual license plate numbers as test data. You have a text file with some plate numbers you want to analyze, so you first try reading from that text file and printing out the license plates, to test your file-reading logic. But when you run your program, only the last number prints 8 times! What went wrong?

## Implementation Details

If you open the ``plates.txt`` file, you’ll notice that there are actually 8 different license plate numbers. There are a few errors in the distribution code that are causing this to happen. Let’s start by walking through the code.

We first check for command-line arguments, since ``argv[1]`` should be the text file that contains the license plates. We then create a character array of length 7, since the plate numbers are 6 ``char``s long and we need to save space for the NUL terminator. Now we create an array of ``char *``’s (character pointers, otherwise known as ``string``s!) to store the 8 plate numbers. We create a file pointer to our external text file, create a variable to hold the index of each array element, and begin reading the file and saving the plate numbers to the array. Finally, to test that we did this correctly, we print out the values in the array.

However, when we compile and execute this code, something is clearly wrong. You’ll need to make the appropriate corrections!

## Debugging

Take a close look at what values are actually being added to the array. You can experiment with debug50 to find the error in the distribution code.

> **Hints**
>
> What exactly does the variable ``buffer`` hold that’s being assigned to each element of the ``plates`` array?
>
> Note that the ``plates`` array as an array of ``char *``’s or string pointers.
>
> So when we assign the char array ``buffer`` to a ``char *``, what actually happens?

Is there a better way to copy license plate numbers to the ``license`` array?

> **More Hints**
>
> Would ``strcpy`` come in useful here?
>
> If you copy data to a pointer, where will that data go?
>
> Is ``malloc`` required here?

## Checking for Memory Leaks

Once your program seems to be working properly, run valgrind to make sure there are no memory leaks.

```
valgrind ./license plates.txt
```

You may end up with something like this:

    ==24478== HEAP SUMMARY:
    ==24478==     in use at exit: 528 bytes in 9 blocks
    ==24478==   total heap usage: 10 allocs, 1 frees, 4,624 bytes allocated
    ==24478== 
    ==24478== 56 bytes in 8 blocks are definitely lost in loss record 1 of 2
    ==24478==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==24478==    by 0x109207: main (license.c:30)
    ==24478== 
    ==24478== 472 bytes in 1 blocks are still reachable in loss record 2 of 2
    ==24478==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==24478==    by 0x4A086CD: __fopen_internal (iofopen.c:65)
    ==24478==    by 0x4A086CD: fopen@@GLIBC_2.2.5 (iofopen.c:86)
    ==24478==    by 0x1091CD: main (license.c:20)
    ==24478== 
    ==24478== LEAK SUMMARY:
    ==24478==    definitely lost: 56 bytes in 8 blocks
    ==24478==    indirectly lost: 0 bytes in 0 blocks
    ==24478==      possibly lost: 0 bytes in 0 blocks
    ==24478==    still reachable: 472 bytes in 1 blocks
    ==24478==         suppressed: 0 bytes in 0 blocks
    ==24478== 
    ==24478== For lists of detected and suppressed errors, rerun with: -s
    ==24478== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

There seem to be two kinds of memory errors here that need to be corrected!

> Hint
>
> Your line numbers may be different, but note here that there seems to be a memory problem in ``main`` on line 30 (something to do with ``malloc``?), and line 20 (a problem related to ``fopen``?). What might the distribution code be missing?

## How to Test Your Code

Your program should behave per the examples below.

    license/ $ ./license plates.txt
    11ZT00
    1KAD21
    78ZZ01
    99ZZ11
    72ZZ21
    98ZZ31
    44ZW41
    34ZZ51
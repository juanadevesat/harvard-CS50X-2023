# Hello

### Getting Started

Proceed to write your first program by typing precisely these lines into hello.c:

```c
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
}
```

### Getting User Input

Suffice it to say, no matter how you compile or execute this program, it only ever prints hello, world. Let’s personalize it a bit, just as we did in class.

Modify this program in such a way that it first prompts the user for their name and then prints hello, so-and-so, where so-and-so is their actual name.

### Hints

**Don’t recall how to prompt the user for their name?**

Recall that you can use ``get_string`` as follows, storing its return value in a variable called ``name`` of type ``string``.

```c
string name = get_string("What's your name? ");
```

**Don’t recall how to format a string?**

Don’t recall how to join (i.e., concatenate) the user’s name with a greeting? Recall that you can use printf not only to print but to format a string (hence, the f in printf), a la the below, wherein name is a string.

```c
printf("hello, %s\n", name);
```

**Use of undeclared identifier?**

Seeing the below, perhaps atop other errors?

```
error: use of undeclared identifier 'string'; did you mean 'stdin'?
```

Recall that, to use get_string, you need to include cs50.h (in which get_string is declared) atop a file, as with:

```c
#include <cs50.h>
```

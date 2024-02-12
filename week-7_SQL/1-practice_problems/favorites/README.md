# Favorites

## Learning Goals

- Become familiar with SQL
- Practice using `SELECT` and `UPDATE` operations

Background
In 2021’s Week 7 lecture, we created a SQL database, `favorites.db`, with a table of CS50 students’ favorite TV shows. As often happens when importing raw data, however, we have some inconsistencies and typos to take care of (lest our queries become clumsy and our results inaccurate!).

Your job is to use the SQL `UPDATE` keyword to clean up this database, so it can be more effectively used for analysis.

## Implementation Details

Let’s first take a look at the data. Recall that you’ll need to use SQLite, a lightweight “database engine”, to open `favorites.db`. We’ll use the third (and latest) version of SQLite. You can open `favorites.db`, then, by executing

```
sqlite3 favorites.db
```

so long as your terminal’s working directory is the same directory in which `favorites.db` is located.

In your `sqlite3` prompt, try executing

```
.schema
```

to see the commands used to create the two tables in this database, `shows` and `genres`.

Now try viewing the data inside of `shows` by executing

```
SELECT * FROM shows;
```

Scrolling up, notice that the very first title in `shows` already looks like it might pose a problem. We want “How i met your mother” to be title-cased! Let’s `UPDATE` this title by executing

```
UPDATE shows SET title = "How I Met Your Mother" WHERE title = "How i met your mother";
```

While you could retype each incorrectly entered show title, it’s much more efficient to select muliple variations of the same show and `UPDATE` these to the correct spelling. Maybe the `LIKE` keyword could come in handy! There are many titles to clean up, including all of the below:

- Adventure Time
- Arrow
- Avatar: The Last Airbender
- Brooklyn Nine-Nine
- Community
- Family Guy
- Friends
- Game of Thrones
- Gilmore Girls
- Grey’s Anatomy
- How I Met Your Mother
- It’s Always Sunny in Philadelphia
- Parks and Recreation
- Sherlock
- Squid Game
- The Bachelorette
- The Crown
- The Office
- The Queen’s Gambit
- The Untamed

If pressed for time, though, some of the more interesting clean-ups involve these shows:

- Brooklyn Nine-Nine
- Game of Thrones
- Grey’s Anatomy
- It’s Always Sunny in Philadelphia
- Parks and Recreation
- The Office

Be sure to save each of these SQL statements to store in a new file `favorites.sql`.

## How to Test Your Code
Once you have completed all of your database `UPDATE`s, you may want to `SELECT` all titles and list these alphabetically to make sure that all are correct.
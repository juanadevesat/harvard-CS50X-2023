SELECT DISTINCT (people.name) FROM movies
    JOIN stars ON movie_id = movies.id
    JOIN people ON people.id = person_id
    WHERE movies.id IN
    (SELECT movies.id FROM people
        JOIN stars ON people.id = person_id
        JOIN movies ON movie_id = movies.id
        WHERE name = 'Kevin Bacon')
    AND people.name NOT LIKE '%Kevin Bacon%';
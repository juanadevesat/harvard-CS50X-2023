SELECT title from movies
    JOIN stars ON movies.id = movie_id
    JOIN people ON person_id = people.id
    WHERE name = 'Bradley Cooper'
    OR name = 'Jennifer Lawrence'
    group by title
    having COUNT(title) > 1;
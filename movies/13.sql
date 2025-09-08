SELECT people.name
FROM people
WHERE people.name != 'Kevin Bacon'
And people.id IN (
    SELECT stars.person_id
    FROM stars
    WHERE stars.movie_id IN (
        SELECT stars.movie_id
        FROM stars
        WHERE stars.person_id IN (
            SELECT people.id
            FROM people
            WHERE people.name = 'Kevin Bacon'
            AND people.birth = 1958
        )
    )
);















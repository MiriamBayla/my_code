-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find crime scene description
SELECT description
FROM crime_scene_reports
WHERE month = 7
AND day = 28
AND year = 2023
AND street = 'Humphrey Street';

-- Read the interviews from wittnesses of bakery crime scene
SELECT transcript
FROM interviews
WHERE year = 2023
AND month = 7
AND day = 28;

-- Get passport numbers and names of people who exited the bakery's parking lot at specific time, as well as
-- made a less-than-minute phone call on that day
SELECT passport_number, name
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND activity LIKE 'exit'
    AND hour = 10
    AND minute < 30
)
INTERSECT
SELECT passport_number, name
FROM people
WHERE phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND duration < 100
);

-- Get the names of the people who was on a flight the next day and their id ends with same number as
-- the people who left the parking lot and made a phone call at the above times
SELECT name
FROM people
JOIN passengers ON passengers.passport_number =
people.passport_number
WHERE passengers.passport_number LIKE '%633'
OR '%733' OR '%1' OR '%5';
-- The only name that appears to have a flight the next day as well as left parking lot and made phone call
-- at specific time is 'Bruce'.

-- Get name and passport number of people who had a less than minute phone call with Bruce that day
SELECT name, passport_number
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE caller LIKE '(367) 555-5533'
    AND year = 2023
    AND month = 7
    AND day = 28
    AND duration < 100
);
-- Only 2 people had a less than minute phone call with Bruce that day. Their names are Carl and Robin.

-- When we search in Bruce's flight for a passport number like that of Carl, there are no results.
-- From here we know that Bruce's accomplice was Robin even though we don't have his passport number.
SELECT passport_number
FROM passengers
WHERE passport_number = 7771405611
AND flight_id IN (
    SELECT flight_id
    FROM passengers
    WHERE passport_number = 5773159633
);

-- Now we're checking which city Bruce's flight is going to
SELECT city
FROM airports
WHERE id IN (
    SELECT destination_airport_id
    FROM flights
    WHERE id IN (
        SELECT flight_id
        FROM passengers
        WHERE passport_number = 5773159633)
);
-- The city is 'New York City'.

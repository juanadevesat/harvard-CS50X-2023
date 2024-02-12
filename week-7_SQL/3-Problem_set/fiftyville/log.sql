-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Check logs of crime scene report on July 28, 2021 containing 'CS50 duck':
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street' AND description LIKE '%CS50 duck%';

-- Analise interviews of the three witnesses that mention 'bakery':
SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- Follow Ruth's lead looking at bakery_security_logs:
SELECT hour, minute, activity, bakery_security_logs.license_plate, people.name AS 'car_owner'
    FROM bakery_security_logs JOIN people ON bakery_security_logs.license_plate = people.license_plate
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25
    ORDER BY hour, minute;

-- Follow up on Eugene's lead looking at atm_transactions on Leggett Street before 10:15 am:
SELECT bank_accounts.account_number, bank_accounts.creation_year, people.name, people.phone_number, amount
    FROM atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number JOIN people ON bank_accounts.person_id = people.id
    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
    ORDER BY people.name;

-- Follow up on Raymond's lead looking into phone calls on July 28, 2021 that last less than 60 seconds:
SELECT phone_calls.id, people.name AS caller, receiver, duration
    FROM phone_calls JOIN people ON phone_calls.caller = people.phone_number
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- Cross these three tables to find people who are in all three:
SELECT people.name
    FROM bakery_security_logs JOIN people ON bakery_security_logs.license_plate = people.license_plate
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25
INTERSECT
SELECT people.name
    FROM atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number JOIN people ON bank_accounts.person_id = people.id
    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
INTERSECT
SELECT people.name
    FROM phone_calls JOIN people ON phone_calls.caller = people.phone_number
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- Find out who recieved a call from these suspects:
SELECT phone_calls.id, caller, people.name AS reciever
    FROM phone_calls JOIN people ON phone_calls.receiver = people.phone_number
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND phone_calls.id = 233 OR phone_calls.id = 255;

-- Find out which is the earliest flight that leaves fiftyville:
SELECT *
    FROM flights JOIN airports ON origin_airport_id = airports.id
    WHERE airports.city = 'Fiftyville' AND year = 2021 AND month = 7 AND day = 29
    ORDER BY hour, minute LIMIT 1;

-- Who bought tickets to this flight:
SELECT *
    FROM passengers JOIN people ON passengers.passport_number = people.passport_number
    WHERE flight_id = 36;

-- Where is this flight flying to:
SELECT *
    FROM flights JOIN airports ON destination_airport_id = airports.id
    WHERE flights.id = 36
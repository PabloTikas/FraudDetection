/* ################################################################### */

/*TRANSACTIONS TABLE */

SELECT * FROM transactions LIMIT 10; /* Basic table exploration */

SELECT COUNT(*) FROM transactions; /* Number of rows */
SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'transactions' AND table_schema = 'caixabank_hackathon2024'; /* Number of columns */

SELECT id, count(*) FROM transactions GROUP BY id HAVING COUNT(*) > 1; /* Check duplicates */

/* Null values for each column */

SET @table_name = 'transactions';
SET @sql = '';

SELECT 
    GROUP_CONCAT(
        CONCAT(
            'SUM(CASE WHEN `', COLUMN_NAME, '` IS NULL THEN 1 ELSE 0 END) AS `', COLUMN_NAME, '_nulls`'
        )
    ) INTO @sql
FROM INFORMATION_SCHEMA.COLUMNS
WHERE
	TABLE_SCHEMA = 'caixabank_hackathon2024'
	AND TABLE_NAME = @table_name;

SET @sql = CONCAT('SELECT ', @sql, ' FROM ', @table_name, ';');

PREPARE query FROM @sql;
EXECUTE query;
DEALLOCATE PREPARE query;
	

/* Obtain categories from Grouping fields*/
SELECT DISTINCT use_chip FROM transactions;
SELECT DISTINCT merchant_city FROM transactions;
SELECT COUNT(DISTINCT merchant_city) FROM transactions;
SELECT COUNT(DISTINCT merchant_state) FROM transactions;
SELECT COUNT(DISTINCT mcc) FROM transactions;
SELECT COUNT(DISTINCT errors) FROM transactions;

/* Obtain range from Date fields */
SELECT
	MIN(date_time) AS min_date,
	MAX(date_time) AS max_date,
	DATEDIFF(MAX(date_time), MIN(date_time))/365 AS total_years
FROM transactions;

/* Obtain range from Quant fields */
SELECT
	MIN(amount) AS min_amount,
	MAX(amount) AS max_amount,
	AVG(amount) AS avg_amount
FROM transactions;

/* ################################################################### */

/* BINARY TRAIN LABELS TABLE*/

SELECT * FROM binary_train_labels LIMIT 10; /* Basic table exploration */

SELECT COUNT(*) FROM binary_train_labels; /* Number of rows */
SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'binary_train_labels' AND table_schema = 'caixabank_hackathon2024'; /* Number of columns */

SELECT id, count(*) FROM transactions GROUP BY id HAVING COUNT(*) > 1; /* Check duplicates */

/* Null values for each column */

SET @table_name = 'binary_train_labels';
SET @sql = '';

SELECT 
    GROUP_CONCAT(
        CONCAT(
            'SUM(CASE WHEN `', COLUMN_NAME, '` IS NULL THEN 1 ELSE 0 END) AS `', COLUMN_NAME, '_nulls`'
        )
    ) INTO @sql
FROM INFORMATION_SCHEMA.COLUMNS
WHERE
	TABLE_SCHEMA = 'caixabank_hackathon2024'
	AND TABLE_NAME = @table_name;

SET @sql = CONCAT('SELECT ', @sql, ' FROM ', @table_name, ';');

PREPARE query FROM @sql;
EXECUTE query;
DEALLOCATE PREPARE query;

/*Obtain categories from Grouping fields */
SELECT DISTINCT is_fraud FROM binary_train_labels btl;

/* ################################################################### */

/* USERS TABLE */

SELECT * FROM users LIMIT 10;

SELECT COUNT(*) FROM users; /* Number of rows */
SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'users' AND table_schema = 'caixabank_hackathon2024'; /* Number of columns */

SELECT id, COUNT(*) FROM users GROUP BY id HAVING COUNT(*) > 1; /* Check duplicates */

/* Null values for each column */


SET SESSION group_concat_max_len = 10000; /* Temporarily increase for current session, otherwise error is raised */
SET @table_name = 'users';
SET @sql = '';

SELECT 
    GROUP_CONCAT(
        CONCAT(
            'SUM(CASE WHEN `', COLUMN_NAME, '` IS NULL THEN 1 ELSE 0 END) AS `', COLUMN_NAME, '_nulls`'
        )
    ) INTO @sql
FROM INFORMATION_SCHEMA.COLUMNS
WHERE
	TABLE_SCHEMA = 'caixabank_hackathon2024'
	AND TABLE_NAME = @table_name;

SET @sql = CONCAT('SELECT ', @sql, ' FROM ', @table_name, ';');

PREPARE query FROM @sql;
EXECUTE query;
DEALLOCATE PREPARE query;

/*Obtain categories from Grouping fields */
SELECT DISTINCT gender FROM users;
SELECT DISTINCT num_credit_cards FROM users ORDER BY 1;

/* Obtain range from Date fields */
SELECT
	MIN(birth_year) AS min_birth_year,
	MAX(birth_year) AS max_birth_year,
	MAX(birth_year) - MIN(birth_year) AS birth_year_range
FROM users;

/* Obtain range from Quant fields */
SELECT
	MIN(current_age) AS min_age,
	MAX(current_age) AS max_age,
	AVG(current_age) AS avg_age
FROM users;

SELECT
	MIN(retirement_age) AS min_age,
	MAX(retirement_age) AS max_age,
	AVG(retirement_age) AS avg_age
FROM users;

SELECT
	MIN(per_capita_income) AS min_income,
	MAX(per_capita_income) AS max_income,
	AVG(per_capita_income) AS avg_income
FROM users;

SELECT
	MIN(yearly_income) AS min_income,
	MAX(yearly_income) AS max_income,
	AVG(yearly_income) AS avg_income
FROM users;

SELECT
	MIN(total_debt) AS min_debt,
	MAX(total_debt) AS max_debt,
	AVG(total_debt) AS avg_debt
FROM users;

SELECT
	MIN(credit_score) AS min_score,
	MAX(credit_score) AS max_score,
	AVG(credit_score) AS avg_score
FROM users;

SELECT
	MIN(num_credit_cards) AS min_cards,
	MAX(num_credit_cards) AS max_cards,
	AVG(num_credit_cards) AS avg_cards
FROM users;

/* ################################################################### */

/* CARDS TABLE */

SELECT * FROM cards LIMIT 10; 

SELECT COUNT(*) FROM cards; /* Number of rows */
SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'cards' AND TABLE_SCHEMA='caixabank_hackathon2024'; /* Number of columns */

SELECT id, COUNT(*) FROM cards GROUP BY id HAVING COUNT(*) > 1; /*Check duplicates*/

SELECT
	user_id,
	MAX(num_cards_issued) AS cards_issued,
	COUNT(*) AS total_cards_per_user
FROM cards 
GROUP BY user_id
HAVING COUNT(*) > 1; /* Verify what "num_cards_issued" means. Question: Is it the number of cards owned by the user? Answer: No. */

SELECT
	card_type,
	credit_limit
FROM cards
WHERE card_type='Debit' OR card_type='Debit (Prepaid)';

/* Null values for each column */

SET @table_name = 'cards';
SET @sql = '';

SELECT 
    GROUP_CONCAT(
        CONCAT(
            'SUM(CASE WHEN `', COLUMN_NAME, '` IS NULL THEN 1 ELSE 0 END) AS `', COLUMN_NAME, '_nulls`'
        )
    ) INTO @sql
FROM INFORMATION_SCHEMA.COLUMNS
WHERE
	TABLE_SCHEMA = 'caixabank_hackathon2024'
	AND TABLE_NAME = @table_name;

SET @sql = CONCAT('SELECT ', @sql, ' FROM ', @table_name, ';');

PREPARE query FROM @sql;
EXECUTE query;
DEALLOCATE PREPARE query;

/*Obtain categories from Grouping fields */

SELECT DISTINCT card_brand FROM cards;
SELECT DISTINCT card_type FROM cards;
SELECT DISTINCT has_chip FROM cards;
SELECT DISTINCT card_on_dark_web FROM cards;


/*Obtain range from Date fields */

SELECT
	MAX(expires) AS max_expiration_date,
	MIN(expires) AS min_expiration_date,
	DATEDIFF(MAX(expires), MIN(expires))/365 AS total_range
FROM cards;

SELECT
	MAX(acct_open_date) AS max_open_date,
	MIN(acct_open_date) AS min_open_date,
	DATEDIFF(MAX(acct_open_date), MIN(acct_open_date))/365 AS total_range
FROM cards;

/*Obtain range from Quant fields */

SELECT
	MAX(credit_limit) AS max_limit,
	MIN(credit_limit) AS min_limit,
	AVG(credit_limit) AS avg_limit
FROM cards;


--https://github.com/EdukronCodes/SQL/blob/main/sql%20assignment1.md
--SELECT * FROM SH.CUSTOMERS
--🧱 A. Aggregation & Grouping (20 Questions)
-- 1. Find the total, average, minimum, and maximum credit limit of all customers.

-- SELECT 
--        AVG(CUST_CREDIT_LIMIT) AS AVG_CREDIT_LIMIT,
--        SUM(CUST_CREDIT_LIMIT) AS TOTAL_CREDIT_LIMIT,
--        MAX(CUST_CREDIT_LIMIT) AS MAX_CREDIT_LIMIT,
--        MIN(CUST_CREDIT_LIMIT) AS MIN_CREDIT_LIMIT
-- FROM SH.CUSTOMERS

-- 2. Count the number of customers in each income level.

-- SELECT CUST_INCOME_LEVEL, COUNT(*) AS CUST_COUNT
-- FROM SH.CUSTOMERS
-- GROUP BY CUST_INCOME_LEVEL

--3. Show total credit limit by state and country.

-- SELECT CUST_STATE_PROVINCE AS STATE,
-- COUNTRY_ID AS COUNTRY,
-- SUM(CUST_CREDIT_LIMIT) AS TOTAL
-- FROM SH.CUSTOMERS 
-- GROUP BY CUST_STATE_PROVINCE,COUNTRY_ID

--4. Display average credit limit for each marital status and gender combination.

-- SELECT CUST_MARITAL_STATUS,CUST_GENDER, AVG(CUST_CREDIT_LIMIT) AS AVG_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- GROUP BY CUST_MARITAL_STATUS,CUST_GENDER

-- 5. Find the top 3 states with the highest average credit limit.
-- SELECT CUST_STATE_PROVINCE, AVG(CUST_CREDIT_LIMIT) AS HIGHEST_AVG_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- GROUP BY CUST_STATE_PROVINCE
-- ORDER BY HIGHEST_AVG_CREDIT_LIMIT DESC
-- FETCH FIRST 3 ROWS ONLY

--6. Find the country with the maximum total customer credit limit.
-- SELECT COUNTRY_ID, MAX(CUST_CREDIT_LIMIT) AS TOTAL_CUST_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- GROUP BY COUNTRY_ID
-- ORDER BY TOTAL_CUST_CREDIT_LIMIT DESC
-- FETCH FIRST 1 ROWS ONLY

--7. Show the number of customers whose credit limit exceeds their state average.

-- SELECT COUNT(*) AS NUM_CUSTOMERS_ABOVE_STATE_AVG
-- FROM SH.CUSTOMERS CUST
-- JOIN (
--     SELECT CUST_STATE_PROVINCE, AVG(CUST_CREDIT_LIMIT) AS STATE_AVG_CREDIT
--     FROM SH.CUSTOMERS
--     GROUP BY CUST_STATE_PROVINCE
-- ) STATE_AVG
-- ON CUST.CUST_STATE_PROVINCE = STATE_AVG.CUST_STATE_PROVINCE
-- WHERE CUST.CUST_CREDIT_LIMIT > STATE_AVG.STATE_AVG_CREDIT

--8. Calculate total and average credit limit for customers born after 1980.

-- SELECT SUM(CUST_CREDIT_LIMIT) AS TOTAL_CREDIT_LIMIT, AVG(CUST_CREDIT_LIMIT) AS AVG_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- WHERE CUST_YEAR_OF_BIRTH >1980

--9. Find states having more than 50 customers.
-- SELECT CUST_STATE_PROVINCE,COUNT(*) AS NUM_CUST 
-- FROM SH.CUSTOMERS
-- GROUP BY CUST_STATE_PROVINCE
-- HAVING COUNT(*)>50

-- 10. List countries where the average credit limit is higher than the global average.
-- SELECT COUNTRY_ID, AVG(CUST_CREDIT_LIMIT) AS AVG_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- GROUP BY COUNTRY_ID
-- HAVING AVG(CUST_CREDIT_LIMIT) > (SELECT AVG(CUST_CREDIT_LIMIT) FROM SH.CUSTOMERS);

-- 11. Calculate the variance and standard deviation of customer credit limits by country
-- SELECT COUNTRY_ID,VAR_POP(CUST_CREDIT_LIMIT) AS VARIANCE , STDDEV_POP(CUST_CREDIT_LIMIT) AS STD_DEV
-- FROM SH.CUSTOMERS
-- GROUP BY COUNTRY_ID

-- 12. Find the state with the smallest range (max–min) in credit limits.

-- SELECT CUST_STATE_PROVINCE,
--     MAX(CUST_CREDIT_LIMIT) - MIN(CUST_CREDIT_LIMIT) AS CREDIT_LIMIT_RANGE
-- FROM SH.CUSTOMERS
-- GROUP BY CUST_STATE_PROVINCE
-- ORDER BY CREDIT_LIMIT_RANGE ASC
-- FETCH FIRST 1 ROW ONLY

-- 13. Show the total number of customers per income level and the percentage contribution of each.

-- SELECT CUST_INCOME_LEVEL,
--     COUNT(*) AS NUM_CUSTOMERS,
--     ROUND( (COUNT(*) * 100.0) / SUM(COUNT(*)) OVER (), 2) AS PERCENTAGE_CONTRIBUTION
-- FROM SH.CUSTOMERS
-- GROUP BY CUST_INCOME_LEVEL
-- ORDER BY NUM_CUSTOMERS DESC

-- 14. For each income level, find how many customers have NULL credit limits.

-- SELECT CUST_INCOME_LEVEL,
--     COUNT(*) AS NUM_CUSTOMERS_WITH_NULL_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- WHERE CUST_CREDIT_LIMIT IS NULL
-- GROUP BY CUST_INCOME_LEVEL
-- ORDER BY CUST_INCOME_LEVEL

--15. Display countries where the sum of credit limits exceeds 10 million.

-- SELECT COUNTRY_ID,
--     SUM(CUST_CREDIT_LIMIT) AS TOTAL_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- GROUP BY COUNTRY_ID
-- HAVING SUM(CUST_CREDIT_LIMIT) > 10000000

-- 16. Find the state that contributes the highest total credit limit to its country.

-- SELECT COUNTRY_ID, CUST_STATE_PROVINCE, TOTAL_STATE_CREDIT
-- FROM (SELECT COUNTRY_ID,CUST_STATE_PROVINCE,
--         SUM(CUST_CREDIT_LIMIT) AS TOTAL_STATE_CREDIT,
--         RANK() OVER (PARTITION BY COUNTRY_ID ORDER BY SUM(CUST_CREDIT_LIMIT) DESC) AS RANK_IN_COUNTRY
--     FROM SH.CUSTOMERS
--     GROUP BY COUNTRY_ID, CUST_STATE_PROVINCE)
-- WHERE RANK_IN_COUNTRY = 1

-- 17. Show total credit limit per year of birth, sorted by total descending.

-- SELECT CUST_YEAR_OF_BIRTH,
--     SUM(CUST_CREDIT_LIMIT) AS TOTAL_CREDIT_LIMIT
-- FROM SH.CUSTOMERS
-- GROUP BY CUST_YEAR_OF_BIRTH
-- ORDER BY TOTAL_CREDIT_LIMIT DESC

-- 18. Identify customers who hold the maximum credit limit in their respective country.

-- SELECT *FROM SH.CUSTOMERS c1
-- WHERE CUST_CREDIT_LIMIT = (
--     SELECT MAX(CUST_CREDIT_LIMIT)
--     FROM SH.CUSTOMERS c2
--     WHERE c2.COUNTRY_ID = c1.COUNTRY_ID)

-- 19. Show the difference between maximum and average credit limit per country.

-- SELECT COUNTRY_ID,
--     MAX(CUST_CREDIT_LIMIT) - AVG(CUST_CREDIT_LIMIT) AS MAX_AVG_DIFF
-- FROM SH.CUSTOMERS
-- GROUP BY COUNTRY_ID

-- 20. Display the overall rank of each state based on its total credit limit (using GROUP BY + analytic rank).

-- SELECT CUST_STATE_PROVINCE,TOTAL_STATE_CREDIT,
--     RANK() OVER (ORDER BY TOTAL_STATE_CREDIT DESC) AS STATE_RANK
-- FROM (SELECT CUST_STATE_PROVINCE,
--         SUM(CUST_CREDIT_LIMIT) AS TOTAL_STATE_CREDIT
--     FROM SH.CUSTOMERS
--     GROUP BY CUST_STATE_PROVINCE)
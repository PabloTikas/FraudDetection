
/* Merchant categories with most fraud (in US$) */
SELECT
	t.mcc,
	SUM(t.amount)
FROM transactions t
LEFT JOIN binary_train_labels btl ON btl.transaction_id = t.id
WHERE btl.is_fraud > 0
GROUP BY t.mcc
ORDER BY sum(t.amount) DESC
LIMIT 10;

/* States with most fraud (in US$) */
SELECT
	t.merchant_state,
	SUM(t.amount)
FROM transactions t
LEFT JOIN binary_train_labels btl ON btl.transaction_id = t.id
WHERE btl.is_fraud > 0
GROUP BY t.merchant_state
ORDER BY sum(t.amount) DESC
LIMIT 10;

/* Note: NULL merchant_state indicates ONLINE transactions. It makes sense that most fraudulent transactions are online */

/* Time Evolution of Total Transactions & Fraud Ratio */
SELECT
	YEAR(t.date_time) AS "YEAR",
	COUNT(*) AS "Total Transactions",
	100*COUNT(CASE WHEN btl.is_fraud = 1 THEN 1 END)/COUNT(*) AS "Fraud Ratio"	
FROM transactions t
LEFT JOIN binary_train_labels btl ON btl.transaction_id = t.id
GROUP BY YEAR(t.date_time)
ORDER BY YEAR(t.date_time);

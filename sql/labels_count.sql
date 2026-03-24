/* Query 1: Count fraudulent transactions */

SELECT COUNT(*) 
FROM transactions t
LEFT JOIN binary_train_labels btl ON btl.transaction_id = t.id 
WHERE btl.is_fraud=1;

/* Answer 1: 13.332 fraudulent transactions */

/* Query 2: Count non-fraudulent transactions */

SELECT COUNT(*)
FROM transactions t
LEFT JOIN binary_train_labels btl ON btl.transaction_id = t.id 
WHERE btl.is_fraud=0;

/*Answer 2: 8.901.631 non-fraudulent transactions */

/* Query 3: Unlabeled transactions */
SELECT COUNT(*) - (8901631+ 13332)
FROM transactions t;

/*Answer 3: 4.390.952 unlabeled transactions */



# Financial Transactions Dataset
## Raw Data Report

*This comprehensive financial dataset created by Caixabank Tech for the 2024 AI Hackathon combines transaction records, customer information, and card data from a banking institution, spanning across the 2010s decade. The dataset is designed for multiple analytical purposes, including synthetic fraud detection, customer behavior analysis, and expense forecasting.*

https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets

### Database Schema

#### Transactions Table

##### Type
Main Table

##### Description

Table containing card transactions.
- **Number of rows:** 13.305.915
- **Number of columns:** 12

##### Fields
- **id (type: integer)** = transaction identifier (unique) [0 nulls].
- **date_time (type: timestamp)** = timestamp for transaction [0 nulls].
- **user_id (type: integer)** = card owner's identifier [0 nulls].
- **card_id (type: integer)** = card's identifier [0 nulls].
- **amount (type: float)** = total transaction value (in US $, negative values indicate returns) [0 nulls].
- **use_chip (type: string)** = type of transaction (Swift, Online) [0 nulls].
- **merchant_id (type: integer)** = merchant's identifier [0 nulls].
- **merchant_city (type: string)** = merchant's city [0 nulls].
- **merchant_state (type: string)** = merchant's state [1.563.700 nulls].
- **zip (type: integer)** = merchant's zip code [1.652.706 nulls].
- **mcc (type: integer)** = merchant's category code, a four-digit number assigned by card networks to classify a business by the type of goods or services it provides (decoder in "mcc.json") [0 nulls].
- **errors (type: string)** = indicates any error that might have ocurred during the transaction [13.094.522 nulls].

###### Grouping fields
*These are fields that can be used to group data*
- **use_chip:** 3 categories
- **merchant_city:** 12.492 categories
- **merchant_state:** 200 categories
- **mcc:** 109 categories
- **errors:** 23 categories

###### Date fields
*These fields provide temporal context for the data, enabling analysis of when events occur, how frequently they happen, and how they evolve over time.*
- **date_time:** [Min. date = *2010-01-01 00:01:00*, Max. date = *2019-10-31 23:59:00*, Range Length = *9.8 years*]


###### Quant fields
*These fields provide quantitative insights into the data, answering questions such as: 'How much…?' or 'How many...?'*
- **amount:** [Min. = *-500\$*, Max. = *6.820,2\$*, Avg. = *42,97\$*]

##### Related Tables

- **users** through *user_id*
- **cards** through *card_id*
- **binary_train_labels** through *id*

#### Binary Train Labels Table

##### Type
Target Table

##### Description

Table containing fraudulent/non-fraudulent labels for card transactions.
- **Number of rows:** 8.914.963
- **Number of columns:** 2

##### Fields
- **transaction_id (type: integer)** = transaction identifier (unique) [0 nulls].
- **is_fraud (type: integer)** = fraudulent (1) / non-fraudulent (0) labels [0 nulls].

***Note:** Even though there are no nulls in this table, one must notice the difference between the number of rows in the 'transactions' table (+13M rows) and this 'binary_train_labels' table (<9M rows). This means that when joined together, there will be transactions left unlabelled (i.e. with null values).*

###### Grouping fields
*These are fields that can be used to group data*
- **is_fraud:** 2 categories

###### Date fields
*These fields provide temporal context for the data, enabling analysis of when events occur, how frequently they happen, and how they evolve over time.*

None

###### Quant fields
*These fields provide quantitative insights into the data, answering questions such as: 'How much…?' or 'How many...?'*

None

##### Related Tables

- **transactions** through *transaction_id*

#### Users Table

##### Type
Complementary Table

##### Description

Table containing user information.
- **Number of rows:** 2000
- **Number of columns:** 14

##### Fields
- **id (type: integer)** = card user's identifier (unique) [0 nulls].
- **current_age (type: integer)** = current age of the user [0 nulls].
- **retirement_age (type: integer)** = expected retirement age for the user [0 nulls].
- **birth_year (type: integer)** = user's birth year [0 nulls].
- **birth_month (type: integer)** = user's birth month [0 nulls].
- **gender (type: string)** = user's gender [0 nulls].
- **address (type: string)** = user's home address [0 nulls].
- **latitude (type: float)** = geographical latitude (in º) [0 nulls].
- **longitude (type: float)** = geographical longitude (in º) [0 nulls].
- **per_capita_income (type: float)** = avg of yearly income among all residents in the household (in US $) [0 nulls].
- **yearly_income (type: float)** = user's yearly income (in US $) [0 nulls].
- **total_debt (type: float)** = user's total debt (in US $) [0 nulls].
- **credit_score (type: integer)** = score assigned to the user by financial entities based on risk profile. Higher scores indicate a more trustworthy borrower [0 nulls].
- **num_credit_cards (type: integer)** = number of credit cards owned by the user [0 nulls].

###### Grouping fields
*These are fields that can be used to group data*
- **current_age:** use bins
- **retirement_age:** use bins
- **gender:** 2 categories
- **credit_score:** use bins
- **num_credit_cards:** use bins

###### Date fields
*These fields provide temporal context for the data, enabling analysis of when events occur, how frequently they happen, and how they evolve over time.*
- **birth_year:** [Min. = *1918*, Max. = *2002*, Range Length = *84 years*]


###### Quant fields
*These fields provide quantitative insights into the data, answering questions such as: 'How much…?' or 'How many...?'*
- **current_age:** [Min. = *18*, Max. = *101*, Avg. = *45,4*]
- **retirement_age:** [Min. = *50*, Max. = *79*, Avg. = *66,2*]
- **per_capita_income:** [Min. = *0\$*, Max. = *163.145\$*, Avg. = *23.141,9\$*]
- **yearly_income:** [Min. = *1\$*, Max. = *307.018\$*, Avg. = *45.715\$*]
- **total_debt:** [Min. = *0\$*, Max. = *516.263\$*, Avg. = *63.709,7\$*]
- **credit_score:** [Min. = *480*, Max. = *850*, Avg. = *709,7*]
- **num_credit_cards:** [Min. = *1*, Max. = *9*, Avg. = *3,1*]


##### Related Tables

- **transactions** through *id*

#### Cards Table

##### Type
Complementary Table

##### Description

Table containing card information.
- **Number of rows:** 6.146
- **Number of columns:** 13

##### Fields
- **id (type: integer)** = card's identifier (unique) [0 nulls].
- **user_id (type: integer)** = card's owner identifier [0 nulls].
- **card_brand (type: string)** = card's brand [0 nulls].
- **card_type (type: string)** = card's type (credit, debit or debit prepaid) [0 nulls].
- **card_number (type: integer)** = card's number (unique) [0 nulls].
- **expires (type: date)** = card's expiration date [0 nulls].
- **cvv (type: integer)** = Card Verification Value, a 3-digit code for an extra layer of protection [0 nulls].
- **has_chip (type: string)** = indicates if the card has a chip [0 nulls].
- **num_cards_issued (type: integer)** = number of card reissues (if stolen, lost, etc.) [0 nulls]. *Question: shouldn't the card_number change when reissued?*
- **credit_limit (type: float)** = card's credit limit (for 'Debit' cards, this can be though of as "spending caps") [0 nulls].
- **acct_open_date (type: date)** = associated account opening date [0 nulls].
- **year_pin_last_changed (type: integer)** = last year where card's PIN code was changed [0 nulls].
- **card_on_dark_web (type: string)** = indicates whether card information is on the Dark Web [0 nulls].

###### Grouping fields
*These are fields that can be used to group data*
- **card_brand:** 4 categories
- **card_type:** 3 categories
- **has_chip:** 2 categories
- **num_cards_issued:** use bins
- **year_pin_last_changed:** use bins
- **credit_limit:** use bins
- **card_on_dark_web:** 1 category (superfluous)

###### Date fields
*These fields provide temporal context for the data, enabling analysis of when events occur, how frequently they happen, and how they evolve over time.*
- **expires:** [Min. date = *1997-07-01*, Max. date = *2024-12-01*, Range Length = *27.4 years*]
- **acct_open_date:** [Min. date = *1991-01-01*, Max. date = *2020-02-01*, Range Length = *29.1 years*]

###### Quant fields
*These fields provide quantitative insights into the data, answering questions such as: 'How much…?' or 'How many...?'*
- **credit_limit:** [Min. = *0,00\$*, Max. = *151.223,00\$*, Avg. = *14.347,49\$*]

##### Related Tables

- **transactions** through *id*
- **users** through *user_id*


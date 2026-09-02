# Dataset Schema Report

## device.csv
|   Column Order | Column Name   | Data Type   | Nullable   | Unique Candidate   | Primary ID Candidate   | Timestamp Column   | Categorical Column   | Numerical Column   |
|---------------:|:--------------|:------------|:-----------|:-------------------|:-----------------------|:-------------------|:---------------------|:-------------------|
|              1 | id            | String      | False      | True               | True                   | False              | False                | False              |
|              2 | date          | String      | False      | False              | False                  | True               | False                | False              |
|              3 | user          | String      | False      | False              | False                  | False              | False                | False              |
|              4 | pc            | String      | False      | False              | False                  | False              | False                | False              |
|              5 | activity      | String      | False      | False              | False                  | False              | False                | False              |

## email.csv
|   Column Order | Column Name   | Data Type   | Nullable   | Unique Candidate   | Primary ID Candidate   | Timestamp Column   | Categorical Column   | Numerical Column   |
|---------------:|:--------------|:------------|:-----------|:-------------------|:-----------------------|:-------------------|:---------------------|:-------------------|
|              1 | id            | String      | False      | True               | True                   | False              | False                | False              |
|              2 | date          | String      | False      | False              | False                  | True               | False                | False              |
|              3 | user          | String      | False      | False              | False                  | False              | False                | False              |
|              4 | pc            | String      | False      | False              | False                  | False              | False                | False              |
|              5 | to            | String      | False      | False              | False                  | False              | False                | False              |
|              6 | cc            | String      | True       | False              | False                  | False              | False                | False              |
|              7 | bcc           | String      | True       | False              | False                  | False              | False                | False              |
|              8 | from          | String      | False      | False              | False                  | False              | False                | False              |
|              9 | size          | Int64       | False      | False              | False                  | False              | False                | True               |
|             10 | attachments   | Int64       | False      | False              | False                  | False              | False                | True               |
|             11 | content       | String      | False      | True               | False                  | False              | False                | False              |

## file.csv
|   Column Order | Column Name   | Data Type   | Nullable   | Unique Candidate   | Primary ID Candidate   | Timestamp Column   | Categorical Column   | Numerical Column   |
|---------------:|:--------------|:------------|:-----------|:-------------------|:-----------------------|:-------------------|:---------------------|:-------------------|
|              1 | id            | String      | False      | True               | True                   | False              | False                | False              |
|              2 | date          | String      | False      | False              | False                  | True               | False                | False              |
|              3 | user          | String      | False      | False              | False                  | False              | False                | False              |
|              4 | pc            | String      | False      | False              | False                  | False              | False                | False              |
|              5 | filename      | String      | False      | True               | False                  | False              | False                | False              |
|              6 | content       | String      | False      | False              | False                  | False              | False                | False              |

## http.csv
|   Column Order | Column Name   | Data Type   | Nullable   | Unique Candidate   | Primary ID Candidate   | Timestamp Column   | Categorical Column   | Numerical Column   |
|---------------:|:--------------|:------------|:-----------|:-------------------|:-----------------------|:-------------------|:---------------------|:-------------------|
|              1 | id            | String      | False      | True               | True                   | False              | False                | False              |
|              2 | date          | String      | False      | False              | False                  | True               | False                | False              |
|              3 | user          | String      | False      | False              | False                  | False              | False                | False              |
|              4 | pc            | String      | False      | False              | False                  | False              | False                | False              |
|              5 | url           | String      | False      | False              | False                  | False              | False                | False              |
|              6 | content       | String      | False      | True               | False                  | False              | False                | False              |

## logon.csv
|   Column Order | Column Name   | Data Type   | Nullable   | Unique Candidate   | Primary ID Candidate   | Timestamp Column   | Categorical Column   | Numerical Column   |
|---------------:|:--------------|:------------|:-----------|:-------------------|:-----------------------|:-------------------|:---------------------|:-------------------|
|              1 | id            | String      | False      | True               | True                   | False              | False                | False              |
|              2 | date          | String      | False      | False              | False                  | True               | False                | False              |
|              3 | user          | String      | False      | False              | False                  | False              | False                | False              |
|              4 | pc            | String      | False      | False              | False                  | False              | False                | False              |
|              5 | activity      | String      | False      | False              | False                  | False              | False                | False              |

## psychometric.csv
|   Column Order | Column Name   | Data Type   | Nullable   | Unique Candidate   | Primary ID Candidate   | Timestamp Column   | Categorical Column   | Numerical Column   |
|---------------:|:--------------|:------------|:-----------|:-------------------|:-----------------------|:-------------------|:---------------------|:-------------------|
|              1 | employee_name | String      | False      | True               | False                  | False              | False                | False              |
|              2 | user_id       | String      | False      | True               | True                   | False              | False                | False              |
|              3 | O             | Int64       | False      | False              | False                  | False              | False                | True               |
|              4 | C             | Int64       | False      | False              | False                  | False              | False                | True               |
|              5 | E             | Int64       | False      | False              | False                  | False              | False                | True               |
|              6 | A             | Int64       | False      | False              | False                  | False              | False                | True               |
|              7 | N             | Int64       | False      | False              | False                  | False              | False                | True               |


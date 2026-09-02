# Data Dictionary

## device.csv
| Field Name   | Data Type   | Description                                           | Nullable   |   Missing Values |   Unique Values | Is Primary Key Candidate   | Is Categorical   |
|:-------------|:------------|:------------------------------------------------------|:-----------|-----------------:|----------------:|:---------------------------|:-----------------|
| id           | String      | Auto-generated description for id in device.csv       | False      |                0 |          405380 | True                       | False            |
| date         | String      | Auto-generated description for date in device.csv     | False      |                0 |          399631 | False                      | False            |
| user         | String      | Auto-generated description for user in device.csv     | False      |                0 |             265 | False                      | False            |
| pc           | String      | Auto-generated description for pc in device.csv       | False      |                0 |             971 | False                      | False            |
| activity     | String      | Auto-generated description for activity in device.csv | False      |                0 |               2 | False                      | False            |

## email.csv
| Field Name   | Data Type   | Description                                             | Nullable   |   Missing Values |   Unique Values | Is Primary Key Candidate   | Is Categorical   |
|:-------------|:------------|:--------------------------------------------------------|:-----------|-----------------:|----------------:|:---------------------------|:-----------------|
| id           | String      | Auto-generated description for id in email.csv          | False      |                0 |         2629979 | True                       | False            |
| date         | String      | Auto-generated description for date in email.csv        | False      |                0 |         2384107 | False                      | False            |
| user         | String      | Auto-generated description for user in email.csv        | False      |                0 |            1000 | False                      | False            |
| pc           | String      | Auto-generated description for pc in email.csv          | False      |                0 |            1000 | False                      | False            |
| to           | String      | Auto-generated description for to in email.csv          | False      |                0 |          659170 | False                      | False            |
| cc           | String      | Auto-generated description for cc in email.csv          | True       |          1617054 |          150742 | False                      | False            |
| bcc          | String      | Auto-generated description for bcc in email.csv         | True       |          2212977 |             615 | False                      | False            |
| from         | String      | Auto-generated description for from in email.csv        | False      |                0 |            2678 | False                      | False            |
| size         | Int64       | Auto-generated description for size in email.csv        | False      |                0 |           65123 | False                      | False            |
| attachments  | Int64       | Auto-generated description for attachments in email.csv | False      |                0 |              10 | False                      | False            |
| content      | String      | Auto-generated description for content in email.csv     | False      |                0 |         2629964 | False                      | False            |

## file.csv
| Field Name   | Data Type   | Description                                         | Nullable   |   Missing Values |   Unique Values | Is Primary Key Candidate   | Is Categorical   |
|:-------------|:------------|:----------------------------------------------------|:-----------|-----------------:|----------------:|:---------------------------|:-----------------|
| id           | String      | Auto-generated description for id in file.csv       | False      |                0 |          445581 | True                       | False            |
| date         | String      | Auto-generated description for date in file.csv     | False      |                0 |          432924 | False                      | False            |
| user         | String      | Auto-generated description for user in file.csv     | False      |                0 |             264 | False                      | False            |
| pc           | String      | Auto-generated description for pc in file.csv       | False      |                0 |             956 | False                      | False            |
| filename     | String      | Auto-generated description for filename in file.csv | False      |                0 |          445581 | False                      | False            |
| content      | String      | Auto-generated description for content in file.csv  | False      |                0 |          423033 | False                      | False            |

## http.csv
| Field Name   | Data Type   | Description                                        | Nullable   |   Missing Values |   Unique Values | Is Primary Key Candidate   | Is Categorical   |
|:-------------|:------------|:---------------------------------------------------|:-----------|-----------------:|----------------:|:---------------------------|:-----------------|
| id           | String      | Auto-generated description for id in http.csv      | False      |                0 |        28434423 | True                       | False            |
| date         | String      | Auto-generated description for date in http.csv    | False      |                0 |        12527236 | False                      | False            |
| user         | String      | Auto-generated description for user in http.csv    | False      |                0 |            1000 | False                      | False            |
| pc           | String      | Auto-generated description for pc in http.csv      | False      |                0 |            1000 | False                      | False            |
| url          | String      | Auto-generated description for url in http.csv     | False      |                0 |            6033 | False                      | False            |
| content      | String      | Auto-generated description for content in http.csv | False      |                0 |        28434286 | False                      | False            |

## logon.csv
| Field Name   | Data Type   | Description                                          | Nullable   |   Missing Values |   Unique Values | Is Primary Key Candidate   | Is Categorical   |
|:-------------|:------------|:-----------------------------------------------------|:-----------|-----------------:|----------------:|:---------------------------|:-----------------|
| id           | String      | Auto-generated description for id in logon.csv       | False      |                0 |          854859 | True                       | False            |
| date         | String      | Auto-generated description for date in logon.csv     | False      |                0 |          338041 | False                      | False            |
| user         | String      | Auto-generated description for user in logon.csv     | False      |                0 |            1000 | False                      | False            |
| pc           | String      | Auto-generated description for pc in logon.csv       | False      |                0 |            1003 | False                      | False            |
| activity     | String      | Auto-generated description for activity in logon.csv | False      |                0 |               2 | False                      | False            |

## psychometric.csv
| Field Name    | Data Type   | Description                                                      | Nullable   |   Missing Values |   Unique Values | Is Primary Key Candidate   | Is Categorical   |
|:--------------|:------------|:-----------------------------------------------------------------|:-----------|-----------------:|----------------:|:---------------------------|:-----------------|
| employee_name | String      | Auto-generated description for employee_name in psychometric.csv | False      |                0 |            1000 | False                      | False            |
| user_id       | String      | Auto-generated description for user_id in psychometric.csv       | False      |                0 |            1000 | True                       | False            |
| O             | Int64       | Auto-generated description for O in psychometric.csv             | False      |                0 |              41 | False                      | False            |
| C             | Int64       | Auto-generated description for C in psychometric.csv             | False      |                0 |              41 | False                      | False            |
| E             | Int64       | Auto-generated description for E in psychometric.csv             | False      |                0 |              41 | False                      | False            |
| A             | Int64       | Auto-generated description for A in psychometric.csv             | False      |                0 |              41 | False                      | False            |
| N             | Int64       | Auto-generated description for N in psychometric.csv             | False      |                0 |              30 | False                      | False            |


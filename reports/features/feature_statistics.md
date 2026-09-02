# Feature Engineering Statistical Report

## Module: user_features
- Total Users/Entities: 1000
- Total Features: 6

### Basic Statistics
|       |   Total_Login_Count |   Total_Logout_Count |   Host_Switching_Count |   Night_Activity_Count |   Weekend_Activity_Count |   Average_Logins_Per_Day |
|:------|--------------------:|---------------------:|-----------------------:|-----------------------:|-------------------------:|-------------------------:|
| count |                1000 |                 1000 |              1000      |              1000      |                1000      |                     1000 |
| mean  |                   0 |                    0 |                11.542  |                21.441  |                   6.156  |                        0 |
| std   |                   0 |                    0 |                48.4694 |                73.7349 |                  21.4876 |                        0 |
| min   |                   0 |                    0 |                 1      |                 0      |                   0      |                        0 |
| 25%   |                   0 |                    0 |                 1      |                 0      |                   0      |                        0 |
| 50%   |                   0 |                    0 |                 1      |                 0      |                   0      |                        0 |
| 75%   |                   0 |                    0 |                 2      |                 0      |                   0      |                        0 |
| max   |                   0 |                    0 |               317      |               429      |                 190      |                        0 |

## Module: file_features
- Total Users/Entities: 246
- Total Features: 4

### Basic Statistics
|       |   Total_Files_Accessed |   Unique_Files_Accessed |   Sensitive_File_Access_Count |   File_Host_Switching_Count |
|:------|-----------------------:|------------------------:|------------------------------:|----------------------------:|
| count |                 246    |                  246    |                        246    |                    246      |
| mean  |                1016.26 |                 1016.26 |                        911.52 |                     10.1138 |
| std   |                1354.32 |                 1354.32 |                       1217.07 |                     44.7266 |
| min   |                   1    |                    1    |                          1    |                      1      |
| 25%   |                 226.25 |                  226.25 |                        201.25 |                      1      |
| 50%   |                 432    |                  432    |                        385    |                      1      |
| 75%   |                1174    |                 1174    |                       1043.25 |                      1      |
| max   |                6085    |                 6085    |                       5432    |                    271      |

## Module: usb_features
- Total Users/Entities: 249
- Total Features: 5

### Basic Statistics
|       |   USB_Insert_Count |   USB_Removal_Count |   After_Hours_USB_Usage |   Weekend_USB_Usage |   Unique_USB_PCs |
|:------|-------------------:|--------------------:|------------------------:|--------------------:|-----------------:|
| count |                249 |                 249 |                249      |            249      |         249      |
| mean  |                  0 |                   0 |                 35.5863 |             42.6546 |          17.6386 |
| std   |                  0 |                   0 |                142.179  |            145.723  |          82.0297 |
| min   |                  0 |                   0 |                  0      |              0      |           1      |
| 25%   |                  0 |                   0 |                  0      |              0      |           1      |
| 50%   |                  0 |                   0 |                  0      |              0      |           1      |
| 75%   |                  0 |                   0 |                  2      |              4      |           1      |
| max   |                  0 |                   0 |                789      |           1084      |         489      |

## Module: email_features
- Total Users/Entities: 1000
- Total Features: 4

### Basic Statistics
|       |   Emails_Sent |   Unique_Recipients |   External_Emails_Sent |   Email_Host_Switching |
|:------|--------------:|--------------------:|-----------------------:|-----------------------:|
| count |      1000     |           1000      |              1000      |                   1000 |
| mean  |       250     |            148.163  |                55.922  |                      1 |
| std   |       162.748 |             85.9114 |                41.3241 |                      0 |
| min   |        26     |             23      |                 0      |                      1 |
| 25%   |        90     |             76      |                19      |                      1 |
| 50%   |       269     |            156      |                54      |                      1 |
| 75%   |       338.25  |            195.25   |                83      |                      1 |
| max   |      1107     |            424      |               237      |                      1 |

## Module: web_features
- Total Users/Entities: 1000
- Total Features: 3

### Basic Statistics
|       |   Total_Website_Visits |   Unique_URLs_Visited |   After_Hours_Web_Usage |
|:------|-----------------------:|----------------------:|------------------------:|
| count |               1000     |             1000      |              1000       |
| mean  |                250     |               50.129  |                 0.812   |
| std   |                171.519 |               22.7653 |                 4.04735 |
| min   |                 23     |               10      |                 0       |
| 25%   |                 79     |               32      |                 0       |
| 50%   |                262     |               50.5    |                 0       |
| 75%   |                342     |               66      |                 0       |
| max   |               1200     |              118      |                49       |

## Module: temporal_features
- Total Users/Entities: 1000
- Total Features: 3

### Basic Statistics
|       |   Mean_Time_Between_Events |   Max_Time_Between_Events |   Peak_Activity_Hour |
|:------|---------------------------:|--------------------------:|---------------------:|
| count |             1000           |            1000           |       1000           |
| mean  |                2.66454e-17 |               1.24345e-16 |          2.84217e-17 |
| std   |                1.0005      |               1.0005      |          1.0005      |
| min   |               -3.05364     |              -7.28056     |         -0.953168    |
| 25%   |               -0.666196    |               0.165741    |         -0.953168    |
| 50%   |                0.705795    |               0.288168    |         -0.758047    |
| 75%   |                0.774236    |               0.3776      |          1.19317     |
| max   |                0.799499    |               0.582512    |          1.77853     |

## Module: session_features
- Total Users/Entities: 1000
- Total Features: 3

### Basic Statistics
|       |   Average_Events_Per_Session |   Average_Session_Duration |   Session_Density |
|:------|-----------------------------:|---------------------------:|------------------:|
| count |               1000           |             1000           |    1000           |
| mean  |                 -1.77636e-17 |                1.24345e-16 |      -4.84945e-16 |
| std   |                  1.0005      |                1.0005      |       1.0005      |
| min   |                 -0.489196    |               -1.66658     |      -1.20946     |
| 25%   |                 -0.480852    |               -0.49909     |      -0.757869    |
| 50%   |                 -0.472508    |               -0.407763    |      -0.374977    |
| 75%   |                  0.16997     |                0.19879     |       0.499529    |
| max   |                  5.5017      |                4.29957     |       4.26681     |

## Module: statistical_features
- Total Users/Entities: 1000
- Total Features: 5

### Basic Statistics
|       |   Mean_Daily_Events |   Median_Daily_Events |   Std_Daily_Events |   Min_Daily_Events |   Max_Daily_Events |
|:------|--------------------:|----------------------:|-------------------:|-------------------:|-------------------:|
| count |      1000           |        1000           |     1000           |        1000        |         1000       |
| mean  |         3.44613e-16 |          -1.03029e-16 |        7.81597e-17 |           1.259    |            3.462   |
| std   |         1.0005      |           1.0005      |        1.0005      |           0.562348 |            2.41711 |
| min   |        -0.489196    |          -0.450678    |       -0.721336    |           1        |            2       |
| 25%   |        -0.480852    |          -0.450678    |       -0.549977    |           1        |            2       |
| 50%   |        -0.472508    |          -0.450678    |       -0.549977    |           1        |            2       |
| 75%   |         0.16997     |           0.346277    |        0.295824    |           1        |            5       |
| max   |         5.5017      |           5.92497     |        4.9528      |           4        |           15       |

## Module: risk_indicators
- Total Users/Entities: 1000
- Total Features: 3

### Basic Statistics
|       |   Host_Switching_Score |   Late_Night_Score |   Weekend_Activity_Score |
|:------|-----------------------:|-------------------:|-------------------------:|
| count |              1000      |          1000      |                1000      |
| mean  |                11.542  |            21.441  |                   6.156  |
| std   |                48.4694 |            73.7349 |                  21.4876 |
| min   |                 1      |             0      |                   0      |
| 25%   |                 1      |             0      |                   0      |
| 50%   |                 1      |             0      |                   0      |
| 75%   |                 2      |             0      |                   0      |
| max   |               317      |           429      |                 190      |


# Enterprise Feature Catalog

| Feature Name                | Source Module        | Data Type   | Future Graph Usage   |
|:----------------------------|:---------------------|:------------|:---------------------|
| Total_Login_Count           | user_features        | UInt32      | Node Feature         |
| Total_Logout_Count          | user_features        | UInt32      | Node Feature         |
| Host_Switching_Count        | user_features        | UInt32      | Node Feature         |
| Night_Activity_Count        | user_features        | UInt32      | Node Feature         |
| Weekend_Activity_Count      | user_features        | UInt32      | Node Feature         |
| Average_Logins_Per_Day      | user_features        | Float64     | Node Feature         |
| Total_Files_Accessed        | file_features        | UInt32      | Node Feature         |
| Unique_Files_Accessed       | file_features        | UInt32      | Node Feature         |
| Sensitive_File_Access_Count | file_features        | UInt32      | Node Feature         |
| File_Host_Switching_Count   | file_features        | UInt32      | Node Feature         |
| USB_Insert_Count            | usb_features         | UInt32      | Node Feature         |
| USB_Removal_Count           | usb_features         | UInt32      | Node Feature         |
| After_Hours_USB_Usage       | usb_features         | UInt32      | Node Feature         |
| Weekend_USB_Usage           | usb_features         | UInt32      | Node Feature         |
| Unique_USB_PCs              | usb_features         | UInt32      | Node Feature         |
| Emails_Sent                 | email_features       | UInt32      | Node Feature         |
| Unique_Recipients           | email_features       | UInt32      | Node Feature         |
| External_Emails_Sent        | email_features       | UInt32      | Node Feature         |
| Email_Host_Switching        | email_features       | UInt32      | Node Feature         |
| Total_Website_Visits        | web_features         | UInt32      | Node Feature         |
| Unique_URLs_Visited         | web_features         | UInt32      | Node Feature         |
| After_Hours_Web_Usage       | web_features         | UInt32      | Node Feature         |
| Mean_Time_Between_Events    | temporal_features    | Float64     | Node Feature         |
| Max_Time_Between_Events     | temporal_features    | Float64     | Node Feature         |
| Peak_Activity_Hour          | temporal_features    | Float64     | Node Feature         |
| Average_Events_Per_Session  | session_features     | Float64     | Edge/Node Feature    |
| Average_Session_Duration    | session_features     | Float64     | Edge/Node Feature    |
| Session_Density             | session_features     | Float64     | Edge/Node Feature    |
| Mean_Daily_Events           | statistical_features | Float64     | Node Feature         |
| Median_Daily_Events         | statistical_features | Float64     | Node Feature         |
| Std_Daily_Events            | statistical_features | Float64     | Node Feature         |
| Min_Daily_Events            | statistical_features | UInt32      | Node Feature         |
| Max_Daily_Events            | statistical_features | UInt32      | Node Feature         |
| Host_Switching_Score        | risk_indicators      | UInt32      | Node Feature         |
| Late_Night_Score            | risk_indicators      | UInt32      | Node Feature         |
| Weekend_Activity_Score      | risk_indicators      | UInt32      | Node Feature         |

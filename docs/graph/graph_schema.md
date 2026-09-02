# Graph Schema

## Node Types

| Type | Source | Key Features |
|------|--------|--------------|
| User | LDAP, psychometric | role, department, Big Five scores |
| PC | logon | is_shared, assigned_users |
| Email | email.csv | size, attachments, topics |
| File | file.csv | file_type, topics |
| URL | http.csv | domain, topics |

## Edge Types

| Relation | Source → Target | Source File |
|----------|----------------|-------------|
| logon | User → PC | logon.csv |
| logoff | User → PC | logon.csv |
| device_connect | User → Device | device.csv |
| email_send | User → Email | email.csv |
| email_receive | Email → User | email.csv |
| file_copy | User → File | file.csv |
| http_visit | User → URL | http.csv |
| works_with | User → User | LDAP + email |

All edges are temporally stamped with the event datetime.

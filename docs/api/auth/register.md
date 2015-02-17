User Registration
=======================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/auth/register/ |
| Method          | POST               |
| Content-Type    | application/json   |


#####Payload - raw

| Paramether    | Type     | Validator
| ------------- | ---------|-----------------------|
| Username      | String   | ^[A-Za-z0-9-_]{4,25}$ |
| Password      | String   | min_length=4          |
| E-Mail        | String   | EmailField            |

#####Request ([Other request types](../example.md))

```bash
curl -X POST  -H "Content-Type: application/json"
     -d '{"username":"bahattincinic", "email": "bahattincinic@gmail.com", "password": "123456"}'
     http://arguman.org/api/v1/auth/register/
```

#####Response (Status: 201 CREATED)

```json
{"email": "bahattincinic@gmail.com", "username": "bahattincinic"}
```

User Registration
=======================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/auth/register/ |
| Method          | POST               |
| Content-Type    | application/json   |


##### Payload - raw

| Paramether    | Type     | Required
| ------------- | ---------|-----------------------|
| Username      | String   | Yes                   |
| Password      | String   | Yes                   |
| E-Mail        | String   | No                    |

##### Request

```bash
curl -X POST  -H "Content-Type: application/json"
     -d '{"username":"bahattincinic", "email": "bahattincinic@gmail.com", "password": "123456"}'
     http://arguman.org/api/v1/auth/register/
```

##### Response (Status: 201 CREATED)

```json
{"email": "bahattincinic@gmail.com", "username": "bahattincinic"}
```

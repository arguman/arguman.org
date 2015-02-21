User Registration
=======================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/auth/register/ |
| Method          | POST               |
| Content-Type    | application/json   |


#####Payload - raw

| Paramether    | Type     | Zorunlu Alan
| ------------- | ---------|-----------------------|
| Username      | String   | Evet                  |
| Password      | String   | Evet                  |
| E-Mail        | String   | Hayir                 |

#####Request

```bash
curl -X POST  -H "Content-Type: application/json"
     -d '{"username":"bahattincinic", "email": "bahattincinic@gmail.com", "password": "123456"}'
     http://arguman.org/api/v1/auth/register/
```

#####Response (Status: 201 CREATED)

```json
{"email": "bahattincinic@gmail.com", "username": "bahattincinic"}
```

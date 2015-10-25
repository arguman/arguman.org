Authentication
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/auth/login/|
| Method          | POST               |
| Content-Type    | application/json   |


#####Payload - Raw

| Paramether    | Type     | Required |
| ------------- | ---------| ------------ |
| Username      | String   | Yes          |
| Password      | String   | Yes          |


#####Request

```bash
curl -X POST  -H "Content-Type: application/json"
     -d '{"username":"<username>","password":"<password>"}'
     http://arguman.org/api/v1/auth/login/
```

#####Response (Status: 200 OK)

```json
{
 "token": "d2b443e34d64124dd6d20044c39f6a6c82fd0ee2",
}
```

Using Tokens
=========================
You need to put the received token to headers like this:

#####Request

```bash
curl -X GET  -H "Authorization: Token 173f758803eb1fb0ffaf36a782caaa885bd42af2"
             -H "Content-Type: application/json"
             http://arguman.org/api/v1/user/
```

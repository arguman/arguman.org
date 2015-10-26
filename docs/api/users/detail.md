User details
=======================

| Key             | Value                      |
| ----------------|----------------------------|
| URL             | /api/v1/users/`<username>`/ |
| Method          | GET                        |
| Content-Type    | application/json           |


#####Request

```bash
curl -X GET -H "Content-Type: application/json"
      http://arguman.org/api/v1/users/bahattincinic/
```

#####Response (Status: 200 OK)

```json
{
  "id": 515,
  "username": "bahattincinic",
  "absolute_url": "/api/v1/users/bahattincinic/",
  "avatar": "https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
}
```


Logged in User's details
===============================

| Key             | Value                      |
| ----------------|----------------------------|
| URL             | /api/v1/user/              |
| Method          | GET                        |
| Content-Type    | application/json           |

#####Request

```bash
curl -X GET  -H "Authorization: Token 173f758803eb1fb0ffaf36a782caaa885bd42af2"
     http://arguman.org/api/v1/user/
```

#####Response (Status: 200 OK)

```json
{
  "id": 515,
  "username": "bahattincinic",
  "absolute_url": "/api/v1/users/bahattincinic/",
  "avatar": "https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
}
```

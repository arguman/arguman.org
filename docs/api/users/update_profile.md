Updating User Profile
===========================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/v1/user/                                         |
| Method          | PUT                                                   |
| Content-Type    | application/json                                      |
| Authentication  | Yes                                                   |


##### Payload - Raw

| Paramether    | Type     |  Required |
| ------------- | ---------| --------------|
| username      | String   |  Yes          |
| email         | String   |  No           |
| new_password1 | String   |  No           |
| new_password2 | String   |  No           |

##### Additional Info
1. new_password1 and new_password2 fields should both be provided to change the password.
2. new_password1 and new_password2 fields should have the same value.


##### Request

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"username": "bahattincinic"}'
     http://arguman.org/api/v1/user/
```

##### Response (Status: 200 OK)

```json
{
   "id":1,
   "username":"bahattincinic",
   "absolute_url":"/api/v1/users/bahattincinic/",
   "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
}
```

##### Change Password

```bash
curl -X PUT -H "Content-Type: application/json"
            -d '{"username": "bahattincinic", "new_password1": "1", "new_password2": "1"}'
     http://arguman.org/api/v1/user/
```

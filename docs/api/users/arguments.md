 Arguments owned a user
==================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/v1/users/`<username>`/arguments/owner/           |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Content-Type    | application/json                                      |

##### Request

```bash
curl -X GET -H "Content-Type: application/json"
     http://arguman.org/api/v1/users/bahattincinic/arguments/owner/
```

##### Response (Status: 200 OK)

```json
{
 "count": 100,
 "next": null,
 "previous": null,
 "results": [

 ]
}
```


All arguments a user contributed
==================================


| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/v1/users/`<username>`/arguments/contributed      |
| Method          | GET                                                   |
| Status Codes    | 200                                                   |
| Content-Type    | application/json                                      |

##### Request

```bash
curl -X GET -H "Content-Type: application/json"
     http://arguman.org/api/v1/users/bahattincinic/arguments/contributed/
```

##### Response (Status: 200 OK)

```json
{
 "count": 100,
 "next": null,
 "previous": null,
 "results": [

 ]
}
```

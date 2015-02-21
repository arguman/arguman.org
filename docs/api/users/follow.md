Kullanıcının Takipçilerinin Listesi
===========================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/v1/users/`<username>`/followers/                 |
| Method          | GET                                                   |
| Content-Type    | application/json                                      |

#####Request

```bash
curl -X GET -H "Content-Type: application/json"
     http://arguman.org/api/v1/users/bahattincinic/followers/
```

#####Response (Status: 200 OK)

```json
{
 "count": 2,
 "next": null,
 "previous": null,
 "results": [
   {
      "id": 10,
      "username": "hmert",
      "absolute_url": "/api/v1/users/hmert/",
      "avatar": "https://secure.gravatar.com/avatar/c4121c306f8f0c6505033103b3aeeeb7.jpg?s=80&r=g&d=mm"
   },
   {
      "id": 947,
      "username": "aslanakali",
      "absolute_url": "/api/v1/users/aslanakali/",
      "avatar": "https://secure.gravatar.com/avatar/9bd0aaf69e659854e9259d438257bd67.jpg?s=80&r=g&d=mm"
   },
  ]
}
```

Kullanicinin Takip Ettiği Kişilerin Listesi
===========================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/v1/users/`<username>`/followings/                 |
| Method          | GET                                                   |
| Content-Type    | application/json                                      |

#####Request

```bash
curl -X GET -H "Content-Type: application/json"
     http://arguman.org/api/v1/users/bahattincinic/followings/
```

#####Response (Status: 200 OK)

```json
{
 "count": 1,
 "next": null,
 "previous": null,
 "results": [
   {
     "id": 1,
     "username": "fatiherikli",
     "absolute_url": "/api/v1/users/fatiherikli/",
     "avatar": "https://secure.gravatar.com/avatar/e70aa173a95f239ee3aa4768b441cb83.jpg?s=80&r=g&d=mm"
   }
  ]
}
```

Kullanıcıyı Takip Etmek
==============================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/v1/users/`<username>`/follow/                    |
| Method          | POST                                                  |
| Status Codes    | 201                                                   |
| Content-Type    | application/json                                      |
| Authentication  | Evet                                                  |

#####Request

```bash
curl -X POST -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://arguman.org/api/v1/users/bahattincinic/follow/
```

#####Response (Status: 201 CREATED)

  `<Response body is empty>`


Kullanıcıyı Takipten Çıkartmak
==============================================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/users/`<username>`/follow/                       |
| Method          | DELETE                                                |
| Status Codes    | 204                                                   |
| Content-Type    | application/json                                      |
| Authentication  | Evet                                                  |

#####Request

```bash
curl -X DELETE -H "Authorization: Token d2b443e34d64124dd6d20044c39f6a6c82fd0ee2"
     http://arguman.org/api/v1/users/bahattincinic/follow/
```

#####Response (Status: 204 NO CONTENT)

  `<Response body is empty>`

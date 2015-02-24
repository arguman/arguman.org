Kullanıcı Bilgilerini Güncelleme & Şifre Değiştirme
===========================
| Key             | Value                                                 |
| ----------------|-------------------------------------------------------|
| URL             | /api/v1/user/                                         |
| Method          | PUT                                                   |
| Content-Type    | application/json                                      |
| Authentication  | Evet                                                  |


#####Payload - Raw

| Paramether    | Type     |  Zorunlu Alan |
| ------------- | ---------| --------------|
| username      | String   |  Evet         |
| email         | String   |  Hayır        |
| new_password1 | String   |  Hayır        |
| new_password2 | String   |  Hayır        |

#####Ek Bilgi
1. new_password1 ve new_password2 alanlari gonderildigi taktirde sifre degistirme islemi yapilir.
2. new_password1 ve new_password2 bilgilerinin ayni olmasi gerekmekte.


#####Request

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"username": "bahattincinic"}'
     http://arguman.org/api/v1/user/
```

#####Response (Status: 200 OK)

```json
{
   "id":1,
   "username":"bahattincinic",
   "absolute_url":"/api/v1/users/bahattincinic/",
   "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
}
```


#####Şifre Değiştirme

```bash
curl -X PUT -H "Content-Type: application/json"
            -d '{"username": "bahattincinic", "new_password1": "1", "new_password2": "1"}'
     http://arguman.org/api/v1/user/
```

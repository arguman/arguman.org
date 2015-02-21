Argüman Eklemek
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/ |
| Method          | POST               |
| Content-Type    | application/json   |
| Authentication  | Evet               |


#####Payload - Raw

| Paramether    | Type     |  Zorunlu Alan |
| ------------- | ---------| --------------|
| title         | String   |  Evet         |
| sources       | String   |  Hayır        |
| owner         | String   |  Hayır        |


#####Request

```bash
curl -X POST  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              -d '{"title":"Sanat toplum içindir.", "sources": "Türk Dil Kurumu", "owner": "http://google.com/"}'
              http://localhost:8080/api/v1/arguments/
```

#### Response (201 Created)

```json
{
   "id":5,
   "user":{
      "id":1,
      "username":"bahattincinic",
      "absolute_url":"/api/v1/users/bahattincinic/",
      "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
   },
   "title":"Sanat toplum i\u00e7indir.",
   "slug":"sanat-toplum-icindir",
   "description":null,
   "owner":"http://google.com/",
   "sources":"T\u00fcrk Dil Kurumu",
   "premises":[

   ],
   "date_creation":"20-02-2015 12:02",
   "absolute_url":"/api/v1/arguments/5/",
   "report_count":0,
   "is_featured":false
}
```
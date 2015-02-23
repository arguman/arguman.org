Önerme Eklemek
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/ |
| Method          | POST               |
| Content-Type    | application/json   |
| Authentication  | Evet               |


#####Payload - Raw

| Paramether    | Type     |  Zorunlu Alan |
| ------------- | ---------| --------------|
| premise_type  | Integer  |  Evet         |
| text          | String   |  Evet         |
| parent        | String   |  Hayır        |
| sources       | String   |  Hayır        |


#####Ek Bilgi
1. **premise_type:** 3 değer alabilir. Bunlar 0, 1 ve 2. (0 ama, 1 çünkü, 2 ancak)
2. **text:** Önerme içeriğidir. Maksimum 300 karakter uzunluğunda olabilir.
3. **parent:** Önermenin neye yazıldığıdır. eğer değer gönderilmez ise Argümana yazılmıştır. Gönderilmiş ise id si verilen önermeye yazılmıştır.



#####Argümana önerme göndermek

#####Request

```bash
curl -X POST  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              -d '{"premise_type": 1, "text": "Api Denemesidir."}'
              http://arguman.org/api/v1/arguments/1/premises/
```

#### Response (201 Created)

```json
{
   "id":11,
   "user":{
      "id":1,
      "username":"bahattincinic",
      "absolute_url":"/api/v1/users/bahattincinic/",
      "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
   },
   "text":"Api Denemesidir.",
   "sources":null,
   "parent":null,
   "absolute_url":"/api/v1/arguments/1/premises/11/support/",
   "premise_type":1,
   "date_creation":"23-02-2015 11:02",
   "supporters":[

   ]
}
```


#####Önermeye Önerme göndermek

#####Request

```bash
curl -X POST  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              -d '{"premise_type": 1, "text": "Api Denemesidir.", "parent": "10"}'
              http://arguman.org/api/v1/arguments/1/premises/
```

#### Response (201 Created)

```json
{
   "id":10,
   "user":{
      "id":1,
      "username":"bahattincinic",
      "absolute_url":"/api/v1/users/bahattincinic/",
      "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
   },
   "text":"Api Denemesidir.",
   "sources":null,
   "parent":8,
   "absolute_url":"/api/v1/arguments/1/premises/10/support/",
   "premise_type":1,
   "date_creation":"23-02-2015 11:02",
   "supporters":[

   ]
}
```
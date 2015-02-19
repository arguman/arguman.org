Önermeyi Desteklemek
=======================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/`<id>`/support/|
| Method          | POST               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X POST  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/premises/1/support/
```

#####Response (Status: 201 CREATED)

  `<Response body is empty>`


Önermeyi Desteklemekten Vazgeçmek
=======================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/`<id>`/support/|
| Method          | DELETE               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X DELETE  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
                -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/premises/1/support/
```

#####Response (Status: 204 NO CONTENT)

  `<Response body is empty>`


Önermeyi Deskeleyenlerin Listesini Almak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/`<id>`/supporters/|
| Method          | GET               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X GET  -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/premises/1/supporters/
```


#### Response

```json
{
   "count":1,
   "next":null,
   "previous":null,
   "results":[
      {
         "id":1,
         "username":"bahattincinic",
         "absolute_url":"/api/v1/users/bahattincinic/",
         "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
      }
   ]
}
```

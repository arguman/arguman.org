Argüman Listesini Almak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/|
| Method          | GET               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X DELETE  -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/
```


#### Response

```json
{
   "count":2,
   "next":null,
   "previous":null,
   "results":[
      {
         "id":3,
         "user":{
            "id":5,
            "username":"haha",
            "absolute_url":"/api/v1/users/haha/",
            "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
         },
         "title":"helevele",
         "slug":"helevele",
         "description":null,
         "owner":"",
         "sources":"",
         "premises":[
            {
               "id":4,
               "user":{
                  "id":5,
                  "username":"haha",
                  "absolute_url":"/api/v1/users/haha/",
                  "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
               },
               "text":"helve",
               "sources":"",
               "parent":null,
               "absolute_url":"/api/v1/arguments/3/premises/4/support/",
               "premise_type":"Çünkü",
               "date_creation":"16-01-2015 16:01",
               "supporters":[

               ]
            },
            {
               "id":5,
               "user":{
                  "id":5,
                  "username":"haha",
                  "absolute_url":"/api/v1/users/haha/",
                  "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
               },
               "text":"ds",
               "sources":"",
               "parent":4,
               "absolute_url":"/api/v1/arguments/3/premises/5/support/",
               "premise_type":"Çünkü",
               "date_creation":"16-01-2015 16:01",
               "supporters":[

               ]
            },
            {
               "id":7,
               "user":{
                  "id":1,
                  "username":"bahattincinic",
                  "absolute_url":"/api/v1/users/bahattincinic/",
                  "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
               },
               "text":"vc",
               "sources":"",
               "parent":5,
               "absolute_url":"/api/v1/arguments/3/premises/7/support/",
               "premise_type":"Çünkü",
               "date_creation":"16-02-2015 21:02",
               "supporters":[

               ]
            }
         ],
         "date_creation":"16-01-2015 16:01",
         "absolute_url":"/api/v1/arguments/3/",
         "report_count":0,
         "is_featured":true
      },
      {
         "id":1,
         "user":{
            "id":1,
            "username":"bahattincinic",
            "absolute_url":"/api/v1/users/bahattincinic/",
            "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
         },
         "title":"Test",
         "slug":"test",
         "description":null,
         "owner":"T.C. Anayasas\u0131",
         "sources":"http://google.com/ http://wikipedia.com/",
         "premises":[
            {
               "id":1,
               "user":{
                  "id":1,
                  "username":"bahattincinic",
                  "absolute_url":"/api/v1/users/bahattincinic/",
                  "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
               },
               "text":"Test",
               "sources":"",
               "parent":null,
               "absolute_url":"/api/v1/arguments/1/premises/1/support/",
               "premise_type":"Çünkü",
               "date_creation":"05-01-2015 21:01",
               "supporters":[

               ]
            },
            {
               "id":2,
               "user":{
                  "id":1,
                  "username":"bahattincinic",
                  "absolute_url":"/api/v1/users/bahattincinic/",
                  "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
               },
               "text":"fdf",
               "sources":"fdfd",
               "parent":null,
               "absolute_url":"/api/v1/arguments/1/premises/2/support/",
               "premise_type":"Çünkü",
               "date_creation":"07-01-2015 17:01",
               "supporters":[
                  {
                     "id":1,
                     "username":"bahattincinic",
                     "absolute_url":"/api/v1/users/bahattincinic/",
                     "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
                  }
               ]
            },
            {
               "id":3,
               "user":{
                  "id":1,
                  "username":"bahattincinic",
                  "absolute_url":"/api/v1/users/bahattincinic/",
                  "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
               },
               "text":"Test",
               "sources":"test",
               "parent":1,
               "absolute_url":"/api/v1/arguments/1/premises/3/support/",
               "premise_type":"Çünkü",
               "date_creation":"15-01-2015 20:01",
               "supporters":[

               ]
            }
         ],
         "date_creation":"05-01-2015 21:01",
         "absolute_url":"/api/v1/arguments/1/",
         "report_count":7,
         "is_featured":false
      }
   ]
}
```


Argüman Listesinin Detayını Almak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/|
| Method          | GET               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X GET  -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/
```


Argümanın Önermelerini Almak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/|
| Method          | GET               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X GET  -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/premises/
```


Argümanları En son eklenmişlere göre sıralamak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/?ordering=-date_creation|
| Method          | GET               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X GET  -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/?ordering=-date_creation
```



Argümanların arasında seçilmişleri almak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/?is_featured=True|
| Method          | GET               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X GET  -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/?is_featured=True
```


Argümanların arasında arama yapmak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/?search=hede|
| Method          | GET               |
| Content-Type    | application/json   |


#####Request

```bash
curl -X GET  -H "Content-Type: application/json"
              http://arguman.org/api/v1/arguments/1/?search=hede
```

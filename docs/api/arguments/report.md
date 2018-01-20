Reporting Fallacies
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/`<id>`/report/|
| Method          | POST               |
| Content-Type    | application/json   |
| Authentication  | Yes                |


##### Payload - Raw

| Paramether    | Type     | Required |
| ------------- | ---------| ------------ |
| fallacy_type  | String   | Yes          |


**Fallacy Types:**

https://github.com/arguman/arguman.org/blob/master/web/premises/fallacies.json


##### Request

```bash
curl -X POST  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              -d '{"fallacy_type":"Appeal To Authority"}'
              http://arguman.org/api/v1/arguments/1/premises/1/report/
```

#### Response

```json
{
   "fallacy_type":"Begging The Question",
   "reporter":{
      "id":1,
      "username":"bahattincinic",
      "absolute_url":"/api/v1/users/bahattincinic/",
      "avatar":"https://secure.gravatar.com/avatar/c1184fefac22e49bbf59e3775ef6e9dd.jpg?s=80&r=g&d=mm"
   },
   "premise":{
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
   "contention":{
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
      "report_count":6,
      "is_featured":false
   }
}
```

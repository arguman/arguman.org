Listing notifications
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/notifications/|
| Method          | GET                |
| Content-Type    | application/json   |
| Authentication  | Yes                |


#####Request

```bash
curl -X GET   -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/
```


#### Response

```json
{
   "count":2,
   "next":null,
   "previous":null,
   "results":[
      {
         "sender":{
            "id":1,
            "username":"bahattincinic",
            "absolute_url":"/api/v1/users/bahattincinic/",
            "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
         },
         "recipient":{
            "id":1,
            "username":"bahattincinic",
            "absolute_url":"/api/v1/users/bahattincinic/",
            "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
         },
         "date_created":"19-02-2015 18:02",
         "notification_type":"supported-a-premise",
         "is_read":true,
         "target_object_id":1,
         "id":15,
         "text": "bahattincinic Test argümanındaki önermeni destekledi."
      },
      {
         "sender":null,
         "recipient":{
            "id":1,
            "username":"bahattincinic",
            "absolute_url":"/api/v1/users/bahattincinic/",
            "avatar":"https://secure.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e.jpg?s=80&r=g&d=mm"
         },
         "date_created":"19-02-2015 18:02",
         "notification_type":"reported-as-fallacy",
         "is_read":true,
         "target_object_id":7,
         "id":14,
         "text": "Test argümanındaki önermeniz Bir Bilen Safsatası olarak bildirildi."
      }
   ]
}
```

Notification detail
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/notifications/`<id>`/|
| Method          | GET               |
| Content-Type    | application/json   |
| Authentication  | Yes                |

```bash
curl -X GET   -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/15/
```

Getting already read notifications
========================================

```bash
curl -X GET   -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/15/?is_read=True
```


Getting not yet read notifications
========================================

```bash
curl -X GET   -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/15/?is_read=False
```

Ordering the notifications by their creation date
========================================

```bash
curl -X GET   -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/15/?ordering=-date_created
```

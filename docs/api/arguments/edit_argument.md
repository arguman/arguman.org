Editing an Argument
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/ |
| Method          | PUT               |
| Content-Type    | application/json   |
| Authentication  | Yes                |


##### Payload - Raw

| Paramether    | Type     |  Required |
| ------------- | ---------| --------------|
| title         | String   |  Yes          |
| sources       | String   |  No           |
| owner         | String   |  No           |
| is_published  | Boolean  |  Yes          |

##### Additional Info
Only the owner can delete an argument.

##### Request

```bash
curl -X PUT  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              -d '{"title":"Sanat toplum içindir.", "sources": "Türk Dil Kurumu", "owner": "http://google.com/", "is_published": true}'
              http://arguman.org/api/v1/arguments/9/
```

#### Response (200 OK)

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
   "sources":"Türk Dil Kurumu",
   "premises":[

   ],
   "date_creation":"20-02-2015 12:02",
   "absolute_url":"/api/v1/arguments/5/",
   "report_count":0,
   "is_featured":false,
   "is_published":true
}
```
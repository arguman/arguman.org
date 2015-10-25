Getting the public newsfeed
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/newsfeed/public/|
| Method          | GET                |
| Content-Type    | application/json   |


#####Additional Information
1. You can use `?page=<page_number>` to change pages.
2. Default result limit is 20 per page. You can specify a custom limit by `?limit=<limit_number>`

#####Request

```bash
curl -X GET  -H "Content-Type: application/json"
              http://arguman.org/api/v1/newsfeed/public/
```


#### Response

```json
{
   "previous":null,
   "results":[
      {
         "date_created":"2015-02-20T17:17:25.509",
         "sender":{
            "username":"bahattincinic",
            "email":"bahattincinic@gmail.com"
         },
         "recipients":[
            6,
            1
         ],
         "related_object":{
            "owner":"http://google.com/",
            "uri":"/sanat-toplum-icindir-078aafd5cf1943468a3d23691a5e76e6",
            "title":"Sanat toplum i\u00e7indir."
         },
         "news_type":0,
         "_id":"54e76c25ad48386cbcee46ea",
         "object_id":7
      },
      {
         "date_created":"2015-02-20T17:15:42.483",
         "sender":{
            "username":"bahattincinic",
            "email":"bahattincinic@gmail.com"
         },
         "recipients":[
            6,
            1
         ],
         "related_object":{
            "owner":"http://google.com/",
            "uri":"/sanat-toplum-icindir-19dca39424c24e31a748d30e21abf76c",
            "title":"Sanat toplum i\u00e7indir."
         },
         "news_type":0,
         "_id":"54e76bbead48386c7bd48e74",
         "object_id":6
      },
      {
         "date_created":"2015-02-20T12:36:51.852",
         "sender":{
            "username":"bahattincinic",
            "email":"bahattincinic@gmail.com"
         },
         "recipients":[
            6,
            1
         ],
         "related_object":{
            "owner":"http://google.com/",
            "uri":"/sanat-toplum-icindir",
            "title":"Sanat toplum i\u00e7indir."
         },
         "news_type":0,
         "_id":"54e72a63ad483860f2d25a81",
         "object_id":5
      }
   ],
   "next":"http://arguman.org/api/v1/newsfeed/public/?page=2"
}
```
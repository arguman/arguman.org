Kullanıcıya Özel Haber Kaynağını Almak
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/newsfeed/private/|
| Method          | GET               |
| Content-Type    | application/json   |
| Authentication  | Evet               |


#####Ek Bilgi
1. Sayfa değiştirmek için `?page=<page_number>` şeklinde sayfa değiştirebilirsiniz
2. Varsayılan limitleme sayfa başına 20 adet. bunu değiştirmek için `?limit=<limit_number>` şeklinde istek yapabilirsiniz.

#####Request

```bash
curl -X GET   -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/newsfeed/private/
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
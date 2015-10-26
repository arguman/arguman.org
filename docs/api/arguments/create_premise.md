Adding a Premise
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/ |
| Method          | POST               |
| Content-Type    | application/json   |
| Authentication  | Yes                |


#####Payload - Raw

| Paramether    | Type     |  Required     |
| ------------- | ---------| --------------|
| premise_type  | Integer  |  Yes          |
| text          | String   |  Yes          |
| parent        | String   |  No           |
| sources       | String   |  No           |


#####Additional Information1
1. **premise_type:** can be 1,2 or 3. (0 for but, 1 for because, 2 for however)
2. **text:** Premise itself. Maximum 300 characters.
3. **parent:** ID of the parent premise. If empty, then it's a top level premise. 


#####Adding a premise to an argument

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


#####Adding a premise to another premise

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
Editing a Premise
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/premises/`<id>`/ |
| Method          | PUT               |
| Content-Type    | application/json   |
| Authentication  | Yes                |


#####Payload - Raw

| Paramether    | Type     |  Required |
| ------------- | ---------| --------------|
| premise_type  | Integer  |  Yes          |
| text          | String   |  Yes          |
| parent        | String   |  No           |
| sources       | String   |  No           |


#####Additional Info
1. **premise_type:** 0 for but, 1 for because, 2 for however.
2. **text**: Content of the premise. Maximum 300 characters.
3. **parent:** ID of the parent premise. If empty, then it's a top level premise. 
4. Only the owner can delete a premise.

#####Editing a premise

#####Request

```bash
curl -X PUT  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              -d '{"premise_type": 1, "text": "Api Denemesidir."}'
              http://arguman.org/api/v1/arguments/1/premises/9/
```

#### Response (200 OK)

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

Deleting an Argument
=======================
| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/arguments/`<id>`/ |
| Method          | DELETE             |
| Content-Type    | application/json   |
| Authentication  | Yes                |

##### Additional Info
Only the owner can delete their arguments.

##### Request

```bash
curl -X DELETE  -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
                -H "Content-Type: application/json"
                http://arguman.org/api/v1/arguments/9/
```

##### Response (Status: 204 NO CONTENT)

  `<Response body is empty>`

Marking all notifications as read
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/notifications/|
| Method          | PATCH                |
| Content-Type    | application/json   |
| Authentication  | Yes                |

#####Request

```bash
curl -X PATCH -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/
```


Marking a notification as read
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/notifications/`<id>`/|
| Method          | PATCH                |
| Content-Type    | application/json   |
| Authentication  | Yes                |

#####Request

```bash
curl -X PATCH -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/1/
```

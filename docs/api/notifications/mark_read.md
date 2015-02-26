Tüm bildirimleri Okundu olarak işaretlemek
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/notifications/|
| Method          | PATCH                |
| Content-Type    | application/json   |
| Authentication  | Evet               |

#####Request

```bash
curl -X PATCH -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/
```


Sadece birini okundu olarak işaretlemek
========================================

| Key             | Value              |
| ----------------|--------------------|
| URL             | /api/v1/notifications/`<id>`/|
| Method          | PATCH                |
| Content-Type    | application/json   |
| Authentication  | Evet               |

#####Request

```bash
curl -X PATCH -H "Authorization: Token 66e84d2dd71ecb992c9baa331c72eca58f239909"
              -H "Content-Type: application/json"
              http://arguman.org/api/v1/notifications/1/
```

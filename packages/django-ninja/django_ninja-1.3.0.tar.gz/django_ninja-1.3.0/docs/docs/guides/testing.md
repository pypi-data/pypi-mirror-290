# Testing

**Django Ninja** is fully compatible with standard [django test client](https://docs.djangoproject.com/en/dev/topics/testing/tools/) , but also provides a test client to make it easy to test just APIs without middleware/url-resolver layer making tests run faster.

To test the following API:
```python
from ninja import NinjaAPI, Schema

api = NinjaAPI()
router = Router()

class HelloResponse(Schema):
    msg: str
    
@router.get("/hello", response=HelloResponse)
def hello(request):
    return {"msg": "Hello World"}

api.add_router("", router)
```

You can use the Django test class:
```python
from django.test import TestCase
from ninja.testing import TestClient

class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        response = client.get("/hello")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Hello World"})
```

It is also possible to access the deserialized data using the `data` property:
```python
    self.assertEqual(response.data, {"msg": "Hello World"})
```

Arbitrary attributes can be added to the request object by passing keyword arguments to the client request methods:
```python
class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        # request.company_id will now be set within the view
        response = client.get("/hello", company_id=1)
```

It is also possible to specify headers, both from the TestCase instanciation and the actual request:
```python
    client = TestClient(router, headers={"A": "a", "B": "b"})
    # The request will be made with {"A": "na", "B": "b", "C": "nc"} headers
    response = client.get("/test-headers", headers={"A": "na", "C": "nc"})
```

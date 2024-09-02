import requests 

def test_register(data):
    response = requests.post("http://localhost:5000/register", data=data)
    print (f"Status Code :{response.status_code}\nResponse Body :{response.json()}")


def test_login(data):
    response = requests.post("http://localhost:5000/login", data=data)
    print (f"Status Code :{response.status_code}\nResponse Body :{response.json()}")


# Tests

test_register(
    {
    "username":"Moon",
    "email":"naomie@gmail.com",
    "password":"Azerty",
    "confirm-password":"Azerty"
    }
)

test_login(
    {
    "email":"naomie@gmail.com",
    "password":"Azerty"
    }
)
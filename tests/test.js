
async function testRoute(url,body) {
    let response = await fetch(`http://localhost:5000/${url}`,{
        method: "POST",
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    })
    let response_json = await response.json()    
    console.log(response_json);
    
}

testRoute("register",{
    "username":"Moon",
    "email":"naomie@gmail.com",
    "password":"Azerty",
    "confirm-password":"Azerty"
    })

testRoute("login",{
        "email":"naomie@gmail.com",
        "password":"Azerty"
    })

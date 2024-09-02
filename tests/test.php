<?php 
function testRoute($url,$body) {
    $options = [ 
        'http' => [ 
            'method'  => 'POST', 
            'header'  => 'Content-type: application/json', 
            'body' => $body
        ], 
    ]; 
      
    $context  = stream_context_create($options); 
      
    $response = file_get_contents('http://localhost:5000/'.$url, false, $context); 

    return json_decode($response);
};

$url = 'register'; 
$data = ['username' => 'Rophen',
         'email' => 'rophen2@yahoo.fr',
         'password' => 'Azerty2003',
         'confirm-password' => 'Azerty2003']; 
  
$response = testRoute($url,$data);
  
echo $response; 
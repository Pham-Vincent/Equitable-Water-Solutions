<?php 
  $envFile = __DIR__ . '/.env';
  if (file_exists($envFile)) {
      $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
      foreach ($lines as $line) {
          list($key, $value) = explode('=', $line, 2);
          $_ENV[$key] = $value;
          putenv("$key=$value");
      }
  }
  
  // Retrieve environment variables
  $host = getenv('DB_HOST');
  $user = getenv('DB_USER');
  $password = getenv('DB_PASS');
  $database = getenv('DB_NAME');
  

  
  $conn=new mysqli($host, $user, $password, $database);
  if($conn->connect_error){
    echo('Connection Error'. $conn->connect_error);
  }
  else{
    $sql ='Select * From SurfaceWater_Withdrawals';
    $results = mysqli_query($conn,$sql);
    foreach($results as $result){
      echo($result['site_description1'] . "\n");
    }
  }
  
  ?>
<?php 
  $envFile = __DIR__ . '/../env/.env';
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

  mysqli_set_charset($conn, 'utf8');
  
  //$sql = "SELECT ic_site_id, site_description1, state_name, county_name, lat_dd, long_dd FROM SurfaceWater_Withdrawals"; // Adjust table and column names as per your database schema
  $sql = "SELECT Hydrocode, Source_Type, Latitude, Longitude, Locality, Year_2016, Year_2017, Year_2018, Year_2019, Year_2020 FROM VA_Permits WHERE Latitude > 1.1";
  $result = $conn->query($sql);

  $data = array();

if ($result->num_rows > 0) {
    // Fetch each row from the result set
    while($row = $result->fetch_assoc()) {
        // Add latitude and longitude values to the data array
        $data[] = $row;
    }
}

  // Close database connection
  $conn->close();

  //encode data as json
  $json = json_encode($data);

  //Directory its going to be stored as
  $directory = __DIR__ . '/../json/';
  //create json file with stored data
  $file = 'Va_Permit.json'; 
  //create File Path where the data is going to be stored
  $filepath = $directory . $file;
  file_put_contents($filepath, $json);

  echo "Data has been written to $file";
  
  ?>
<?php
include 'flag.php';
if (isset($_GET['source'])) {
  highlight_file(__FILE__);
  exit;
}
srand(floor(time()));

// Get next random number
$rand1 = rand(0, 100);
$rand2 = rand(0, 100);
// Check prediction is set and it is numeric
?>
<!DOCTYPE html>
<html>

<head>
  <title>Random Number</title>
</head>

<body>
  <h1>Random Number</h1>
  <p>Random number is: <?php echo $rand1; ?></p>
  <p>What's up next?</p>
  <form action="index.php" method="get">
    <input type="text" name="prediction" />
    <input type="submit" value="Submit" />
    <!-- Link to source code: /?source -->
  </form>
  <?php
  echo "<p>\n";
  if (isset($_GET['prediction']) && is_numeric($_GET['prediction'])) {
    $prediction = $_GET['prediction'];
    // Make prediction a integer
    $prediction = intval($prediction);
    if ($prediction == $rand1 + $rand2) {
      echo $flag . "\n";
    } else {
      echo "Wrong!\n";
    }
  }
  echo "</p>\n";
  ?>
</body>
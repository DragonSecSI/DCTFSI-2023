<?php
// Start the session
session_start();
include "api/db.php";
?>

<!DOCTYPE html>
<html lang="en">
<?php include "head.php"; ?>

<body>
  <div class="container mx-auto">
    <h1>Flag mail</h1>
    <form action="api/login.php" method="post">
      <input type="text" name="username" placeholder="Uporabniško ime" autocomplete="off" />
      <input type="password" name="password" placeholder="Geslo" autocomplete="off" />
      <input type="submit" value="Prijava" />
      <?php
      if (isset($_SESSION['error'])) {
        echo "<p>Napačno uporabniško ime ali geslo</p>";
        unset($_SESSION['error']);
      }
      ?>
      <!-- Jože vedno pozabi svoje geslo! Ime: programer, Geslo: <?php echo $db['programer']['geslo']; ?> -->
    </form>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>

</body>

</html>
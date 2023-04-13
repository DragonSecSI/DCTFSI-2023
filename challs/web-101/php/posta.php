<?php
// Start the session
session_start();
if (!isset($_SESSION["username"])) {
    header("Location: index.php");
}
include "api/db.php";

?>

<!DOCTYPE html>
<html lang="en">
<?php include "head.php"; ?>

<body>
    <div class="container">
        <nav>
            <a href="posta.php">Domov</a>
            <a id="logout" href="api/logout.php">Odjava</a>
        </nav>
        <h1>Flag mail</h1>
        <p> Pozdravljen, <?php echo $_SESSION["username"]; ?> </p>
        <p>Tu je tvoja pošta:</p>
        <div id="predal">
            <?php
            // Create a table
            foreach ($db[$_SESSION["username"]]["posta"] as $sporocilo) {
                echo "<div class='sporocilo'>";
                echo "<p class='from'>Od: " . $sporocilo["from"] . "</p>";
                echo "<p class='subject'>Zadeva: " . $sporocilo["subject"] . "</p>";
                echo "<p class='message'>" . nl2br($sporocilo["message"]) . "</p>";
                echo "</div>";
            }
            ?>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>

</body>

</html>
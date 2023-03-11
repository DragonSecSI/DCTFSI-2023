<?php
// Start the session
session_start();
include "db.php";

if (isset($_POST["username"]) && isset($_POST["password"])) {
    $username = $_POST["username"];
    $password = $_POST["password"];
    if (isset($db[$username]) && $db[$username]['geslo'] === $password) {
        $_SESSION["username"] = $username;
        header("Location: /posta.php");
    } else {
        $_SESSION["error"] = "Napačno uporabniško ime ali geslo";
        header("Location: /index.php");
    }
}

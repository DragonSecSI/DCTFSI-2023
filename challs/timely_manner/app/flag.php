<?php
$flag = "$FLAG";
if (basename(__FILE__) == basename($_SERVER["SCRIPT_FILENAME"])) {
    // Redirect to the thing from environment variable
    header("Location: $REDIRECT_URL");
    echo "Not so fast!";
    die();
}

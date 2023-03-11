const express = require("express");
const jwt = require("jsonwebtoken");
const router = express.Router();

const { ADMIN_PASSWORD, PRIV_KEY } = require("../config");

router
  .route("/admin_login")
  .get((req, res) => res.render("admin_login"))
  .post((req, res) => {
    const { username, password } = req.body;
    if (username === "admin" && password === ADMIN_PASSWORD) {
      const token = jwt.sign({ user: username }, PRIV_KEY, { algorithm: "RS256" });
      res.cookie("session", token);
      return res.redirect("/admin_panel");
    }
    return res.redirect("/admin_login");
  });

module.exports = router;

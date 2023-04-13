const express = require("express");
const router = express.Router();

const { isAdmin } = require("../middleware/jwt");
const { FLAG } = require("../config");

router.use(isAdmin);

router
  .route("/admin_panel")
  .get((req, res) => res.render("admin_panel", { flag: FLAG }));

module.exports = router;

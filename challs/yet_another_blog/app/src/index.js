const express = require("express");
const cookieParser = require("cookie-parser");
const helmet = require("helmet");
const morgan = require("morgan");

const { PORT, HOST } = require("./config");

// Routes
const auth = require("./routes/auth");
const home = require("./routes/home");
const admin = require("./routes/admin");
const path = require("path");
const app = express();

app.set("view engine", "ejs");
app.set("views", "src/views");

app.use(helmet());
app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use("/static", express.static(path.join(__dirname, "static")));
app.use(morgan("common"));


app.use(home);
app.use(auth);
app.use(admin);

app.use((err, req, res, next) => {
  console.error(err);
  return res.status(500).send("Internal server error");
});

app.listen(PORT, HOST, () => {
  console.log(`Application is on http://${HOST}:${PORT}`);
});

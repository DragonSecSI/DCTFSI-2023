const jwt = require("jsonwebtoken");
const { PUB_KEY } = require("../config");
const cookieExtractor = function (req) {
  var token = null;
  if (req && req.cookies) {
    token = req.cookies["session"];
  }
  return token;
};

const isAdmin = (req, res, next) => {
  const token = cookieExtractor(req);
  if (token) {
    jwt.verify(
      token,
      PUB_KEY,
      { algorithms: ["RS256", "ES256", "HS256"] },
      (err, decoded) => {
        if (err) {
          console.log("Error: " + err);
          return res.redirect("/admin_login");
        }
        if (decoded.user !== "admin") {
          return res.redirect("/admin_login");
        }
        req.user = decoded.user;
        return next();
      }
    );
  } else {
    return res.redirect("/admin_login");
  }
};
module.exports = { isAdmin  };

const express = require("express");
const router = express.Router();

const posts = [
  {
    img:"/static/img/blog1.jpg",
    title: "Welcome to my blog!",
    content: "This is my first post. I hope you enjoy it!",
  },
  {
    img:"/static/img/blog2.jpg",
    title: "My second post",
    content: "This is my second post. I hope you enjoy it!",
  },
  {
    img:"/static/img/blog3.jpg",
    title: "My third post",
    content: "This is my third post. I hope you enjoy it!",
  },
];

router.route("/")
.get((req, res) => res.render("blog", { posts }));

module.exports = router;

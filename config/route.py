from back.url.route import Routes

# route the root url
Routes.get("/", "index.html")
Routes.get("/about-me", "about.html")
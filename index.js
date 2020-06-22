//This file routes urls to their appropriate fuctions using Express

//**READ THIS BEFORE RUNNING: Make sure you install the python dependencies by running...
// "pip3 install -r pinScraping/requirements.txt" from the projects root directory
// or else turing a url into a pin won't work. (Ask Dylan if you need help)
var bodyParser = require("body-parser");
var express = require("express");
var exphbs = require("express-handlebars");
var fs = require("fs");
// const MongoClient = require("mongodb").MongoClient;
var app = express();
const mongoose = require("mongoose");
const Item = require("./models/Item.js");

//Make connection to db

// "mongodb+srv://Dylan:Webdeviscool@cluster0-ykvju.mongodb.net/test?retryWrites=true&w=majority"
const db =
  "mongodb+srv://cs290:webdeviscool@pinterlist-bynox.mongodb.net/CS_290_Final?retryWrites=true&w=majority";
mongoose
  .connect(db, {
    useNewUrlParser: true,
    useCreateIndex: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("MongoDB Connected..."))
  .catch((err) => console.log(err));

app.use(express.json());

app.use(bodyParser.urlencoded({ extended: true }));
app.engine("handlebars", exphbs({ defaultLayout: "main" }));
app.set("view engine", "handlebars");

//serve static files
app.use(express.static(__dirname + "/static"));

app.get("/", (req, res) => {
  res.status(200).render("base");
});

//This function is called when a get request is sent to the '/recipe' url
app.post("/", (req, res, next) => {
  // Spawning a child process to run python code.
  var inputURL = req.body.inputURL;
  console.log("== inside of post func");

  var spawn = require("child_process").spawn;

  //if cleaned send to URL, if not don't respond
  var process = spawn("python3", ["pinScraping/scraping_main.py", inputURL]);
  console.log("== child process starting");
  // Takes recipe data from the python script and loads it into a json object called 'payload'
  process.stdout.on("data", function (data) {
    console.log("Pipe data from python script ...");
    var payload = JSON.parse(data.toString()); //turns recipe data into a json obj
    console.log("==Payload: ", payload);

    context = payload;
    var recipe = {
      recipeId: inputURL,
      ingredients: payload.items,
    };

    const newItem = new Item(recipe);

    console.log("==item below: ");
    newItem.save().then((item) => console.log(item));

    res.render("return_list", context);
  });
});

//This function coverts the mongoose document to an object.
const multipleMongooseToObj = (arrayOfMongooseDocuments) => {
  const tempArray = [];
  if (arrayOfMongooseDocuments.length !== 0) {
    arrayOfMongooseDocuments.forEach((doc) => tempArray.push(doc.toObject()));
  }
  return tempArray;
};

//**ABHI**   SHOW INGREDIENTS PAGE
app.get("/showIngredients", async (req, res, next) => {
  //query searched items
  try {
    const items = multipleMongooseToObj(await Item.find({})); //Get all items in db
    console.log("==items:", items);
    res.render("showDatabase", {
      items: items,
    });
  } catch (err) {
    console.error(err);
  }
});

app.post("/pinToList/addIngredient", function (req, res, next) {
  if (req.body && req.body.name && req.body.ingredients) {
    var id = req.body.inputURL;
    var ingredient = req.body.ingredient;
    //test.recipes.insertOne(recipe);
    var recipe_to_add = collection.find({ recipeId: id });
    recipe_to_add.ingredients.push(ingredient);
  } else {
    next();
  }
});

app.get("/return", (req, res) => {
  res.status(200).render("return_list");
});

//404 handler
app.get("*", function (req, res) {
  res.status(404).render("404");
});

app.listen(3000, function () {
  console.log("== Server listening on port 3000");
});

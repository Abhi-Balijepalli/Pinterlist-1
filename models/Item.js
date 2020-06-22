//This schema is currently obsolete
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

//Creaate Schema

const ItemSchema = new Schema(
  {
    recipeId: {
      type: String,
      required: true,
    },
    ingredients: [
      {
        type: String,
        required: true,
      },
    ],
  },
  {
    toObject: {
      virtuals: true,
    },
    toJSON: {
      virtuals: true,
    },
  }
);

module.exports = Item = mongoose.model("item", ItemSchema);

'use strict';

const mongoose = require('mongoose');

const MovieSchema = mongoose.Schema({
  title: {
    type: String,
    required: true,
    maxlength: 100,
    minlength: 1
  },
  created: {
    type: Date,
    default: new Date(),
  },
  year: {
    type: Date,
    min: 1897,
    max: 3000
  }
});

module.exports = {
  Movie: mongoose.model('Movie', MovieSchema),
};


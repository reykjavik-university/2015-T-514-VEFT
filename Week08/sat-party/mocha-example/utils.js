'use strict';

const convert = function(dollar_value) {
  if (dollar_value < 0) {
    throw new Error('Value must be positive');
  }
  return dollar_value - 10;
}

module.exports = {
  convert: convert
}

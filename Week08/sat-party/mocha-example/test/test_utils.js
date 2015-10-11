'use strict';

const assert = require('assert');
const utils = require('../utils');

describe('convert.utils', function() {

  it('should convert dollar to isk', function() {
    const val = utils.convert(30);
    const expected = 20;
    assert(val === expected);
  });

});

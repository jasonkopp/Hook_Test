var fs = require('fs');

module.exports = {
  props: {
    mp4ra: { type: Object }
  },
  template: fs.readFileSync(__dirname + '/misc.vue', 'utf8')
};

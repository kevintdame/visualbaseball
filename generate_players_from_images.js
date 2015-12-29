var fs = require('fs');

var fileNames = fs.readdirSync('images/rankometer');

var items = fileNames.map(function(fileName) {
  var playerName = fileName.replace('-', ' ').replace('.png', '');
  return '{"value":"' + playerName + '", "icon": "' + fileName + '"}';
});

fs.writeFileSync('player.json', '[\n' + items.join(',\n') + '\n]');

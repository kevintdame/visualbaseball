var fs = require('fs');

var fileNames = fs.readdirSync('images/rankometer');

console.log(fileNames);

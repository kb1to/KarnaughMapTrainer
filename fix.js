const fs = require('fs');
let content = fs.readFileSync('index.js', 'utf8');
// No fix needed really since the warning is in Python, but let's double check if the string outputted correctly
console.log(content.includes("\\s+"));

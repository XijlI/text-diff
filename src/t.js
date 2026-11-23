const Diff = require('./diff.min.js');
const a = ['the',' ','quick',' ','brown',' ','fox'];
const b = ['the',' ','fast',' ','brown',' ','fox'];
console.log(JSON.stringify(Diff.diffArrays(a,b)));
console.log(JSON.stringify(Diff.diffArrays(['a','b','c'],['a','x','y','c'])));
console.log(JSON.stringify(Diff.diffArrays(['a'],['a','b'])));

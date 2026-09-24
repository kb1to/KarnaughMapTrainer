let eq = "A*B + C'";
let jsEq = eq.replace(/\s+/g, '');
jsEq = jsEq.replace(/([a-zA-Z0-9_]+)'/g, '!$1');
jsEq = jsEq.replace(/([a-zA-Z0-9_)'\]])(?=[a-zA-Z0-9_(!\[])/g, '$1*');
jsEq = jsEq.replace(/\*/g, '&&').replace(/\+/g, '||');
console.log(jsEq);

eq = "AB + C'D";
jsEq = eq.replace(/\s+/g, '');
jsEq = jsEq.replace(/([a-zA-Z0-9_]+)'/g, '!$1');
jsEq = jsEq.replace(/([a-zA-Z0-9_)'\]])(?=[a-zA-Z0-9_(!\[])/g, '$1*');
jsEq = jsEq.replace(/\*/g, '&&').replace(/\+/g, '||');
console.log(jsEq);

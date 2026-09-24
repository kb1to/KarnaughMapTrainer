const fs = require('fs');

// 1. Update HTML
let html = fs.readFileSync('index.html', 'utf8');

// Replace axis spans and add kmap-container
html = html.replace(/<span class="axis col-ax".*?<\/span>/, '');
html = html.replace(/<span class="axis row-ax".*?<\/span>/, '');
html = html.replace(/<div class="km-inner">([\s\S]*?)<\/div>/, '<div id="kmap-container" style="position:relative; margin: 2rem;">\n          <div id="axis-lines"></div>\n          $1\n        </div>');

// Remove btn-save-group
html = html.replace(/<button id="btn-save-group" class="action-btn">Lock In Group<\/button>/, '');

fs.writeFileSync('index.html', html);

// 2. Update CSS
let css = fs.readFileSync('index.css', 'utf8');
css += `
/* Axis Lines */
.var-line {
  position: absolute;
  display: flex;
  font-weight: 800;
  color: var(--accent);
  font-size: 1.1rem;
}
.var-line.top-axis {
  border-top: 3px solid var(--accent);
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 0.3rem;
}
.var-line.left-axis {
  border-left: 3px solid var(--accent);
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.3rem;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
}
/* Editable variable names */
.var-name {
  outline: none;
  cursor: text;
  background: rgba(255,255,255,0.1);
  padding: 0 0.2rem;
  border-radius: 4px;
}
.var-name:focus {
  background: rgba(255,255,255,0.3);
}
`;
fs.writeFileSync('index.css', css);


import re

with open('index.js', 'r') as f:
    js = f.read()

new_render_axes = """function renderAxesLines() {
    UI.axisLines.innerHTML = '';
    const CELL = 3.5; 

    const createTopLine = (name, leftCells, widthCells, varIndex, level) => {
        let div = document.createElement('div');
        div.className = 'var-line top-axis';
        div.style.left = `calc(${CELL * (leftCells + 1)}rem)`;
        div.style.width = `calc(${CELL * widthCells}rem)`;
        div.style.top = `calc(-0.8rem - ${level * 1.8}rem)`;
        
        let span = document.createElement('span');
        span.className = 'var-name';
        span.contentEditable = true;
        span.innerText = name;
        span.addEventListener('input', (e) => { state.varNames[varIndex] = e.target.innerText.trim(); renderTruthTable(); });
        div.appendChild(span);
        UI.axisLines.appendChild(div);
    };

    const createLeftLine = (name, topCells, heightCells, varIndex, level) => {
        let div = document.createElement('div');
        div.className = 'var-line left-axis';
        div.style.top = `calc(${CELL * (topCells + 1)}rem)`;
        div.style.height = `calc(${CELL * heightCells}rem)`;
        div.style.left = `calc(-0.8rem - ${level * 1.8}rem)`;
        
        let span = document.createElement('span');
        span.className = 'var-name';
        span.contentEditable = true;
        span.innerText = name;
        span.addEventListener('input', (e) => { state.varNames[varIndex] = e.target.innerText.trim(); renderTruthTable(); });
        div.appendChild(span);
        UI.axisLines.appendChild(div);
    };

    if (state.numVars === 2) {
        createLeftLine(state.varNames[0], 1, 1, 0, 0); 
        createTopLine(state.varNames[1], 1, 1, 1, 0);
    } else if (state.numVars === 3) {
        createLeftLine(state.varNames[0], 1, 1, 0, 0); 
        createTopLine(state.varNames[1], 2, 2, 1, 0);  
        createTopLine(state.varNames[2], 1, 2, 2, 1);  
    } else if (state.numVars === 4) {
        createLeftLine(state.varNames[0], 2, 2, 0, 0); 
        createLeftLine(state.varNames[1], 1, 2, 1, 1); 
        createTopLine(state.varNames[2], 2, 2, 2, 0); 
        createTopLine(state.varNames[3], 1, 2, 3, 1); 
    }
}"""

js = re.sub(r'function renderAxesLines\(\) \{[\s\S]*?function renderKMap\(\)', new_render_axes + '\n\nfunction renderKMap()', js)

with open('index.js', 'w') as f:
    f.write(js)

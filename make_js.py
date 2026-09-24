import os

js_code = """const state = {
    numVars: 3,
    truthTable: [],
    varNames: ['A', 'B', 'C', 'D'],
    draftGroup: new Set(),
    lockedGroups: []
};

const UI = {
    varBtns: document.querySelectorAll('.vbtn'),
    btnNew: document.getElementById('btn-new'),
    btnClear: document.getElementById('btn-clear'),
    btnCheck: document.getElementById('sol-btn'),
    solIn: document.getElementById('sol-in'),
    feedback: document.getElementById('feedback'),
    kmapContainer: document.getElementById('kmap-container'),
    axisLines: document.getElementById('axis-lines'),
    kmapHead: document.querySelector('#kmap thead tr'),
    kmapBody: document.querySelector('#kmap tbody'),
    truthHeadVar: document.getElementById('truth-var-th'),
    truthBody: document.querySelector('#truth tbody')
};

const GRAY_1 = [0, 1];
const GRAY_2 = [0, 1, 3, 2];

function init() {
    setupListeners();
    generateProblem();
}

function setupListeners() {
    UI.varBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            UI.varBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            state.numVars = parseInt(e.target.dataset.v);
            generateProblem();
        });
    });

    UI.btnNew.addEventListener('click', generateProblem);
    UI.btnClear.addEventListener('click', () => {
        state.draftGroup.clear();
        state.lockedGroups = [];
        UI.solIn.value = '';
        render();
        setFeedback('', '');
    });

    UI.btnCheck.addEventListener('click', checkSolution);

    // Keyup for locking group on Ctrl release
    document.addEventListener('keyup', (e) => {
        if ((e.key === 'Control' || e.key === 'Meta') && state.draftGroup.size > 0) {
            lockGroup();
        }
    });
}

function lockGroup() {
    let gArr = Array.from(state.draftGroup);
    let cube = checkSubcube(gArr);
    if (!cube) {
        setFeedback("Invalid group! Must be a rectangular power of 2.", "error");
        state.draftGroup.clear();
        render();
        return;
    }
    
    // Generate term
    let term = generateTerm(cube.mask, cube.base);
    
    // Add to input
    let currentEq = UI.solIn.value.trim();
    if (currentEq === '') {
        UI.solIn.value = term;
    } else {
        UI.solIn.value = currentEq + ' + ' + term;
    }
    
    state.lockedGroups.push(new Set(state.draftGroup));
    state.draftGroup.clear();
    setFeedback("Group added!", "success");
    render();
}

function generateTerm(mask, base) {
    if (mask === (1 << state.numVars) - 1) return '1'; // covers whole map
    
    let parts = [];
    for (let v = 0; v < state.numVars; v++) {
        let bitIndex = state.numVars - 1 - v;
        if ((mask & (1 << bitIndex)) === 0) {
            // Variable is fixed
            let isOne = (base & (1 << bitIndex)) !== 0;
            let vName = state.varNames[v];
            parts.push(isOne ? vName : vName + "'");
        }
    }
    return parts.join('*');
}

function generateProblem() {
    state.draftGroup.clear();
    state.lockedGroups = [];
    state.truthTable = [];
    const size = 1 << state.numVars;
    for (let i = 0; i < size; i++) {
        let r = Math.random();
        if (r < 0.4) state.truthTable.push(1);
        else if (r < 0.8) state.truthTable.push(0);
        else state.truthTable.push('X');
    }
    
    if (state.numVars === 2) state.varNames = ['A', 'B'];
    else if (state.numVars === 3) state.varNames = ['A', 'B', 'C'];
    else if (state.numVars === 4) state.varNames = ['A', 'B', 'C', 'D'];
    
    UI.solIn.value = '';
    setFeedback('', '');
    render();
}

function render() {
    renderAxesLines();
    renderKMap();
    renderTruthTable();
}

function getColsRows() {
    let cols = state.numVars >= 3 ? 4 : 2;
    let rows = state.numVars === 4 ? 4 : 2;
    let colGray = cols === 4 ? GRAY_2 : GRAY_1;
    let rowGray = rows === 4 ? GRAY_2 : GRAY_1;
    let colBits = cols === 4 ? 2 : 1;
    return { cols, rows, colGray, rowGray, colBits };
}

function renderAxesLines() {
    UI.axisLines.innerHTML = '';
    const CELL = 3.5; // rem
    const BORDER = 2; // px approx 0.125rem. We'll ignore minor pixel offsets for simplicity

    const createTopLine = (name, leftCells, widthCells, varIndex) => {
        let div = document.createElement('div');
        div.className = 'var-line top-axis';
        div.style.left = `calc(${CELL * (leftCells + 1)}rem)`;
        div.style.width = `calc(${CELL * widthCells}rem)`;
        div.style.top = `-1.5rem`;
        div.style.height = `1rem`;
        
        let span = document.createElement('span');
        span.className = 'var-name';
        span.contentEditable = true;
        span.innerText = name;
        span.addEventListener('input', (e) => { state.varNames[varIndex] = e.target.innerText.trim(); renderTruthTable(); });
        div.appendChild(span);
        UI.axisLines.appendChild(div);
    };

    const createLeftLine = (name, topCells, heightCells, varIndex) => {
        let div = document.createElement('div');
        div.className = 'var-line left-axis';
        div.style.top = `calc(${CELL * (topCells + 1)}rem)`;
        div.style.height = `calc(${CELL * heightCells}rem)`;
        div.style.left = `-1.5rem`;
        div.style.width = `1rem`;
        
        let span = document.createElement('span');
        span.className = 'var-name';
        span.contentEditable = true;
        span.innerText = name;
        span.addEventListener('input', (e) => { state.varNames[varIndex] = e.target.innerText.trim(); renderTruthTable(); });
        div.appendChild(span);
        UI.axisLines.appendChild(div);
    };

    if (state.numVars === 2) {
        // A is bottom row (row 1)
        createLeftLine(state.varNames[0], 1, 1, 0);
        // B is right col (col 1)
        createTopLine(state.varNames[1], 1, 1, 1);
    } else if (state.numVars === 3) {
        // A is bottom row
        createLeftLine(state.varNames[0], 1, 1, 0);
        // B is right 2 cols (cols 2, 3)
        createTopLine(state.varNames[1], 2, 2, 1);
        // C is middle 2 cols (cols 1, 2)
        createTopLine(state.varNames[2], 1, 2, 2);
    } else if (state.numVars === 4) {
        // A is bottom 2 rows (rows 2, 3)
        createLeftLine(state.varNames[0], 2, 2, 0);
        // B is middle 2 rows (rows 1, 2)
        createLeftLine(state.varNames[1], 1, 2, 1);
        // C is right 2 cols (cols 2, 3)
        createTopLine(state.varNames[2], 2, 2, 2);
        // D is middle 2 cols (cols 1, 2)
        createTopLine(state.varNames[3], 1, 2, 3);
    }
}

function renderKMap() {
    const { cols, rows, colGray, rowGray, colBits } = getColsRows();
    
    UI.kmapHead.innerHTML = '<th></th>';
    for (let c = 0; c < cols; c++) {
        let binStr = colGray[c].toString(2).padStart(colBits, '0');
        UI.kmapHead.innerHTML += `<th>${binStr}</th>`;
    }

    UI.kmapBody.innerHTML = '';
    for (let r = 0; r < rows; r++) {
        let tr = document.createElement('tr');
        let rowBinStr = rowGray[r].toString(2).padStart(state.numVars - colBits, '0');
        tr.innerHTML = `<th>${rowBinStr}</th>`;
        
        for (let c = 0; c < cols; c++) {
            let index = (rowGray[r] << colBits) | colGray[c];
            let td = document.createElement('td');
            let val = state.truthTable[index];
            td.innerText = val;
            if (val === 'X') td.classList.add('val-X');
            
            td.addEventListener('mousedown', (e) => {
                if (e.ctrlKey || e.metaKey) {
                    if (state.draftGroup.has(index)) state.draftGroup.delete(index);
                    else state.draftGroup.add(index);
                    renderKMapColors(); // fast re-render just for selection
                }
            });
            td.addEventListener('mouseenter', (e) => {
                if (e.buttons === 1 && (e.ctrlKey || e.metaKey)) {
                    state.draftGroup.add(index);
                    renderKMapColors();
                }
            });
            
            td.id = 'cell-' + index;
            tr.appendChild(td);
        }
        UI.kmapBody.appendChild(tr);
    }
    renderKMapColors();
}

function renderKMapColors() {
    const size = 1 << state.numVars;
    for (let i = 0; i < size; i++) {
        let td = document.getElementById('cell-' + i);
        if (!td) continue;
        td.className = '';
        if (state.truthTable[i] === 'X') td.classList.add('val-X');
        
        if (state.draftGroup.has(i)) td.classList.add('cell-selected');
        
        for (let g = 0; g < state.lockedGroups.length; g++) {
            if (state.lockedGroups[g].has(i)) {
                td.classList.add(`group-${g % 8}`);
            }
        }
    }
}

function renderTruthTable() {
    UI.truthHeadVar.innerText = state.varNames.join(', ');
    UI.truthBody.innerHTML = '';
    const size = 1 << state.numVars;
    for (let i = 0; i < size; i++) {
        let tr = document.createElement('tr');
        let binStr = i.toString(2).padStart(state.numVars, '0');
        let val = state.truthTable[i];
        tr.innerHTML = `<td>${i}</td><td>${binStr}</td><td>${val}</td>`;
        
        for (let g = 0; g < state.lockedGroups.length; g++) {
            if (state.lockedGroups[g].has(i)) {
                tr.classList.add(`group-${g % 8}`);
            }
        }
        
        UI.truthBody.appendChild(tr);
    }
}

function setFeedback(msg, type) {
    UI.feedback.innerText = msg;
    UI.feedback.className = type ? `fb-${type}` : '';
}

// Validation Logic
function checkSolution() {
    let eq = UI.solIn.value.trim();
    let groupRes = validateGroups();
    let eqRes = { ok: true, msg: '' };
    
    if (eq.length > 0) {
        eqRes = validateEquation(eq);
    } else if (state.lockedGroups.length === 0) {
        setFeedback("Please draw groups (Ctrl+Drag) or write an equation.", "error");
        return;
    }

    if (!groupRes.ok && state.lockedGroups.length > 0) {
        setFeedback("Group Error: " + groupRes.msg, "error");
        return;
    }
    
    if (eq.length > 0 && !eqRes.ok) {
        setFeedback("Equation Error: " + eqRes.msg, "error");
        return;
    }

    setFeedback("Perfect! Solution is correct and strictly optimal.", "success");
}

function checkSubcube(indices) {
    if (indices.length === 0) return false;
    let l = indices.length;
    if ((l & (l - 1)) !== 0) return false;
    let k = Math.log2(l);

    let base = indices[0];
    let mask = 0;
    for (let x of indices) mask |= (base ^ x);

    let setBits = 0;
    for (let i = 0; i < state.numVars; i++) {
        if ((mask & (1 << i)) !== 0) setBits++;
    }
    if (setBits !== k) return false;

    for (let x of indices) {
        if ((x & ~mask) !== (base & ~mask)) return false;
    }
    return { valid: true, mask: mask, base: base & ~mask };
}

function validateGroups() {
    if (state.lockedGroups.length === 0) return { ok: true, msg: '' };
    
    let covered = new Set();
    let onesCount = 0;
    for (let i = 0; i < state.truthTable.length; i++) {
        if (state.truthTable[i] === 1) onesCount++;
    }

    for (let i = 0; i < state.lockedGroups.length; i++) {
        let gArr = Array.from(state.lockedGroups[i]);
        let cube = checkSubcube(gArr);
        if (!cube) return { ok: false, msg: `Group ${i+1} is not a valid 2^k rectangle.` };

        for (let idx of gArr) {
            if (state.truthTable[idx] === 0) return { ok: false, msg: `Group ${i+1} covers a 0!` };
            if (state.truthTable[idx] === 1) covered.add(idx);
        }

        let isPrime = true;
        for (let b = 0; b < state.numVars; b++) {
            if ((cube.mask & (1 << b)) === 0) {
                let canExpand = true;
                for (let idx of gArr) {
                    let neighbor = idx ^ (1 << b);
                    if (state.truthTable[neighbor] === 0) {
                        canExpand = false; break;
                    }
                }
                if (canExpand) {
                    isPrime = false; break;
                }
            }
        }
        if (!isPrime) return { ok: false, msg: `Group ${i+1} is not maximal (not a Prime Implicant). Expand it!` };
    }

    if (covered.size !== onesCount) {
        return { ok: false, msg: `You missed some 1s! All 1s must be covered.` };
    }
    
    return { ok: true, msg: 'Groups valid.' };
}

function validateEquation(eq) {
    let jsEq = eq.replace(/\s+/g, '');
    jsEq = jsEq.replace(/([a-zA-Z0-9_]+)'/g, '!$1');
    jsEq = jsEq.replace(/([a-zA-Z0-9_)'\]])(?=[a-zA-Z0-9_(!\[])/g, '$1*');
    jsEq = jsEq.replace(/\*/g, '&&').replace(/\+/g, '||');

    let userTT = [];
    const size = 1 << state.numVars;
    
    for (let i = 0; i < size; i++) {
        let context = {};
        for (let v = 0; v < state.numVars; v++) {
            context[state.varNames[v]] = (i & (1 << (state.numVars - 1 - v))) !== 0;
        }
        
        let keys = Object.keys(context);
        let vals = Object.values(context);
        try {
            let func = new Function(...keys, `return !!(${jsEq});`);
            let res = func(...vals);
            userTT.push(res ? 1 : 0);
        } catch (e) {
            return { ok: false, msg: `Syntax error in equation.` };
        }
    }

    for (let i = 0; i < size; i++) {
        let expected = state.truthTable[i];
        let got = userTT[i];
        if (expected === 1 && got === 0) return { ok: false, msg: `Equation yields 0 for minterm ${i}, should be 1.` };
        if (expected === 0 && got === 1) return { ok: false, msg: `Equation yields 1 for minterm ${i}, should be 0.` };
    }

    return { ok: true, msg: 'Equation matches.' };
}

init();
"""

with open('index.js', 'w') as f:
    f.write(js_code)

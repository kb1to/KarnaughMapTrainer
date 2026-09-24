import re

with open('index.css', 'r') as f:
    css = f.read()

# Replace the Axis Lines part
new_css_part = """/* Axis Lines */
#kmap-container {
  margin: 4rem 4rem 1rem 4rem !important;
}

.var-line {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  box-sizing: border-box;
}

.var-line.top-axis {
  border: 3px solid var(--accent);
  border-bottom: none;
  height: 0.5rem;
}
.var-line.top-axis .var-name {
  position: absolute;
  top: -1.6rem;
}

.var-line.left-axis {
  border: 3px solid var(--accent);
  border-right: none;
  width: 0.5rem;
}
.var-line.left-axis .var-name {
  position: absolute;
  left: -1.5rem;
}

/* Editable variable names */
.var-name {
  font-weight: 800;
  font-size: 1.1rem;
  outline: none;
  cursor: text;
  background: var(--bg);
  padding: 0 0.2rem;
  border-radius: 4px;
  line-height: 1;
}
.var-name:focus {
  background: rgba(255,255,255,0.2);
}"""

css = re.sub(r'/\* Axis Lines \*/[\s\S]*?(?=\Z)', new_css_part, css)

with open('index.css', 'w') as f:
    f.write(css)


const countEl = document.querySelector('#count');
let count = 0;
function render() { countEl.textContent = count; }
document.querySelector('#plus').addEventListener('click', () => { count++; render(); });
document.querySelector('#minus').addEventListener('click', () => { count--; render(); });
document.querySelector('#reset').addEventListener('click', () => { count = 0; render(); });
render();

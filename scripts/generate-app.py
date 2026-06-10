#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
TEMPLATE = ROOT / "templates" / "static-app"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[áàäâã]", "a", text)
    text = re.sub(r"[éèëê]", "e", text)
    text = re.sub(r"[íìïî]", "i", text)
    text = re.sub(r"[óòöôõ]", "o", text)
    text = re.sub(r"[úùüû]", "u", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text[:60] or "app"


def reset_project(name: str) -> Path:
    path = PROJECTS / name
    if path.exists():
        shutil.rmtree(path)
    (path / "src").mkdir(parents=True)
    (path / "dist").mkdir(parents=True)
    return path


def write_common(path: Path, name: str, description: str) -> None:
    (path / "package.json").write_text(
        json.dumps(
            {
                "name": name,
                "version": "1.0.0",
                "private": True,
                "scripts": {
                    "start": "npx serve .",
                    "build": f"bash ../../scripts/build-static.sh {name}",
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (path / "manifest.json").write_text(
        json.dumps(
            {
                "name": name,
                "description": description,
                "type": "static",
                "created_by": "software-factory",
                "entrypoint": "index.html",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (path / "README.md").write_text(
        f"# {name}\n\n{description}\n\n## Desarrollo\n\n```bash\ncd projects/{name}\nnpm start\n```\n\n## Build\n\n```bash\ncd ../..\n./scripts/build-static.sh {name}\n```\n",
        encoding="utf-8",
    )


def app_tateti(path: Path, name: str) -> None:
    description = "Juego clásico de tatetí 3x3 para dos jugadores locales."
    (path / "index.html").write_text("""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Tatetí</title>
  <link rel="stylesheet" href="src/styles.css" />
</head>
<body>
  <main class="app">
    <h1>Tatetí</h1>
    <p class="subtitle">Jugá en pareja, turno por turno.</p>
    <section id="board" class="board" aria-label="Tablero de tatetí"></section>
    <p id="status" class="status">Turno de X</p>
    <button id="reset" type="button">Reiniciar</button>
  </main>
  <script src="src/app.js"></script>
</body>
</html>
""", encoding="utf-8")
    (path / "src/styles.css").write_text("""* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #0f172a;
  color: #f8fafc;
  font-family: system-ui, sans-serif;
}
.app { text-align: center; }
h1 { margin: 0 0 8px; font-size: clamp(2.5rem, 10vw, 5rem); }
.subtitle { color: #cbd5e1; }
.board {
  display: grid;
  grid-template-columns: repeat(3, minmax(72px, 110px));
  gap: 12px;
  margin: 28px auto;
}
.cell {
  min-height: 92px;
  border: 0;
  border-radius: 18px;
  background: #1e293b;
  color: #67e8f9;
  font-size: 4rem;
  font-weight: 900;
  cursor: pointer;
}
.cell.o { color: #fbbf24; }
.cell:disabled { cursor: default; }
.status { min-height: 1.5em; font-weight: 800; }
button {
  border: 0;
  border-radius: 999px;
  padding: 12px 20px;
  background: #38bdf8;
  color: #082f49;
  font-weight: 800;
  cursor: pointer;
}
""", encoding="utf-8")
    (path / "src/app.js").write_text("""const boardEl = document.querySelector('#board');
const statusEl = document.querySelector('#status');
const resetBtn = document.querySelector('#reset');
let board = Array(9).fill(null);
let turn = 'X';
let done = false;

const wins = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6]
];

function winner() {
  for (const [a, b, c] of wins) {
    if (board[a] && board[a] === board[b] && board[a] === board[c]) return board[a];
  }
  return null;
}

function render() {
  boardEl.innerHTML = '';
  board.forEach((value, index) => {
    const btn = document.createElement('button');
    btn.className = 'cell' + (value ? ` ${value.toLowerCase()}` : '');
    btn.textContent = value || '';
    btn.disabled = Boolean(value || done);
    btn.addEventListener('click', () => play(index));
    boardEl.append(btn);
  });
  const win = winner();
  if (win) {
    statusEl.textContent = `Ganó ${win}`;
    done = true;
    return;
  }
  if (board.every(Boolean)) {
    statusEl.textContent = 'Empate';
    done = true;
    return;
  }
  statusEl.textContent = `Turno de ${turn}`;
}

function play(index) {
  if (done || board[index]) return;
  board[index] = turn;
  turn = turn === 'X' ? 'O' : 'X';
  render();
}

resetBtn.addEventListener('click', () => {
  board = Array(9).fill(null);
  turn = 'X';
  done = false;
  render();
});

render();
""", encoding="utf-8")
    write_common(path, name, description)


def app_todo(path: Path, name: str) -> None:
    description = "Lista de tareas simple con guardado en el navegador."
    (path / "index.html").write_text("""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Lista de tareas</title>
  <link rel="stylesheet" href="src/styles.css" />
</head>
<body>
  <main class="app">
    <h1>Lista de tareas</h1>
    <p class="subtitle">Agregá tareas y marcá las que ya terminaste.</p>
    <form id="form" class="form">
      <input id="task" name="task" placeholder="Nueva tarea..." autocomplete="off" required />
      <button type="submit">Agregar</button>
    </form>
    <ul id="list" class="list"></ul>
    <p id="empty" class="empty">No hay tareas todavía.</p>
  </main>
  <script src="src/app.js"></script>
</body>
</html>
""", encoding="utf-8")
    (path / "src/styles.css").write_text("""* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  padding: 24px;
  background: linear-gradient(135deg, #111827, #0f172a);
  color: #f8fafc;
  font-family: system-ui, sans-serif;
}
.app { max-width: 720px; margin: 0 auto; }
h1 { margin: 0 0 8px; font-size: clamp(2.2rem, 8vw, 4rem); }
.subtitle { margin: 0 0 24px; color: #cbd5e1; }
.form { display: flex; gap: 10px; margin-bottom: 20px; }
input { flex: 1; padding: 14px 16px; border: 0; border-radius: 14px; font: inherit; }
button { border: 0; border-radius: 14px; padding: 14px 18px; background: #38bdf8; color: #082f49; font-weight: 800; cursor: pointer; }
.list { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
li { display: flex; align-items: center; gap: 10px; padding: 14px; border-radius: 14px; background: rgba(255,255,255,0.08); }
li.done span { text-decoration: line-through; color: #94a3b8; }
li span { flex: 1; }
.delete { background: #fb7185; color: #450a0a; padding: 8px 12px; }
.empty { color: #94a3b8; text-align: center; }
@media (max-width: 560px) { .form { flex-direction: column; } }
""", encoding="utf-8")
    (path / "src/app.js").write_text("""const form = document.querySelector('#form');
const input = document.querySelector('#task');
const list = document.querySelector('#list');
const empty = document.querySelector('#empty');
const key = 'software-factory-todos';
let tasks = JSON.parse(localStorage.getItem(key) || '[]');

function save() {
  localStorage.setItem(key, JSON.stringify(tasks));
}

function render() {
  list.innerHTML = '';
  tasks.forEach((task, index) => {
    const li = document.createElement('li');
    li.className = task.done ? 'done' : '';
    const check = document.createElement('button');
    check.type = 'button';
    check.textContent = task.done ? 'Desmarcar' : 'Hecho';
    check.addEventListener('click', () => {
      task.done = !task.done;
      save();
      render();
    });
    const text = document.createElement('span');
    text.textContent = task.text;
    const del = document.createElement('button');
    del.type = 'button';
    del.className = 'delete';
    del.textContent = 'Borrar';
    del.addEventListener('click', () => {
      tasks.splice(index, 1);
      save();
      render();
    });
    li.append(check, text, del);
    list.append(li);
  });
  empty.hidden = tasks.length > 0;
}

form.addEventListener('submit', event => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  tasks.push({ text, done: false });
  input.value = '';
  save();
  render();
});

render();
""", encoding="utf-8")
    write_common(path, name, description)


def app_tip(path: Path, name: str) -> None:
    description = "Calculadora de propinas para restaurantes."
    (path / "index.html").write_text("""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Calculadora de propinas</title>
  <link rel="stylesheet" href="src/styles.css" />
</head>
<body>
  <main class="app">
    <h1>Propinas</h1>
    <p class="subtitle">Calculá propina y total por persona.</p>
    <label>Importe <input id="bill" type="number" min="0" step="0.01" value="0" /></label>
    <label>Propina % <input id="tip" type="number" min="0" step="1" value="10" /></label>
    <label>Personas <input id="people" type="number" min="1" step="1" value="1" /></label>
    <section class="results">
      <div><span>Propina</span><strong id="tipTotal">$0.00</strong></div>
      <div><span>Total</span><strong id="total">$0.00</strong></div>
      <div><span>Por persona</span><strong id="perPerson">$0.00</strong></div>
    </section>
  </main>
  <script src="src/app.js"></script>
</body>
</html>
""", encoding="utf-8")
    (path / "src/styles.css").write_text("""* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #052e16;
  color: #f0fdf4;
  font-family: system-ui, sans-serif;
}
.app { width: min(520px, 100%); padding: 28px; border-radius: 24px; background: #064e3b; }
h1 { text-align: center; margin: 0 0 8px; }
.subtitle { text-align: center; color: #bbf7d0; margin-top: 0; }
label { display: grid; gap: 6px; margin: 16px 0; font-weight: 700; }
input { padding: 14px; border: 0; border-radius: 14px; font: inherit; }
.results { display: grid; gap: 12px; margin-top: 24px; }
.results div { padding: 16px; border-radius: 16px; background: rgba(255,255,255,0.1); }
.results span { display: block; color: #bbf7d0; }
.results strong { display: block; font-size: 2rem; margin-top: 4px; }
""", encoding="utf-8")
    (path / "src/app.js").write_text("""const inputs = [...document.querySelectorAll('input')];
const bill = document.querySelector('#bill');
const tip = document.querySelector('#tip');
const people = document.querySelector('#people');

function money(value) {
  return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value || 0);
}

function render() {
  const billValue = Math.max(0, Number(bill.value) || 0);
  const tipValue = Math.max(0, Number(tip.value) || 0);
  const peopleValue = Math.max(1, Number(people.value) || 1);
  const tipTotal = billValue * tipValue / 100;
  const total = billValue + tipTotal;
  document.querySelector('#tipTotal').textContent = money(tipTotal);
  document.querySelector('#total').textContent = money(total);
  document.querySelector('#perPerson').textContent = money(total / peopleValue);
}

inputs.forEach(input => input.addEventListener('input', render));
render();
""", encoding="utf-8")
    write_common(path, name, description)


def app_pomodoro(path: Path, name: str) -> None:
    description = "Temporizador Pomodoro para trabajar en bloques."
    (path / "index.html").write_text("""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pomodoro</title>
  <link rel="stylesheet" href="src/styles.css" />
</head>
<body>
  <main class="app">
    <h1>Pomodoro</h1>
    <p id="time" class="time">25:00</p>
    <div class="actions">
      <button id="start" type="button">Iniciar</button>
      <button id="pause" type="button">Pausar</button>
      <button id="reset" type="button">Reiniciar</button>
    </div>
  </main>
  <script src="src/app.js"></script>
</body>
</html>
""", encoding="utf-8")
    (path / "src/styles.css").write_text("""* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #7c2d12, #111827);
  color: #fff7ed;
  font-family: system-ui, sans-serif;
}
.app { text-align: center; }
h1 { margin: 0 0 24px; }
.time { font-size: clamp(4rem, 20vw, 8rem); font-weight: 900; font-variant-numeric: tabular-nums; }
.actions { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
button { border: 0; border-radius: 999px; padding: 14px 20px; background: #fdba74; color: #431407; font-weight: 900; cursor: pointer; }
""", encoding="utf-8")
    (path / "src/app.js").write_text("""const timeEl = document.querySelector('#time');
const startBtn = document.querySelector('#start');
const pauseBtn = document.querySelector('#pause');
const resetBtn = document.querySelector('#reset');
const total = 25 * 60;
let remaining = total;
let timer = null;

function format(seconds) {
  const m = String(Math.floor(seconds / 60)).padStart(2, '0');
  const s = String(seconds % 60).padStart(2, '0');
  return `${m}:${s}`;
}

function render() {
  timeEl.textContent = format(remaining);
}

function tick() {
  remaining = Math.max(0, remaining - 1);
  render();
  if (remaining === 0) pause();
}

function start() {
  if (timer) return;
  timer = setInterval(tick, 1000);
}

function pause() {
  clearInterval(timer);
  timer = null;
}

function reset() {
  pause();
  remaining = total;
  render();
}

startBtn.addEventListener('click', start);
pauseBtn.addEventListener('click', pause);
resetBtn.addEventListener('click', reset);
render();
""", encoding="utf-8")
    write_common(path, name, description)


def app_counter(path: Path, name: str) -> None:
    description = "Contador simple con botones de sumar, restar y reiniciar."
    (path / "index.html").write_text("""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Contador</title>
  <link rel="stylesheet" href="src/styles.css" />
</head>
<body>
  <main class="app">
    <h1>Contador</h1>
    <p id="count" class="count">0</p>
    <div class="actions">
      <button id="minus" type="button">-1</button>
      <button id="reset" type="button">Reiniciar</button>
      <button id="plus" type="button">+1</button>
    </div>
  </main>
  <script src="src/app.js"></script>
</body>
</html>
""", encoding="utf-8")
    (path / "src/styles.css").write_text("""* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #312e81;
  color: #eef2ff;
  font-family: system-ui, sans-serif;
}
.app { text-align: center; }
h1 { margin: 0 0 24px; }
.count { font-size: clamp(5rem, 24vw, 10rem); font-weight: 900; }
.actions { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
button { border: 0; border-radius: 999px; padding: 14px 20px; background: #a5b4fc; color: #111827; font-weight: 900; cursor: pointer; }
""", encoding="utf-8")
    (path / "src/app.js").write_text("""const countEl = document.querySelector('#count');
let count = 0;
function render() { countEl.textContent = count; }
document.querySelector('#plus').addEventListener('click', () => { count++; render(); });
document.querySelector('#minus').addEventListener('click', () => { count--; render(); });
document.querySelector('#reset').addEventListener('click', () => { count = 0; render(); });
render();
""", encoding="utf-8")
    write_common(path, name, description)


def app_notes(path: Path, name: str) -> None:
    description = "Bloc de notas simple con guardado local."
    (path / "index.html").write_text("""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Notas</title>
  <link rel="stylesheet" href="src/styles.css" />
</head>
<body>
  <main class="app">
    <h1>Notas</h1>
    <p class="subtitle">Escribí una nota y se guarda en este navegador.</p>
    <textarea id="note" placeholder="Escribí acá..."></textarea>
    <p id="saved" class="saved">Guardado automáticamente.</p>
  </main>
  <script src="src/app.js"></script>
</body>
</html>
""", encoding="utf-8")
    (path / "src/styles.css").write_text("""* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  padding: 24px;
  background: #172554;
  color: #eff6ff;
  font-family: system-ui, sans-serif;
}
.app { max-width: 760px; margin: 0 auto; }
h1 { margin: 0 0 8px; }
.subtitle { margin-top: 0; color: #bfdbfe; }
textarea {
  width: 100%;
  min-height: 55vh;
  resize: vertical;
  border: 0;
  border-radius: 18px;
  padding: 18px;
  font: 1.1rem/1.6 system-ui, sans-serif;
}
.saved { color: #bfdbfe; text-align: center; }
""", encoding="utf-8")
    (path / "src/app.js").write_text("""const note = document.querySelector('#note');
const key = 'software-factory-note';
note.value = localStorage.getItem(key) || '';
note.addEventListener('input', () => {
  localStorage.setItem(key, note.value);
});
""", encoding="utf-8")
    write_common(path, name, description)


def generate(request: str) -> tuple[str, str, Path]:
    text = request.lower()
    if any(word in text for word in ['tateti', 'tic tac', 'tictactoe', 'tres en raya']):
        return 'tateti', 'Juego clásico de tatetí 3x3 para dos jugadores locales.', app_tateti
    if any(word in text for word in ['tarea', 'tareas', 'todo', 'pendiente', 'pendientes']):
        return 'lista-tareas', 'Lista de tareas simple con guardado en el navegador.', app_todo
    if any(word in text for word in ['propina', 'propinas', 'restaurante', 'restaurantes']):
        return 'calculadora-propinas', 'Calculadora de propinas para restaurantes.', app_tip
    if any(word in text for word in ['pomodoro', 'temporizador', 'timer']):
        return 'pomodoro', 'Temporizador Pomodoro para trabajar en bloques.', app_pomodoro
    if any(word in text for word in ['contador', 'contar']):
        return 'contador', 'Contador simple con botones de sumar, restar y reiniciar.', app_counter
    if any(word in text for word in ['nota', 'notas', 'bloc']):
        return 'notas', 'Bloc de notas simple con guardado local.', app_notes
    base = slugify(request)
    return base, request.strip() or 'App estática generada por Software Factory.', None


def main() -> int:
    if len(sys.argv) < 3:
        print('Uso: generate-app.py <pedido> <nombre-proyecto>', file=sys.stderr)
        return 2
    request = sys.argv[1]
    forced_name = sys.argv[2]
    default_name, description, builder = generate(request)
    name = forced_name or default_name
    name = slugify(name)
    path = reset_project(name)
    if builder:
        builder(path, name)
    else:
        (path / "index.html").write_text("""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Software Factory App</title>
  <link rel="stylesheet" href="src/styles.css" />
</head>
<body>
  <main class="app">
    <h1>App generada</h1>
    <p class="subtitle">Este proyecto quedó creado. Ahora un agente puede reemplazar esta plantilla por la app específica.</p>
    <p id="request" class="request"></p>
  </main>
  <script src="src/app.js"></script>
</body>
</html>
""", encoding="utf-8")
        (path / "src/styles.css").write_text("""* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px; background: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; }
.app { max-width: 720px; padding: 32px; border-radius: 24px; background: rgba(255,255,255,0.08); }
h1 { margin-top: 0; }
.subtitle, .request { color: #cbd5e1; line-height: 1.5; }
""", encoding="utf-8")
        (path / "src/app.js").write_text("""document.querySelector('#request').textContent = 'Pedido: ' + new URLSearchParams(location.search).get('q');
""", encoding="utf-8")
        write_common(path, name, description)
    print(path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

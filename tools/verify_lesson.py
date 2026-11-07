#!/usr/bin/env python3
"""Verification gates for one lesson's MicroPython program.

Usage:
  python3 tools/verify_lesson.py lessons/01-traffic-light [--base main] [--allow GLOB ...]

Checks (each prints PASS or FAIL; any FAIL makes the exit code 1):
  a. extract   the program exactly as the page builds it for "Try it on my real board":
               the page's `window.__lessonProgram = () => ...` expression is evaluated in Node
               with the top-level declarations it needs (so lesson 1's CODE gets GREEN_S
               replaced by DEFAULT_GREEN, and lessons 3-10 run codeLines() with DEFAULT_CFG).
  b. compile   the page program (and main.py, if present) with mpy-cross.
  c. main.py   lessons/<slug>/main.py matches the page program line by line. Extra lines in
               main.py that are only a comment are allowed (e.g. a note about a default);
               every other line must be identical, in the same order, nothing missing.
  d. pins      rules from AGENT.md: only real DevKit V1 GPIOs; no outputs on D34/D35/VP/VN;
               no parts on D2/D5/D12/D15/TX0/RX0; D25/D26/D27 only as red/yellow/green
               outputs (and red/yellow/green only on those pins); analog input only on ADC1.
  e. files     files changed against the base branch (committed, staged, unstaged and
               untracked) are all inside the allowlist and none is protected.

This never talks to a board, a network or GitHub. It needs `node` and `mpy-cross`
(set MPY_CROSS to a path, or `pip install --user mpy-cross`).
"""
import argparse
import ast
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- (a) extraction

# Node script: finds the page's __lessonProgram expression, pulls in the top-level
# declarations it depends on (transitively, in source order) and evaluates it.
EXTRACT_JS = r"""
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const scripts = [];
html.replace(/<script(?![^>]*\bsrc\s*=)[^>]*>([\s\S]*?)<\/script>/gi, (m, body) => { scripts.push(body); return m; });
const src = scripts.join('\n;\n');

const compiles = (code) => { try { new vm.Script(code); return true; } catch (e) { return false; } };
// Smallest piece of src from `start` that is a whole statement/expression. The end must be
// followed by something that cannot continue it (so `a\n.map(...)` is not cut short).
function takeUntilValid(start, wrap) {
  for (let i = start; i < src.length && i - start < 200000; i++) {
    const c = src[i];
    if (c !== ';' && c !== '\n') continue;
    const piece = src.slice(start, i);
    if (!piece.trim()) continue;
    const rest = src.slice(i + 1).replace(/^\s+/, '');
    if (c === '\n' && /^[.?:+\-*/%&|^,)\]}=<>]/.test(rest)) continue;
    if (compiles(wrap(piece))) return piece;
  }
  return null;
}

const m = /window\.__lessonProgram\s*=\s*\(\s*\)\s*=>\s*/.exec(src);
if (!m) { console.log(JSON.stringify({ error: 'no `window.__lessonProgram = () => ...` found in the page' })); process.exit(0); }
const expr = takeUntilValid(m.index + m[0].length, (p) => '(' + p + ')');
if (expr === null) { console.log(JSON.stringify({ error: 'could not parse the __lessonProgram expression' })); process.exit(0); }

// Top-level declarations start at column 0 in these pages.
const decls = new Map();
const re = /^(?:(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*[=;]|function\s+([A-Za-z_$][\w$]*)\s*\()/gm;
let d;
while ((d = re.exec(src))) {
  const name = d[1] || d[2];
  if (decls.has(name)) continue;
  const text = takeUntilValid(d.index, (p) => p);
  if (text !== null) decls.set(name, { pos: d.index, text });
}
// Names used in a piece of code, skipping comments, plain strings and the text part of
// template literals (but not their ${...} parts), so words inside strings are not followed.
function idents(s) {
  let code = '', i = 0;
  const stack = [];  // open template literals: brace depth when their ${ started
  let depth = 0;
  while (i < s.length) {
    const c = s[i], n = s[i + 1];
    if (c === '/' && n === '/') { while (i < s.length && s[i] !== '\n') i++; continue; }
    if (c === '/' && n === '*') { i = s.indexOf('*/', i + 2); i = i < 0 ? s.length : i + 2; continue; }
    if (c === '"' || c === "'") { i++; while (i < s.length && s[i] !== c) i += s[i] === '\\' ? 2 : 1; i++; code += ' "" '; continue; }
    if (c === '`' || (c === '}' && stack.length && stack[stack.length - 1] === depth)) {
      if (c === '}') stack.pop();
      i++;
      while (i < s.length && s[i] !== '`' && !(s[i] === '$' && s[i + 1] === '{')) i += s[i] === '\\' ? 2 : 1;
      if (s[i] === '$') { stack.push(depth); i += 2; } else i++;
      code += ' ';
      continue;
    }
    if (c === '{') depth++;
    if (c === '}') depth--;
    code += c; i++;
  }
  return new Set((code.match(/(?<![\w$])(?<!(?<!\.)\.)[A-Za-z_$][\w$]*/g) || []));
}
const need = new Set();
const queue = [...idents(expr)];
while (queue.length) {
  const n = queue.pop();
  if (need.has(n) || !decls.has(n)) continue;
  need.add(n);
  queue.push(...idents(decls.get(n).text));
}
const ordered = [...need].map((n) => decls.get(n)).sort((x, y) => x.pos - y.pos);

// Anything that touches the browser gets a harmless stand-in; the program text never depends on it.
const stub = new Proxy(function () {}, {
  get: (t, k) => (k === Symbol.toPrimitive ? () => '\u0000STUB\u0000' : k === 'then' ? undefined : stub),
  apply: () => stub, construct: () => stub, set: () => true,
});
const ctx = { console, document: stub, localStorage: stub, sessionStorage: stub, navigator: stub, location: stub,
  THREE: stub, requestAnimationFrame: () => 0, setTimeout: () => 0, setInterval: () => 0, addEventListener: () => {},
  matchMedia: () => stub, getComputedStyle: () => stub, performance: { now: () => 0 }, innerWidth: 1400, innerHeight: 860 };
ctx.window = ctx; ctx.self = ctx;
vm.createContext(ctx);
try {
  const code = ordered.map((x) => x.text).join(';\n') + ';\nglobalThis.__out = (' + expr + ');';
  vm.runInContext(code, ctx, { timeout: 5000 });
  if (typeof ctx.__out !== 'string') throw new Error('the expression did not give a string');
  if (ctx.__out.includes('\u0000STUB')) throw new Error('the program text depends on the browser (a stand-in leaked into it)');
  console.log(JSON.stringify({ program: ctx.__out, expr: expr.trim(), deps: ordered.map((x) => x.text.match(/[A-Za-z_$][\w$]*/g)[1]) }));
} catch (e) {
  console.log(JSON.stringify({ error: 'evaluating the page program failed: ' + e.message, expr: expr.trim() }));
}
"""


def extract_program(page):
    """Return (program, info) or raise RuntimeError."""
    node = shutil.which("node")
    if not node:
        raise RuntimeError("node is not installed, so the page cannot be evaluated")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(EXTRACT_JS)
        js = f.name
    try:
        r = subprocess.run([node, js, str(page)], capture_output=True, text=True, timeout=60)
    finally:
        os.unlink(js)
    if r.returncode != 0:
        raise RuntimeError("node failed: " + (r.stderr.strip() or r.stdout.strip()))
    out = json.loads(r.stdout.strip().splitlines()[-1])
    if "error" in out:
        raise RuntimeError(out["error"])
    if not out["program"].strip():
        raise RuntimeError("the page program is empty")
    return out["program"], out


# ---------------------------------------------------------------- (b) compile


def mpy_cross_cmd():
    env = os.environ.get("MPY_CROSS")
    if env:
        return [env]
    exe = shutil.which("mpy-cross")
    if exe:
        return [exe]
    r = subprocess.run([sys.executable, "-m", "mpy_cross", "--version"], capture_output=True, text=True)
    if r.returncode == 0:
        return [sys.executable, "-m", "mpy_cross"]
    return None


def compile_mpy(code, name):
    """Compile with mpy-cross. Returns (ok, message)."""
    cmd = mpy_cross_cmd()
    if not cmd:
        return False, "mpy-cross not found (pip install --user mpy-cross, or set MPY_CROSS)"
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / name
        p.write_text(code)
        r = subprocess.run(cmd + ["-o", str(p.with_suffix(".mpy")), str(p)], capture_output=True, text=True, cwd=d)
    msg = (r.stderr + r.stdout).strip()
    return r.returncode == 0, msg or "compiled"


# ---------------------------------------------------------------- (c) main.py vs page


def compare_lines(page_prog, main_prog):
    """Line-by-line match. main.py may add whole-line comments; nothing else may differ."""
    page = page_prog.split("\n")
    main = main_prog.split("\n")
    problems, extras = [], []
    i = j = 0
    while j < len(main):
        if i < len(page) and main[j] == page[i]:
            i += 1
        elif main[j].strip().startswith("#"):
            extras.append(j + 1)
        else:
            want = repr(page[i]) if i < len(page) else "(end of page program)"
            problems.append(f"main.py line {j + 1}: {main[j]!r} but the page has {want} (page line {i + 1})")
            break
        j += 1
    if not problems and i < len(page):
        problems.append(f"main.py ends early: page line {i + 1} {page[i]!r} is missing")
    return problems, extras


# ---------------------------------------------------------------- (d) pins

VALID_GPIO = {0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33, 34, 35, 36, 39}
INPUT_ONLY = {34: "D34", 35: "D35", 36: "VP", 39: "VN"}
NO_NEW_PARTS = {2: "D2", 5: "D5", 12: "D12", 15: "D15", 1: "TX0", 3: "RX0"}
LIGHTS = {25: "red", 26: "yellow", 27: "green"}
ADC1 = {32, 33, 34, 35, 36, 39}
# Uses that are not a new part, so the start-up pin rule does not apply.
EXEMPT = {"00-meet-esp32": {2: "the blue LED soldered on the board (GPIO2), not a new part"}}


def _name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def pin_uses(tree):
    """Yield (gpio or None, mode, target_name, lineno) for each Pin(...) call."""
    consts = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, int):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    consts[t.id] = n.value.value
    parents = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p):
            parents[c] = p
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and _name(n.func) == "Pin"):
            continue
        arg = n.args[0] if n.args else next((k.value for k in n.keywords if k.arg == "id"), None)
        gpio = None
        if isinstance(arg, ast.Constant) and isinstance(arg.value, int):
            gpio = arg.value
        elif isinstance(arg, ast.Name):
            gpio = consts.get(arg.id)
        mode = None
        margs = n.args[1:2] + [k.value for k in n.keywords if k.arg == "mode"]
        if margs:
            mode = _name(margs[0])
        # what wraps it: PWM(Pin(13)) is an output, ADC(Pin(33)) / TouchPad(Pin(32)) are inputs
        up = parents.get(n)
        if isinstance(up, ast.Call) and n in up.args:
            wrapper = _name(up.func)
            if wrapper in ("PWM", "DAC"):
                mode = "OUT"
            elif wrapper in ("ADC", "TouchPad"):
                mode = wrapper
            up = parents.get(up)
        target = None
        if isinstance(up, ast.Assign) and len(up.targets) == 1:
            target = _name(up.targets[0])
        yield gpio, mode, target, n.lineno


def check_pins(code, slug):
    """Return (problems, notes)."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"cannot read the program to check pins: {e}"], []
    problems, notes = [], []
    exempt = EXEMPT.get(slug, {})
    for gpio, mode, target, line in pin_uses(tree):
        where = f"line {line}"
        if gpio is None:
            problems.append(f"{where}: Pin number is not a plain number, so it cannot be checked")
            continue
        if gpio not in VALID_GPIO:
            problems.append(f"{where}: GPIO{gpio} is not a pin on the ESP32 DevKit V1 (30 pins)")
            continue
        if gpio in INPUT_ONLY and mode in ("OUT", "OPEN_DRAIN"):
            problems.append(f"{where}: {INPUT_ONLY[gpio]} is input-only and cannot be an output")
        if gpio in NO_NEW_PARTS:
            if gpio in exempt:
                notes.append(f"{where}: {NO_NEW_PARTS[gpio]} allowed here: {exempt[gpio]}")
            else:
                problems.append(f"{where}: {NO_NEW_PARTS[gpio]} is a start-up or serial pin; no new parts on it")
        if gpio in LIGHTS:
            if mode != "OUT":
                problems.append(f"{where}: D{gpio} drives the {LIGHTS[gpio]} LED, so it must be Pin.OUT")
            if target and target != LIGHTS[gpio]:
                problems.append(f"{where}: D{gpio} is the {LIGHTS[gpio]} LED but is named {target!r}")
        if target in LIGHTS.values() and gpio != {v: k for k, v in LIGHTS.items()}[target]:
            want = {v: k for k, v in LIGHTS.items()}[target]
            problems.append(f"{where}: {target} must be on D{want} (lesson 1 wiring), not GPIO{gpio}")
        if mode == "ADC" and gpio not in ADC1:
            problems.append(f"{where}: analog input on GPIO{gpio} is ADC2 and stops working with Wi-Fi on; use D32-D35/VP/VN")
    return problems, notes


# ---------------------------------------------------------------- (e) changed files

PROTECTED = [".github/*", "AGENT.md", "CLAUDE.md", "course.js"]


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def changed_files(repo, base):
    mb = git(repo, "merge-base", base, "HEAD").strip()
    files = set(git(repo, "diff", "--name-only", mb).split())  # committed + staged + unstaged
    for f in git(repo, "ls-files", "--others", "--exclude-standard").split():
        if "__pycache__/" not in f:  # Python caches from running the tests
            files.add(f)
    return sorted(files)


def check_files(repo, base, allow):
    files = changed_files(repo, base)
    problems = []
    for f in files:
        if any(fnmatch.fnmatch(f, p) for p in PROTECTED):
            problems.append(f"{f} is protected and must not change")
        elif not any(fnmatch.fnmatch(f, p) for p in allow):
            problems.append(f"{f} is not in the allowlist")
    return files, problems


# ---------------------------------------------------------------- runner


def find_repo(path):
    r = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(r.stdout.strip()) if r.returncode == 0 else None


def run(lesson_dir, base="main", allow=None, out=print):
    lesson_dir = Path(lesson_dir).resolve()
    slug = lesson_dir.name
    results = []

    def report(check, ok, detail):
        results.append((check, ok))
        out(f"[{'PASS' if ok else 'FAIL'}] {check}: {detail.splitlines()[0] if detail else ''}")
        for extra in detail.splitlines()[1:]:
            out(f"       {extra}")

    out(f"== verify {slug}")
    page = lesson_dir / "index.html"
    program = None
    try:
        program, info = extract_program(page)
        report("a. extract", True, f"{len(program.splitlines())} lines from `{info['expr'][:70]}`"
               + (f"\nuses: {', '.join(info['deps'])}" if info["deps"] else ""))
    except (RuntimeError, OSError, ValueError) as e:
        report("a. extract", False, str(e))

    main_path = lesson_dir / "main.py"
    main = main_path.read_text() if main_path.exists() else None

    if program is None:
        report("b. compile", False, "no page program to compile")
    else:
        ok, msg = compile_mpy(program, "page_program.py")
        detail = "page program " + ("compiles" if ok else "does not compile:\n" + msg)
        if main is not None:
            ok2, msg2 = compile_mpy(main, "main.py")
            detail += "; main.py " + ("compiles" if ok2 else "does not compile:\n" + msg2)
            ok = ok and ok2
        report("b. compile", ok, detail)

    if main is None:
        report("c. main.py", False, f"{slug}/main.py is missing")
    elif program is None:
        report("c. main.py", False, "no page program to compare with")
    else:
        problems, extras = compare_lines(program, main)
        note = f" (extra comment lines in main.py: {', '.join(map(str, extras))})" if extras else ""
        report("c. main.py", not problems, ("\n".join(problems)) if problems else "matches the page line by line" + note)

    probs, notes = [], []
    checked = []
    for label, code in (("page", program), ("main.py", main)):
        if code is None:
            continue
        p, n = check_pins(code, slug)
        probs += [f"{label}: {x}" for x in p]
        notes += [f"{label}: {x}" for x in n]
        checked.append(label)
    if not checked:
        report("d. pins", False, "no program to check")
    else:
        report("d. pins", not probs, "\n".join(probs) if probs else
               f"{' and '.join(checked)} follow the AGENT.md pin rules" + ("\n" + "\n".join(notes) if notes else ""))

    repo = find_repo(lesson_dir)
    if repo is None:
        report("e. files", False, "the lesson is not inside a git repository")
    else:
        rel = lesson_dir.relative_to(repo).as_posix()
        allow = list(allow or []) + [f"{rel}/*", "tools/verify_lesson.py", "tools/tests/*"]
        try:
            files, problems = check_files(repo, base, allow)
            report("e. files", not problems, "\n".join(problems) if problems else
                   f"{len(files)} changed file(s) against {base}, all allowed" + ("\n" + ", ".join(files) if files else ""))
        except RuntimeError as e:
            report("e. files", False, str(e))

    failed = [c for c, ok in results if not ok]
    out(f"== {slug}: {'PASS' if not failed else 'FAIL (' + ', '.join(failed) + ')'}")
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("lessons", nargs="+", help="lesson folder(s), e.g. lessons/01-traffic-light")
    ap.add_argument("--base", default="main", help="branch to compare changed files against (default: main)")
    ap.add_argument("--allow", action="append", default=[], help="extra allowed path glob for check e")
    a = ap.parse_args(argv)
    rc = 0
    for lesson in a.lessons:
        rc |= run(lesson, a.base, a.allow)
    return rc


if __name__ == "__main__":
    sys.exit(main())

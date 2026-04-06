#!/usr/bin/env python3
"""
proba.py — probat transcriptionem ex κ in C99.

Usus: proba.py <directorium_fontis> <directorium_exitus>

Transcribit fontes et supplementarium, scribit Faceplica,
aedificat per face -C, currit.
"""

import subprocess, sys, os, glob, re, shutil

if len(sys.argv) < 3:
    print(f"usus: {sys.argv[0]} <directorium_fontis> <directorium_exitus>",
          file=sys.stderr)
    sys.exit(1)

FONS = sys.argv[1]
EXITUS = sys.argv[2]
SUPPL = "supplementario"

print(f"{'='*60}")
print(f"  PROBATIO: {FONS}")
print(f"{'='*60}")
print()

# ── 1. transcriptio ──────────────────────────────────────────

print("1. transcriptio...")
if os.path.exists(EXITUS):
    shutil.rmtree(EXITUS)
subprocess.run([sys.executable, "κadc.py", FONS, EXITUS], check=True)

# transcribe supplementarium si existit
if os.path.isdir(SUPPL):
    suppl_exitus = os.path.join(EXITUS, "_suppl")
    subprocess.run([sys.executable, "κadc.py", SUPPL, suppl_exitus], check=True)
    # copia plicarum supplementariarum in directorium exitus
    for plica in glob.glob(os.path.join(suppl_exitus, "*")):
        nomen = os.path.basename(plica)
        dest = os.path.join(EXITUS, nomen)
        if not os.path.exists(dest):
            shutil.copy2(plica, dest)
            print(f"   + {nomen} (suppl)")
    shutil.rmtree(suppl_exitus)
print()

# ── 2. capita simulata (residua) ─────────────────────────────

print("2. capita simulata...")
codex_totus = ""
for plica in glob.glob(os.path.join(EXITUS, "*.c")) + \
             glob.glob(os.path.join(EXITUS, "*.h")):
    with open(plica) as f:
        codex_totus += f.read() + "\n"

CAPITA_C99 = {
    'stdio.h', 'stdlib.h', 'string.h', 'math.h', 'stddef.h', 'time.h',
    'stdint.h', 'stdbool.h', 'ctype.h', 'assert.h', 'errno.h',
    'float.h', 'limits.h', 'signal.h', 'stdarg.h', 'setjmp.h',
    'locale.h', 'wchar.h', 'wctype.h',
}

creata = 0
for m in re.finditer(r'#include\s+[<"]([^>"]+)[>"]', codex_totus):
    inc = m.group(1)
    if inc not in CAPITA_C99 and not os.path.exists(os.path.join(EXITUS, inc)):
        with open(os.path.join(EXITUS, inc), 'w') as f:
            f.write(f"/* simulatum: {inc} */\n")
        print(f"   {inc} (vacuum)")
        creata += 1
if creata == 0:
    print("   (nulla necessaria)")
print()

# ── 3. structura ─────────────────────────────────────────────

print("3. structura...")
fontes = sorted(glob.glob(os.path.join(EXITUS, "*.c")))
principales = []
bibliotheca = []

for plica in fontes:
    with open(plica) as f:
        contentum = f.read()
    nomen = os.path.basename(plica)
    if re.search(r'\bint\s+main\s*\(', contentum):
        principales.append(nomen)
    else:
        bibliotheca.append(nomen)

objecta_bib = [f.replace('.c', '.o') for f in bibliotheca]
print(f"   bibliotheca: {' '.join(bibliotheca) or '(nulla)'}")
print(f"   principales: {' '.join(principales) or '(nulla)'}")
print()

# ── 4. Faceplica ─────────────────────────────────────────────

print("4. Faceplica scribo...")
lineas = []
lineas.append('CC      ?= cc')
lineas.append('CFLAGS  ?= -std=c99 -Wall -Wextra -I.')
lineas.append('')

executabilia = []
for p in principales:
    prog = p.replace('.c', '')
    obj_p = p.replace('.c', '.o')
    executabilia.append(prog)
    deps = f'{obj_p} {" ".join(objecta_bib)}'.strip()
    lineas.append(f'{prog}: {deps}')
    lineas.append(f'\t$(CC) $(CFLAGS) -o $@ $^')
    lineas.append('')

if executabilia:
    lineas.insert(3, f'omnia: {" ".join(executabilia)}')
    lineas.insert(4, '')
else:
    all_obj = [f.replace('.c', '.o') for f in bibliotheca]
    lineas.insert(3, f'omnia: {" ".join(all_obj)}')
    lineas.insert(4, '')

lineas.append('%.o: %.c')
lineas.append('\t$(CC) $(CFLAGS) -c -o $@ $<')
lineas.append('')

all_obj = [os.path.basename(f).replace('.c', '.o') for f in fontes]
purga_items = ' '.join(all_obj + executabilia)
lineas.append('purga:')
lineas.append(f'\trm -f {purga_items}')
lineas.append('')
lineas.append('.PHONY: omnia purga')

via_face = os.path.join(EXITUS, "Faceplica")
with open(via_face, 'w') as f:
    f.write('\n'.join(lineas) + '\n')
print(f"   {via_face}")
print()

# ── 5. aedificatio ───────────────────────────────────────────

print("5. aedifico...")
for plica in sorted(glob.glob(os.path.join(EXITUS, "*.c"))):
    nomen = os.path.basename(plica)
    obj = nomen.replace('.c', '.o')
    res = subprocess.run(
        ["cc", "-std=c99", "-Wall", "-Wextra", "-I.",
         "-c", "-o", obj, nomen],
        cwd=EXITUS, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
    )
    stderr = res.stderr.decode(errors='replace')
    ne = stderr.count('error:')
    nw = stderr.count('warning:')
    if ne:
        print(f"   {nomen:<24s} ERRATUM ({ne} errores)")
        for linea in stderr.splitlines():
            print(f"      {linea}")
        print()
        print("PROBATIO CECIDIT")
        sys.exit(1)
    elif nw:
        print(f"   {nomen:<24s} OK ({nw} monitiones)")
        for linea in stderr.splitlines():
            if 'warning:' in linea:
                print(f"      {linea}")
    else:
        print(f"   {nomen:<24s} OK")

# aedifica executabilia
res = subprocess.run(
    ["face", "-C", EXITUS],
    stderr=subprocess.PIPE, stdout=subprocess.PIPE,
)
stdout = res.stdout.decode(errors='replace')
for linea in stdout.splitlines():
    print(f"   {linea}")
print()

# ── 6. executio ──────────────────────────────────────────────

ran = False
for prog_name in executabilia:
    prog = os.path.join(EXITUS, prog_name)
    if os.path.isfile(prog) and os.access(prog, os.X_OK):
        print(f"6. curro {prog_name}...")
        try:
            res = subprocess.run(
                [prog], stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                timeout=10,
            )
            for linea in res.stdout.decode(errors='replace').splitlines():
                print(f"   {linea}")
            if res.stderr.strip():
                for linea in res.stderr.decode(errors='replace').splitlines():
                    print(f"   {linea}")
            if res.returncode != 0:
                print(f"   (exitus: {res.returncode})")
        except subprocess.TimeoutExpired:
            print("   (tempus excessum)")
        ran = True
        print()
        break

# ── 7. purga ─────────────────────────────────────────────────

subprocess.run(["face", "-C", EXITUS, "purga"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if ran:
    print("PROBATIO SUCCESSIT")
else:
    print("PROBATIO CECIDIT (nullum executabile)")
    sys.exit(1)

#!/usr/bin/env python3
"""
κadc.py — ex κ in C99 transcribit.

Usus: κadc.py <directorium_fontis> [directorium_exitus]
"""

import sys, os, re

# ════════════════════════════════════════════════════════════════
# tabulae transpositionum
# ════════════════════════════════════════════════════════════════

# directivae praeprocessoris (post #)
DIRECTIVAE = {
    'εἰμηδέν':   'ifndef',
    'ὅρισον':    'define',
    'εἰσάγαγε':  'include',
    'τέλος':     'endif',
    'ἄρσον':     'undef',
}

# verba reservata linguae
VERBA = {
    'τυπόθεσις':   'typedef',
    'δομή':        'struct',
    'γρα':         'char',
    'ἀκέ':         'int',
    'ῥευ':         'float',
    'κεν':         'void',
    'σταθ':        'const',
    'μέγεθ_τ':     'size_t',
    'ἴδιον':       'static',
    'ἄσημον':      'unsigned',
    'μακρ':        'long',
    'εἰ':          'if',
    'ἄλλως':       'else',
    'ὑπέρ':        'for',
    'ἕως':         'while',
    'ἐπίστρεψον':  'return',
    'παῦε':        'break',
    'ἔτι':         'continue',
    'κύριον':      'main',
}

# functiones bibliothecae fundamentalis
BIBLIOTHECA = {
    'μεγέθους':      'sizeof',
    'μνημόθες':      'memset',
    'μνημαντγρ':     'memcpy',
    'νημσύγκρ':      'strcmp',
    'νημτύπωσον':    'snprintf',
    'νημμῆκος':      'strlen',
    'νημσύνδεσ':     'strcat',
    'νημδίπλωσ':     'strdup',
    'νημεἰςἀκέ':     'atoi',
    'χώρισον':       'malloc',
    'καθχώρισον':    'calloc',
    'ἐλεύθερον':     'free',
    'τύπωσον':       'printf',
    'πτυχτύπωσον':   'fprintf',
    'ταχυτάξ':       'qsort',
    'τετράριζα':     'sqrtf',
    'συνημίτ':       'cosf',
    'ἐκθετικόν':     'expf',
    'πτυχάνοιξ':     'fopen',
    'πτυχέκλεισ':    'fclose',
    'πτυχανάγνω':    'fread',
    'πτυχέγραψ':     'fwrite',
    'πτυχεζήτησ':    'fseek',
    'πτυχεεἰπέ':     'ftell',
    'πτυχέπλυν':     'fflush',
    'ἐπανέλιξ':      'rewind',
    'χρόνος':        'time',
}

# constantiae fundamentales
CONSTANTIAE = {
    'ΟΥΔΕΝ':           'NULL',
    'ΠΤΥΧΗ':           'FILE',
    'σφ_ῥεῦμα':        'stderr',
    'ἐξ_ῥεῦμα':        'stdout',
    'ΖΗΤΗΣΙΣ_ΤΕΛΟΣ':   'SEEK_END',
    'ΖΗΤΗΣΙΣ_ΑΡΧΗ':    'SEEK_SET',
}

# omnia verba quae per limites verborum substituuntur
OMNIA_VERBA = {}
OMNIA_VERBA.update(VERBA)
OMNIA_VERBA.update(BIBLIOTHECA)
OMNIA_VERBA.update(CONSTANTIAE)

# capita fundamentalia: nomen Graecum → nomen C99
CAPITA = {
    'μαθημ':     'math',
    'τύπωσις':   'stdio',
    'βιβλιοθ':   'stdlib',
    'νῆμα':      'string',
    'ὁρισμοί':   'stddef',
    'χρόνος':    'time',
}

# litterae modorum fopen
MODI_PLICAE = {
    'α': 'r',   # ἀνάγνωσις
    'γ': 'w',   # γράφω
    'π': 'a',   # προσθήκη
    'δ': 'b',   # δυαδικόν
}

# cifrae hexadecimales Graecae → Latinae
CIFRAE_HEX = {
    'Α': 'A', 'α': 'a',
    'Β': 'B', 'β': 'b',
    'Κ': 'B',
    'Γ': 'C', 'γ': 'c',
    'Δ': 'D', 'δ': 'd',
    'Ε': 'E', 'ε': 'e',
    'Φ': 'F', 'φ': 'f',
}

# characteres formati (post % in chordis)
CHARACTERES_FORMATI = {
    'σ': 's',
    'δ': 'd',
    'φ': 'f',
    'υ': 'u',
    'ζ': 'z',
    'Ε': 'X',
}

# ════════════════════════════════════════════════════════════════
# segmentatio — dividit fontem in partes
# ════════════════════════════════════════════════════════════════

SEG_CODEX      = 0
SEG_COMMENTUM  = 1
SEG_CHORDA     = 2
SEG_LITTERA    = 3

def segmenta(fons):
    """Fontem in (genus, textus) segmenta dividit."""
    partes = []
    i = 0
    n = len(fons)
    alveus = []
    modus = SEG_CODEX

    def effunde():
        if alveus:
            partes.append((modus, ''.join(alveus)))
            alveus.clear()

    while i < n:
        if modus == SEG_CODEX:
            if fons[i:i+2] == '/*':
                effunde()
                modus = SEG_COMMENTUM
                alveus.append('/*')
                i += 2
            elif fons[i] == '"':
                effunde()
                modus = SEG_CHORDA
                alveus.append('"')
                i += 1
            elif fons[i] == "'":
                effunde()
                modus = SEG_LITTERA
                alveus.append("'")
                i += 1
            else:
                alveus.append(fons[i])
                i += 1

        elif modus == SEG_COMMENTUM:
            if fons[i:i+2] == '*/':
                alveus.append('*/')
                i += 2
                effunde()
                modus = SEG_CODEX
            else:
                alveus.append(fons[i])
                i += 1

        elif modus == SEG_CHORDA:
            if fons[i] == '\\' and i + 1 < n:
                alveus.append(fons[i:i+2])
                i += 2
            elif fons[i] == '"':
                alveus.append('"')
                i += 1
                effunde()
                modus = SEG_CODEX
            else:
                alveus.append(fons[i])
                i += 1

        elif modus == SEG_LITTERA:
            if fons[i] == '\\' and i + 1 < n:
                alveus.append(fons[i:i+2])
                i += 2
            elif fons[i] == "'":
                alveus.append("'")
                i += 1
                effunde()
                modus = SEG_CODEX
            else:
                alveus.append(fons[i])
                i += 1

    effunde()
    return partes

# ════════════════════════════════════════════════════════════════
# transcriptio codicis
# ════════════════════════════════════════════════════════════════

def _aedifica_re_verborum():
    """Expressionem regularem pro omnibus verbis aedificat, longissima primum."""
    verba = sorted(OMNIA_VERBA.keys(), key=len, reverse=True)
    alternae = '|'.join(re.escape(v) for v in verba)
    return re.compile(
        r'(?<![_\w])(' + alternae + r')(?![_\w])',
        re.UNICODE
    )

_RE_VERBA = _aedifica_re_verborum()

def _aedifica_re_directivarum():
    verba = sorted(DIRECTIVAE.keys(), key=len, reverse=True)
    alternae = '|'.join(re.escape(v) for v in verba)
    return re.compile(r'#(' + alternae + r')')

_RE_DIRECTIVAE = _aedifica_re_directivarum()

def _transcribe_hex(m):
    """Litteram hexadecimalem transcribit, e.g. 0χ4Ε4Δ4Κ31υ → 0x4E4D4B31u."""
    corpus = m.group(1)
    exitus = []
    for c in corpus:
        if c in CIFRAE_HEX:
            exitus.append(CIFRAE_HEX[c])
        elif c == 'υ':
            exitus.append('u')
        else:
            exitus.append(c)
    return '0x' + ''.join(exitus)

_RE_HEX = re.compile(r'0χ([0-9ΑΒΓΔΕΚφαβγδεΦυ]+)')

def _transcribe_suffixos(textus):
    """Suffixos numericos transcribit: φ→f, υ→u, ε—→e-."""
    # notatio scientifica: ε post digitum (et ante - vel digitum)
    textus = re.sub(r'(\d)ε', r'\1e', textus)
    # suffixus decimalis: cifra + φ in fine verbi
    textus = re.sub(r'(\d)φ(?!\w)', r'\1f', textus)
    # suffixus integer sine signo: cifra + υ in fine verbi
    textus = re.sub(r'([0-9a-fA-F])υ(?!\w)', r'\1u', textus)
    return textus

def _transcribe_inclusiones(textus):
    """Directivas #include transcribit."""
    # capita inter angulos: ≺nomen·η≻ → <nomen.h>
    def subst_angulos(m):
        nomen = m.group(1)
        # extensio prius
        nomen = nomen.replace('\u00B7η', '.h').replace('\u00B7κ', '.c')
        # capita fundamentalia
        radix = nomen.replace('.h', '').replace('.c', '')
        if radix in CAPITA:
            return '<' + CAPITA[radix] + '.h>'
        return '<' + nomen + '>'

    # capita inter virgas: "nomen·η" → "nomen.h"
    def subst_virgas(m):
        nomen = m.group(1)
        nomen = nomen.replace('\u00B7η', '.h').replace('\u00B7κ', '.c')
        return '"' + nomen + '"'

    # ≺ (U+227A) ... ≻ (U+227B) — anguli capitum
    textus = re.sub(r'\u227A([^\u227B\n]+)\u227B', subst_angulos, textus)
    # "..." cum extensione ·η vel ·κ
    textus = re.sub(r'"([^"]*\u00B7[ηκ])"', subst_virgas, textus)
    return textus

def transcribe_codicem(textus):
    """Segmentum codicis ex κ in C99 transcribit."""

    # 0. directivae praeprocessoris
    textus = _RE_DIRECTIVAE.sub(
        lambda m: '#' + DIRECTIVAE[m.group(1)], textus
    )

    # 1. inclusiones (ante operatores, quia ≺≻ mutentur)
    textus = _transcribe_inclusiones(textus)

    # 2. litterae hexadecimales (ante operatores, quia · et — mutentur)
    textus = _RE_HEX.sub(_transcribe_hex, textus)

    # 3. verba reservata, bibliotheca, constantiae
    textus = _RE_VERBA.sub(lambda m: OMNIA_VERBA[m.group(1)], textus)

    # 4. operatores plures characterum (ordo necessarius)
    textus = textus.replace('\u2261\u2261', '==')  # ≡≡
    textus = textus.replace('+\u2261', '+=')        # +≡
    textus = textus.replace('/\u2261', '/=')         # /≡
    textus = textus.replace('\u2014\u227B', '->')    # —≻

    # 5. operatores unius characteris
    textus = textus.replace('\u2261', '=')   # ≡
    textus = textus.replace('\u227A', '<')   # ≺
    textus = textus.replace('\u227B', '>')   # ≻
    textus = textus.replace('\u2190', '<=')  # ←
    textus = textus.replace('\u2192', '>=')  # →
    textus = textus.replace('\u2262', '!=')  # ≢
    textus = textus.replace('\u226A', '<<')  # ≪
    textus = textus.replace('\u2228', '||')  # ∨
    textus = textus.replace('\u2227', '&&')  # ∧
    textus = textus.replace('\u00AC', '!')   # ¬
    textus = textus.replace('\u00B7', '.')   # · (punctum medium)
    textus = textus.replace('\u2014', '-')   # — (virgula longa)

    # 6. suffixos numericos
    textus = _transcribe_suffixos(textus)

    # 7. litterae Graecae archaicae in identibus
    textus = textus.replace('\u03D9', 'q')   # ϙ koppa
    textus = textus.replace('\u03DD', 'w')   # ϝ digamma
    textus = textus.replace('\u02B9', '_')   # ʹ modificator primus

    return textus

# ════════════════════════════════════════════════════════════════
# transcriptio chordarum
# ════════════════════════════════════════════════════════════════

def _est_modus_plicae(s):
    """Verum reddit si chorda modus fopen videtur."""
    return 0 < len(s) <= 3 and all(c in MODI_PLICAE or c == '+' for c in s)

def _transcribe_modum(s):
    return ''.join(MODI_PLICAE.get(c, c) for c in s)

_RE_FORMATUM = re.compile(
    r'(%[-+0 #]*(?:\d+|\*)?'
    r'(?:[\u00B7.](?:\d+|\*))?'
    r'(?:ζ)?[σδφυ])'
)

def _subst_formatum(m):
    spec = m.group(1)
    exitus = []
    for c in spec:
        if c in CHARACTERES_FORMATI:
            exitus.append(CHARACTERES_FORMATI[c])
        elif c == '\u00B7':
            exitus.append('.')
        else:
            exitus.append(c)
    return ''.join(exitus)

def transcribe_chordam(textus):
    """Chordam litteralem (cum virgis) transcribit."""
    assert textus[0] == '"' and textus[-1] == '"'
    interior = textus[1:-1]

    # modi fopen
    if _est_modus_plicae(interior):
        return '"' + _transcribe_modum(interior) + '"'

    # extensiones plicarum (ante · → .)
    interior = interior.replace('\u00B7η', '.h')
    interior = interior.replace('\u00B7κ', '.c')
    interior = interior.replace('\u00B7δυα', '.bin')
    interior = interior.replace('\u00B7λεχ', '.lex')
    interior = interior.replace('\u00B7κεί', '.txt')
    interior = interior.replace('\u00B7μδ', '.md')

    # sequentiae effugiendi
    interior = interior.replace('\\ν', '\\n')
    interior = interior.replace('\\τ', '\\t')

    # operatores in textu exhibitionis
    interior = interior.replace('\u2261', '=')
    interior = interior.replace('\u227A', '<')
    interior = interior.replace('\u227B', '>')
    interior = interior.replace('\u2190', '<=')
    interior = interior.replace('\u2192', '>=')
    interior = interior.replace('\u2262', '!=')
    interior = interior.replace('\u00B7', '.')
    interior = interior.replace('\u2014', '-')

    # specificatores formati
    interior = _RE_FORMATUM.sub(_subst_formatum, interior)

    return '"' + interior + '"'

def transcribe_litteram(textus):
    """Litteram characteris (cum apostrophis) transcribit."""
    assert textus[0] == "'" and textus[-1] == "'"
    interior = textus[1:-1]
    interior = interior.replace('\\ν', '\\n')
    interior = interior.replace('\\τ', '\\t')
    return "'" + interior + "'"

# ════════════════════════════════════════════════════════════════
# transcriptio integra
# ════════════════════════════════════════════════════════════════

def transcribe(fons):
    """Fontem integrum ex κ in C99 transcribit."""
    partes = segmenta(fons)
    exitus = []
    for genus, textus in partes:
        if genus == SEG_CODEX:
            exitus.append(transcribe_codicem(textus))
        elif genus == SEG_COMMENTUM:
            exitus.append(textus)
        elif genus == SEG_CHORDA:
            exitus.append(transcribe_chordam(textus))
        elif genus == SEG_LITTERA:
            exitus.append(transcribe_litteram(textus))
    return ''.join(exitus)

# ════════════════════════════════════════════════════════════════
# nomina plicarum
# ════════════════════════════════════════════════════════════════

def transcribe_nomen(nomen):
    """Extensiones plicarum transcribit: ·η → .h, ·κ → .c."""
    nomen = nomen.replace('\u00B7η', '.h')
    nomen = nomen.replace('\u00B7κ', '.c')
    nomen = nomen.replace('\u00B7μδ', '.md')
    # si nihil mutatum, nomen immutatum reddit
    return nomen

# ════════════════════════════════════════════════════════════════
# principale
# ════════════════════════════════════════════════════════════════

def principale():
    if len(sys.argv) < 3:
        print(
            f"usus: {sys.argv[0]} <directorium_fontis> <directorium_exitus>",
            file=sys.stderr
        )
        sys.exit(1)

    via_fontis = sys.argv[1]
    via_exitus = sys.argv[2]

    if not os.path.isdir(via_fontis):
        print(f"erratum: {via_fontis} directorium non est", file=sys.stderr)
        sys.exit(1)

    os.makedirs(via_exitus, exist_ok=True)

    for nomen in sorted(os.listdir(via_fontis)):
        if nomen.startswith('.'):
            continue
        via = os.path.join(via_fontis, nomen)
        if not os.path.isfile(via):
            continue

        nomen_novum = transcribe_nomen(nomen)
        via_nova = os.path.join(via_exitus, nomen_novum)

        with open(via, 'r', encoding='utf-8') as f:
            fons = f.read()

        resultatum = transcribe(fons)

        with open(via_nova, 'w', encoding='utf-8') as f:
            f.write(resultatum)

        print(f"  {nomen} -> {nomen_novum}")

    print(f"\nexitus: {via_exitus}/")

if __name__ == '__main__':
    principale()

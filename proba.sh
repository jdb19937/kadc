#!/bin/sh
#
# proba.sh — probat transcriptionem ex κ in C99.
#
# Currit κadc.py, creat capita vacua simulata
# pro dependentiis externis, deinde cpp in omnibus plicis probat.

set -e

FONS="proba.κ"
EXITUS="proba.κ.c99"
PROBA_DIR="${EXITUS}/_proba"

# --- transcribe ---
echo "1. transcriptio..."
python3 κadc.py "$FONS" "$EXITUS"
echo ""

# --- capita simulata pro dependentiis externis ---
echo "2. capita simulata creo..."
mkdir -p "$PROBA_DIR"
for caput in φάντασμα.h χορηγός_π.h ἐργαλεῖα.h; do
    echo "/* simulatum */" > "${PROBA_DIR}/${caput}"
    echo "   ${caput}"
done
echo ""

# --- proba cpp ---
echo "3. probo cpp..."
errores=0
recta=0
for plica in "${EXITUS}"/*.h "${EXITUS}"/*.c; do
    nomen=$(basename "$plica")
    if cc -std=c99 -E -I"${EXITUS}" -I"${PROBA_DIR}" "$plica" > /dev/null 2>&1; then
        printf "   %-24s OK\n" "$nomen"
        recta=$((recta + 1))
    else
        printf "   %-24s ERRATUM\n" "$nomen"
        cc -std=c99 -E -I"${EXITUS}" -I"${PROBA_DIR}" "$plica" 2>&1 >/dev/null | head -3
        errores=$((errores + 1))
    fi
done
echo ""

# --- purga ---
rm -rf "$PROBA_DIR"

# --- summarium ---
summa=$((recta + errores))
echo "summarium: ${recta}/${summa} rectae"
if [ "$errores" -gt 0 ]; then
    echo "PROBATIO CECIDIT"
    exit 1
else
    echo "PROBATIO SUCCESSIT"
    exit 0
fi

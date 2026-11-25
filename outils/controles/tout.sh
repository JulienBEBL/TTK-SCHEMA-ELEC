#!/bin/sh
# v39 (24/11) : génère un essai et lance TOUS les contrôles. Usage : sh outils/controles/tout.sh <sortie.xrs> [JJ/MM/AAAA]
# Attendu : 0 problème, 0 erreur (28 attentions connues), total 0, numéros 0 problème, cadres 0, textes 0, D11 0, 0 doublon, symboles 0 (v41).
R="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$1"; C="$R/outils/controles"
cd "$R/outils" || exit 1
export PYTHONIOENCODING=utf-8 TTK_LIB='C:\Users\Public\Documents\Elec-CAO\sym_electrotech' TTK_DATE="${2:-$(date +%d/%m/%Y)}"
python ttk_schema.py "$OUT" | tail -4
echo "=== verifier"; python xrs_tool.py verifier "$OUT" | sed -n 3p
echo "=== chevauchements (élargi)"; python xrs_chevauchements.py "$OUT" | tail -15
echo "=== numeros"; python xrs_numeros.py "$OUT" 10,11,12,13,20,21,30,31,32,40,41,42,43,50,60,61,62,63,64 | head -5
echo "=== cadres"; python "$C/cadres.py" "$OUT" | tail -3
echo "=== textes hors 10-69"; python "$C/textes.py" "$OUT" 01,02,03,70,71,72,73,80,85,90,91,92 | tail -3
echo "=== 24 V / 0 V"; python "$C/d11.py" "$OUT" | tail -1
echo "=== bornes"; python "$C/bornes.py" "$OUT" | head -4
echo "=== symboles CUSTOM"; python "$C/symboles.py" | tail -3

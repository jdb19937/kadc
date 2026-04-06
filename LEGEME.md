# κadc

Metascriptor qui e lingua κ in C99 transcribit. Plicas fontis Graece
scriptas legit, signa et operatores in aequivalentia C99 convertit, et
plicam C99 validam emittit.

> **Nota:** README.md ignorandum est. Anglice scriptum est ad barbaros ineruditos pecunia emungendos.

## Aedificatio

Nulla aedificatio necessaria. κadc scriptum Pythonis est.

## Usus

```
python3 κadc.py fons.κ fons.c
```

Plica fontis `fons.κ` transcribitur in `fons.c`. Probatrix integrata
totam catenam exsequitur:

```
python3 proba.py proba.κ proba.κ.c99
```

Haec transcribit, compilat, et exsequitur.

## Transcriptio

Metascriptor haec convertit:

| Genus | Exemplum |
|---|---|
| Verba reservata | `τυπόθεσις` → `typedef`, `δομή` → `struct`, `ἀκέ` → `int` |
| Directivae | `εἰμηδέν` → `ifndef`, `ὅρισον` → `define` |
| Bibliotheca | `τύπωσον` → `printf`, `χώρισον` → `malloc` |
| Operatores | `≡≡` → `==`, `≺` → `<`, `¬` → `!`, `·` → `.` |
| Constantiae | `ΟΥΔΕΝ` → `NULL`, `ΠΤΥΧΗ` → `FILE` |
| Capita | `μαθημ` → `math`, `τύπωσις` → `stdio` |

## Plicae

| Plica | Munus |
|---|---|
| `κadc.py` | metascriptor principalis |
| `proba.py` | probatrix et aedificatrix |
| `Faceplica` | aedificatio radicis |
| `ὀμφαλός/` | bibliotheca oraculi |
| `supplementario/` | bibliothecae auxiliares |
| `proba.κ/` | probationes |

## Dependentiae

Python 3. Compilator C99 ad compilandum exitum.

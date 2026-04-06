# κadc

A source-to-source transpiler that converts κ language into clean, portable C99. Every keyword, every operator, every standard library call has a precise mapping — the transpiler reads κ source files, tokenizes them with full awareness of strings, comments, and character literals, and emits valid C99 that compiles with any standards-compliant compiler. No intermediate representations, no bloated ASTs, no dependencies beyond Python 3. One script, one pass, correct output.

## How It Works

The transpiler operates on a complete translation table — reserved words, preprocessor directives, library functions, operators, format specifiers, even hexadecimal digit names all have defined mappings. The tokenizer splits source into segments (code, strings, comments, character literals) and applies the appropriate transformation to each. Operators like `≡≡`, `≺`, `≻`, `¬`, `∨`, `∧` become their C99 equivalents. Dot access, arrow dereference, assignment — every syntactic element is handled.

This is not a toy or a proof of concept. The transpiler builds a complete neural network inference library with tens of thousands of lines of source — matrix operations, tokenizers, training loops, softmax sampling, file I/O — all transpiled from κ to C99 and compiled without warnings.

## Getting Started

Transpile a single file:

```bash
python3 κadc.py source.κ output.c
```

Build and run a full project with the integrated test harness:

```bash
python3 proba.py proba.κ proba.κ.c99
```

The harness transpiles every source file, generates stub headers for missing includes, detects entry points and library functions, produces a Makefile, compiles everything with `cc -std=c99`, and runs the result. One command from source to execution.

## The Oracle Library

The `ὀμφαλός/` directory contains a complete neural network inference engine — the crown jewel of the κ ecosystem. Transformer architecture, BPE tokenization, weight loading, text generation with temperature and top-k sampling. Forty thousand lines of κ source that transpile to production-grade C99 with zero external dependencies. No BLAS, no LAPACK, no framework. Pure computation from first principles.

## License

Free. Public domain. Use however you like.

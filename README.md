# music-arithmetic
Language for describing music compositions in exact frequencies

## Dependencies
- python (developed and tested with python 3.4.0)
- music21
- pyparsing

## Examples
This is an example of music arithmetic code.
As you see you can just write notes from the equally tempered scale by the usual names.
```
(
    c (e, g) (f, a) (e, g) (d, f) (c, e) (g/2, (d d) | .5) c
)
```
The same piece but in pure notation is like this.
```
261.6 * (
    1 (5/4, 3/2) (4/3, 5/3) (5/4, 3/2) (9/8, 4/3) (1, 5/4) (3/4, (9/8 9/8) | .5) 1
)
```

## Language description

Numbers can be constructed by the usual expressions.
Numbers are frequencies by default.
A duration parameter can be specified after a `|` symbol, which has a low precedence
Parenthesis are not needed for tuples anymore, so they can replace curly brackets.

So we have the rationals with the usual operators
`*` and `/` (precedence 4)
extended with frequency constants and the operators
`|` (duration operator, precedence 3)
` ` (serial operator, precedence 2)
`,` (parallel operator, precedence 1)

The advantage of choosing this precedence order is that we can write multiple voices easily
```
(
    c g a g f e d   c,
    c e f e d c g/2 c
)
```

An equivalent way of writing this piece in a chord-by-chord fashion could be as follows.
```
(
    c (e, g) (f, a) (e, g) (d, f) (c, e) (g/2, (d d) | .5) c
)
```

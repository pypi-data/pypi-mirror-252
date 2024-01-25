**Install**
```
pip install combocmd
```

**Examples**

```
combocmd --strings hello world
hello,hello;hello,world;world,world

combocmd --strings hello world --AsepB " " --PsepP ","
hello hello,hello world,world world
```

```
combocmd --strings hello world --cmd "echo {combocmdA} {combocmdB}"
world world
world hello
hello world
hello hello
```

```
combocmd --strings 1 2 --cmdAB "echo cmdAB x={combocmdA} y={combocmdB}" --cmdBA "echo cmdBA x={combocmdA} y={combocmdB}" --AisB cmdAB
cmdAB x=1 y=1
cmdAB x=1 y=2
cmdBA x=2 y=1
cmdAB x=2 y=2
```

```
combocmd --strings 1 2 --cmd "echo {a}{a}{a}{b}{b}{b}" --combocmdA {a} --combocmdB {b}
111111
222111
111222
222222
```

```
mkdir -p demo; combocmd --strings 1 2 --cmd "echo '{A}{B}' > demo/{A}{B}" --combocmdA {A} --combocmdB {B}; combocmd --strings demo/* --cmd "echo {combocmdA} {combocmdB}"
demo/21 demo/21
demo/22 demo/21
demo/22 demo/12
demo/12 demo/21
demo/11 demo/22
demo/22 demo/22
demo/11 demo/12
demo/21 demo/11
demo/22 demo/11
demo/12 demo/12
demo/12 demo/22
demo/21 demo/12
demo/21 demo/22
demo/11 demo/11
demo/11 demo/21
demo/12 demo/11
```

```
combocmd --strings 1 2 --cmdAB "echo '{A}{B}'" --cmdBA "echo '{A}{B}'" --combocmdA {A} --combocmdB {B}
12
11
22
21
combocmd --strings 1 2 --cmdAB "echo '{A}{B}'" --cmdBA "echo '{A}{B}'" --combocmdA {A} --combocmdB {B} --runRepeats
11
11
12
21
22
22
```

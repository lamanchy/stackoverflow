# StackOverflow GDD
## název hry
## autory hry
## popis cílové skupiny
## chtěný herní zážitek
## počet hráčů
## délka herní instance
## herní pravidla
## mechaniky
## smyčky
## identifikované problémy/neznámé návrhu hry

### original text:

A script for testing possible gameplay of card game with the same name.

The basic version:

+ at the beginning of each game, each players get a five cards of programs, and one output value is randomly selected form 
the deck of values

+ at the beginning of each round an input value is randomly selected from the deck of values. Then, each player tries
to select program from his has, such that it transforms input value as close to output value as possible.

+ recursive programs can throw exception "Stack Overflow"

I have just a few more ideas which I want to write down somewhere. 

There should be different types of values and programs by difficulty.

+ green values 1 to 20, natural numbers
+ green programs - simple ones, the output should be again inside green values, operations should be simple
+ yellow values -20 to +100, whole
+ yellow programs - more difficult one, but still fairly simple, no type errors, no recursive, first mega simple
programs (for i in range(3): x += 2)
+ red values +- 200, simple rational numbers
+ red programs - High school math (quadratic, exponential, sin, cos, sqrt, log, fibonaci), simple programs, 
type errors, recursive errors etc. 
+ black something awful, pi, e, difficult programs, complex numbers?

It is important, that we make all combinations playable and balanced. So only "green" game makes sense, but also 
"green + yellow + red"

Which means, that the results should be distributed more less evenly. It wouldn't make sense if most of the combinations
would yield... 1. 
 
Also, when yellow has input values of -20 to 100, output values has to be in that range, because....

1. The most interesting idea is, that you could "stack" programs, each round you could select more than one program,
so the result would be program2(program1(input)). That way, it could be even more about skill, but there would be also
bigger risk, if you would fail, you would loose all those programs. If you wouldn't fail, you would get as many new
programs as you used. 
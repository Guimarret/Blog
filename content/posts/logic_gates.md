---
title: "Logic gates"
date: 2024-01-17T15:04:23-03:00
draft: false
---


 
Using the transistor base in here: [transistor]( {{< ref "/posts/transistor.md" >}}). 

I'm gonna talk about logic gates and some basic possibilities like adders, subtractors, multipliers, and dividers. The main idea in these basic posts is to trace the way to assembly instructions and so on.

These logic gates are the lowest level we can reach in hardware processing. Obviously, these instructions alone don't create anything really meaningful, but the correct combination can create computers and processing machines of any type (except quantum computers, but we're not gonna talk about them today)  

So logic gates are simply a transistor sequence that creates properties (AND, OR, NAND, NOR, XOR and XNOR)

- The X in the name means "exclusively", like in the OR gate that usually would accept 1|1, but with X it'll only accept the 1|0 (the order of the factors doesn't matter) 
- The N means the opposite of the original logic gate output.
- At the bottom of the image there are some "grounds" that I recommend looking into in <a href="https://www.build-electronic-circuits.com/what-is-ground/" target="_blank"> this </a> explanation before continuing 
- The +6V is the place where electricity comes from, and the out is where it comes out if the logic gate sustains the correct input (the input is just the electrical presence in A or B that'll activate the transistor)

Transistor level approach:
- AND (The first input and the second simultaneously):
    {{< figure src="/img/logic_gates/and.webp"
       alt="AND gate built from transistors at the transistor level"
       caption="Figure 1 - AND gate (transistor level)"
       align="center" >}}
- OR (The first input, the second, or both):
    {{< figure src="/img/logic_gates/or.webp"
       alt="OR gate built from transistors at the transistor level"
       caption="Figure 2 - OR gate (transistor level)"
       align="center" >}}
- NAND (The first input, the second, or none of them):
    {{< figure src="/img/logic_gates/nand.webp"
       alt="NAND gate built from transistors at the transistor level"
       caption="Figure 3 - NAND gate (transistor level)"
       align="center" >}}
- NOR (Both of them off):
    {{< figure src="/img/logic_gates/nor.webp"
       alt="NOR gate built from transistors at the transistor level"
       caption="Figure 4 - NOR gate (transistor level)"
       align="center" >}}

Truth tables:
{{< figure src="/img/logic_gates/logic_gates.webp"
   alt="Truth tables for the AND, OR, NAND, NOR, XOR and XNOR logic gates"
   caption="Figure 5 - Logic gate truth tables"
   align="center" >}}

I didn't put XOR and XNOR transistor-level images because they use the other basic gates and i think it'll confuse more than help right now.

Now you might be thinking something like:

-"Why would I even have to know this"

And I tell you that this is the base of any normal computer (the quantum computer is the only different one that I can think of right now, but we're not gonna talk about them today)

Now I'm gonna take a more practical approach with something more easily understandable, the *adder*:

## Adder

- If you need some basic idea help in binary mathematics this
<a href="https://byjus.com/maths/binary-operation/" target="_blank"> site </a> can help.

The adders use this logic gate setup (I'm gonna start using these images with the minimal representation of the logic gates, because it would become bothersome to use so much space with logic gates at transistor level):
{{< figure src="/img/logic_gates/adder.webp"
   alt="Full adder built from the minimal representation of logic gates"
   caption="Figure 6 - Full adder built from logic gates"
   align="center" >}}

The adder receives 3 inputs, the binary of the first number, the second, and the "carry-in" (cin), but if it's the first comparison the cin is ignored, because the carry-in is the carried number from the last operation, aka the COUT that appears at the end of the circuit. So, for a better visualization, this is the truth table:
{{< figure src="/img/logic_gates/adder_truth_table.webp"
   alt="Truth table of the full adder with inputs A, B, carry-in and outputs S and carry-out"
   caption="Figure 7 - Adder truth table"
   align="center" >}}

So, if we have 2 numbers, 1001 and 1000, the adder circuit will compare the far right number from both. In this case it'll be 1 and 0, resulting in S = 1 and Cout = 0, creating the first bit of the output, which is S (1).
With this, we conclude that the adder will be run for every bit we have in our sum operation. In this situation we have 2 numbers of 4 bits, so the adder is gonna be run 4 times to get the full output/result.

If you want to see some real implementation of this adder there is this <a href="https://www.youtube.com/watch?v=X31B1pVow1o" target="_blank"> incredible video </a>

## Subtractor

The subtractor uses the same base as the adder, but we have to think about some problems, for example, the negative numbers.

If we think about it directly, the binary number technically groups just positive numbers, so the solution in this case is to use the MSB (most significant bit) as a sign for positive (0) or negative (1). So, if the number is positive like 1010 (10 in decimal) it would be 01010, and the opposite would be 11010 (-10 in decimal).

There are also two types of circuits for subtractors, the full subtractor and the half subtractor, and they apply to different situations. The "full" has 3 inputs, so we can carry the output of the last run and so on for more complex operations, while the half is useful just for operations with 2 bits.

The logic circuit of the subtractor (the full one, because it's more useful and interesting)

{{< figure src="/img/logic_gates/circuit_logic_subtractor.webp"
   alt="Full subtractor logic circuit built from logic gates"
   caption="Figure 8 - Full subtractor logic circuit"
   align="center" >}}

The truth table of the subtractor:

{{< figure src="/img/logic_gates/subtractor_full.webp"
   alt="Truth table of the full subtractor with inputs, borrow-in and the difference and borrow-out outputs"
   caption="Figure 9 - Full subtractor truth table"
   align="center" >}}

It's important to highlight that there are also other ways to construct the logic gates in the circuit to get the same truth table (AKA.. build a subtractor in this case), so the purpose of the circuits is to return the expected outputs from the truth tables.

If you want to go deeper into the subtractors I recommend this <a href="https://circuitdigest.com/tutorial/full-subtractor-circuit-and-its-construction" target="_blank"> site </a>, because there are many more details that I'm not going to cover here. After all, it would change the main topic.

## Multiplier

First things first, the multiplication consists of multiple comparisons between the multiplicand and the multiplier, and the number of runs of the circuit depends on the binary bit/byte "size".

For example:
{{< figure src="/img/logic_gates/binary_multiplication.webp"
   alt="Example of binary multiplication done as a series of shifts and additions"
   caption="Figure 10 - Binary multiplication example"
   attr="Source: circuitdigest.com"
   attrlink="https://circuitdigest.com/tutorial/full-subtractor-circuit-and-its-construction"
   align="center" >}}

The comparison is made between each bit in the number and then we make a sum to resolve the problem. Technically this is also the way we do multiplication in school, but there the number type is decimal instead of binary.

Then we reach the complex part, the logic circuit, because theoretically we could just sum the multiplicand with itself multiplier times, but nothing is that simple, and I'm gonna show just a basic resolution for now. Then, in other posts, we'll go deeper into how the ALU (part of the processor) actually makes operations...

So, continuing..
This is the logic circuit for a multiplier with 2-bit numbers

{{< figure src="/img/logic_gates/multiplier_logic_gate.webp"
   alt="Logic circuit of a 2-bit multiplier built from AND gates and adders"
   caption="Figure 11 - 2-bit multiplier logic circuit"
   align="center" >}}

And here is the truth table:

{{< figure src="/img/logic_gates/truth_table_multiplier.webp"
   alt="Truth table of the 2-bit multiplier with its inputs and product outputs"
   caption="Figure 12 - Multiplier truth table"
   align="center" >}}

For each bit we have in the multiplication we get 2 more columns in the truth table and 2 more inputs/outputs, so in this setup things don't scale very well, but it's possible anyway

## Divider

So, for the last one, we have the divider, which brings other implications like numbers from the rational field, and these numbers weren't possible until now because we hadn't gotten any number different from an integer. To solve this problem we could use floats (I'm gonna talk more about that in another post, but the technical name of the integer problem would be underflow)

The truth table is the simplest of all:
{{< figure src="/img/logic_gates/divider_truth_table.jpg"
   alt="Truth table of the binary divider, showing that division by zero is undefined"
   caption="Figure 13 - Divider truth table"
   align="center" >}}

Because if we think about it a little, we reach the conclusion that division by zero is meaningless

So, to keep the same schema as the multiplier, we are gonna use the 2-bit division:

{{< figure src="/img/logic_gates/two_bit_binary_division_circuit.webp"
   alt="2-bit binary division circuit built using only AND and XOR logic gates"
   caption="Figure 14 - 2-bit binary division circuit"
   align="center" >}}

It's interesting, by the way, that only AND and EX-OR logic gates are necessary..

The inputs are both 2-bit numbers and the output C's are the quotient, so if we expose the output somewhere we get the result (this is a simplified version of real-life usage, because for better approaches we probably would have to implement floating points and some other things, and I think that for now this is enough)


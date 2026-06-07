---
title: "Memory"
date: 2026-06-07T17:24:42-03:00
draft: True
math: true
---

So, this is a extensive and sometimes boring matter but also really important..

I'm going to start with latches and flip-flops and hoperfully end in ram/sram

## Latch/Flip-flops

For a fresh start and just for contextualization, Latch and Flip-flops are bi-stable memory elements, that means they can hold binary information depending on the state.

The difference between both is that the Latch don't have a clock and keeps the input and output at check constantly while the Flip-flops have progressive changes based on the impulses for example.

I'm gonna make this part progressive, starting from the base latch to Flip-flop, D type, JK type and finally T type

### S-R

![](/img/memory/sr-flip-flop-logic-diagram.jpg)
Uses two inputs, Set and Reset.

The idea in the SR type is to make one of the outputs, always be on (as long as there is current), and it works like a _switch_ that changes the output only if the buttom assigned to the other value is pressed. For example a button in a machine that is on of off, the S-R would be a good design base in learning purposes to be in the eletrical system to keep the machine on or off.

Looking at a bigger picture the circuit to store a 32 bits is needed 32 of these and get the output of Q for example to get the actual data (don't really matter if is the Q or $\bar{Q}$ here because the system is symmetrical so is just arbitrarily decided at the first time and later on is just replicated). If you need to erase the values you can just pass the reset signal for every latch.

(We can't let them both be 0 because it would return an invalid output and also if both are 1 it also means it's an error because at logic level it can't be possible)

>If it doesn't make sense watch this [video](https://www.youtube.com/watch?v=KM0DdEaY5sY)

### Flip-Flop version

Have 3 inputs:

![](/img/memory/sr-flip-flop-logic-circuit.jpg)

Just for a glance we can tell that the difference is the AND gates in the left and the Clk (clock), the logic addition have the purpose to accept signal only when the clock send the signal, so we can get a tempo of the execution creating a more solid utilization for real world situations.

### D

In the D type, we change the S input name to D with a reverse logic gate in and the R to E, creating a new output of truth table that it's impossible to have invalid states as before (1|1 and 0|0 input)

![](/img/memory/internal-logic-d-latch.webp)

And the E can be though as the clock for this version.

### JK

<!-- ⏺ Memory post roadmap

  0. The core trick — bistability
  Cross-coupled NOR/NAND gates: output fed back into input so the circuit "sticks" at a value. This is why a circuit can remember at
  all. One figure, short.

  1. SR latch
  Set/Reset, the forbidden 1|1 and 0|0 states. (you have this)

  2. Why a clock
  Quick motivation: coordinating many bits, avoiding races. Sets up everything clocked.

  3. Gated SR / gated D latch
  Add an enable line; D removes the invalid state. (you have D)

  ▎ Terminology fix: your current "Flip-Flop version" (clocked SR) is a gated latch — level-triggered, transparent while the clock
  ▎ is high. Not yet a flip-flop.

  4. Latch → flip-flop: edge triggering (master–slave)
  The transparency problem and how chaining two latches makes it update only on the clock edge. This is what actually separates
  latch from flip-flop.

  5. JK
  Repurpose SR's forbidden combo into a toggle.

  6. T
  JK with inputs tied → pure toggle → counters. Short, it's a special case.

  7. Registers
  Stack D flip-flops on a shared clock to hold a full word (your "32 of these" idea pays off here).

  8. Addressing — decoders & multiplexers
  How you select one register out of many. The bridge to addressable memory.

  9. SRAM cell & array
  6-transistor cell (a latch + access transistors), word lines / bit lines, the grid layout.

  10. DRAM (contrast)
  Capacitor + refresh: denser but volatile-by-leakage. SRAM vs DRAM trade-off.

  11. (optional close) Memory hierarchy
  Registers → cache (SRAM) → main memory (DRAM). Frames where each piece lives. -->
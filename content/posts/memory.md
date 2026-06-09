---
title: "Memory"
date: 2026-06-07T17:24:42-03:00
draft: True
math: true
---

So, this is an extensive and sometimes boring matter but also essential.

I'm going to start with latches and flip-flops and hopefully end in RAM/SRAM.

## Latch/Flip-flops

For a fresh start and just for contextualization, latches and flip-flops are bi-stable memory elements. That means they can hold binary information depending on the state.

The difference between both is that the latch doesn't have a clock and keeps the input and output in check constantly, while the flip-flops have progressive changes based on the impulses, for example.

I'm going to make this part progressive, starting from the base latch to flip-flop, D type, JK type, and finally T type.

### S-R Latch

{{< figure src="/img/memory/sr-flip-flop-logic-diagram.jpg"
   alt="S-R latch built from cross-coupled gates with Set and Reset inputs"
   caption="Figure 1 — S-R latch"
   align="center" >}}

Uses two inputs, Set and Reset.

The idea in the SR type is to make one of the outputs always be on (as long as there is current), and it works like a _switch_ that changes the output only if the button assigned to the other value is pressed. For example, a button in a machine that is on or off, the S-R would be a good design base for learning purposes to be in the electrical system to keep the machine on or off.

Looking at a bigger picture, the circuit to store 32 bits is needed, 32 of these, and get the output of Q, for example, to get the actual data (it doesn't really matter whether it's the Q or $\bar{Q}$ here because the system is symmetrical, so it's just arbitrarily decided at the first time and later on is just replicated). If you need to erase the values, you can just pass the reset signal for every latch.

(We can't let them both be 0 because it would return an invalid output, and also if both are 1, it also means it's an error because at the logic level it can't be possible.)

>If it doesn't make sense watch this [video](https://www.youtube.com/watch?v=KM0DdEaY5sY)


### D Latch

{{< figure src="/img/memory/internal-logic-d-latch.webp"
   alt="D latch internal logic: a single data input split by a NOT gate into the Set and Reset lines, gated by an enable"
   caption="Figure 2 — D latch"
   align="center" >}}

Now instead of using two buttons to Set and Reset the state, we can centralize it in one and change the state by clicking this button with the _Define_. We added the _NOT_ logic gate there that will force the system to be oppositely synced. We still have the _CLK_ from before, but now it's called the _E_ (stands to enable) but works as usual.

With that, we remove a problem of inconsistency state because both are off or on, for example. With the enforcement of opposedly sync, we remove race conditions.

### Flip-Flop 

{{< figure src="/img/memory/sr-flip-flop-logic-circuit.jpg"
   alt="Clocked SR flip-flop: SR inputs ANDed with a clock line so updates only happen on the clock"
   caption="Figure 3 — Clocked SR flip-flop"
   align="center" >}}

The difference here is that it has 3 inputs, and there are these _AND_ logic gates that lock the update to be based on the clock. From now on, it can be updated based on time and will accept a signal only when the clock sends the signal, so we can get a tempo of the execution, creating a more solid utilization for real world situations. 

This scenario setup also means we can save information based on the clock, imagine the same _CK_ wire is plugged into multiple flip-flops, we can save information and be certain it will maintain the same state until the next clock.


### JK - Flip Flop

{{< figure src="/img/memory/J-K-flip-flop-diagram.png"
   alt="JK flip-flop with the Q and Q-bar outputs fed back into the input AND gates"
   caption="Figure 4 — JK flip-flop"
   align="center" >}}

Consider the pulse detector as the _clock_ we already saw before. We can spot that the difference is these extra lines going from the end to the start (important to remember is that this _AND_ from the image needs all 3 inputs to activate). These lines ensure that there is no _faulty_ state like J and K equals 1 because even if that happens, the output will still be only one high.

>This create a possible race condition thought, if you keep both J and K clicked and the clock keeps high for some time the output is undefined until we release the buttons or the clock button. You can think of that as the _processing_ time of the current passing by the wires the final state decider.

### T - Flip Flop

{{< figure src="/img/memory/t_flip_flop.png"
   alt="T flip-flop: a JK flip-flop with its J and K inputs tied together into a single toggle line"
   caption="Figure 5 — T flip-flop"
   attr="Source: hackatronic.com"
   attrlink="https://www.hackatronic.com/t-flip-flop-truth-table-circuit-diagram-working-and-applications/"
   align="center" >}}

Here would be a variation of the JK but unifying the J and K input, this results in the changing state of the output from one to another (when the clock is high, of course), you can see in the truth table. It looks a bit useless, but there is a good application for that, counting.

You put one after another, linking one output to the T of the next one. This way, it's like passing the values foward, the leftmost one will increase by one every _CLK_ cycle.

{{< figure src="/img/memory/t_flip_flop_count.png"
   alt="Chained T flip-flops acting as a binary ripple counter, each stage toggling at half the rate of the previous"
   caption="Figure 6 — T flip-flops chained as a counter"
   attr="Source: ResearchGate"
   attrlink="https://www.researchgate.net/publication/220990006_Static_consistency_checking_for_Verilog_wire_interconnects_Using_dependent_types_to_check_the_sanity_of_Verilog_descriptions"
   align="center" >}}

So, at first the value will be $0000$, then we have the first cycle, and the first flip flop output will be one of them $0001$, when the next cycle arrives, the first latch will turn the output to zero, and the value will be passed to the next flip-flop, and the bit counter will be $0010$. The third cycle arrives, and the output of the first flip flop turns 1 again, and the counter will be changed to $0011$ then every cycle the binary numeral will be increased by one. You can also think that every cycle means adding one to the counter (considering the T is always high).

0000 → 0001 → 0010 → 0011 → 0100 → 0101 → ... → 1111 → 0000

The max value we can count in this 4-bit setup is 8, then it returns to zero.
<!--
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
---
title: "Memory"
date: 2026-06-07T17:24:42-03:00
draft: True
math: true
---

So, this is an extensive and sometimes boring matter but also essential.

I'm going to start with latches and flip-flops and hopefully end in RAM/SRAM.

# Latch/Flip-flops

For a fresh start and just for contextualization, latches and flip-flops are bi-stable memory elements. That means they can hold binary information depending on the state.

The difference between both is that the latch doesn't have a clock and keeps the input and output in check constantly, while the flip-flops have progressive changes based on the impulses, for example.

I'm going to make this part progressive, starting from the base latch to flip-flop, D type, JK type, and finally T type.

## S - R Latch

{{< figure src="/img/memory/sr-flip-flop-logic-diagram.jpg"
   alt="S-R latch built from cross-coupled gates with Set and Reset inputs"
   caption="Figure 1 - S-R latch"
   align="center" >}}

Uses two inputs, Set and Reset.

The idea in the SR type is to make one of the outputs always be on (as long as there is current), and it works like a _switch_ that changes the output only if the button assigned to the other value is pressed. For example, a button in a machine that is on or off, the S-R would be a good design base for learning purposes to be in the electrical system to keep the machine on or off.

Looking at a bigger picture, the circuit to store 32 bits is needed, 32 of these, and get the output of Q, for example, to get the actual data (it doesn't really matter whether it's the Q or $\bar{Q}$ here because the system is symmetrical, so it's just arbitrarily decided at the first time and later on is just replicated). If you need to erase the values, you can just pass the reset signal for every latch.

(We can't let them both be 0 because it would return an invalid output, and also if both are 1, it also means it's an error because at the logic level it can't be possible.)

>If it doesn't make sense watch this [video](https://www.youtube.com/watch?v=KM0DdEaY5sY)

## D - Latch

{{< figure src="/img/memory/internal-logic-d-latch.webp"
   alt="D latch internal logic: a single data input split by a NOT gate into the Set and Reset lines, gated by an enable"
   caption="Figure 2 - D latch"
   align="center" >}}

Now instead of using two buttons to Set and Reset the state, we can centralize it in one and change the state by clicking this button with the _Define_. We added the _NOT_ logic gate there that will force the system to be oppositely synced. We still have the _CLK_ from before, but now it's called the _E_ (stands to enable) but works as usual.

With that, we remove a problem of inconsistency state because both are off or on, for example. With the enforcement of opposedly sync, we remove race conditions.

## Flip-Flop 

{{< figure src="/img/memory/sr-flip-flop-logic-circuit.jpg"
   alt="Clocked SR flip-flop: SR inputs ANDed with a clock line so updates only happen on the clock"
   caption="Figure 3 - Clocked SR flip-flop"
   align="center" >}}

The difference here is that it has 3 inputs, and there are these _AND_ logic gates that lock the update to be based on the clock. From now on, it can be updated based on time and will accept a signal only when the clock sends the signal, so we can get a tempo of the execution, creating a more solid utilization for real world situations. 

This scenario setup also means we can save information based on the clock. Imagine the same _CK_ wire is plugged into multiple flip-flops, we can save information and be certain it will maintain the same state until the next clock.


## JK - Flip Flop

{{< figure src="/img/memory/J-K-flip-flop-diagram.png"
   alt="JK flip-flop with the Q and Q-bar outputs fed back into the input AND gates"
   caption="Figure 4 - JK flip-flop"
   align="center" >}}

Consider the pulse detector as the _clock_ we already saw before. We can spot that the difference is these extra lines going from the end to the start (important to remember is that this _AND_ from the image needs all 3 inputs to activate). These lines ensure that there is no _faulty_ state like J and K equals 1 because even if that happens, the output will still be only one high.

>This create a possible race condition thought, if you keep both J and K clicked and the clock keeps high for some time the output is undefined until we release the buttons or the clock button. You can think of that as the _processing_ time of the current passing by the wires the final state decider.

## T - Flip Flop

{{< figure src="/img/memory/t_flip_flop.png"
   alt="T flip-flop: a JK flip-flop with its J and K inputs tied together into a single toggle line"
   caption="Figure 5 - T flip-flop"
   attr="Source: hackatronic.com"
   attrlink="https://www.hackatronic.com/t-flip-flop-truth-table-circuit-diagram-working-and-applications/"
   align="center" >}}

Here would be a variation of the JK but unifying the J and K input, this results in the changing state of the output from one to another (when the clock is high, of course), you can see in the truth table. It looks a bit useless, but there is a good application for that, counting.

You put one after another, linking one output to the T of the next one. This way, it's like passing the values foward, the leftmost one will increase by one every _CLK_ cycle.

{{< figure src="/img/memory/t_flip_flop_count.png"
   alt="Chained T flip-flops acting as a binary ripple counter, each stage toggling at half the rate of the previous"
   caption="Figure 6 - T flip-flops chained as a counter"
   attr="Source: ResearchGate"
   attrlink="https://www.researchgate.net/publication/220990006_Static_consistency_checking_for_Verilog_wire_interconnects_Using_dependent_types_to_check_the_sanity_of_Verilog_descriptions"
   align="center" >}}

So, at first the value will be $0000$, then we have the first cycle, and the first flip flop output will be one of them $0001$, when the next cycle arrives, the first latch will turn the output to zero, and the value will be passed to the next flip-flop, and the bit counter will be $0010$. The third cycle arrives, and the output of the first flip flop turns 1 again, and the counter will be changed to $0011$ then every cycle the binary numeral will be increased by one. You can also think that every cycle means adding one to the counter (considering the T is always high).

0000 → 0001 → 0010 → 0011 → 0100 → 0101 → ... → 1111 → 0000

The max value we can count in this 4-bit setup is 15 (1111), giving 16 distinct states, then it returns to zero.

# Registers

>This part is going to be half baked tbh. It's too much things to cover and I don't have the technicall knowledge and the didatics to abstract everything.

Registers are the blocks used by the CPU or processing unit to manage data. I'm going to focus on normal CPUs to smooth the transition/pivot to the next posts. 

The actual structure of the register can vary, so I will show the CPU internal registers and cache systems, starting with the architectural registers. There are multiple types/classes of internal registers.

From the architectural registers, there are the General-purpose registers (GPRs), Floating-point registers (FPRs), Vector / SIMD registers (going to talk about these guys in the post about database optimization, I guess), Program counter (PC), Stack pointer (SP), Status / flag registers, Control / System registers, and Segment registers. While in the pipeline-stage registers, there are IF/ID, ID/EX, EX/MEM and MEM/WB. Depending on the processor architecture, the registers will have different sizes, like 8, 16, 32, 64, 128, 256 or 512 bits. The 32 and 64 are the most popular these days for home computers and servers, of course, because of the popularity they are more compatible with most software and applications. 

These registers, except for some GPRs, the FPRs, and the Vector/SIMD registers, are all D flip-flop (for reference, the D latch we already saw but have a clock in the _E_ input) type, and this is mostly because of the reliability. The SR latch has an inconsistent state of S=R=1, and the JK has undefined behavior when changing the value while the clock is active. The D doesn't have any of this problem because the only possible output is 0 or 1 independently of the situation, as we can see in the truth table:

{{< figure src="/img/memory/d_type_flip-flop.png"
   alt="D flip-flop truth table: the output Q simply follows the D input on each clock edge"
   caption="Figure 7 - D flip-flop truth table"
   attr="Source: GeeksforGeeks"
   attrlink="https://www.geeksforgeeks.org/digital-logic/applications-of-flip-flop/"
   align="center" >}}

I tried to find some flip-flops at the silicon die level, but it's integrated into the chip, and I couldn't find any good images representing it. If you are interested in a deeper level, I recommend this [Wikipedia](https://en.wikipedia.org/wiki/Flip-flop_(electronics)) page about flip flops as the guide.

If you are curious about the silicon die, here is one example from [Ken Shirriff's blog](https://www.righto.com/) of the Intel 8086 processor:

{{< figure src="/img/memory/silicon_die_x8086.png"
   alt="Annotated silicon die of the Intel 8086 processor highlighting its flip-flops"
   caption="Figure 8 - Flip-flops on the Intel 8086 silicon die"
   attr="Source: Ken Shirriff's blog (Intel 8086 flip-flops)"
   attrlink="https://www.righto.com/2023/09/8086-flip-flops.html"
   align="center" >}}

>I pretend to write about processor architectures in the future, but don't know when and I'm still missing too much technically speaking

A small recap: we now know about some of the lowest possible structures used to store bits, we also know that this structure (D flip-flops) is used in the internals and in pipelines connecting processes. But what about the next level? The processor cache (L1, L2, L3, ...) and what about even farther memories? The RAM, VRAM memories, etc.?

# Cache memory

For bigger blocks of memory, the processor has to rely on other storage systems apart from the _registers,_ and the next ones in the queue of memory capacity are the L1, L2 and L3. You can think of these as the first, second and third levels/lines. They increase progressively in size and inversely in speed when it comes to the time it takes to get or insert some data into them.

Here is one example of a multi-core architecture with the L1, L2, L3 labeled in the image.

> If you are interested I recommend this [thread](https://superuser.com/questions/196143/where-exactly-l1-l2-and-l3-caches-located-in-computer) and the [blog post](https://pikuma.com/blog/understanding-computer-cache) from pikuma (source of the image below)

{{< figure src="/img/memory/i5_first_gen_processor_l1_l2_l3.png"
   alt="Multi-core CPU layout with the L1, L2 and L3 cache levels labeled"
   caption="Figure 9 - L1/L2/L3 cache in a multi-core CPU"
   attr="Source: Pikuma (understanding computer cache)"
   attrlink="https://pikuma.com/blog/understanding-computer-cache"
   align="center" >}}

Now, getting back to the theme itself, these L memories don't use the D flip-flop architecture but the SRAM.

## SRAM

Stands for static random-access memory (SRAM), this memory main purpose is to be compact and fast while maintaining realiability. We are going to use as base the 6T SRAM cell architecture, because this is the most common one. There is also the 4T (T stands for transistor here), even being smaller this one suffers from stability and data leakage. (I'm still not that proficient in eletrics to explain the leakage but it's associated with the resistor load being enoughly high to minimze the current or something, also this point is 100% open to revision and I pretend to write more about when I feel ready).

>The S in SRAM differ from D in DRAM from next topic in the meaning of static and dynamic. Static stands for the state of the bit saved, it's going to be the same forever as long as there is current, while the dynamic have to be _rehydrated_ with otherwise it looses the saved data, deeper approach in later in the text.

Here is the simplified diagram of the 6T SRAM (6 transistors Static Random Access Memory):

{{< figure src="/img/memory/SRAM_Cell_Inverter_Loop_simplied.png"
   alt="Simplified 6T SRAM cell: two cross-coupled inverters forming the storage loop, drawn at a high level without the individual transistors"
   caption="Figure 10 - Simplified 6T SRAM cell (inverter loop)"
   attr="Source: Wikimedia Commons"
   attrlink="https://commons.wikimedia.org/wiki/File:SRAM_Cell_Inverter_Loop.png"
   align="center" >}}


<details style="margin: 1rem 0; padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9;">
<summary style="cursor: pointer; font-weight: 500; color: #000000;"> Click to see the real cell design</summary>

They are the same but this one show all the transistors instead of the high level vision:

{{< figure src="/img/memory/Standard-6T-SRAM-Cell.png"
   alt="Standard 6T SRAM cell: two cross-coupled inverters back to back, with two access pass transistors gated by the word line (WL) connecting the cell to the bit lines (BL and BLB)."
   caption="Figure 11 - Standard 6T SRAM cell"
   attr="Source: ResearchGate (Standard 6T SRAM cell)"
   attrlink="https://www.researchgate.net/figure/Standard-6T-SRAM-Cell-a-6T-SRAM-cell-working-In-standard-6T-SRAM-cell-the-two_fig1_327513798"
   align="center" >}}
</details>

Starting with these dual NOT logic gate, this gate change the input so if 1 entered the other side will be 0:

{{< figure src="/img/memory/dual_not_logic_gate.png"
   alt="Two NOT gates back to back: a 1 entering one side forces a 0 on the other"
   caption="Figure 12 - Cross-coupled NOT gates (the storage loop)"
   align="center" >}}

>As simple as it get, it will just inverse the signal.

Here there is two transistors that just link the output of the dual gate inside with the outsite. So, if the wordline is one, this gate will be open, otherwise it'll not. (The transistor can be used as a gate and amplifier, this case will be used as the gate connection, and the gate controller is this worldline).

{{< figure src="/img/memory/connector_transistor.png"
   alt="Two access transistors linking the cell's internal nodes to the outside bit lines, opened or closed by the wordline"
   caption="Figure 13 - Access transistors gated by the wordline"
   align="center" >}}

You can think of this worldline as a row selector, used by higher level systems to decide which transistor will be used. Because the worldline is the connection to the data wire $BL$ and $\bar{BL}$ and without that we can't access the data inside the circuit from any outside system. Don't forget that each SRAM structure will represent one bit so we have to get a way to manage it to make different sizes of data for example 1 byte which have to group 8 of these in sequence. We can also use the worldline number for addressing, because these structures will be groupped so we have to use something to address the exact place each bit is located.

And now for the $BL$ and the $\bar{BL}$ from the simplified draw. It stands for Bitline, the reason one have the bar is just to differ and later on we are going to use it to find if a value is 1 or 0 based on the current on them. 

### Read

Here is how we interpret the data coming from $BL$ and the $\bar{BL}$. Important to say that when we talk about data signal 0 or 1 it is actually:
- 0: Close to 0V or GND/Vss which stands to "Voltage Source Supply"(this one exist mostly on MOS/CMOS and FETs which is our case).
- 1: Equal to 1V or positive in general can be called Vdd which stands to "Voltage drain drain".

To read the data from $BL$ and $\bar{BL}$ we compare the voltage from the first one with the second, so:

- $BL > \bar{BL} = 1$
- $BL < \bar{BL} = 0$

>To the read happen we have to get the wordline active, otherwise the data catched is from other memory cell.

This comparison is done using a Differential sense amplifier


<!-- CMOS inverter -->

<!-- Differential sense amplifier -->

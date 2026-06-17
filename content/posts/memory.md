---
title: "Memory"
date: 2026-06-07T17:24:42-03:00
draft: True
math: true
---

So, this is an extensive and sometimes boring matter but also essential.

I'm going to start with latches and flip-flops and hopefully end in RAM/SRAM.

Recommendations for those who came to peek:

- [Memory circuits pdf](https://cc.ee.ntu.edu.tw/~lhlu/eecourses/Electronics3/Electronics_Ch17.pdf)
- [SRAM memories](https://thefragmentationparadox.blogspot.com/2014/12/sram-memories.html) most technical high quality content i readed
- [SRAM architecture lecture](https://youtu.be/kypPuQpAQJc?si=g0jk-CLbLHoHrvfT)
- [Ben eater](https://www.youtube.com/@BenEater) is the recommendation for anything related to eletronics and flip-flops
- [Sense amplifiers](https://www.youtube.com/watch?v=MXnZiiuHXIo&lc=UgxlTip-2RsqoBp_75p4AaABAg) intuition drawing

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

Stands for static random-access memory (SRAM), this memory's main purpose is to be compact and fast while maintaining reliability. We are going to use as a base the 6T SRAM cell architecture because this is the most common one. There is also the 4T (T stands for transistor here), even being smaller, this one suffers from stability and data leakage. (I'm still not that proficient in electronics to explain the leakage, but it's associated with the resistor load being high enough to minimize the current or something, also this point is 100% open to revision, and I pretend to write more about it when I feel ready).

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

They are the same, but this one shows all the transistors instead of the high level vision:

{{< figure src="/img/memory/Standard-6T-SRAM-Cell.png"
   alt="Standard 6T SRAM cell: two cross-coupled inverters back to back, with two access pass transistors gated by the word line (WL) connecting the cell to the bit lines (BL and BLB)."
   caption="Figure 11 - Standard 6T SRAM cell"
   attr="Source: ResearchGate (Standard 6T SRAM cell)"
   attrlink="https://www.researchgate.net/figure/Standard-6T-SRAM-Cell-a-6T-SRAM-cell-working-In-standard-6T-SRAM-cell-the-two_fig1_327513798"
   align="center" >}}
</details>

Starting with these dual NOT logic gates, this gate changes the input so if 1 is entered, the other side will be 0:

{{< figure src="/img/memory/dual_not_logic_gate.png"
   alt="Two NOT gates back to back: a 1 entering one side forces a 0 on the other"
   caption="Figure 12 - Cross-coupled NOT gates (the storage loop)"
   align="center" >}}

>As simple as it get, it will just inverse the signal.

Here there are two transistors that just link the output of the dual gate inside with the outside. So, if the wordline is one, this gate will be open, otherwise it'll not. (The transistor can be used as a gate and amplifier, this case will be used as the gate connection, and the gate controller is this worldline).

{{< figure src="/img/memory/connector_transistor.png"
   alt="Two access transistors linking the cell's internal nodes to the outside bit lines, opened or closed by the wordline"
   caption="Figure 13 - Access transistors gated by the wordline"
   align="center" >}}

You can think of this worldline as a row selector, used by higher level systems to decide which transistor will be used. Because the worldline is the connection to the data wire $BL$ and $\bar{BL}$, and without that we can't access the data inside the circuit from any outside system. Don't forget that each SRAM structure will represent one bit, so we have to get a way to manage it to make different sizes of data, for example, 1 byte, which has to group 8 of these in sequence. We can also use the worldline number for addressing because these structures will be grouped, so we have to use something to address the exact place each bit is located.

And now for the $BL$ and the $\bar{BL}$ from the simplified draw. It stands for Bitline, the reason one has the bar is just to differ, and later on we are going to use it to find if a value is 1 or 0 based on the current on them. 

### Read

Here is how we interpret the data coming from $BL$ and the $\bar{BL}$. Important to say that when we talk about data signal 0 or 1, it is actually:
- 0: Close to 0V or GND/Vss, which stands for “Voltage Source Supply” (this one exists mostly on MOS/CMOS and FETs, which is our case).
- 1: Equal to 1V or positive in general can be called Vdd, which stands for “Voltage drain drain”.

To read the data from $BL$ and $\bar{BL}$, we compare the voltage from the first one with the second, so:

- $BL > \bar{BL} = 1$
- $BL < \bar{BL} = 0$

>To the read happen we have to get the wordline active, otherwise the data catched is from other memory cell.

This comparison is done using a differential sense amplifier, the general idea for sense amplifiers is REALLY well explained in [this video](https://www.youtube.com/watch?v=kypPuQpAQJc). Not going to lie, I spent quite a bit of time to understand this whole SRAM composition, and to be honest, mostly because of the electrical part, which I understood nothing about at the start.

The sense amplifier's goal is to amplify, of course, but why? Because there is noise in the signal, and when we talk about extremely small transistors, the capacity of grounding the voltage or increasing is smaller than in denser transistors. So we do the trick of amplifying the signal to compare afterward. This way we get a better output, not perfect, but it doesn't matter, mostly because comparing 0.99 to 0.5 is much better than 0.8 to 0.64, for example, when the difference is minimal, the chance of missing because of noise is big. Fixing the difference problem, we can get a clean digital output with minimal trickery afterward and actually use the data from the bits. In the image below, we can see the moment things happen:

{{< figure src="/img/memory/sense_amplier_video_electron_tube_take.png"
   alt="Differential sense amplifier in action: the small voltage gap between BL and BL-bar being driven apart into a clean digital level"
   caption="Figure 14 - Differential sense amplifier amplifying the bitline difference"
   attr="Source: YouTube (sense amplifier explanation)"
   attrlink="https://www.youtube.com/watch?v=kypPuQpAQJc"
   align="center" >}}

The precharge is a prerequisite to read and write, you can consider that to be the current being set to the average state like 0.5V, so the distance to the 0V or to the 1V is smaller. It's not exactly that, but this is ok for the intuition. Then we connect the wordline, and the data is passed onwards to the sense amplifier, which we can see that amplifies the voltage exponentially, and then the data is passed to the next stages of the pipeline.


### Write

Writing into the SRAM (6T) is simple, we just have to activate the wordline and pass the data to the bitline and bitline bar. The inside system with two NOT gates and the Vss (ground or 0V) and Vdd (voltage drain or 1V for us) will do the job of _normalizing_ the current inside, also the SRAM works as a sense amplifier.

>When I say 1V or 0V is mostly a simplification but for didatics it works (in real world it can be other values or approximation, a reason to the sense amplifier exist if you think about). 

After the bitlines pass the inverted voltage and the wordline disconnects, we get the data stored in the system.

### SRAM System

This is a schema of a 48-bit (the less ugly and visually friendly architecture I could find, tbh) SRAM group. I will not explain the drivers, decoders, and deeper on sense amplifiers today, but it's good to know things exist as a whole.

{{< figure src="/img/memory/static_ram_group.png"
   alt="Schematic of a 48-bit SRAM array with its address decoder, drivers, and sense amplifiers around the cell grid"
   caption="Figure 15 - 48-bit SRAM array (decoder, drivers, sense amplifiers)"
   attr="Source: aeapr.com.br"
   attrlink="https://www.aeapr.com.br/?a=44263698071270"
   align="center" >}}

A more realistic and complete draw would be this one, but with 32-bit 6x4:

{{< figure src="/img/memory/32_bit_sram.png"
   alt="More detailed 32-bit SRAM array arranged as a 6x4 grid of cells with its surrounding logic"
   caption="Figure 16 - 32-bit SRAM array (6x4)"
   attr="Source: The Fragmentation Paradox (SRAM memories)"
   attrlink="https://thefragmentationparadox.blogspot.com/2014/12/sram-memories.html"
   align="center" >}}

 I think the intuition and the perception of the SRAM architecture and functionality are well developed, so let's move to the DRAM or the memory system for the RAM memory from the pc.

## DRAM

For the DRAM, let's remember what it stands for: Dynamic Random Access Memory. The difference here is that we have to keep charging the system, otherwise, it “forgets” what the value of the bit is.

So, for the start, let's see what a capacitor is while looking for this representation:

{{< figure src="/img/memory/schematic_diagram_capacitor.png"
   alt="Schematic diagram of a parallel-plate capacitor: two conductive plates separated by a dielectric, storing charge across the gap"
   caption="Figure 17 - Parallel-plate capacitor"
   attr="Source: ResearchGate (parallel-plate capacitor schematic)"
   attrlink="https://www.researchgate.net/figure/A-schematic-diagram-of-a-the-design-of-a-parallel-plate-capacitor-adapted-from_fig2_334446617"
   align="center" >}}

The purpose of the capacitor is to store energy. The design is as simples as it can be, the capacitor have two conductive plates on the sides and the dieletric in the middle. The two conductive plates have opposite charge and the dieletric will evict the energy to be passed from one to another, so the energy _sits_ there. Important to say that it doesnt stays there forever, it leaks progressively. The dieletric is not perfect, it have some tiny conductivity and the transistor that blocks the current access also have some leakage. With enough time is normal to the current to change from the original value.

Now we know the capacitor functionality and limitations. This is the design for the DRAM:

{{< figure src="/img/memory/dram_design.png"
   alt="DRAM cell: a single capacitor storing the bit, connected through one access transistor to the bitline and gated by the wordline"
   caption="Figure 18 - DRAM cell (1T1C)"
   attr="Source: mean9park (DRAM Operation)"
   attrlink="https://mean9park.github.io/DRAM_Operation/"
   align="center" >}}

We have the capacitor storing the value and one transistor connecting the bitline that's activated based on the wordline. And that's it, the functionality of the writing and reading is similar to the SRAM storage system when it comes to wordline and bitline but here there is only one bitline instead of two. Now instead of 6T or 6 transistors we just need one capacitor and one transistor to store a bit, the size of the system for each bit is much smaller and with that we can put a lot more DRAMs in a smaller space which will call a denser memory system.

But it's not all flowers, as I said before the capacitor leaks and this change from the default features from the SRAM memory. The DRAM will have to be _Dynamically_ refreshed (Name mentioned! _Dynamic Random Access Memory_), so let's see how it works.

### Refreshing

We can think of the refresh as a _READ_ and _WRITE_ operation that have to run once a while to keep the data "reliable". I said reliable because it's not that concrete, we are working with diffent current in a analog signal and transforming to a digital output. So, for the analog signal we have the current in the wordline as Vdd/2 or 0.5V for didatics as I said before, the Vdd or 1V will be the 1 and the GND or 0v will be the 0. 

Taking that into consideration, the leak will happen to the point the sense amplifier will not recognize if it's one or another. You can say that the GND/0 will kept 0 so it will always know, right? No, because the 0V is also being leaked because of the capacitor and the transistor connecting the wordline leaks, so it keep going from GND to Vdd/2 from wordline. Knowing it leaks from the both sides, we have to refresh the data in a safe interval to guarantee the realiability of the data and this one is 64ms according to the standard set by the industry, not gonna dive in this point but this value is a sweet spot considering the temperature (leakage roughly doubles each 10°C), capacitor's insulator (measure for the evicting of energy throughput), transistor leakage and some other factors.

Important to say that the write operation will only happen at row level so the refresh can't be done at a all cell simultaneously. In reality the refresh is happening basically everytime because it keep going from row to row and every 64ms it refresh all the rows in the _Bank_ (group of dram cell).

The first state is the dram cell charge degradation in row 3 that was originally 1V, 0V and 1V respectivelly:

{{< figure src="/img/memory/dram_1.png"
   alt="DRAM refresh step 1: the charges stored in row 3 (originally 1V, 0V, 1V) have leaked and drifted away from their original levels"
   caption="Figure 19 - Refresh step 1: charge degradation"
   align="center" >}}

The second state is the Bitline charging to Vdd/2 or 0.5V in the example:

{{< figure src="/img/memory/dram_2.png"
   alt="DRAM refresh step 2: the bitline is precharged to Vdd/2 (0.5V) before the cell is connected"
   caption="Figure 20 - Refresh step 2: bitline precharged to Vdd/2"
   align="center" >}}

The third state the wordline is activated and the bitline starts to equalize the current towards the charge inside the DRAM cell.

{{< figure src="/img/memory/dram_3.png"
   alt="DRAM refresh step 3: the wordline is activated and the bitline starts to equalize toward the charge stored in the cell"
   caption="Figure 21 - Refresh step 3: charge sharing"
   align="center" >}}

Technically the last state would be the last because the Sense Amplifier is connected directly in the bitline but for simplification reasons here is the final one. The sense amplifier will identify the change in the bitline and amplify the current towards the identified charge, it works similar to the SRAM but now we have only one line.

{{< figure src="/img/memory/dram_4.png"
   alt="DRAM refresh step 4: the sense amplifier detects the small shift on the bitline and drives it to the full level, restoring the cell's original value"
   caption="Figure 22 - Refresh step 4: sense amplifier restores the value"
   align="center" >}}

### Architecture

I think the refreshing topic also explained about the read and the writing (refresh does both if you think a bit about). Here I'm gonna be direct to the point because the post is getting too long, again... 

The architecture of the DRAM blocks of memory is divided in _Channel > DIMM > Rank > Chip > Bank > Row/column > DRAM cell_:

- Channel — The bus between CPU and memory.
- DIMM — The physical stick you plug into a slot.
- Rank — A group of chips on a DIMM that fire together to deliver one full data word.
- Chip — A single DRAM IC, only provides part of the data word (x4, x8, or x16 bits wide).
- Bank — An independent sub-array inside a chip, banks work in parallel.
- Row — A line of cells inside a bank that gets "opened" as a unit.
- Column — Within an open row, picks which bits to actually read or write.
- Cell — One transistor + one capacitor. Stores a single bit.

{{< figure src="/img/memory/chip_bank_hierarchy.png"
   alt="DRAM organization hierarchy: a chip divided into independent banks, each bank a grid of rows and columns of cells"
   caption="Figure 23 - DRAM chip and bank hierarchy"
   attr="Source: mean9park (DRAM Operation)"
   attrlink="https://mean9park.github.io/DRAM_Operation/"
   align="center" >}}

For those interested in DRAM the most complete post I readed about DRAM was [this](https://newsletter.semianalysis.com/p/the-memory-wall).

As I said before I'm not gonna dive deeper than this today, because it would go too far from the focus that's memory itself.

## Other types

> This one is mostly for curiosity and to to call a spade a spade, I really pretend to write more about these topics in the near future by the way, but they are usually too dense and I'm a bit lazy...

With the basics of the DRAM cell archtecture we could move to some newer systems. Since the 2000's the industry use the DDR, yes the one from DDR1, DDR2, DDR3, DDR4 and the DDR5. Which stands for double data rate, every cycle from the clock (the _clk_ we talked about) it makes two transfers. 

### VRAM

There is the memory used internally in graphic cards (GPU) which people usually calls VRAM. This one can mean GDDR which is the previous DDR but specialized in graphics (usually means more parallelism and vectorization) but some high-end GPU these days mainly because of AI accelerator uses HBM, which stands to high bandwitch memory. The main difference in these besides the paralelization is that the memory is accessed sequentially instead of randomically (gonna talk more about that in a next moment too) and have more capacity of processing via throughput and raw capacity, these type of memory can be find in:

| Memory | Bandwidth | Typical capacity | Where you find it |
|---|---|---|---|
| **DDR5-6400** (CPU) | ~50 GB/s per channel | 32-128 GB | Desktops, laptops, servers |
| **LPDDR5X** (mobile) | ~70 GB/s per channel | 8-32 GB | Phones, ultrabooks |
| **GDDR6** | ~500-700 GB/s | 8-24 GB | Gaming GPUs |
| **GDDR6X** | ~1 TB/s | 8-24 GB | RTX 4080/4090 |
| **GDDR7** | ~1.5 TB/s | 12-32 GB | RTX 50-series |
| **HBM3** | ~3 TB/s | 80-141 GB | H100, MI300 |
| **HBM3E** | ~5 TB/s | 141-192 GB | B200, MI325X |

### TPU

Them there is the TPU which uses all of them, but the focus is in matrix multiplication basically aiming for AI in training, optimizing and developing models which under the hood is all matrix operations. This one I mentioned mostly to set in stone that I'm gonna write one post in the future completely focused on. Will be after the neural networks part 2 and the transformers, RAG, dense retrieval I guess, but it will happen.

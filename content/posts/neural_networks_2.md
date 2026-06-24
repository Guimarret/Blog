---
title: "Neural networks 2"
date: 2026-06-19T12:25:58-03:00
draft: true
math: true
---

# Foundation

Hello, again. Continuing the neural networks trail, today we are gonna take a look at the CNN, RNN and maybe training at scale implementations.

I didn't explictly said but the last post is mostly the technicall and mathematical visualization, focused in building intuition on the matter. The actual application in real life get's more difficult because we also have to be aware of optimizing the training setup, otherwise in just unusable. If you get yourself in late 70's which is when they were researching and testing the technics from the last post, the hardware and storage was just too expensive and for contextualization it's easy and simple to train models that get's massively big.

>With that in mind, this post should have less heavy math _but_ more usage of matrices.

Let's start with calculating the activation of some layer using matrices (will make it easier to visualize later).

## Activation calculation - Matrices

Using the neural network from the last post:

{{< figure src="/img/neural_net/multilayer_multiunit.png" 
   alt="Multineuron multiunit" 
   caption="Figure 1 - Multi-unit Multineuron visualization" 
   align="center" >}}

In the last post I said the calculation for the layer L would be the weights connecting the last neurons multiplying the activation of the neurons in the origin and summing everything, or mathematically:

$$z_j^{(L)} = w_{j0}^{(L)} a_0^{(L-1)} + w_{j1}^{(L)} a_1^{(L-1)} + w_{j2}^{(L)} a_2^{(L-1)} + b_j^{(L)}$$

>Two times because there are two neurons in the output layer (L)

But it is a bit too tiresome to multiply every single neuron for every layer and everything again for every forward pass in the training which can extends to thousands of training inputs.

So let's rewrite using matrices:

Since layer $L$ has 2 neurons (Output, Output 2) and layer $L-1$ has 3 neurons, the weight matrix is $2 \times 3$:

$$\begin{bmatrix} a_0^{(L)} \\ a_1^{(L)} \end{bmatrix} = \sigma \left( \begin{bmatrix} W_{00} & W_{01} & W_{02} \\ W_{10} & W_{11} & W_{12} \end{bmatrix} \cdot \begin{bmatrix} a_0^{(L-1)} \\ a_1^{(L-1)} \\ a_2^{(L-1)} \end{bmatrix} + \begin{bmatrix} b_0 \\ b_1 \end{bmatrix} \right)$$

Simpler, right? Now we can visualize everything in one block without getting too much information.

>Reminder, matrices are represented in row and column, $M_{RowxColumn}$. 

>Multiplying two matrix $M_{2x3}$ and $N_{3x1}$ the output is the rows of the first and the columns of the second, so MxN = $R_{2x1}$ (which is our case)

>Summing matrices keep the dimensions and just sums element by element.

You can also think that for each activation neuron there will be one row of weights, one column of activations from the last layer with N rows and one column with one bias for each activation neuron.

It's easier to process more data in one batch this way because the data is _collapsed_ in matrices.

## Training techniques

Considering the matrices calculations let's jump to training techniques. By techniques I mean ways of processing the data, for example you can update the gradient descent in the training considering one dataset input, multiple inputs or even the whole dataset for every step. Abstractively you can think of it by running towards the _minima_ based on each input, on the batch or the dataset as a whole.

Doting the i's and crossing the t's, the gradient descent calculated based on the complete dataset for every step is the _batch_ training, the sliced dataset would be the _mini-batch_ training and the version that updates for every input is the stochastic. So, we have the Batch gradient descent, the mini-batch gradient descent and the stochastic gradient descent.

This plot is a convex surface and the lines are proceeding towards the minima:

{{< figure src="/img/neural_net_2/training_techniques_gd.png" 
   alt="Multineuron multiunit" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

>The SGD in the substitle is white... I saw too late, sorry.

We can see the difference in rote but they end up at least close to each other in the end. The end here stands for the decreased error surface point.

This next plot is the comparison between the error calculation and the number of steps. The purpose of this one is to enphatise the increase in steps and decrease in mathematical complexity/mathematical steps for each processing steps. Important to remember that computers are much more efficient in _simpler_ but parallel tasks than intensive individual tasks, even more if we consider the GPU (graphic processing unit). As already explained in the memory post, these units are perfect for these matrices calculations, you can paralellize thousands of executions (important to say that execution here don't mean steps but smaller steps like weight updates or forward processing for example)

{{< figure src="/img/neural_net_2/comparison_steps.png" 
   alt="Multineuron multiunit" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}




<!-- ## CNN -->
<!-- James briggs ref - https://www.youtube.com/watch?v=ZBfpkepdZlw -->
<!-- RNN | LSTM-->
<!-- Training at scale (Adam, AdamW) -->
<!-- ![Neural Networks](/img/neural_net/neural_networks.png) -->
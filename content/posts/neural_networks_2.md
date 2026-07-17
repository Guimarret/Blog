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

## Basic training techniques (Batch, Small-batch and SGD)

Considering the matrices calculations let's jump to training techniques. By techniques I mean ways of processing the data, for example you can update the gradient descent in the training considering one dataset input, multiple inputs or even the whole dataset for every step. Abstractively you can think of it by running towards the _minima_ based on each input, on the batch or the dataset as a whole.

Doting the i's and crossing the t's, the gradient descent calculated based on the complete dataset for every step is the _batch_ training, the sliced dataset would be the _mini-batch_ training and the version that updates for every input is the stochastic. So, we have the Batch gradient descent, the mini-batch gradient descent and the stochastic gradient descent.

This plot is a convex surface and the lines are proceeding towards the minima:

{{< figure src="/img/neural_net_2/training_techniques_gd.png" 
   alt="Multineuron multiunit" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

>The SGD in the substitle is white... I saw too late, sorry. Also the gradience goes from lowest to highest as blue to orange

We can see the difference in rote but they end up at least close to each other in the end. The end here stands for the decreased error surface point.

This next plot is the comparison between the error calculation and the number of steps. The purpose of this one is to enphatise the increase in steps and decrease in mathematical complexity/mathematical steps for each processing steps. Important to remember that computers are much more efficient in _simpler_ but parallel tasks than intensive individual tasks, even more if we consider the GPU (graphic processing unit). As already explained in the memory post, these units are perfect for these matrices calculations, you can paralellize thousands of executions (important to say that execution here don't mean steps but smaller steps like weight updates or forward processing for example)

{{< figure src="/img/neural_net_2/comparison_steps.png" 
   alt="Multineuron multiunit" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

But even memory parallelization gets a ceiling. I plotted the relation of the total processing time with the MSE reduction and it gets clear that the curve which reachs the MSE minimal line faster in the mini-batch.

{{< figure src="/img/neural_net_2/mini_batch_cumulative_wall_clock.png" 
   alt="Multineuron multiunit" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

With that in mind we can reach the next step which is applying that into the first industry worldwide usable tool aka CNN for recognizing handwriting

# Convolutional Neural Networks (CNN)

The first industry product with real evaluation using neural networks was number and letter handwriting recognition, in the US it was used to help the mail service to automatize zip codes and also sort hadwritten digits on paper for the financial sector. Earlier the problem for image processing were the size and absence of spatial context like information because everything gets flattened. 

The intuition for this one is more direct, if you want to evaluate something you have to get the data somewhere. Naturally you will select the training data to make the output more reliable BUT if you just select anything as training the output will also be anything.

That said, we want to find a way to train the model to recognize things from image. To do that, Yann Lecun in 1989 published this solution [link](http://yann.lecun.com/exdb/publis/pdf/lecun-89e.pdf) which basically *IS* the CNN until 2010 (the year alex net was released and things got another route and also exploded to other areas, but we are going to talk about that later). In the article they introduce their setup.

{{< figure src="/img/neural_net_2/cnn_initial_structure.png" 
   alt="CNN scheme" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

## Image, Kernels and Convolution

First things first "what is a convolution". It is a mathematical operation between two function that produces a third one that represents how de second function influences the first one.

Using the example from 3Blue1Brown from the [convolution video](https://www.youtube.com/watch?v=KuXjwB4LzSA), if have any curiosity in convolutions, want to dive deeper or have more intuition about what it represents in reality I recommend the video before the rest of this post.

{{< figure src="/img/neural_net_2/convolution_3blue1brown.png" 
   alt="CNN scheme" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

You can imagine that the output image of the kirby represent some spectre of the original image, like part of the original one but showing biased type of information. That's part of the purpose, in images to explicity some data we use this kernel, for example you can blur the image to reduce the details of the image, the edge detection in kirby which also have two collors focus based on the side which can be easily percepted that stands out in the output.

>The function in the middle that apply the changes is called kernel, this kernel can be seen as a matrix weight from the last post, following the first post idea (we'll also need to train the weights to be more efficient in some patterns later on). 

But for now let's think about it in the same way of the perceptron you could set manually some weight setup to distinguish some pattern that will output if your needs are attended or not. With that in mind look to the image context, you could want to find one circle + one diagonal line and say it's a six, but could be a rotated nine, allucinate some other number or even have more than one number in the same image mistakingly. We want to find a reliable way to find patterns in the whole image without any position, horizontality or verticality restriction. 

{{< figure src="/img/neural_net_2/kernel_comparison.png" 
   alt="CNN scheme" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

To make that using the Lecun technique from the paper we use run the kernel phase to make features stand out (lines, corners, shades, excess of definition and any possible thing that helps imply what is happening the block), then run another kernel phase again to stand even more and them compact all unit into a small number of unit new layer of 30 units and then do it again into the last layer with 10 units wich represents the digits from 0-9.

Diving deeper in technical details now, observe that applying the kernel in the images will reduce in half their size in each one of the steps that still keeps the image format in the Lecun example, this is called _Pooling_. The image goes from 256 to 64, 16 (importante to observe that the kernel "copy's" still exists there but also reduced in size, in Lecun example there are 12 of them in all the layers after the input one). This is done intentionally to reduce the computation needed to process afterwards operations with weight and the backpropagation that have to reach each one of the units in all layers.

>There are some types of pooling, but to explain a bit about I got this example of Max (max values between the 4 units in this case) and average whitch would calculate the average of the neighbour units. (The average one is used to blur and have the technical name of gaussian blur)

<!-- Pooling example with stride 2 -->
{{< figure src="/img/neural_net_2/pooling_stride_2.png" 
   alt="CNN scheme" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

Them finally in the last layer they use one the nonlinear function (remember that we need to use some sort of nonlinear function like this one otherwise all the neurons we see it's just fancy drawing because mathematically would collapse to one massive matrix operation) $tanh$ to output the most "activated" weight.

>In Lecun work they used the value range for each unit as -1 to 1 considering grayscale, in other words black to white gradient. So because of this the marked range in the $tanh$ is like that. 

<!-- Tanh function example -->
{{< figure src="/img/neural_net_2/tanh_activation.png" 
   alt="CNN scheme" 
   caption="Figure 2 - Multi-unit Multineuron visualization" 
   align="center" >}}

I created the second image like this to refresh the way the gradiente descent work on the nonlinear/activation function. Using this as a hook to say that Lecun used the mean squared error (MSE) function as the Loss function. As expected, because of the MSE + Tanh can have some behavior that softmax would'nt, like two values close to the activation but it's okay at the end of the day because we can just get the max value itself that will have a satisfying accuracy.









<!-- James briggs ref - https://www.youtube.com/watch?v=ZBfpkepdZlw -->
<!-- RNN | LSTM-->
<!-- Training at scale (Adam, AdamW) -->
<!-- ![Neural Networks](/img/neural_net/neural_networks.png) -->
---
title: "Neural networks 2"
date: 2026-06-19T12:25:58-03:00
draft: true
math: true
---

# Foundation

Hello again. Continuing the neural networks trail, today we are gonna take a look at the CNN, RNN and maybe some training at scale implementations.

I didn't explicitly say it, but the last post was mostly the technical and mathematical visualization, focused on building intuition on the matter. The actual application in real life gets more difficult because we also have to be aware of optimizing the training setup, otherwise it's just unusable. If you put yourself back in the late 70's, which is when they were researching and testing the techniques from the last post, the hardware and storage were just too expensive, and for context it is really easy to end up training models that get massively big.

>With that in mind, this post should have less heavy math _but_ more usage of matrices.

Let's start with calculating the activation of some layer using matrices (will make it easier to visualize later).

## Activation calculation - Matrices

Using the neural network from the last post:

{{< figure src="/img/neural_net/multilayer_multiunit.png" 
   alt="Multilayer, multi-unit neural network diagram" 
   caption="Figure 1 - Multilayer, multi-unit neural network from the last post" 
   align="center" >}}

In the last post I said the calculation for layer L would be the weights connecting the last neurons, multiplying the activation of the neurons in the origin and summing everything, or mathematically:

$$z_j^{(L)} = w_{j0}^{(L)} a_0^{(L-1)} + w_{j1}^{(L)} a_1^{(L-1)} + w_{j2}^{(L)} a_2^{(L-1)} + b_j^{(L)}$$

>Two times because there are two neurons in the output layer (L)

But it is a bit too tiresome to multiply every single neuron for every layer, and do everything again for every forward pass in the training, which can extend to thousands of training inputs.

So let's rewrite using matrices:

Since layer $L$ has 2 neurons (Output, Output 2) and layer $L-1$ has 3 neurons, the weight matrix is $2 \times 3$:

$$\begin{bmatrix} a_0^{(L)} \\ a_1^{(L)} \end{bmatrix} = \sigma \left( \begin{bmatrix} W_{00} & W_{01} & W_{02} \\ W_{10} & W_{11} & W_{12} \end{bmatrix} \cdot \begin{bmatrix} a_0^{(L-1)} \\ a_1^{(L-1)} \\ a_2^{(L-1)} \end{bmatrix} + \begin{bmatrix} b_0 \\ b_1 \end{bmatrix} \right)$$

Simpler, right? Now we can visualize everything in one block without getting too much information.

>Reminder, matrices are represented in row and column, $M_{RowxColumn}$. 

>Multiplying two matrices $M_{2x3}$ and $N_{3x1}$, the output takes the rows of the first and the columns of the second, so MxN = $R_{2x1}$ (which is our case)

>Summing matrices keeps the dimensions and just sums element by element.

You can also think of it like this: for each activation neuron there will be one row of weights, one column of activations from the last layer with N rows, and one column with one bias for each activation neuron.

It's easier to process more data in one batch this way because the data is _collapsed_ in matrices.

## Basic training techniques (Batch, Small-batch and SGD)

Considering the matrix calculations, let's jump to training techniques. By techniques I mean ways of processing the data. For example, you can update the gradient descent in the training considering one dataset input, multiple inputs or even the whole dataset for every step. Abstractly, you can think of it as running towards the _minima_ based on each input, on the batch or on the dataset as a whole.

Dotting the i's and crossing the t's, the gradient descent calculated based on the complete dataset for every step is the _batch_ training, the sliced dataset would be the _mini-batch_ training, and the version that updates for every input is the stochastic one. So, we have the batch gradient descent, the mini-batch gradient descent and the stochastic gradient descent.

This plot is a convex surface and the lines are proceeding towards the minima:

{{< figure src="/img/neural_net_2/training_techniques_gd.png" 
   alt="Gradient descent paths on a convex error surface" 
   caption="Figure 2 - Batch, mini-batch and SGD paths towards the minima" 
   align="center" >}}

>The SGD in the subtitle is white... I noticed too late, sorry. Also the gradient goes from lowest to highest as blue to orange

We can see the difference in route but they end up at least close to each other in the end. The end here stands for the decreased error surface point.

This next plot is the comparison between the error calculation and the number of steps. The purpose of this one is to emphasize the increase in steps and the decrease in mathematical complexity for each processing step. It's important to remember that computers are much more efficient at _simpler_ but parallel tasks than at intensive individual tasks, even more so if we consider the GPU (graphics processing unit). As already explained in the memory post, these units are perfect for these matrix calculations, you can parallelize thousands of executions (important to say that execution here doesn't mean steps but smaller steps like weight updates or forward processing for example)

{{< figure src="/img/neural_net_2/comparison_steps.png" 
   alt="Error against the number of steps for each training technique" 
   caption="Figure 3 - Error against the number of steps for each technique" 
   align="center" >}}

But even memory parallelization hits a ceiling. I plotted the relation of the total processing time with the MSE reduction and it gets clear that the curve which reaches the MSE minimal line faster is the mini-batch one.

{{< figure src="/img/neural_net_2/mini_batch_cumulative_wall_clock.png" 
   alt="Cumulative wall-clock time against MSE reduction" 
   caption="Figure 4 - Cumulative wall-clock time against MSE reduction" 
   align="center" >}}

With that in mind we can reach the next step, which is applying all of that to the first industry worldwide usable tool, aka the CNN for recognizing handwriting

# Convolutional Neural Networks (CNN)

The first industry product with real evaluation using neural networks was number and letter handwriting recognition. In the US it was used to help the mail service automate zip codes and also to sort handwritten digits on paper for the financial sector. Earlier, the problem for image processing was the size and the absence of spatial context information, because everything gets flattened.

The intuition for this one is more direct, if you want to evaluate something you have to get the data from somewhere. Naturally you will select the training data to make the output more reliable, BUT if you just select anything as training, the output will also be anything.

That said, we want to find a way to train the model to recognize things from an image. To do that, Yann LeCun in 1989 published this solution [link](http://yann.lecun.com/exdb/publis/pdf/lecun-89e.pdf) which basically *IS* the CNN up until 2012 (the year AlexNet was released and things took another route and also exploded into other areas, but we are going to talk about that later). In the article they introduce their setup.

{{< figure src="/img/neural_net_2/cnn_initial_structure.png" 
   alt="LeCun's original CNN architecture" 
   caption="Figure 5 - LeCun's original CNN structure from the 1989 paper" 
   align="center" >}}

## Image, Kernels and Convolution

First things first, "what is a convolution". It is a mathematical operation between two functions that produces a third one, which represents how the second function influences the first one.

Using the example from 3Blue1Brown in the [convolution video](https://www.youtube.com/watch?v=KuXjwB4LzSA), if you have any curiosity about convolutions, want to dive deeper or want more intuition about what it represents in reality, I recommend the video before the rest of this post.

{{< figure src="/img/neural_net_2/convolution_3blue1brown.png" 
   alt="Convolution of a kernel over a Kirby image" 
   caption="Figure 6 - Convolution example from the 3Blue1Brown video" 
   align="center" >}}

You can imagine that the output image of the Kirby represents some spectrum of the original image, like part of the original one but showing a biased type of information. That's part of the purpose, in images, to make some data explicit we use this kernel. For example you can blur the image to reduce its details, or the edge detection in Kirby, which also has two color focuses based on the side, something that can be easily perceived and stands out in the output.

>The function in the middle that applies the changes is called the kernel. This kernel can be seen as a weight matrix from the last post, following the first post's idea (we'll also need to train the weights to be more efficient at some patterns later on). 

But for now let's think about it in the same way as the perceptron, you could manually set up some weights to distinguish a pattern that will output whether your needs are met or not. With that in mind, look at the image context, you could want to find one circle + one diagonal line and say it's a six, but it could be a rotated nine, it could hallucinate some other number or even mistakenly have more than one number in the same image. We want to find a reliable way to find patterns in the whole image without any position, horizontality or verticality restriction. 

{{< figure src="/img/neural_net_2/kernel_comparison.png" 
   alt="Comparison of different kernels applied to an image" 
   caption="Figure 7 - Comparison of different kernels applied to an image" 
   align="center" >}}

To do that using the LeCun technique from the paper, we run the kernel phase to make features stand out (lines, corners, shades, excess of definition and any possible thing that helps imply what is happening in the block), then run another kernel phase to make them stand out even more, and then compact all the units into a new layer with a small number of units, 30 units, and then do it again into the last layer with 10 units which represent the digits from 0-9.

Diving deeper into technical details now, observe that applying the kernel to the images will halve each spatial dimension in every one of the steps that still keeps the image format in the LeCun example, this is called _Pooling_. Halving each dimension drops the number of units per map to a quarter, so it goes from 256 to 64 to 16 (important to observe that the kernel "copies" still exist there but also reduced in size, in the LeCun example there are 12 of them in all the layers after the input one). This is done intentionally to reduce the computation needed to process the later operations with weights and the backpropagation, which have to reach each one of the units in all layers.

>There are some types of pooling, but to explain a bit about them I got this example of Max (the max value between the 4 units in this case) and average, which would calculate the average of the neighbouring units. (The average one blurs the image, and since every neighbour gets the same weight it is a box/mean blur)

<!-- Pooling example with stride 2 -->
{{< figure src="/img/neural_net_2/pooling_stride_2.png" 
   alt="Max and average pooling with stride 2" 
   caption="Figure 8 - Max and average pooling with stride 2" 
   align="center" >}}

Then finally in the last layer they use a nonlinear function (remember that we need to use some sort of nonlinear function like this one, otherwise all the neurons we see are just a fancy drawing because mathematically it would collapse into one massive matrix operation), the $tanh$, to output the most "activated" weight.

>In LeCun's work they used the value range for each unit as -1 to 1 considering grayscale, in other words a black to white gradient. So because of this the marked range in the $tanh$ is like that. 

<!-- Tanh function example -->
{{< figure src="/img/neural_net_2/tanh_activation.png" 
   alt="Tanh activation function and its gradient" 
   caption="Figure 9 - Tanh activation function" 
   align="center" >}}

I created the second image like this to refresh the way the gradient descent works on the nonlinear/activation function. Using this as a hook to say that LeCun used the mean squared error (MSE) function as the loss function. As expected, the MSE + Tanh can have some behavior that softmax wouldn't, like two values close to the activation, but it's okay at the end of the day because we can just get the max value itself, which will have a satisfying accuracy.









<!-- Next steps for this post (CNN -> AlexNet arc):
- Cross-entropy + softmax as the fix for MSE+tanh
- Backprop through conv layers / weight sharing (brief)
- Vanishing gradients with tanh/sigmoid -> motivates ReLU
- Gap years: LeNet-5, AI winter, SVMs displacing NNs for vision
- AlexNet: ReLU + Dropout + data augmentation + GPUs + ImageNet scale (closes the arc)
-->

<!-- Post 3 (separate topic, not part of this arc):
- RNN | LSTM
- Training at scale (Adam, AdamW, batch norm, LR schedules)
- James briggs ref - https://www.youtube.com/watch?v=ZBfpkepdZlw
-->
<!-- ![Neural Networks](/img/neural_net/neural_networks.png) -->
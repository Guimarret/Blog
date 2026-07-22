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

I created the second image like this to refresh the way the gradient descent works on the nonlinear/activation function. Using this as a hook to say that LeCun used the mean squared error (MSE) function as the loss function. As expected, the MSE + Tanh can have some behavior that softmax wouldn't, like two values close to the activation, but it's okay at the end of the day because we can just get the max value itself $argmax()$, which will have a satisfying accuracy.

We already talked about that in the last post but, if you look at the derivative of the tanh, it has the biggest influence in the middle and flattens in the low and high ends. This means the biggest correction only applies when the "activation" is happening in the middle, so if a massive error value lands in it, there's a good chance it gets stuck in the minimal correction.

>We talked about that in the vanishing gradient topic but just refreshing the specific details.

## LeNet-5

In 1998, LeNet-5 was released as the new state of the art for convolutional neural networks. This one improved the accuracy in overall performance and had a more structured and engineered architecture. The training dataset was almost 10x larger, now with 60000 training images, and they used bigger images as inputs. Let's review the changes.

{{< figure src="/img/neural_net_2/lenet-5-architecture.png" 
   alt="Tanh activation function and its gradient" 
   caption="Figure 9 - Tanh activation function" 
   align="center" >}}

Now the input is twice the size, instead of 16 it's 32x32 (with padding so the edge information doesn't get lost after the kernel process). Convolution and subsampling processes are separated (the C subtitle means convolution, S for subsampling, and F for fully connected). More features in the layers, one of which has 6 layers of low-level features, and the following one also has 6 layers but downsamples the previous one (keeps 6 feature maps but reduces the resolution from 28x28 to 14x14).

At convolution 3 they chose a completely different strategy from the original 89's CNN. The feature maps connect differently, using features from the previous sampling. Imagine this like the combination of earlier information. I said that some low-level features could be like lines, edges, etc. Now we want to combine these into newer possible information, like some "higher" level feature based on the previous one. The setup they used is:

- 6 of the C3 maps connect to 3 contiguous feature maps from S2 (maps {0,1,2}, {1,2,3}, {2,3,4}, and so on, wrapping around).
- 6 more connect to 4 contiguous feature maps from S2.
- 3 more connect to 4 non-contiguous feature maps from S2.
- The last 1 connects to all 6 S2 maps.

Now we have a new type of layer that's based on core low-level features to improve the previous processing capacity.

Then we subsample again, reaching S4, which has a dimension of 5x5 with 16 maps. We convolve all of them into 120 independently weighted filters. This is a bit confusing, but they just used all the 16 maps with 5x5px 120x (which each time would be a different filter for the input) to produce 120 units in the layer C5. All the units generated are connected to every pixel in every map, 120 x 16 x 5 x 5, which results in 48120 parameters. These lines connecting everything have unique weights which are gonna be trained later.

Next layer is the fully connected (6) which has 86 units that can be called neurons. Till that layer we used a normal $tanh$ activation function in the training part, but it's gonna change in the next one.

>For curiosity's sake, the 86 number is because 7x12 is the pixel bitmap used to represent stylized ASCII character images, which for now is not that important considering we just read numbers, not full ASCII, but that's the reason for the number.

Finally, the final layer has 10 output values that represent the 0-9 range of numbers. The units don't compute the weighted sum like normal neurons, but the distance. This one is a bit special because they changed the loss function to the Radial Basis Function (RBF).

$$y_i = \sum_{j} (x_j - w_{ij})^2$$

The $x_j$ is the $j$-th value of the last layer's 84-value vector. The $w_{ij}$ is the $j$-th value of the prototype vector, which also has 84 values.

>The prototype vector is a handmade vector that basically draws the digit value in the 7x12 bitmap board so the recognizing system is guided more directly. Also, you can infer that here the system is walking towards a new breakthrough in recognizing. They are setting everything up to expand to all ASCII characters.

Since the measured value in the loss system is distance, the best output value from each sum will be the minimal one, mathematically speaking:

$$\text{predicted class} = \arg\min_i , y_i$$   

### Training system

Considering the minimal distance system, we create a new problem, the chance of the system cheating during training, reaching some average value between all values in the prototype vector. With that, the training and everything would be meaningless.

To solve that they created a modified system for training:

$$E(W) = \frac{1}{P} \sum_{p=1}^{P} \left[ y_{D^p}\left(x^p, W\right) + \log\left( e^{-j} + \sum_i e^{-y_i\left(x^p, W\right)} \right) \right]$$

$P$ is the total number of training examples, $x^p$ is the $p$-th training input, $D^p$ is the correct class label for the training input (if the image had a 6 drawn on it, the class label here would be 6).

The $y_{D^p}$ is the distance to the correct class's prototype, given the training value and the network's current weight $W$. So this one keeps getting smaller during training, so the distance keeps shrinking.

This is added to the first value inside the log, $e^{-j}$, which is a mechanism to prevent the next term from pushing values further. When the value is small enough it becomes indifferent, close to the small $e^{-j}$, so it stops getting smaller (it's like the training incentive is designed not to run past the point where it doesn't change anything in the system). So it just keeps the next term from making the log too small, as a margin.

And the next value in the log is what actually does the job. To make it simple, I put this plot below for intuition. The sum makes it run the operation with the $e$ for all the classes (0-9), so we get the value of $e$ elevated to the _negative_ value of the distance between:
- Output vector from F6 for the input $x^p$
- Correct class from the prototype vector

Or simplifying, the distance between the values generated from the training data and the correct vector from the prototype.

The value is negative because we want to train the log to get smaller while the distance from the class increases (to avoid the convergence to an average value I talked about before):
- If $y_i$ (distance) is small, $e^{-y_i}$ is large.
- If $y_i$ (distance) is large, $e^{-y_i}$ is close to zero.

{{< figure src="/img/neural_net_2/euler_exponent_neg.png" 
   alt="Tanh activation function and its gradient" 
   caption="Figure 9 - Tanh activation function" 
   align="center" >}}

Wrapping up, since the overall objective $E(W)$ is being minimized, and this term is being added, the training pushes to make this log term small too. Making $\log(\ldots)$ small means making the sum inside small, which means pushing every $e^{-y_i}$ down, which also means pushing every $y_i$ up (larger distances) across all classes.

So, this fights against the risk we talked about, the training system converging to some average value based on the prototype.

### THE CATCH

Now you say, yeah, ok, but why are we getting so deep in this model's design? LeCun's team was good, we already got that, but this is too much, right?

No, and here I say why. This error calculation formula below also looks like a more modern formula that ended up revolutionizing the training system:

If you get the loss formula from LeNet-5 and change $z_i = -y_i$, it becomes (this change means turning the negative distance into a "score", or, the smaller the distance, the bigger the score):

$$E(W) = -z_{D^p} + \log\left( e^{-j} + \sum_i e^{z_i} \right)$$

And if you compare with the standard softmax cross-entropy loss:

$$\text{CE} = -z_{D^p} + \log\left( \sum_i e^{z_i} \right)$$

It's the same shape. The LeCun team basically reinvented the cross-entropy shape years before it became the standard for classification.

>I think this is amazing.

But later on the CNNs architecture dropped this fixed handmade prototype to use softmax + cross entropy mostly because of generalization possibilities with these one, that doesn't get limited to 0-9 numbers but at some point can cover anything imaginable in images. 


The training also flows backwards in the same behavior as before, it also changes the weights in each connection, which in the end amounts to 60k~ updates in each step:

- C1: 6 maps × (5×5 + 1 bias) = 156
- S2: 6 maps × (1 coefficient + 1 bias) = 12
- C3: 60 sparse connections × 25 weights + 16 biases = 1,516
- S4: 16 maps × (1 coefficient + 1 bias) = 32
- C5: 120 × (16×5×5 + 1 bias) = 48,120
- F6: 84 × (120 + 1 bias) = 10,164

The activation used in the middle which is $tanh$ has the same problem with any loss function but it's a bit worse with MSE as I said in the last post, the gradient vanishing. The complete utilization of the value only happens in the peak of the middle graph so, usually it just uses part of the calculated value (look at the tanh vs its derivative again that makes more sense), and by calculated value I'm talking about the weight times input plus the bias that scales recursively till the last layer. So the weight updates get smaller as we go backwards. 

Here Rectified Linear Unit (RELU) comes into action for the next steps of the neural network development, it's a simple activation function (non-linear function) that is just $f(x) = max(0,x)$ and this means that if the value is negative it becomes 0 and otherwise it keeps as is. With that there is no shrinking in the value after the activation as happened with $tanh$ because now if the value is positive it goes forward unscated, this also apply to backward propagation because now the weight update don't suffer with gradient vanishing anymore.

The tradeoff here is that RELU can suffer with dead neurons, which are the ones that get stuck at 0 so there is no values to propagate forward or backwards, its becomes a dead road in the middle. 

>The solution is a newer Leaky ReLu which changes the function to $f(x) = max(0.1x, x)$ which create a possibility to recover from becoming a dead neuron, but we can talk about that later.

<!-- Next steps for this post (CNN -> AlexNet arc):
1. Cross-entropy + softmax as the fix for MSE + RBF
2. Backprop through conv layers / weight sharing
3. Vanishing gradients with tanh/sigmoid → motivates ReLU
4. The gap years: LeNet-5, AI winter, SVMs displacing NNs for vision
5. AlexNet: closes the arc
-->

<!-- Post 3 (separate topic, not part of this arc):
- RNN | LSTM
- Training at scale (Adam, AdamW, batch norm, LR schedules)
- James briggs ref - https://www.youtube.com/watch?v=ZBfpkepdZlw
-->
<!-- ![Neural Networks](/img/neural_net/neural_networks.png) -->
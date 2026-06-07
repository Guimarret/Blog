---
title: "Neural networks"
date: 2026-05-19T17:58:15-03:00
draft: true
math: true
---

>I just had a uni class about natural language processing and it lit up the need to write about it to reinforce my learning in the topic

Me 2 weeks in the future here, I didn't expect this post to become this big and didn't cover everything I wanted. In the future I'll also cover CNN, RNN, Transformer, and so on. After finishing this post, I thought maybe it's not for everyone because it became a bit too technical with heavy math (I gave my best in simplifying, but I still have a lot to learn,  this is the most I've written in one shot in my life until now). So for those who came here just to peek, here are some recommendations:
- Want some visual reference and not much math? I recommend this [youtube playlist](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi), the 1-3 videos will explain everything from this blog post but more friendly, and the didactics are flawless.
- Some history is embedded in the content. My recommendation is this [page](https://com-cog-book.github.io/com-cog-book/features/roadmap-nn-mod-cog.html), which also walks similarly to mine in the math too, but it's a different pacing.
- Generalist thing about machine learning in general i recommend this [site](https://www.byhand.ai/) from Professor Tom Yeh, he is spectacular and shows things in a way I never even imagined.

I'm going to try to cover everything from zero to present. I am not sure if it will be too technical or anything like that, but I will try to make it focused on didactics. That said, let's start..

# Perceptron
You can think of the perceptron as being the start of neural network applications. It was published in 1958 and explained how we could train artificial neurons to output desired data. The idea is pretty simple, it takes inputs of some type, and based on some parameters and thresholds, it outputs something with the desired behavior.

{{< figure src="/img/neural_net/perceptron.png"
   alt="Diagram of a perceptron: weighted inputs feeding into a summation and a threshold function"
   caption="Figure 1 — The perceptron"
   align="center" >}}

Let's start with a simple example: If you want the neuron to activate (in a binary scenario) when and only when the sum of some inputs is equal to or bigger than 4, you can set the threshold function's minimum value to be 4 for the true case. False for the rest.

There's a catch to make things more flexible: each input also has a weight, which can make it more or less important, like a 0.5 in the first input and a 2 in the second input. This will multiply the 1 in case of true so we can get different relevance for each input.
Considering all this information, we can now think of some situations in which the threshold function is not that obvious and we don't know the ideal weight.
So in this case we have to change it little by little while testing to reach the ideal input. For example, a group of inputs that should output yes or no for a complex question like the buy-more or sell-some action trade (which buy stays for true and sell for false).

### Training and the learning rate

It's kind of complicated to think about for the first time, but it makes sense. We don't care how the weights are set but only if the output is correct. So we have to provide a data source of example with the source of truth, like a datasheet with multiple lines, where each line will have 200 inputs and the desired result.
Then create a function to change the weights individually based on the desired result so it becomes more propitious to get the correct answer.

{{< figure src="/img/neural_net/learning_rates_formula.png"
   alt="Perceptron weight-update formula"
   caption="Figure 2 — Perceptron weight-update rule"
   align="center" >}}

This function can look a bit odd, but it's simple. We have the new calculated value, the current weight that multiplies the input, the learning rate, the input at step time, the expected output at the step time, and the actual output the neuron produced at that step. The correction is driven by the difference between the expected and the actual output (expected − actual), so without comparing the two, there would be nothing to correct.

The most important is the learning rate, which will tell how much correction should be applied. If it's too much, it will be a problem for scenarios in which this input should have less value or the activation shouldn't happen. If it's too little, it will take too long, and you will run this process more times than needed.

If we look from the high ground, it just applies a little change to the weight, which will direct the total sum closer to the desired state. (You can look at it for more time or reflect on it if needed).

But this fix in weight will happen for all the input weights at the same time. This way we get closer to the desired result by a learning rate factor of η. (It's possible it overfits, which would be a neuron specialized in the dataset getting accuracy of 100% in the training runs and 30% in the actual test. But you don't have to give much thought to that for now.)

So after all this mathematics and changing the weights of your perceptron, it becomes actually useful, and when you feed it new real-world data, it outputs with a good accuracy (what is good here depends on context because a probability of rain accuracy of 80% can be okay, I mean, if it misses in 20% of the cases is not the end of the world).  So now you can set up your tech house with multiple sensors and connect everything to your local PC to run and feed the Perceptron and know everything about the chances of your roommate “forgetting” to do the dishes again.

# ADALINE
>I was pondering going directly to multilayer perceptron and explaining backpropagation there. But it would be missing something, so I think ADALINE is a good context bridge. 
This topic will be a bit math-heavy, so take your time to understand and digest the topics. I'm not going to bring anything outside basic math without a proper explanation of what it is and how it works. Some graph visualization will be necessary for simplification, so be ready.

ADALINE came after the perceptron and is the same except for the evolution in training. Just to recap, the error computation in the perceptron is the comparison between the expected output and the current output, which will be subtracted and multiplied by the learning rate and the input value. Also important to observe that it only corrects too much or nothing, which also isn't ideal for training.

First, ADALINE changes the error calculation format, instead of the previously described one, we are going to use what is called the mean squared error. This one can change the weights of the neuron even when it have the correct values. Which creates a more optimized training system.

This system also outputs continuous values, which is completely different from the perceptron that gave a binary result (the threshold only comes back at the very end if you actually need a yes/no). A good example of neuron function that is in ADALINE scope is noise cancellation, which gets the frequency input and the output is the frequency that should be emitted to neutralize. 

### Squared error and MSE

Let's dive into how the MSE (mean squared error) formula works, starting with square errors, which is:
 $$(y_j - \hat{y}_j)^2$$ 

It's simple, we just calculate the square of the difference between the expected and the predicted value.

The mean squared error (MSE) is the "MEAN" of the square error function, so we divide the sum of all square errors summed by the number of times it was summed. Don't be scared of the formula, it's just the mathematical way of representing, and I'm going to leave it here so the nerdy ones just get what I'm talking about without reading everything:

$$MSE = \frac{1}{n} \sum_{j=1}^{n} (y_j - \hat{y}_j)^2 = \frac{1}{n}\left[(y_1 - \hat{y}_1)^2 + \ldots + (y_n - \hat{y}_n)^2\right]$$

But what does this mean, like, how do we use it, and why are we talking about that?

- Sorry for that, but we are going to need more math context to aggregate the meaning of things.

Consider a perceptron with 1 input and 2 weights (bias is a weight, but we can ignore that for now). It will have this format, which is the classic linear function (it's a straight line). The slope will be defined by the weights, and if I can force a bit of your memory, the extra variable would change the starting point of the line. In our case, the B is a phantom constant, and the weight of this constant is the BIAS. Don't give it much thought, and for now just think of it as 0 so it doesn't interfere in the graph, which we can think of as a way to change the threshold talked about before. (Make it easier to be reached, for example.)

$$\hat{y} = w_1 b + w_2 x_1$$

When we plot that (insert into a graph), we unlock some visual properties:

{{< figure src="/img/neural_net/function_plot.jpg"
   alt="Linear function plotted against data points, showing the best-fit line"
   caption="Figure 3 — Linear function fit (linear regression)"
   attr="Plot source"
   attrlink="https://com-cog-book.github.io/com-cog-book/features/adaline.html#Threshold-decision-function"
   align="center" >}}


The vertical axis represents the predicted value, and the pink dots the expected values (the real values without the weights).

>This plot represents the linear regression of inputs and outputs, you also don't have to get all the nuances of what this means but it is kind of a trend of the function indicating the relationship between inputs and outputs.

This represents the line that best fits the points in the Cartesian plane. Also thinkable as trying to find a line that reduces the distance between the pink dots and the line, don't forget that the only variable we can change there is the weight. 

### The error surface and minima

At the end of the day, when considering multiple inputs, we are looking for the “minimum” total squared errors (which is summed across all data points). So to demonstrate a real situation with two inputs (it's not possible to visualize more dimensions, too, so we are going to show everything from now on considering only two inputs and generalize for more inputs):

{{< figure src="/img/neural_net/error_surface_1.png" 
   alt="Convex error surface (bowl shape) over two weights" 
   caption="Figure 4 — Error surface (convex bowl)" 
   align="center" >}}

>In optimization maths this is a [convex optimization](https://en.wikipedia.org/wiki/Convex_optimization) problem.

This graph represents the influence of the weights in the inputs when compared to the sum of squared errors.

As said before, we are looking for the lowest point in the vertical axis that has the lowest value for the sum of error, which means the best pair of weights for every input possible or even the optimal function. The name of this lowest point is minima. 

In the case of ADALINE only a unique minima is possible because it's an exclusive convex problem, but in other situations you could have multiple bases/low points. Of course only one would be the lowest, which is called the global minima but could have other local minimas that's called local minima.

>Cool view of neural networks is that all of it is just some optimization problem in which, given some input, we want to achieve the lowest error summing rates.

### Gradient Descent algorithm

This algorithm is the union of the Loss function(MSE) with some tweaks to reach the minima. I really mean just minima because it works for convex and nonconvex problems, but in the latter it is not guaranteed to reach the global minima.

So, considering this plot:

{{< figure src="/img/neural_net/gradient_desc.png" 
   alt="Non-convex error surface with multiple minima" 
   caption="Figure 5 — Non-convex error surface" 
   align="center" >}}

We can think again about earlier observations, we want to reach the minima but how do we use the MSE in the learning process? We already know looking at the plot what's the direction but how we generalize this and apply in some perceptron with more than 2 inputs.

First let me put the MSE function here again:

$$E(\hat{y}, y) = \frac{1}{n} \sum_{j=1}^{n} (\hat{y}_j - y_j)^2$$

Think about that function, what if we could test the result of MSE if we slightly changed the weight? 

If the MSE reduced means we are walking in the right direction, if not we can go make the opposite weight change, like instead of increase we decrease it.

There is a mathematical way of testing a function with the smallest possible value to get the answer we need. But it's gonna return us a new function which is always point to the steepest ascent. (Derivatives) Here is the mathematical show off:

Start with the squared error function because we can change it at input value level, so it can optimize the weights even more specifically:

$$L(w) = (\hat{y} - y)^2$$

Take the derivative with respect to the weight $w$ also the $x$ here comes from the derivative of the predicted value $\hat{y}$ which is $w$.$x$:

$$\frac{\partial L}{\partial w} = 2(\hat{y} - y) \cdot x$$

This derivative tells us the direction in which $L$ increases fastest. Since we want $L$ to decrease, we step in the opposite direction by flipping the sign, also we are gonna call this derivative as the calculated gradient:

$$w_{\text{new}} = w_{\text{old}} - \eta \, \Delta w$$

So the recap is we got the error function, applied a property called derivation which tell us where the steepest ascent is and inverted it's value to run towards the lowest level which is a minima (local for ADALINE and maybe global for nonconvex optimization problems).

Reminder that the \(\eta \) is just the learning rate which we want. If it's too big it will start jumping around and if is too small it will take too much time to reach the optimal goal, as we can see in the image:

{{< figure src="/img/neural_net/learning_rate.png" 
   alt="Effect of the learning rate: small steps converge slowly, large steps overshoot" 
   caption="Figure 6 — Learning rate" 
   align="center" >}}

This way we just discovered the GRADIENT DESCENT algorithm, not that bad right?

# Multilayer perceptron

First, why isn't a single perceptron enough? Because it can only split data with one straight line. Take XOR, the rule "true when exactly one input is true":

| $x_1$ | $x_2$ | XOR |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

{{< figure src="/img/neural_net/xor_plot.png" 
   alt="Two panels: on the left the four XOR points, where no single straight line separates the true points (one diagonal) from the false points (the other); on the right two lines combined isolate the true points, which is what a hidden layer does" 
   caption="Figure 7 - XOR isn't linearly separable, but combining two lines (a hidden layer) solves it" 
   align="center" >}}

In the plot the trues end up on one diagonal and the falses on the other, so no single line can separate them, the data is not _linearly separable_. The fix is to stack perceptrons: one line can't split it, but a few lines combined can, and that's exactly what hidden layers do.

This point is a milestone in training models, perceptrons, etc. There are two reasons for that. The first is that stacking layers lets us represent patterns a single perceptron simply can't, since the hidden layer adds the depth needed to capture more complex relationships. The second is the activation function: until now we leaned on the threshold, but it's not differentiable, so it doesn't play well with gradient descent. The sigmoid fixes that because it outputs a smooth range from 0 to 1, and, more importantly, it's differentiable, which is precisely what lets us run gradient descent (and later backpropagation) across multiple layers. This will open new horizons for learning procedures that use gradient descent at scale.

So, let's dive into it. This image represents a multilayer perceptron, and as clearly represented, it has 3 parts: the input, hidden layers, and output.


{{< figure src="/img/neural_net/multilayer_perceptron.png" id="fig8"
   alt="Multilayer perceptron: one simple hidden layer with linear and sigmoid functions" 
   caption="Figure 8 - Multilayer perceptron" 
   align="center" >}}

Not going to elaborate on the inputs and outputs because it's still the same. The hidden layer is like a block that consists of one or multiple linear and nonlinear functions on the same network. 

>Recap: The linear function will change the values with the weights and the nonlinear functions will treat the value to be outputed (simple example here is the threshold function that will be yes if the value is from one point). Another perspective of linear and nonlinear is the graphic, the name already says everything, one will be a line and the other not, and by non linear you can think of curve or the thresholds.

<details style="margin: 1rem 0; padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9;">
<summary style="cursor: pointer; font-weight: 500; color: #000000;"> Click to see the plot comparison</summary>
{{< figure src="/img/neural_net/linear_nonlinear_plot.png" alt="Linear and nonlinear plot" caption="Figure 9 - Linear and nonlinear plot" align="center" >}}
</details>

We already talked about that, but as Figure 8 shows, the _linear_ part represents the trainable pieces, which is the weight adjustment to the values that are being passed.

The news here is that we can put in multiple processing units, so from now on we can consider more neurons involved in the calculations. This also means that we can represent more complexity and granularity in the pattern it can learn. This has two direct implications: the possibility of having more accuracy and overfitting.

### Overfit

When models are trained or tested for some generalization feature, they use some dataset as a source. With that, we can make it follow the desired behavior, but we can't forget that at the end of the day we are searching for some pattern and trying to follow it. If we go too deep, we'll become specialized in this pattern instead of this _behavior_. This phenomenon is what we call overfit. The simplest solution to prevent overfitting is to separate the dataset, usually 80/20, where 80 is the training data and 20 is the test data. Doing that, we can measure the MSE for both executions. The expected behavior is for the training error to be slightly below the test error, I mean, the training run should have a bit less error occurrence (the MSE can also be called the _Loss_ function).

>This gif is example of overfitting happening in polynomial regression, you can increase the polynomial level but eventually it becomes bounded to overfitting, then the _outlier_ which could be the training data will be left out. Our situation is similar, adding more neurons add granularity and accuracy but can converge in this behavior. In other words, reduce the chances of correctly predicting if your roommate will _forget_ the dishes again.

{{< figure src="/img/neural_net/overfitting.gif" 
   alt="Overfitting animation showing polynomial fits from degree 1 to 15" 
   caption="Figure 10 - Polynomial plot overfit" 
   align="center" >}}

## Activations | Sigmoids $\phi$

The sigmoids, also called _activation_ , will be the nonlinear function that will add expressiveness to our models.

You can see it logically. If a value is changed by weights, you can't just change it again without anything in between because it would collapse as one effective multiplication. When testing the model, the value passed in the neuron will be changed twice, and that's all. So we lose the sensitivity of knowing what changed for this specific neuron weight change. For example, 1 x 0.5 x 0.1 is the same as 1 x 0.05.

To change that, we use the nonlinear functions, in this case the sigmoid, but it could be _tanh_ or _ReLU_. These functions will create a bend in the chain between weight changes, so we gain the granularity of two changes, and we can compare two weight changes to the outputted value/desired output value.

<details style="margin: 1rem 0; padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9;">
<summary style="cursor: pointer; font-weight: 500; color: #000000;"> Click to see the math demonstration</summary>

Suppose we have two linear functions:

$$f(x) = w_1 x + b_1$$

$$g(x) = w_2 x + b_2$$

Now let's compose them - feed the output of $f$ into $g$:

$$g(f(x)) = w_2 \cdot f(x) + b_2$$

$$g(f(x)) = w_2 \cdot (w_1 x + b_1) + b_2$$

$$g(f(x)) = w_2 w_1 x + w_2 b_1 + b_2$$

Let $W = w_2 w_1$ and $B = w_2 b_1 + b_2$. The composed function becomes:

$$g(f(x)) = W x + B$$
</details>


{{< figure src="/img/neural_net/why_the_activation.png" 
   alt="Diagram showing why a nonlinear activation function is needed between linear layers" 
   caption="Figure 11 - Why the activation function is needed" 
   align="center" >}}

The sigma function, as represented below, is a function that creates a range that fits every value, so it doesn't matter whether it's bigger or smaller, it will squash everything between 0 and 1. Also, a good use case would be the chance of activation for example, when the value is bigger, it is “more probable” of activating. When we are talking about training, this can mean almost anything, but imagine the chance of some part of the image being straight or curved. When a group of neurons specialized in detecting curves outputs values above 0.90, together they signal that the image contains a curve.

$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

This is the graph plot of this function:

{{< figure src="/img/neural_net/sigma_plot.png" 
   alt="Plot of the sigmoid function squashing values between 0 and 1" 
   caption="Figure 12 - Sigmoid function plot" 
   align="center" >}}

## Cost functions $\mathcal{L}$

For the sake of simplicity, I was keeping just the MSE, but right now we can have some additional thoughts on that. Considering that training is an optimization problem, the way to measure the error can return different results depending on the output. If our optimization has to prioritize normal number outputs, the MSE is great, but if we want some binary classification, it doesn't work too well because of the activation function. The derivative of the sigmoid flattens every loss calculation that's too minimal or too big. If we consider some prediction that the correct answer is 1 and it outputted 0.01, the error is massive but will be invisible after the derivative of the sigmoid. The same happens if the error is minimal or the value is probably correct. The change in the actual optimization is negligible. The plot below shows the effects side by side.

>Recap: Derivatives points to the steepest ascent. The derivative of the sigmoid correction will only make a difference if the value is _existent_.

{{< figure src="/img/neural_net/derivative_sigmoid.png" 
   alt="Sigmoid and its derivative plotted side by side, the derivative peaking near zero and flattening at the tails" 
   caption="Figure 13 - Derivative of the sigmoid" 
   align="center" >}}

With this we can imply that the sigmoids shouldn't be used for linear and continuous values while keeping the MSE (mean square error), because the training can be ineffective in the low and high gap. While in binary classification, we should avoid the use of MSE.

So the solution for binary classification is:

### Binary cross entropy

This loss function, contrary to the MSE, performs well in binary classifications. 

>Recap: the $\hat{Y}_i$ is the predicted value and the $Y_i$ is the true label/correct value from the training dataset.

> We will always use the negative log because numbers will always range 0 and 1 and this range always returns negative log but still super convenient for quantitative measuring in our case.

>Math reminder $log(1) = 0$ and $log(0) = -\infty$

$$ - (Y_i \cdot \log \hat{Y}_i + (1 - Y_i) \cdot \log(1 - \hat{Y}_i))$$

<details style="margin: 1rem 0; padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9;">
<summary style="cursor: pointer; font-weight: 500; color: #000000;"> Click if you want to see the explanation of why 0 and 1 are not going to show up</summary>
It could be a problem if we get the predicted value equal to 0 or 1, but remember that the cost functions are calculated considering all the linear and nonlinear steps from the network. As I said before, for binary classifications, the activation function is highly recommended (in this case again I'm going to cover only the sigmoid), and the output range is 0 and 1. Mathematically, it never reaches these values (the system can round the number to 0 or 1 if it is too close, but training algorithms usually cap at a minimal value to avoid this situation). If you try to compute $log(0)$, it's going to get a NAN error, and the same goes for numbers too close to 1, so we are safe.
</details>

Let's split the function into two parts:

$$ - (Y_i \cdot \log \hat{Y}_i)$$

This one I'll call the positive part. Here we calculate how well the network predicted the positive class when the answer really was close to 1, because if the correct value is 1, it will multiply the log calculated by one. Therefore, consider 100% of the $\log \hat{Y}_i$, so it attaches something like a weight for how much this error measure is important for positive values.

While in the other part (the negative one), it calculated how well the network predicted the negative class when the answer was close to 0. We multiply the log of $1 - \hat{Y}_i$ (one minus the predicted value) times $1 - Y_i$ because it will multiply 100% of the log only if the $Y_i$ (expected value) is 0, otherwise, it will remove the importance of the calculated log of $1 - \hat{Y}_i$.

$$- ((1 - Y_i) \cdot \log(1 - \hat{Y}_i))$$

This table shows the relation of the sliced parts when put together:

| True label $Y$ | Part A | Part B | Active formula |
|---|---|---|---|
| 1 | $\log(\hat{Y})$ | 0 | $\mathcal{L} = -\log(\hat{Y})$ |
| 0 | 0 | $\log(1 - \hat{Y})$ | $\mathcal{L} = -\log(1 - \hat{Y})$ |

And the plot relation is this:

{{< figure src="/img/neural_net/binary_cross_entropy_plot_agg.png" 
   alt="Binary cross-entropy loss curves: the positive-class term, the negative-class term, and their aggregate plotted against the predicted value" 
   caption="Figure 14 - Cross entropy plot for positive, negative, and agg" 
   align="center" >}}

Also for the optimizing part, it becomes as simple as the MSE.

<details style="margin: 1rem 0; padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9;">
<summary style="cursor: pointer; font-weight: 500; color: #000000;"> ⁣Click if you want to see the math steps of this derivation</summary>
$$
\mathcal{L} = -\left[ Y \log \hat{Y} + (1 - Y) \log(1 - \hat{Y}) \right]
$$

$$
\frac{\partial \mathcal{L}}{\partial \hat{Y}} = \frac{\partial}{\partial \hat{Y}} \left[ -Y \log \hat{Y} \right] + \frac{\partial}{\partial \hat{Y}} \left[ -(1-Y) \log(1 - \hat{Y}) \right]
$$

$$
= -\frac{Y}{\hat{Y}} + \frac{1-Y}{1 - \hat{Y}}
$$

$$
= \frac{-Y(1 - \hat{Y}) + (1-Y)\hat{Y}}{\hat{Y}(1 - \hat{Y})}
$$

$$
= \frac{-Y + Y\hat{Y} + \hat{Y} - Y\hat{Y}}{\hat{Y}(1 - \hat{Y})}
$$

$$
\frac{\partial \mathcal{L}}{\partial \hat{Y}} = \frac{\hat{Y} - Y}{\hat{Y}(1 - \hat{Y})}
$$
</details>

We calculate the derivative of the binary cross-entropy to find the gradient descent and find the steepest ascent. Then just use the negative of this result to find the steepest descent, which is the optimal scenario to reduce the _Loss_:

$$\frac{\partial \mathcal{L}}{\partial \hat{Y}} = \frac{\hat{Y} - Y}{\hat{Y}(1 - \hat{Y})}$$

## Backpropagation algorithm

Now for the actual training, we already know how to apply the gradient descent using two functions (mean square error, binary cross-entropy) in a unique weight situation, but what about multilayer and multineuron?

Let's start visualizing a multilayer example (one neuron per layer):

{{< figure src="/img/neural_net/multineuron.png" 
   alt="Multilayer network with one neuron per layer: input, two hidden layers with activations, and output, with 3 weights and biases feeding the z and activation functions below" 
   caption="Figure 15 - Multilayer (one neuron per layer) visualization" 
   align="center" >}}

Here we can find a neuron with 2 hidden layers, both with an activation function and the output also with an activation function. There are 3 weights in the diagram and arrows pointing where each one fits in the value at point L function.

The variable $z^{(L)}$ is the value being passed after weight and bias calculation at point L when submitted to the function $f(z^{(L)})$ is $a^{(L)}$.

This $f()$ function is just a placeholder for any function, usually activation functions $\phi$, but can be used as identity functions (which do nothing so it only compacts the weights from both sides as we talked before) too in case of MSE regressions.

With these functions and the draw in mind:

$$z^{(L)} = w^{(L)} a^{(L-1)} + b^{(L)}$$

$$a^{(L)} = f(z^{(L)})$$

This is the sequence from input to the output:

$$x \to z^{(L-2)} \to a^{(L-2)} \to z^{(L-1)} \to a^{(L-1)} \to z^{(L)} \to a^{(L)}$$

And this is the feedforward where the values pass once and then proceed to training based on error.

>Now we start to cook the backpropagation idea, think that we want to make the system more optimized aka change the weights to increase the accuracy, push the output towards our goals and how do we do that? Apply derivatives to find the steepest ascent for each layer. I'm gonna use as example the MSE as error function to simplify the steps (the binary cross entropy adds a bit too much visual noise).

>Recap: everything we're about to do is just the _chain rule_ from calculus. When a value passes through a stack of functions, the derivative of the whole thing is the product of the derivative of each step. Backpropagation is literally that rule applied layer by layer, walking from the output back to the input.

> We are not gonna use activation function so I'm obfuscating the $a$ for the $z$ directly, so consider the $z^{(L)} = w^{(L)} z^{(L-1)} + b^{(L)}$

<details style="margin: 1rem 0; padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9;">
<summary style="cursor: pointer; font-weight: 500; color: #000000;"> Click if you want to see the math without hiding the $a$</summary>
The $f$ is the identity function, which does nothing but still is the activation function.

So, consider $a^{(L)} = f(z^{(L)})$:

$$\frac{\partial a^{(L)}}{\partial z^{(L)}} = f'(z^{(L)})$$

$$\nabla^{(L)} = 2(a^{(L)} - y) \cdot f'(z^{(L)})$$
</details>

For the _Loss_ function we use (the per-example version doesn't divide by $n$) $\text{MSE} = (z^{(L)} - y)^2$. If we look to the $z^{(L)}$ we can see that it is dependent on the $z$ from the last layer, so let's insert all $z$ until the input in the function to simplify and get the cost ($\mathcal{L}$):

$$\mathcal{L} = \left( w^{(L)} w^{(L-1)} w^{(L-2)} x + w^{(L)} w^{(L-1)} b^{(L-2)} + w^{(L)} b^{(L-1)} + b^{(L)} - y \right)^2$$

Let's first take the derivative of the cost regarding the input $x$, just to expose the shape of the chain, the gradient stands as a product of weights times the output error (we'll turn this into the actual weight and bias updates right after):

$$\frac{\partial \mathcal{L}}{\partial x} = w^{(L-2)} \cdot w^{(L-1)} \cdot w^{(L)} \cdot 2(z^{(L)} - y)$$

The completely open version after the derivative calculation (the biases are constants with respect to $x$, so they drop out of the leading weight product and only survive inside the residual):
$$\frac{\partial \mathcal{L}}{\partial x} = w^{(L-2)} \cdot w^{(L-1)} \cdot w^{(L)} \cdot 2\left( w^{(L)} w^{(L-1)} w^{(L-2)} x + w^{(L)} w^{(L-1)} b^{(L-2)} + w^{(L)} b^{(L-1)} + b^{(L)} - y \right)$$

>The innermost factor $2(z^{(L)} - y)$ is the only part that depends on the output error, everything in front of it is just the stacked chain of weights. That error factor is what we call the delta $\nabla^{(L)}$, and we anchor it at the layer's pre-activation $z^{(L)}$, not at the input $x$:

$$\nabla^{(L)} = \frac{\partial \mathcal{L}}{\partial z^{(L)}} = 2(z^{(L)} - y)$$

To actually update the weight $w^{(L)}$ from the last connection, we need the gradient with respect to that weight, not with respect to $x$. Since $z^{(L)} = w^{(L)} z^{(L-1)} + b^{(L)}$, the chain gives the delta times the value that fed into the weight:

$$\frac{\partial \mathcal{L}}{\partial w^{(L)}} = \nabla^{(L)} \cdot z^{(L-1)}$$

$$w^{(L)}_{\text{new}} = w^{(L)}_{\text{old}} - \eta \cdot \nabla^{(L)} \cdot z^{(L-1)}$$

And then the actual backpropagation, which is applying that recursively, each layer's $\nabla$ is computed from the next layer's $\nabla$ times the weight connecting them. 

$$\nabla^{(\ell-1)} = \nabla^{(\ell)} \cdot w^{(\ell)}$$ 

If you think about it, the error signal at any layer depends on how wrong the layer in front of it was. So we walk backward through the network, each layer reusing the next layer's $\nabla$ to compute its own, but since each step multiplies by another weight (and another activation derivative if you're using one), the error signal shrinks as it travels backward. The output layer gets the biggest correction, and each earlier layer gets a smaller and smaller piece of it.

The bias gradient is simpler than the weight gradient, there's no input multiplier because the bias isn't multiplied by anything in the forward pass ($\partial z^{(L)} / \partial b^{(L)} = 1$), so it's just the delta itself:

$$\frac{\partial \mathcal{L}}{\partial b^{(L)}} = \nabla^{(L)}$$

>The bias gradient equals the raw delta only because the activation here is the identity, in nonlinear activations the delta also carries the activation derivative. 

$$b^{(L)}_{\text{new}} = b^{(L)}_{\text{old}} - \eta \cdot \nabla^{(L)}$$

### Vanishing gradients

We just saw that each step backward multiplies by another weight and another activation derivative. Now look back at the sigmoid derivative plot, it peaks at 0.25 and gets to almost zero on both tails. So every layer you go back, you're multiplying by something that's at most 0.25 and usually way less.

Multiply a bunch of small numbers together and you can guess what happens: the gradient shrinks fast. $0.25 \times 0.25 \times 0.25$ is already $0.015$. After a handful of layers the correction reaching the early layers is basically nothing, so the first layers barely learn anything. This is called the _vanishing gradient_ problem, and it's the main reason deep networks were so painful to train for a long time.

It's also why people mostly moved away from the sigmoid in the hidden layers. The _ReLU_ (the one we name-dropped earlier) helps a lot here: for positive values its derivative is just 1, so it doesn't squash the signal on the way back, the gradient stays alive through many layers. (It has its own quirks, like neurons that get stuck at zero, but that's a story for another day.)

### Nonlinear activations

Here I'm just going to show the same procedure but without obfuscating the activation.

So, consider $a^{(L)} = f(z^{(L)})$:

$$\frac{\partial a^{(L)}}{\partial z^{(L)}} = f'(z^{(L)})$$

The $f(z^{(L)})$ is the generalized function, and the cost function for this will be:

$$\mathcal{L} = (a^{(L)} - y)^2$$

And the completely opened version:

$$\mathcal{L} = \Big( f\big(w^{(L)} \cdot f(w^{(L-1)} \cdot f(w^{(L-2)} \cdot x + b^{(L-2)}) + b^{(L-1)}) + b^{(L)}\big) - y \Big)^2$$

Now the derivative version of the complete one, and one more time it's the way we have to find the minima:

$$\frac{\partial \mathcal{L}}{\partial x} = w^{(L-2)} \cdot f'(z^{(L-2)}) \cdot w^{(L-1)} \cdot f'(z^{(L-1)}) \cdot w^{(L)} \cdot f'(z^{(L)}) \cdot 2(a^{(L)} - y)$$

We just did the same as before, but instead of proceeding just with the weights because of the activation functions that did nothing, here we open with the actual activation function. It works the same way at the end of the day. 

The gradient for the last layer will be the same as the other one, but instead of just multiplying the weight, we multiply the whole derivative of the activation:

$$\nabla^{(L)} = 2(a^{(L)} - y) \cdot f'(z^{(L)})$$

And the next layer gradient will be similar to the simplified version, just added the obfuscated part but already derived $f'(z^{(L-1)})$

>Pay attention to the ' in the $f'$ it means it's the derivative version of the function. 

$$\nabla^{(L-1)} = \nabla^{(L)} \cdot w^{(L)} \cdot f'(z^{(L-1)})$$

The complete process of weight updating within all phases will be similar to the simplified version too:

$$\frac{\partial \mathcal{L}}{\partial w^{(L)}} = \nabla^{(L)} \cdot a^{(L-1)}$$

$$\frac{\partial \mathcal{L}}{\partial w^{(L-1)}} = \nabla^{(L-1)} \cdot a^{(L-2)}$$

$$\frac{\partial \mathcal{L}}{\partial w^{(L-2)}} = \nabla^{(L-2)} \cdot x$$

The bias calculation is going to be a bit different from the simplified version too because the gradient will change from the one we talked about in the last line. Now the bias will also be part of the activation:

$$\frac{\partial \mathcal{L}}{\partial b^{(L)}} = \nabla^{(L)}$$

$$\frac{\partial \mathcal{L}}{\partial b^{(L)}} = 2(a^{(L)} - y) \cdot f'(z^{(L)})$$

$$\frac{\partial \mathcal{L}}{\partial b^{(L-1)}} = \nabla^{(L)} \cdot w^{(L)} \cdot f'(z^{(L-1)})$$

$$\frac{\partial \mathcal{L}}{\partial b^{(L-2)}} = \nabla^{(L-1)} \cdot w^{(L-1)} \cdot f'(z^{(L-2)})$$

With this we get the weights and the bias updated based on the measured error. We also know how to train and update it backwards, keeping in check how much each detail impacted. Now I'm going to go with the last main point of the backprop algorithm, multineuron in multilayer.

### Multineuron multilayer

It doesn't change much from the multilayer with one neuron in each layer as we already saw, but it gets a bit tricky because of the notation, it's a lot of indices to keep track of.

A simple representation of how the activation and the weight lines will be noted:

{{< figure src="/img/neural_net/index_update.png" 
   alt="Two neurons connected by a weight, showing the index notation: activation a_k from layer L-1 feeding neuron a_j in layer L through weight W_jk" 
   caption="Figure 16 - Weight index notation between two neurons" 
   align="center" >}}

Yes, the weight looks weird, like inverted, but that's how it is. We can read as the activation from the last layer $L-1$ and position $k$ (here position is like horizontally, we can have multiple floors of neurons pointing to the layer from $L$ for example), and the $j$ from the neuron in $L$ is the same as $k$ with a different notation. 

{{< figure src="/img/neural_net/multilayer_multiunit.png" 
   alt="Multineuron multiunit" 
   caption="Figure 17 - Multi-unit Multineuron visualization" 
   align="center" >}}

This is the draw we are going to use as an example to move forward.

I'll reintroduce the $z$ formula but now consider multiple neurons on the same floor and the activation function:

$$z_j^{(L)} = w_{j0}^{(L)} a_0^{(L-1)} + w_{j1}^{(L)} a_1^{(L-1)} + w_{j2}^{(L)} a_2^{(L-1)} + b_j^{(L)}$$

$$a_j^{(L)} = \sigma(z_j^{(L)})$$ 

The only difference is that now we sum all the weights connecting the last layer to this neuron. 


The _Loss_ ($\mathcal{L}$) function will add this $k$ index, which refers to the "floor" the neuron is in the said layer (this works for unified output layers).

$$\mathcal{L} = \sum_{k=1}^{K} (a_k^{(L)} - y_k)^2$$

In our image the output layer has 2 independent neurons, so the total loss is just the sum of the squared error of each one:

$$ \mathcal{L} = (a_0^{(L)} - y_0)^2 + (a_1^{(L)} - y_1)^2$$

And our gradient descent (derivative of the cost function) will be:

$$\nabla_0^{(L)} = 2(a_0^{(L)} - y_0) \cdot f'(z_0^{(L)})$$

$$\nabla_1^{(L)} = 2(a_1^{(L)} - y_1) \cdot f'(z_1^{(L)})$$

>The bias gradient calculation for the output neurons and one bias update:

$$\frac{\partial \mathcal{L}}{\partial b_j^{(L)}} = \nabla_j^{(L)} = 2(a_j^{(L)} - y_j) \cdot f'(z_j^{(L)})$$

$$b_j^{(L)} = b_j^{(L)} - \eta \cdot \nabla_j^{(L)}$$

So, for the weights update based on the gradient descent:

$$w_{jk}^{(L)} = w_{jk}^{(L)} - \eta \cdot \nabla_j^{(L)} \cdot a_k^{(L-1)}$$

<details style="margin: 1rem 0; padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9;">
<summary style="cursor: pointer; font-weight: 500; color: #000000;"> Click if you want to see the calculations for all the weights from $L$</summary>

$$w_{00}^{(L)} = w_{00}^{(L)} - \eta \cdot \nabla_0^{(L)} \cdot a_0^{(L-1)}$$

$$w_{01}^{(L)} = w_{01}^{(L)} - \eta \cdot \nabla_0^{(L)} \cdot a_1^{(L-1)}$$

$$w_{02}^{(L)} = w_{02}^{(L)} - \eta \cdot \nabla_0^{(L)} \cdot a_2^{(L-1)}$$

$$w_{10}^{(L)} = w_{10}^{(L)} - \eta \cdot \nabla_1^{(L)} \cdot a_0^{(L-1)}$$

$$w_{11}^{(L)} = w_{11}^{(L)} - \eta \cdot \nabla_1^{(L)} \cdot a_1^{(L-1)}$$

$$w_{12}^{(L)} = w_{12}^{(L)} - \eta \cdot \nabla_1^{(L)} \cdot a_2^{(L-1)}$$

</details>

>Important to say that each weight is independent so the updates have to pass by all of them one by one, of course the gradient descent itself are just two calculation, for $\nabla_0$ and $\nabla_1$. I know it looks inefficient but for the sake of didactics it's worth. After this topic I'm gonna introduce how it is actually done in computation and real world because this way would be too slow.

For the $L-1$ layer, we are going to sum the gradients from the output and multiply by the activation function of the neuron being calculated:

$$\nabla_j^{(L-1)} = \left( \sum_{i=0}^{n_L - 1} \nabla_i^{(L)} \cdot w_{ij}^{(L)} \right) \cdot f'(z_j^{(L-1)})$$

In our case at layer $L-1$ this is the calculation for each gradient:

$$\nabla_0^{(L-1)} = \left( \nabla_0^{(L)} \cdot w_{00}^{(L)} + \nabla_1^{(L)} \cdot w_{10}^{(L)} \right) \cdot f'(z_0^{(L-1)})$$

$$\nabla_1^{(L-1)} = \left( \nabla_0^{(L)} \cdot w_{01}^{(L)} + \nabla_1^{(L)} \cdot w_{11}^{(L)} \right) \cdot f'(z_1^{(L-1)})$$

$$\nabla_2^{(L-1)} = \left( \nabla_0^{(L)} \cdot w_{02}^{(L)} + \nabla_1^{(L)} \cdot w_{12}^{(L)} \right) \cdot f'(z_2^{(L-1)})$$

This same delta recursion generalizes to any inner layer $\ell$, summing the deltas from the layer in front of it:

$$\nabla_j^{(\ell)} = \left( \sum_{i=0}^{n_{\ell+1} - 1} \nabla_i^{(\ell+1)} \cdot w_{ij}^{(\ell+1)} \right) \cdot f'(z_j^{(\ell)})$$

And just like in the single-neuron case, the bias gradient for each inner-layer neuron is simply its own delta (no input multiplier):

$$\frac{\partial \mathcal{L}}{\partial b_j^{(\ell)}} = \nabla_j^{(\ell)}$$

And that's it, you can just continue applying the weight changing for each layer progressively, and the model will continue learning.

<!-- ## CNN -->

<!-- RNN | LSTM-->

<!-- Training at scale (Adam, AdamW) -->
<!-- ![Neural Networks](/img/neural_net/neural_networks.png) -->

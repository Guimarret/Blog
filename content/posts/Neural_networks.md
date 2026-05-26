---
title: "Neural networks"
date: 2026-05-19T17:58:15-03:00
draft: true
---

>I just had a uni class about natural language processing and it lit up the need to write about to reinforce my learning in the topic

# Foundations

I'm going to try to cover everything from zero to present. I am not sure if it will be too technical or anything like that, but I will try to make it focused on didactics. That said, let's start..

## Perceptron
You can think of the perceptron as being the start of neural network applications. It was published in 1958 and explained how we could train artificial neurons to output desired data. The idea is pretty simple, it takes inputs of some type, and based on some parameters and thresholds, it outputs something with the desired behavior.

![perceptron](/img/neural_net/perceptron.png)

Let's start with a simple example: If you want the neuron to activate (in a binary scenario) when and only when the sum of some inputs is equal to or bigger than 4, you can set the threshold function's minimum value to be 4 for the true case. False for the rest.

There's a catch to make things more flexible: each input also has a weight, which can make it more or less important, like a 0.5 in the first input and a 2 in the second input. This will multiply the 1 in case of true so we can get different relevance for each input.
Considering all this information, we can now think of some situations in which the threshold function is not that obvious and we don't know the ideal weight.
So in this case we have to change it little by little while testing to reach the ideal input. For example, a group of inputs that should output yes or no for a complex question like the buy-more or sell-some action trade (which buy stays for true and sell for false).

It's kind of complicated to think about for the first time, but it makes sense. We don't care how the weights are set but only if the output is correct. So we have to provide a data source of example with the source of truth, like a datasheet with multiple lines, where each line will have 200 inputs and the desired result.
Then create a function to change the weights individually based on the desired result so it becomes more propitious to get the correct answer.

![formula_error_correct](/img/neural_net/learning_rates.png)

This function can look a bit odd, but it's simple. We have the new calculated value, the current weight that multiplies the input, the learning rate, the input at step time, and the expected output at the step time.

The most important is the learning rate, which will tell how much correction should be applied. If it's too much, it will be a problem for scenarios in which this input should have less value or the activation shouldn't happen. If it's too little, it will not activate the function, and you will run this process more times than needed.

If we look from the high ground, it just applies a little change to the weight, which will direct the total sum closer to the desired state. (You can look at it for more time or reflect on it if needed).

But this fix in weight will happen for all the input weights at the same time. This way we get closer to the desired result by a learning rate factor of η. (It's possible it overfits, which would be a neuron specialized in the dataset getting accuracy of 100% in the training runs and 30% in the actual test. But you don't have to give much thought to that for now.)

So after all this mathematics and changing the weights of your perceptron, it becomes actually useful, and when you feed it new real-world data, it outputs with a good accuracy (what is good here depends on context because a probability of rain accuracy of 80% can be okay, I mean, if it misses in 20% of the cases is not the end of the world).  So now you can set up your tech house with multiple sensors and connect everything to your local PC to run and feed the Perceptron and know everything about the chances of your roommate “forgetting” to do the dishes again.

## Multi-Layer Perceptron (MLP)
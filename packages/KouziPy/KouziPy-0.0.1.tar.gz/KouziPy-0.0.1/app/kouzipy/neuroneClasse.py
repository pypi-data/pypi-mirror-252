import random
import math


class Neurone:
    def __init__(self, Ninput):
        self.Weight = [random.randint(1, 999) / 1000 for o in range(Ninput)] # initalization of the weight (random)
        self.Bias = random.randint(1, 999) / 1000 # initalization of the bias (random)
        self.grad = [0 for o in range(Ninput)] # initalization of the gradients (default 0)
        self.batch_grad = [] # all the gradients before optimization
        self.Bias_grad = 0 # initalization of the bias (default 0)
        self.INPUT = 0 # the input of the neuron
        self.loss = False # the result of the cost function (default false)
        self.Y = False # the output of the model (default false)
        self.Y_HAT = False # the neuron output

    def set_zero(self):  # set all wheits to 0
        self.Weight = [0 for o in range(len(self.Weight))]

    def set_bias(self, b): # set the bias
        self.Bias = b

    def set_Y(self, Y): # set output
        self.Y = Y

    def set_weight(self, p): # set the weight of the neuron
        self.Weight = p

    def set_bias(self, b): # set the bias of the neuron
        self.Bias = b 

    def get_weights(self): # get the weights of the neuron
        return self.Weight
    
    def get_bias(self): # get the bias of the neuron
        return self.Bias

    def zero_grad(self): # set all the gradients to 0
        for o in range(len(self.grad)):
            self.grad[o] = 0

    def ReLu(self, x): # The Relu function
        return max(0, x)
    
    def ReLuDx(self, x): # The derivitive of Relu 
        if x > 0:
            return 1
        return 0
    
    def Sigmoid(self, x): # The sigmoid function
        if x > 150:
            x = 150
        if x < -150:
            x = -150
        return 1 / (1 + math.exp(-x))

    def SigmoidDx(self, x): # The derivitive of the sigmoid
        return -math.exp(-x) / (1 + 2*math.exp(-x) + math.exp(-2*x))

    def forward(self, data_inp, activ_function): # compute the output of the neuron with his inputs and his activations functions
        total = 0 # the output
        self.INPUT = data_inp # set the input of the neuron 
        for o in range(len(self.Weight)): # multiply all the weight with their respectives inputs
            total += self.Weight[o] * data_inp[o]
        total += self.Bias # Add the bias

        # compute the output with the activation function
        if activ_function == "relu":
            total = self.ReLu(total)
        elif activ_function == "sigmoid":
            total = self.Sigmoid(total)
        self.Y_HAT = total # set the output of the neuron
        return total
    
    def backward(self, multi=1): # Compute the gradients of the neuron
        # the variable multi will be explaine in the model class but for the rest this is how to compute gradients
        # 2 * (self.Y_HAT - self.Y) is the partial derivitive of the cost function respect to the output
        # self.INPUT[i] is the partial derivitive of the neuron respect to the weight 
        for i in range(len(self.Weight)): # Compute the gradients for each neuron
            self.grad[i] = 2 * (self.Y_HAT - self.Y) * multi * self.INPUT[i]
        self.Bias_grad = 2 * (self.Y_HAT - self.Y) * multi # and for the bias
        self.batch_grad.append([self.grad[i] for i in range(len(self.grad))]) # add the gradient to batch_gradient
        # The batch_grad will be explain in the model class

    def gradient_mean(self): # compute the mean of all the gradients in the batch_grad to get the finals gradients
        for oo in range(len(self.grad)):
            value = 0
            for o in range(len(self.batch_grad)):
                value += self.batch_grad[o][oo]
            self.grad[oo] = value / len(self.batch_grad)

    def reset_batch_grad(self): # read the name of the function and you will certainly understand what it does
        self.batch_grad = []
        
    def optimizer(self, alpha): # update all the weight with the gradients and the learning rate
        for i in range(len(self.Weight)):
            self.Weight[i] -= alpha * self.grad[i]
        self.Bias -= alpha * self.Bias_grad
        

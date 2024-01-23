import random
import math
from LayerClass import Layer


class Model:
    def __init__(self, layer_tup):
        self.all_layer = layer_tup # initalization of the model
        self.W = [lw.weight for lw in self.all_layer] # initalization of all the weights (from the layers)
        self.B = [lb.bias for lb in self.all_layer]  # initalization of all the bias (from the layers)
        self.grad = [o.grad for o in self.all_layer] # initalization of all the gradients (from the layers)
        self.Bias_grad = [o.Bias_grad for o in self.all_layer] # initalization of all the bias grads (from the layers)
        self.activation_function = [0 for o in self.all_layer] # initalization of all the activations functions
        self.batch_grad = [] # list who contains all the gradients calculated of all the data of the batch. the finals gradients will be compute from the mean of those
        self.nperl = [len(self.all_layer[o].neurones) for o in range(len(self.all_layer))] # represent the number of neurons for each layer
        self.YHAT = 0 # the model's prediction
        self.Y = 0 # the value that the model has to reach
        self.all_YHAT = [] # all the outputs of all layers and all neurons
        self.LOSS = False # the actual value computed by the cost function

    def set_weight(self, poids): # set the weights of the model
        for o in range(len(self.all_layer)):
            self.all_layer[o].set_weight(poids[o])

    def set_bias(self, biais): # set the bias of the model
        for o in range(len(self.all_layer)):
            self.all_layer[o].set_bias(biais[o])

    def set_activation_function(self, all_func): # set the activations functions
        # all_func is a list of the function ordered (respect to each layer)
        for o in range(len(all_func)): 
            if all_func[o] == 1:
                self.activation_function[o] = "relu"
            elif all_func[o] == 2:
                self.activation_function[o] = "sigmoid"
            elif all_func[o] == 0:
                self.activation_function[o] = 0 # no activation function for the layer
            else:
                print("Message from Kouzi: This activation function is not define")

    def zero_grad(self): # set all the gradients to 0 (for each layer and neurons)
        for o in range(len(self.all_layer)):
            self.all_layer[o].zero_grad()
            self.grad[o] = self.all_layer[o].grad

    def get_weights(self): # get all the weight of the model
        self.W = [w.get_weights() for w in self.all_layer]
        return self.W
    
    def get_bias(self): # get all the bias of the model
        self.B = [o.get_bias() for o in self.all_layer]
        return self.B
    
    def get_grads(self): # get all the gradients of the model
        self.grad = [o.get_grads() for o in self.all_layer]
        return self.grad
    
    def get_bias_grads(self): # get all the bias grad of the model
        self.Bias_grad = [o.get_bias_grads() for o in self.all_layer]
        return self.Bias_grad
    
    def ReLu(self, x="Kouzi"): # the relu function 
        if x == "Kouzi":
            return 1 # if the x is not given that mean that the function is only a name
        return max(0, x)
    
    def ReLuDx(self, x): # the derivative of the relu function
        if x > 0:
            return 1
        return 0
    
    def Sigmoid(self, x="Kouzi"): # the sigmoid function
        if x == "Kouzi":
            return 2 # if the x is not given that mean that the function is only a name
        return 1 / (1 + math.exp(-x))

    def SigmoidDx(self, x): # the derivative of the sigmoid function
        return -math.exp(-x) / (1 + 2*math.exp(-x) + math.exp(-2*x))
    
    def forward_pass(self, Input): # compute the prediction of the model
        layer_out = Input  # the output of the model
        for o in range(len(self.all_layer)): # for each layer...
            layer_out = self.all_layer[o].forward_layer(layer_out, self.activation_function[o]) # compute the layer's output
            self.all_YHAT.append(layer_out) # collect all the layers's output 
        return layer_out
    
    def Loss(self, pred, y): # a quadratic cost function
        # pred is the prediction of the model
        # y is the value that the model was supposed to give
        self.YHAT = pred
        self.Y = y
        self.LOSS = (pred[0] - y)**2 # pred[0] because the pred value is given in a list
        return self.LOSS
    
    def backward(self):
        factors = [1 for o in range(self.nperl[0])] # set all the factors to 1
        # the factors will be the partials derivitives depending on the layer for each neurons
        self.get_weights() # juste to be sure that the model's weight has been correctly updated from all the neurons 

        for i in range(len(self.all_layer)): # for each layer...
            if i > 0: # don't need to compute the the factors if i == 0 because we are at the first layer
                for o in range(self.nperl[i]): # for each neurons...
                    factors[o] = factors[o] * self.W[len(self.all_layer)-i-1][o][o] # compute the partial derivitive (truct my calculations)
                    # the factors are multiply by their respectives weight because the derivitive of a linear function respect to x is a constant (=> his weight)
                    # we are muliplying the factors by the partial derivitive of the activations functions
                    # [len(self.all_layer)-i-1] these are the index of the layer because we go back in the layers (that's why -i)
                    if self.activation_function[len(self.activation_function)-i-1] == 1: # if the activation function of this layer if a relu
                        factors[o] = factors[o] * self.ReLuDx(self.all_YHAT[len(self.all_layer)-1-i][o]) # if you don't understand go to learn maths
                    elif self.activation_function[len(self.activation_function)-i-1] == 2: # if the activation function of this layer if a sigmoid
                        factors[o] = factors[o] * self.Sigmoid(self.all_YHAT[len(self.all_layer)-1-i][o]) # if you don't understand go to learn maths
            self.all_layer[len(self.all_layer)-1-i].set_Y(self.Y) # set for the actual layer the prediction of the model
            self.all_layer[len(self.all_layer)-1-i].backward(factors) # use the backward method of the layer with the given factors
        add_grad = []

        self.Bias_grad = self.get_bias_grads() # get all the bias grads

        # will create the batch_grad of the model with all the layers's batch_grad
        for i in range(len(self.all_layer)): # for each layer...
            stock_grad = self.all_layer[i].batch_grad[-1].copy() # get the layer's gradients
            add_grad.append(stock_grad) # create the gradients who will be add to the batch_grad
        self.batch_grad.append(add_grad) # add all the gradients to the batch_grad

    def reset_batch_grad(self): # read the name of the function and you will certainly understand what it does
        for o in range(len(self.all_layer)): # for each layer
            self.all_layer[o].reset_batch_grad()
        self.batch_grad = []

    def gradient_mean(self): # compute the mean of all the gradients of the batch to obtains the finals gradients
        for o in range(len(self.all_layer)): # for each layer...
            self.all_layer[o].gradient_mean() # do the mean for all the layers
            self.grad[o] = self.all_layer[o].grad # and get back their gradients

    def optimizer(self, alpha): # update all the weights with the finals gradients and the learning rate
        for i in range(len(self.all_layer)): # for each layer...
            self.all_layer[i].optimizer(alpha)


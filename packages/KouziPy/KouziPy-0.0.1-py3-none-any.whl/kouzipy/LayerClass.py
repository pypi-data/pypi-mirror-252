import math
from neuroneClasse import Neurone


class Layer:
    def __init__(self, Ninp, Noutp):
        self.neurones = [Neurone(Ninp) for o in range(Noutp)] # initalize all the neurons of the layer
        self.Ninp = Ninp # number of input of each neurons 
        self.Noutp = Noutp # number of neuron on the layer
        self.weight = [w.Weight for w in self.neurones] # initalize the weights of the layer with the weights of the neurons 
        self.bias = [b.Bias for b in self.neurones] # initalize all the bias of the layer 
        self.grad = [o.grad for o in self.neurones] # initalize all the gradients of the layer 
        self.Bias_grad = [o.Bias_grad for o in self.neurones] # initalize all the bias gradients of the layer
        self.batch_grad = [] # all the gradients before the optimization
        self.all_y = [] # all the outputs of each neurons
        self.Y = False # the prediction of the model

    def get_inpout(self): # get the number of input of the layer and the number of layer
        return self.Ninp, self.Noutp
    
    def set_Y(self, Y): # set the prediction of the model to the layer (required for the back-propagation)
        self.Y = Y

    def set_weight(self, p): # set all weight respect to the neurons
        for o in range(len(self.neurones)):
            self.neurones[o].set_weight(p[o])
    
    def set_bias(self, b): # set all the bias respect to the neurons
        for o in range(len(self.neurones)):
            self.neurones[o].set_bias(b[o])
    
    def zero_grad(self): # set all the gradients to 0 (even the gradients of each neurons)
        for o in range(len(self.neurones)):
            self.neurones[o].zero_grad()
            self.grad[o] = self.neurones[o].grad

    def get_weights(self): # get all the weights of the layer
        self.weight = [w.get_weights() for w in self.neurones]
        return self.weight
    
    def get_bias(self): # get all the bias of the layer
        self.bias = [o.get_bias() for o in self.neurones]
        return self.bias
    
    def get_grads(self): # get all the grads of the layer
        self.grad = [g.grad for g in self.neurones]
        return self.grad
    
    def get_bias_grads(self): # get all the bias gradients of the model
        self.Bias_grad = [o.Bias_grad for o in self.neurones]
        return self.Bias_grad
    
    def ReLu(self, x): # the relu function
        return max(0, x)
    
    def ReLuDx(self, x): # the derivitive of the relu function
        if x > 0:
            return 1
        return 0
    
    def Sigmoid(self, x): # the sigmoid function
        return 1 / (1 + math.exp(-x))

    def SigmoidDx(self, x): # the derivitive of the sigmoid function
        return -math.exp(-x) / (1 + 2*math.exp(-x) + math.exp(-2*x))
    
    def forward_layer(self, Input, activ_function): # compute the output of the layer
        predict = 0 # prediction of the neurone
        self.all_y = [] # clear the list 
        for y in range(self.Noutp): # for each neurons...
            predict = self.neurones[y].forward(Input, activ_function) # compute the prediction of the neuron
            self.all_y.append(predict) # add the prediction 
        return self.all_y
    
    def backward(self, all_multi=False): # compute all the gradients of the neural network
        if all_multi == False: # all_multi is an optional parameter, if he's not given all the values are set to 1
            all_multi = [1 for o in range(len(self.neurones))]

        stock_grad = [] # the value who will be contain all the gradients 
        for i in range(len(self.neurones)): # for each neurons...
            self.neurones[i].set_Y(self.Y) # set (give) the prediction of the model to the neuron (required for the back-propagation)
            self.neurones[i].backward(all_multi[i]) # compute the gradients of the neuron 
            stock_grad.append([o for o in self.neurones[i].grad])
        self.batch_grad.append(stock_grad) # add the gradients to the batch_grad

    def gradient_mean(self): # compute the mean between all the gradients of the batch
        for o in range(len(self.neurones)): # for each neuron...
            self.neurones[o].gradient_mean() # compute the mean of the neuron's gradients 
            self.grad[o] = self.neurones[o].grad # add the neuron's gradients to the layer's gradients

    def reset_batch_grad(self): # read the name of the function and you will certainly understand what it does
        for o in range(len(self.neurones)):
            self.neurones[o].reset_batch_grad()
        self.batch_grad = []

    def optimizer(self, alpha): # update all the weight of all the layer's neurons
        for i in range(len(self.neurones)):
            self.neurones[i].optimizer(alpha)
    


from cargame import Game
import numpy as np
import matplotlib.pyplot as plt
import pickle
###########################
def relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def init(n_in, n_out):
    variance = 2.0 / (n_in + n_out)
    std_dev = np.sqrt(variance)
    return np.random.normal(0, std_dev, size=(n_in, n_out))

def softmax(x):
  exp = np.exp(x- np.max(x,axis=1,keepdims=True))
  return exp/np.sum(exp,axis=1,keepdims=True)

def predict(w, x):
  logits = np.dot(x,w)
  #softmaxed = softmax(logits)
  return logits

def one_hot(x,n_classes):#x is 1d, like labels
  n_len = len(x)
  mat = np.zeros((n_len,n_classes))
  mat[range(n_len),x] = 1
  return mat

def cross_entropy(y_true, y_pred, eps=1e-15):
  y_true, y_pred = np.array(y_true), np.array(y_pred)#y_true==y_pred==[batch,n_classes]
  n = len(y_true)
  assert y_true.shape==y_pred.shape,f"failed shape{y_true.shape},{y_pred.shape}"
  total = -np.sum(y_true*np.log(y_pred+eps),axis=1)
  return total/n

def grad_descent(W, X, y,out_dim, alpha=0.01, iters=20000):
  n = len(y)
  X = np.array(X)
  y = np.array(y)
  costlist = []
  for i in range(iters):
    layer_outputs = [X]
    for n,w in enumerate(W):
      layer_input = layer_outputs[-1]
      layer_output = predict(w,layer_input)
      if(n!=len(W)-1):
        layer_output = relu(layer_output)
      else:
        layer_output = softmax(layer_output)
      layer_outputs.append(layer_output)
    final_output = layer_outputs[-1]
    cost = np.sum(cross_entropy(y, final_output))/n
    costlist.append(cost.item())
    print(i)
    print(cost.item())

    delta = final_output - y
    for i in range(len(W)-1,-1,-1):
      layer_input = layer_outputs[i]
      grad_w = np.dot(layer_input.T, delta)/n
      grad_w = np.clip(grad_w, -1.0, 1.0)
      W[i] -= alpha * grad_w
      if i > 0:
        delta = np.dot(delta, W[i].T) * np.where(layer_input > 0, 1, 0.01)

  return costlist,W

def log_reg(data,label,sizes,alpha=0.1,epoch=10_000):
  weights = [init(sizes[i], sizes[i + 1]) for i in range(len(sizes) - 1)]
  costlist,newweights = grad_descent(weights, data, label,sizes, alpha, epoch)
  plt.plot(costlist)
  plt.show()
  return newweights,costlist[-1]

def model(weights, X):
    out = X
    for i in range(len(weights) - 1):
        out = relu(predict(weights[i], out))
    out = softmax(predict(weights[-1], out))
    return out
#########################################
KEYS = {"LEFT": 0, "RIGHT": 1, "None": 2}
def train():
  newgame = Game()
  data, keys = newgame.run()

  trainX = np.array(data, dtype=np.float32)
  trainX = trainX/np.max(trainX)
  labelX = np.array([KEYS[label] for label in keys], dtype=np.uint8)

  trainy = one_hot(labelX, 3)
  print(trainX.shape, trainy.shape)
  print(trainX[0])

  newweights, finalloss = log_reg(np.array(trainX),np.array(trainy),sizes=(17,32,32,3))
  print(newweights[-1])
  with open('weights.pkl', 'wb') as file:
    pickle.dump(newweights, file)
  print(newweights)

train()
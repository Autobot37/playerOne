from cargame import Game
import numpy as np
import matplotlib.pyplot as plt
import pickle
###########################
def softmax(x):
  exp = np.exp(x- np.max(x,axis=1,keepdims=True))
  return exp/np.sum(exp,axis=1,keepdims=True)

def predict(w, x):
  logits = np.dot(x,w)
  softmaxed = softmax(logits)
  return softmaxed

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

def grad_descent(w, X, y,out_dim, alpha=0.01, iters=20000):
  n = len(y)
  X = np.array(X)#[10,3]
  w = np.array(w)#[3,2]
  y = np.array(y)#[10,2]
  costlist = []
  for i in range(iters):
    y_pred = predict(w,X)#[10,2]
    cost = np.sum(cross_entropy(y, y_pred))/n#[10]
    costlist.append(cost.item())
    dw = np.dot(X.T, (y_pred - y)) / n
    w = w - alpha*dw
  return costlist,w

def log_reg(data,label,out_dims,alpha=0.1,epoch=10_000):
  weights = np.random.rand(len(data[0]),out_dims)
  costlist,newweights = grad_descent(weights, data, label,out_dims, alpha, epoch)
  plt.plot(costlist)
  plt.show()
  return newweights,costlist[-1]
#########################################


KEYS = {"LEFT": 0, "RIGHT": 1, "None": 2}

def train():
  newgame = Game()
  data, keys = newgame.run()

  trainX = np.array(data, dtype=np.float32)
  labelX = np.array([KEYS[label] for label in keys], dtype=np.uint8)

  trainy = one_hot(labelX, 3)
  print(trainX.shape, trainy.shape)

  newweights, finalloss = log_reg(np.array(trainX),np.array(trainy),out_dims=3)
  print(newweights)
  with open('weights.pkl', 'wb') as file:
    pickle.dump(newweights, file)

train()
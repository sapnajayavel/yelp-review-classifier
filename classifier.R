usefulness_threshold = 5

dataMatrix <- read.csv(paste("features_", usefulness_threshold, sep=""), header=FALSE)
trainTestCutoff = 184000
totalDataRows = dim(dataMatrix)[1]

y <- as.matrix(dataMatrix[seq(trainTestCutoff),1])
trainingX <- dataMatrix[seq(trainTestCutoff),-1]
x <- as.matrix(cbind(rep(1, dim(trainingX)[1]),trainingX))

test_y <- dataMatrix[seq(trainTestCutoff, totalDataRows),1]
testX <- dataMatrix[seq(trainTestCutoff, totalDataRows),-1]
test_x <- as.matrix(cbind(rep(1, dim(testX)[1]),testX))

useful_prob = function(x_t, w_t) {
  return(1 - 1 / (1 + exp(x_t %*% w_t)))
}

avg_loss = function(step_num, yhat, y) {
  return(sum((yhat[1:step_num] - y[1:step_num])^2) / step_num)
}

sgd = function(x, y, eta) {
  w_t = matrix(0, ncol(x), 1)
  yhat = matrix(0, nrow(x), 1)
  loss_vec = matrix(0, nrow(x) / 1000)
  for (row_index in seq(nrow(x))) {
    x_t = x[row_index,]
    y_t = y[row_index]
    yhat[row_index] = round(useful_prob(x_t, w_t))
    w_t = w_t + eta * (x_t * (y_t - useful_prob(x_t, w_t)))
    
    if (row_index %% 1000 == 0) {
      loss_vec[row_index / 1000] = avg_loss(row_index, yhat, y)
    }
  }
  return(list("w"=w_t, "loss"=loss_vec))
}

test_SSE = function(x, y, w) {
  yhat = matrix(0, nrow(x), 1)
  for (row_index in seq(nrow(x))) {
    yhat[row_index] = round(useful_prob(x[row_index,], w))
  }
  
  return(sum((yhat - y)^2))
}

step_sizes = c(0.5, 0.25, 0.125, 0.1)

par(mfrow=c(4,1))
pdf(paste("average_loss_", usefulness_threshold, ".pdf", sep=""), width=5.5, height=4.45)
for (eta in step_sizes) {
  result = sgd(x, y, eta)
  w = result$w
  loss = result$loss
  plot(seq(1000, trainTestCutoff, 1000), loss, xlab="Step Number", ylab="Average Loss")
  title(paste("Step Num vs. Avg Loss, Eta:", eta, "Useful Threshold:", usefulness_threshold))
  
  print(paste("L2 norm at step size", eta, ":", sqrt(sum(w^2))))
  
  print(paste("SSE of predicted Usefulness at step size", eta, ":", test_SSE(test_x, test_y, w)))

  print(paste("Weights of feature vector at step size", eta))
  print(w)
}
dev.off()
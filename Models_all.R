library(dplyr)
library(ggplot2)
library(GGally)
library(caTools)
library(ROCR)
library(MASS)
library(rpart) # CART
library(rpart.plot) # CART plotting
library(randomForest)
library(gbm)
library(caret) # cross validation
########## Read Training and Testing and implement all 4 methods
Train = read.csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Wed_Train_v2.csv")
Test = read.csv("C:/Users/saketha lakshmi/Documents/IEOR242/Project/DataSets/Wed_Test_v2.csv")
X_test = Test[,c(0:37)]
Y_test = Test$Response
colnames(Train)

####### Logistic Regression
mod <- glm(Response ~ ., data=Train, family="binomial")
summary(mod)
predTest = predict(mod, newdata=X_test, type="response")
table(Y_test, predTest > 0.5)

rocr.log.pred <- prediction(predTest, Y_test)
logPerformance <- performance(rocr.log.pred, "tpr", "fpr")
plot(logPerformance, colorize = TRUE)
abline(0, 1)
as.numeric(performance(rocr.log.pred, "auc")@y.values)


############LDA
LdaModel <- lda(Response ~ ., data=Train)
predTestLDA <- predict(LdaModel, newdata=X_test)
predTestLDA_probs <- predTestLDA$posterior[,2]

# Confusion matricies based on decision tree threshold 
table(Y_test, predTestLDA_probs > 1/3)
rocr.lda.pred <- prediction(predTestLDA_probs, Y_test)
ldaPerformance <- performance(rocr.lda.pred, "tpr", "fpr")
plot(ldaPerformance, colorize = TRUE)
abline(0, 1)
as.numeric(performance(rocr.lda.pred, "auc")@y.values)
plot(logPerformance, col="blue")
plot(ldaPerformance, col="red", add=TRUE)
abline(0,1)

#########========= CART model=========================###################
cpVals = data.frame(cp = seq(0, .04, by=.002))
Train$Response = as.factor(Train$Response)
set.seed(123)
train.cart <- train(Response ~ .,
                    data = Train,
                    method = "rpart",
                    tuneGrid = cpVals,
                    trControl = trainControl(method = "cv", number=10),
                    metric = "Accuracy")

# look at the cross validation results, stored as a data-frame
train.cart$results # please ignore kappa #0.002 is the best Cp value
train.cart

# plot the results
ggplot(train.cart$results, aes(x=cp, y=Accuracy)) + geom_point()
# We can increase the size of the points:
ggplot(train.cart$results, aes(x=cp, y=Accuracy)) + geom_point(size=3)
# We can change the default axis labels
ggplot(train.cart$results, aes(x=cp, y=Accuracy)) + geom_point(size=3) +
  xlab("Complexity Parameter (cp)") + geom_line()


# Extract the best model and make predictions
train.cart$bestTune
mod123 = train.cart$finalModel
prp(mod123, digits=3)

# We need to extract the "model matrix" for parole.test before we can make predictions
# This is because caret does not work with factors, instead it creates dummy variables 
#parole.test.mm = as.data.frame(model.matrix(Violator~.+0, data=parole.test))
pred = predict(mod123, newdata=X_test, type="class")
table(Y_test, pred)

######=================Random Forest ============================#
set.seed(99)
train.rf <- train(Response ~ .,
                  data = Train,
                  method = "rf",
                  tuneGrid = data.frame(mtry=1:16),
                  trControl = trainControl(method="cv", number=5, verboseIter = TRUE),
                  metric = "Accuracy")
# RMSE or Rsquared doesn't matter actually -- both will be generated for regression problems
train.rf$results
train.rf
best.rf <- train.rf$finalModel
pred.best.rf <- predict(best.rf, newdata = test.ctr.mm) # can use same model matrix

ggplot(train.rf$results, aes(x = mtry, y = Rsquared)) + geom_point(size = 3) + 
  ylab("CV Rsquared") + theme_bw() + theme(axis.title=element_text(size=18), axis.text=element_text(size=18))





########## 
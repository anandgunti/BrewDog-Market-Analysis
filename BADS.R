library(dplyr)
library(mice)
install.packages("fastcluster")
install.packages('plclust')
library("fastcluster")
brew = read.csv("Brewdog.csv",header = T,stringsAsFactors = T) 
brew$Yeast <- as.factor(brew$Yeast) #converting char data type as factor for analysis
md.pattern(brew,rotate.names = TRUE)
boxplot(brew$FermentationTempCelsius)
boxplot(brew$AttenuationLevel)
boxplot(brew$PH)
boxplot(brew$OG)
boxplot(brew$IBU)
boxplot(brew$ABV)
boxplot(brew$AttenuationLevel)
brew$IBU[brew$IBU == 1085 ] <- NA #setting the outlier as NA 
brew$FermentationTempCelsius[brew$FermentationTempCelsius == 99 ] <- NA 

library("VIM")
library("corrgram")
aggr(brew, numbers=TRUE,prop=FALSE, only.miss = T,combined = T,cex.axis = 0.4)


#correlations
missdata <-brew 
missdata$missing <-as.numeric(!complete.cases(brew)) 
corrgram(missdata,order=TRUE) 

#multiple imputations 
imp<- mice(brew, m = 10 , maxit = 10 , method ="cart")
imp1<- mice(brew, m = 10 , maxit = 10 , method ="pmm")
imp2<- mice(brew, m = 10 , maxit = 10 , method ="rf")
brewimp= complete(imp)
brewimp1= complete(imp1)
brewimp2= complete(imp2)#best data set method random forest based on mean comparison  
summary(brew)
summary(brewimp)
summary(brewimp1)
summary(brewimp2)
str(brewimp2)
b2 = brewimp2


#checking for missing values and evaluating means(Method = Random Forest)
par(mfrow=c(1,2))
hist(brewimp2$ABV,freq=F,xlab = 'ABV(Imputed)',main = "Distribution of ABV after Imputation using Rf method",cex.main=0.9) # very slight shift in shape, but acceptable given the stat in summary
hist(brew$ABV , freq=F,xlab = 'ABV' ,main = "Distribution of ABV before Imputation",cex.main=0.9)
sd(brewimp2$ABV,na.rm=TRUE)
sd(brew$ABV,na.rm=TRUE)

#checking for missing values and evaluating means(Method = Random Forest)
par(mfrow=c(1,2))
hist(brewimp2$EBC,freq=F,xlab = 'EBC(Imputed)',main = "Distribution of EBC after Imputation using Rf method",cex.main=0.9) # very slight shift in shape, but acceptable given the stat in summary
hist(brew$EBC , freq=F,xlab = 'EBC' ,main = "Distribution of EBC before Imputation",cex.main=0.9)
sd(brewimp2$EBC,na.rm=TRUE)
sd(brew$EBC,na.rm=TRUE)

#checking for missing values and evaluating means(Method = Random Forest)
par(mfrow=c(1,2))
hist(brewimp2$IBU,freq=F,xlab = 'IBU(Imputed)',main = "Distribution of IBU after Imputation using Rf method",cex.main=0.9) # very slight shift in shape, but acceptable given the stat in summary
hist(brew$IBU , freq=F,xlab = 'IBU' ,main = "Distribution of IBU before Imputation",cex.main=0.9)
sd(brewimp2$IBU,na.rm=TRUE)
sd(brew$IBU,na.rm=TRUE)

#checking for missing values and evaluating means(Method = Random Forest)
par(mfrow=c(1,2))
hist(brewimp2$FermentationTempCelsius,freq=F,xlab = 'FermentationTempCelsius(Imputed)',main = "Distribution of FermentationTempCelsius after Imputation using Rf method",cex.main=0.7) # distribution is similar,stat summary also supports this 
hist(brew$FermentationTempCelsius , freq=F,xlab = 'FermentationTempCelsius' ,main = "Distribution of FermentationTempCelsius before Imputation",cex.main=0.7)
sd(brewimp2$FermentationTempCelsius,na.rm=TRUE)
sd(brew$FermentationTempCelsius,na.rm=TRUE)



#clustering 
install.packages("NbClust")
library(NbClust)
library(cluster)
brewimp2[,2:8] <- scale(brewimp2[,2:8], center = TRUE, scale = TRUE) #Scaling the data
dm <- daisy(brewimp2[2:9]) #distance calculation 
clust <- agnes(dm, diss = TRUE, method="ward")

ab = as.hclust(clust)
ab$labels = brew$Name[clust$order]
par(mfrow=c(1,1))

#plotting the dendrogram 
require(factoextra)
fviz_dend(ab, cex = 0.25,show_labels=T, k = 4,
          # Manually selected colors
          k_colors = c("jco"),
          rect = TRUE, 
          rect_border = "jco", 
          rect_fill = TRUE,
)

#customizing the dendrogram

fviz_dend(ab, cex = 0.25,show_labels=T, k = 4,
          # Manually selected colors
          k_colors = c("jco"),
          rect = TRUE, 
          rect_border = "jco", 
          rect_fill = TRUE,
        )

#Determing the number of clusters using nbclust 

fviz_nbclust(b2[c(2:8)], kmeans, method = "wss") +
  geom_vline(xintercept = 4, linetype = 2)+
  labs(subtitle = "Elbow method")

cluster <- cutree(clust, k=4)
str(cluster)
# Statistical information about clusters 

table(cluster, brewimp2$Yeast)
tapply(b2$ABV,cluster,mean)
tapply(b2$IBU,cluster,mean)
tapply(b2$EBC,cluster,mean)
tapply(b2$AttenuationLevel,cluster,mean)


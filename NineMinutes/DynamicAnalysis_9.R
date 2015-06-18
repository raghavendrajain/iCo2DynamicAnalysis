# This file plots the data for all the players who played more than 10 mins. 
# Their behavior over time for 10 mins is understood by calculating the probabilities of falling into the 
# smooth zones. No clusters are created. 


playerData_2_3<-read.csv("jerk_clusteringMins_2_3.csv", header=FALSE)
playerData_3_4<-read.csv("jerk_clusteringMins_3_4.csv", header=FALSE)
playerData_4_5<-read.csv("jerk_clusteringMins_4_5.csv", header=FALSE)
playerData_5_6<-read.csv("jerk_clusteringMins_5_6.csv", header=FALSE)
playerData_6_7<-read.csv("jerk_clusteringMins_6_7.csv", header=FALSE)
playerData_7_8<-read.csv("jerk_clusteringMins_7_8.csv", header=FALSE)
playerData_8_9<-read.csv("jerk_clusteringMins_8_9.csv", header=FALSE)

prob2_3<-rowSums(playerData_2_3[, c(11,12)])
prob3_4<-rowSums(playerData_3_4[, c(11,12)])
prob4_5<-rowSums(playerData_4_5[, c(11,12)])
prob5_6<-rowSums(playerData_5_6[, c(11,12)])
prob6_7<-rowSums(playerData_6_7[, c(11,12)])
prob7_8<-rowSums(playerData_7_8[, c(11,12)])
prob8_9<-rowSums(playerData_8_9[, c(11,12)])


probDf <- cbind(prob2_3, prob3_4, prob4_5,  prob5_6, prob6_7, prob7_8, prob8_9)


fit <- kmeans(playerData_2_3, 4) # 4 cluster solution
fit$size
# get cluster means 
allMeans<-aggregate(playerData_2_3, by=list(fit$cluster),FUN=mean)
# append cluster assignment
totalWithClusters <- data.frame(playerData_2_3, fit$cluster)
# get the centers of the clusters
allCenters<-fit$centers

# 
fit$size
cluster1 <- colMeans(probDf[which(totalWithClusters["fit.cluster"]==1), ])
cluster2 <- colMeans(probDf[which(totalWithClusters["fit.cluster"]==2), ])
cluster3 <- colMeans(probDf[which(totalWithClusters["fit.cluster"]==3), ])
cluster4 <- colMeans(probDf[which(totalWithClusters["fit.cluster"]==4), ])


all <- rbind(cluster1, cluster2, cluster3, cluster4)
clusterOrder<-order(-all[,1])
allNew<- all[ order(-all[,1]), ]

tAll <- t(allNew)
tAll
labelsOfClusters<-c("[2,3)", "[3, 4)", "[4, 5)", "[5, 6)", "[6, 7)", "[7, 8)", "[8, 9)")

plot.new()
frame()
matplot(tAll, xlim=c(1,8), ylim=c(0,1), type = c("b"), lty = 1:4, lwd = 2, pch=19, col=c("red","black", "blue","green"), 
        xaxt='n', xlab = "Time Intervals in minutes", ylab = "Probability of driving eco-friendly",
        main = "Time varying probabilites of eco-friendly driving behavior")
legend("bottomright", lty = 1:4, lwd = 2, pch=19,  legend = c("Eco-friendly ", "Gerntle", "Normal", "Crazy"), col=c("red","black", "blue","green")) # optional legend
axis(1, at=1:7, labels=labelsOfClusters)


theClusterSize<-fit$size
theClusterSize<-theClusterSize[clusterOrder]
totalSummary <- rbind(tAll, theClusterSize)

write.table(totalSummary, file = "ClusterPerformance")
write.csv(totalSummary, file = "ClusterPerformance.csv")
totalSummary









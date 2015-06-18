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
playerData_9_10<-read.csv("jerk_clusteringMins_9_10.csv", header=FALSE)

prob2_3<-rowSums(playerData_2_3[, c(11,12)])
prob3_4<-rowSums(playerData_3_4[, c(11,12)])
prob4_5<-rowSums(playerData_4_5[, c(11,12)])
prob5_6<-rowSums(playerData_5_6[, c(11,12)])
prob6_7<-rowSums(playerData_6_7[, c(11,12)])
prob7_8<-rowSums(playerData_7_8[, c(11,12)])
prob8_9<-rowSums(playerData_8_9[, c(11,12)])
prob9_10<-rowSums(playerData_8_9[, c(11,12)])

probDf <- cbind(prob2_3, prob3_4, prob4_5,  prob5_6, prob6_7, prob7_8, prob8_9, prob9_10 )

for (i in 1:25){

plot(probDf[i, 1:8]*100,  y= NULL, xlab = "Time for playing", ylab = "Percentage share in eco-friendly zone", ylim = c(0,100), pch = 2, type='l', lwd=2, col = "green", xaxt='n')
par(new=TRUE)

}




clusterit<-function(fileString, hclustStyle)
{
  currentWorkingData = read.csv(fileString)
  currentDistMatrix = as.dist(as.matrix(currentWorkingData))
  currentHAC = hclust(currentDistMatrix,method=hclustStyle)
  #plot(currentHAC)
  #rect.hclust(currentHAC, k=10)
  currentDendrogram<-as.dendrogram(currentHAC)
  current10Clust<-color_branches(currentDendrogram, k=20)
  plot(current10Clust)
  currentCut=cutree(currentHAC, k=20)
  sortedCut<-sort(currentCut)
  print(sortedCut)
  sortedVector<-as.vector(sortedCut)
  print(sortedVector)
  clusterReport(sortedVector, 20)
}

clusterReport<-function(vect, clusters)
{
  for(i in 1:clusters)
  {
    cat("Cluster ", i)
    val_count = 0
    for(j in 1:length(vect))
    {
      this_value<-vect[j]
      if(this_value == i)
      {
        val_count = val_count + 1
      }
    }
    cat("   Number of members: ", val_count, "\n")
  }
}
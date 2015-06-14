How to use these Files:

finalWeights:  just copy and paste the weights into the distanceMatrixMaker and run it

Rscript_sample_output.txt: the output you would get when running the R script from the R command line

clusterEr.R: 
	- this is the script that defines the function "clusterit"
	- open up a session in RStudio and then navigate to File-->OpenFile and open up this file
	- in the window that pops up with the clusterit code, click the box labeled "Source on Save" then press the save button
	- clusterit should be a function you can call now
	- IMPORTANT, for the dendrogram to print with colored branches you'll need to do:
		packages.install("dendextend")

		then do:
		library(dendextend)
	- now calling clusterit should work just fine
	- "clusterit" takes in 2 parameters:
		fileString- the distance matrix csv file to read from ex. "matrix_100.csv"
		hclustStyle- the type of linkage to use for the hclust algorithm, USE "complete" for the weights I made

	- I forgot to make the number of clusters a pass-inable parameter so you'll have to change the hardcoded values, just put in what you want wherever it says "k=#"


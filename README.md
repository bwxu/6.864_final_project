# 6.864 Project

##Abstract
	
SAT vocabulary questions involve selecting the best word or words out of the choices given to fill in a blank for a block of text.

This project will solve these vocabulary questions by applying the ideas of n-gram models, parsing, and recurrent neural networks in order to correctly rank and identify the best solutions. In particular, we will score each option with our model and select the highest scoring answer as our solution.

##Running the Code

Before running the code, extract the compressed files from dataset. If you get an error while running NGram.py, make sure you have punkt installed (if not, run nltk.download() and install punkt). 

##Data/Corpora

Our training data consists of text from Wall Street Journal and our test data will be multiple choice fill in the blank questions with answers to measure accuracy.

Link to download corpus: https://www.dropbox.com/s/ttne74p1jsjbzwe/LDC95T7.tgz?dl=0
Link to download word vectors: http://aadah.me/misc/vectors.txt

Corpus folders should go under /dataset and vectors.txt should be in the root folder of the files

##Baselines

We will use multiple baselines to compare our results, such as random answering and average SAT test scores. We will also compare it to previous similar classifiers.

##Evaluation

To measure the performance of our system, we will analyze the accuracy of our model in answering easy, medium, and hard questions. We will also look at top 2 accuracy, where we check if the answer was one of our top two choices. Another consideration will be the speed of our algorithm and whether it works within a reasonable time span with a reasonable amount of resources. 

###Report link for project updates/ “lab notebook”

https://docs.google.com/document/d/1ATceKZNPIFECAnmQ0eaU2_6yU07pu4EiijlSCzAv0do/edit

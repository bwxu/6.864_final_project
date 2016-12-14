# 6.864 Project

##Abstract
	
SAT vocabulary questions involve selecting the best word or words out of the choices given to fill in a blank for a block of text.

This project will solve these vocabulary questions by applying the ideas of n-gram models, parsing, and recurrent neural networks in order to correctly rank and identify the best solutions. In particular, we will score each option with our model and select the highest scoring answer as our solution.

##Running the Code

Before running the code, extract the compressed files from dataset. If you get an error while running NGram.py, make sure you have punkt installed (if not, run nltk.download() and install punkt). These are included in the dataset/ directory.

### Dependencies
Python3

    brew install python3
    
NumPy

    pip3 install numpy
    
NLTK

    pip3 install nltk
    
NLTK punkt pickle

    $ python3
    
    $ >>> import nltk
    
    $ >>> nltk.download('punkt')

### n-Gram Model
First, download and extract the holmes training data and test data into the dataset folder. The data is found on https://www.microsoft.com/en-us/research/project/msr-sentence-completion-challenge/. Then, to run the code, use the command,

python3 NGram.py

### Word Embeddings Model
Before running, make sure you have the holmes training and test data in your dataset folder. Also, make sure you have vectors.txt downloaded in the same directory as word_embeddings.py

To run the word embeddings model, use the command

python3 word_embeddings.py

### LSTM Model
Before running make sure you have the WSJ as well as the holmes training and test data in your dataset folder.

Running the LSTM model will save the output generate an output file in the text file with name indicated on line 315 of the code. The output format will be spaced delimited with the question number first followed by the predicted probabilites of answer options a, b, c, d, e in that order. The final line will be the accuracy of the predictions on all of the questions.

To run the forward LSTM model, use the command

python3 LSTM.py --data_path='.' --model=test backwards=False

To run the backwards LSTM model, use the command

python3 LSTM.py --data_path='.' --model=test backwards=True

The "model" flag may be any of small, medium, large, or test. We recommend running test (a very small configuration) for time purposes.

### LSTM Output Data

As mentioned before, the output format is be spaced delimited with the question number first followed by the predicted probabilites of answer options a, b, c, d, e in that order. The final line will be the accuracy of the predictions on all of the questions.

Our output data for the MSR Sentence Completion Challenge:

forward_out_MSR.txt

backwards_out_MSR.txt

bidirectional_out_MSR.txt

Output data for the sample SAT Questions:

forward_out_SAT.txt

backwards_out_SAT.txt

bidirectional_out_SAT.txt

##Data/Corpora

Our training data consists of text from Wall Street Journal and our test data will be multiple choice fill in the blank questions with answers to measure accuracy.

Link to test data: https://www.microsoft.com/en-us/research/project/msr-sentence-completion-challenge/ (click 'test')

Link to holmes training data: https://www.microsoft.com/en-us/research/project/msr-sentence-completion-challenge/ (click 'train')

Link to download corpus: https://www.dropbox.com/s/ttne74p1jsjbzwe/LDC95T7.tgz?dl=0

Link to download word vectors: http://aadah.me/misc/vectors.txt

Corpus folders should go under /dataset and vectors.txt should be in the root folder of the files

##Baselines

We will use multiple baselines to compare our results, such as random answering and average SAT test scores. We will also compare it to previous similar classifiers.

##Evaluation

To measure the performance of our system, we will analyze the accuracy of our model in answering easy, medium, and hard questions. We will also look at top 2 accuracy, where we check if the answer was one of our top two choices. Another consideration will be the speed of our algorithm and whether it works within a reasonable time span with a reasonable amount of resources. 

###Report link for project updates/ “lab notebook”

https://docs.google.com/document/d/1ATceKZNPIFECAnmQ0eaU2_6yU07pu4EiijlSCzAv0do/edit

"""
## Naive Bayes Classifier

This module contains the Naive Bayes Classifier for spam detection. 

Classes:
- NaiveBayesClassifier: Naive Bayes Classifier for spam detection.

The NaiveBayesClassifier class has methods for: 
- initializing the classifier
- training the classifier
- predicting the labels of the given emails.
- calculating the accuracy of the classifier.

University: University of Peloponnese, Department of Informatics and Telecommunications

Course: Artificial Intelligence

Authors: 
- Giannopoulos Georgios
- Giannopoulos Ioannis
"""
from collections import defaultdict
from typing import List, Set
import numpy as np

class NaiveBayesClassifier():
    """
    Naive Bayes Classifier for spam detection.
    """
    
    def __init__(self) -> None:
        """
        Initialize the Naive Bayes Classifier.
        """
        self.spam_word_count = defaultdict(int)
        """Number of times a word appears in spam emails"""
        self.ham_word_count = defaultdict(int)
        """Number of times a word appears in ham emails"""
        self.spam_email_count = 0
        """Number of spam emails"""
        self.ham_email_count = 0
        """Number of ham emails"""
        self.total_emails = 0
        """Total number of emails"""
        self.p_spam = 0
        """Probability of spam emails"""
        self.p_ham = 0
        """Probability of ham emails"""
        self.p_word_given_spam = defaultdict(float)
        """Probability of a word given that the email is spam"""
        self.p_word_given_ham = defaultdict(float)
        """Probability of a word given that the email is ham"""
        self.words = set()
        """Set of all unique words in spam and ham emails"""

    def train(self, emails: List[str], labels: List[str], laplace_smoothing=False):
        """
        Train the Naive Bayes Classifier.

        Calculate the probabilities of spam and ham emails and 
        the probability of each word given that the email is spam or ham.

        Args:
            - emails (list): A list of emails. Each element of the list is expected to be a set of words.
            - labels (list): A list of corresponding labels. Each element of the list is expected to be a string representing a label.
            - laplace_smoothing (bool, optional): If True, apply Laplace Smoothing. Defaults to False.
        """
        self.total_emails = len(emails)
        self.spam_email_count = sum(1 for label in labels if label == 'spam')
        self.ham_email_count = sum(1 for label in labels if label == 'ham')

        # Calculate the probability of spam and ham emails
        self.p_spam = self.spam_email_count / self.total_emails
        self.p_ham = self.ham_email_count / self.total_emails

        # Count the number of times each word appears in spam and ham emails
        for email, label in zip(emails, labels):
            if label == 'spam':
                for word in email:
                    self.spam_word_count[word] += 1
            elif label == 'ham':
                for word in email:
                    self.ham_word_count[word] += 1

        # Create a set that will contain all unique words from spam and ham emails
        # so we can iterate all the words to calculate the probabilities
        self.words = set(self.spam_word_count.keys()).union(set(self.ham_word_count.keys()))

        # Calculate the probability of each word given that the email is spam or ham
        # If laplace_smoothing is True, apply Laplace Smoothing
        if laplace_smoothing:
            for word in self.words:
                self.p_word_given_spam[word] = (self.spam_word_count[word] + 1) / (self.spam_email_count + 2)
                self.p_word_given_ham[word] = (self.ham_word_count[word] + 1) / (self.ham_email_count + 2)
        else:
            for word in self.words:
                self.p_word_given_spam[word] = self.spam_word_count[word] / self.spam_email_count
                self.p_word_given_ham[word] = self.ham_word_count[word] / self.ham_email_count
        
    def predict(self, emails, prevent_underflow=False) -> List[str]:
        """
        Predict the labels of the given emails.
        
        If an email contains a lot of words, the probability 
        of the email being spam or ham can become very small, close to 0, 
        leading to underflow when multiplying the probabilities.
        To prevent underflow, set `prevent_underflow` to True to use the log probabilities.
        
        Args:
            - emails (list): A list of emails. Each element of the list is expected to be a set of words.
            - prevent_underflow (bool, optional): If True, prevent underflow by using the log probabilities. Defaults to False.
        """
        y_pred = []
        if prevent_underflow:
            for email in emails:
                # calculate the log probabilities
                p_spam_given_email = np.log(self.p_spam)
                p_ham_given_email = np.log(self.p_ham)

                for word in email:
                    if word in self.words:
                        p_spam_given_email += np.log(self.p_word_given_spam[word])
                        p_ham_given_email += np.log(self.p_word_given_ham[word])
                # predict the label based on the probabilities
                if p_spam_given_email > p_ham_given_email:
                    y_pred.append('spam')
                else:
                    y_pred.append('ham')     
        else:
            # iterate over each email
            for email in emails:
                p_spam_given_email = self.p_spam
                p_ham_given_email = self.p_ham

                # iterate over each word in the email
                for word in email:

                    # if the word is in the set of unique words, update the probabilities, otherwise the word was not in the training set so we ignore it
                    if word in self.words:
                        p_spam_given_email *= self.p_word_given_spam[word]
                        p_ham_given_email *= self.p_word_given_ham[word]
                # predict the label based on the probabilities
                if p_spam_given_email > p_ham_given_email:
                    y_pred.append('spam')
                else:
                    y_pred.append('ham')
                    
        return y_pred
            
    
    def accuracy(self, y_true: List[str], y_pred: List[str]) -> float:
        """
        Calculate the accuracy of the classifier.
        """
        correct_prediction = 0
        for yt, yp in zip(y_true, y_pred):
            if yt == yp:
                correct_prediction += 1

        return correct_prediction / len(y_true)
    
    def __repr__(self) -> str:
        return f"NaiveBayesClassifier(spam_email_count={self.spam_email_count}, ham_email_count={self.ham_email_count}, total_emails={self.total_emails}, unique_words={len(self.words)}, p_spam={self.p_spam}, p_ham={self.p_ham})"
    
        

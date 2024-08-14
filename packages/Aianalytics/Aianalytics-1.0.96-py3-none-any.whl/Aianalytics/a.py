from PIL import Image
from scipy.fftpack import fft2, ifft2
import numpy as np
import cv2
from skimage.morphology import binary_opening, binary_closing, disk

import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage import filters, img_as_float
from PIL import Image
import matplotlib.pylab as pylab

import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature
import numpy as np

def allai():
    code=r"""
symptomCheckerES
AIBot
bayesTheorem
conditionalProb
familyTree
fuzzyOperations
simulateSupervised
simulateUnsupervised
clustering
svm
intelligentClothesAgent
simulateLanParser
feedforward"""
    print(code)
    
def symptomCheckerES():
    code=r"""
name = input("Enter your name: ")
fever = input("Do you have fever? (yes/no) ").lower()
cough = input("Do you have cough? (yes/no) ").lower()
sob = input("Do you have shortness of breath? (yes/no) ").lower()
st = input("Do you have sore throat? (yes/no) ").lower()
mp = input("Do you have muscle pain? (yes/no) ").lower()
hc = input("Do you have headache? (yes/no) ").lower()
diarrhea = input("Do you have diarrhea? (yes/no) ").lower()
conjuctivitis = input("Do you have conjuctivitis? (yes/no) ").lower()
lot = input("Do you have Loss of Taste? (yes/no) ").lower()
cp = input("Do you have Chest pain or Pressure? (yes/no) ").lower()
lsp = input("Do you have Loss of Speech or Movement? (yes/no) ").lower()

flu_symptoms = (fever=="yes" and cough=="yes" and sob=="yes" and st=="yes" and mp=="yes" and hc=="yes")
corona_symptoms = (diarrhea=="yes" and st=="yes" and fever=="yes" and cough=="yes" and conjuctivitis=="yes" and lot=="yes")
common_cold = (fever=="yes" and cough=="yes")

if flu_symptoms:
    print(name + " YOU HAVE FLU...")
    med = input("Aditi!, would you like to look at same medicine for the flu? (yes/no): ").lower()
    if med == "yes":
        print("Disclaimer: Contact a doctor for better guidance.")
        print("There are four FDA-approved antiviral drugs recommended by CDC to treat flu this season: ")
        print("1. Oseltamivir phosphate")
        print("2. Zanamivir")
        print("3. Peramivir")
        print("4. Baloxavir marboxil")
elif corona_symptoms:
    print(name + " YOU HAVE Corona")
    med = input("Aditi!, would you like to look at some remedies for Corona? (yes/no): ").lower()
    if med == "yes":
        print("TAKE VACCINE AND QUARANTINE")
elif common_cold:
    print(name + " YOU HAVE COMMON CODE")
    med = input("Aditi!, would you like to look at some remedies for Corona? (yes/no): ").lower()
    if med == "yes":
        print("Disclaimer: Contact a doctor for better guidance")
        print("Treatment consists of abti-inflammatories and decongestants. Most people d=recover on their own. ")
        print("1. Nonsteroidal abti-inflammatory drug")
        print("2. Analgesic")
        print("3. Antihistamine")
        print("4. Cough medicine")
        print("5. Decongestant")
else:
    print("Unable to identify")


Program: 2 Flu disease checker:
info=[]
name=input("Enter your name: ")
info.append(name)
age=int(input("Enter your age: "))
info.append(age)
print("----------------------------------------------")
a=["Fever", "Headache", "Tiredness", "Vomitting"]
b=["Urinate a lot", "Feels thirsty", "Weight loss", "Blurry vision", "Feels very hungry", "Feels very tired"]
print("----------------------------------------------")
print(a, b)
symp=input("Enter symptoms as above separated by comm ")
lst=symp.split(",")
print(info)
print("Symptoms: ")
for i in lst:
    print(i)
if i.strip() in a:
    print("You May Have Malaria\n...visit a Doctor")
elif i.strip() in b:
    print("You May Have Diabetes\n...Consume less Sugar")
else:
    print("Symptoms does not Match")


"""
    print(code)


def AIBot():
    code=r"""
Open cmd and install pip –
pip install aiml 
pip install python-aiml 

basic_chat.aiml
<aiml version="1.0.1" encoding="UTF-8">
<!-- basic_chat.aiml -->
 
    <category>
        <pattern>HELLO *</pattern>
        <template>
            Well, Hello PCS!
        </template>
    </category>
 
    <category>
        <pattern>WHAT ARE YOU</pattern>
        <template>
            I'm a bot, and I'm silly!
        </template>
    </category>
 
    <category>
        <pattern>WHAT DO YOU DO</pattern>
        <template>
            I'm here to motivate you!
        </template>
    </category>
 
    <category>
        <pattern>WHO AM I</pattern>
        <template>
            You are a Professional Footballer....
        </template>
    </category>
 
</aiml>
 
std-startup.xml
<aiml version="1.0.1" encoding="UTF-8">
<!--  std-startup.xml  -->
<!--  Category is an atomic AIML unit  -->
<category>
<!--  Pattern to match in user input  -->
<!--  If user enters "LOAD AIML B"  -->
<pattern>LOAD AIML B</pattern>
<!--  Template is the response to the pattern  -->
<!--  This learn an aiml file  -->
<template>
<learn>basic_chat.aiml</learn>
<!--  You can add more aiml files here  -->
<!-- <learn>more_aiml.aiml</learn> -->
</template>
</category>
</aiml>
 
AI_Prac2_Bot.py
import aiml
kernel=aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")
while True:
    input_text=input(">Human:")
    response=kernel.respond(input_text)
    print(">Bot: "+response)

"""
    print(code)


def bayesTheorem():
    code=r"""
Program: 1
def bayes_theorem(p_h, p_e_given_h, p_e_given_not_h):
    not_h= 1 - p_h
    p_e= p_e_given_h * p_h + p_e_given_not_h * not_h
    p_h_given_e= (p_e_given_h * p_h)/p_e
    return p_h_given_e
p_h=float(input("Enter probability of hk having cold P(H): "))
p_e_given_h=float(input("Enter probability of hk observed sneezing when he had cold P(E|H): "))
p_e_given_not_h=float(input("Enter probability of hk observed sneezing when he did not have cold P(E|~H): "))
result=bayes_theorem(p_h, p_e_given_h, p_e_given_not_h)
print("Hk probability of having cold given that he sneezes is P(H|E)= ", round(result, 2))

Program: 2
def bayes_theorem(p_h, p_e_given_h, p_e_given_not_h):
    not_h= 1 - p_h
    p_e= p_e_given_h * p_h + p_e_given_not_h * not_h
    p_h_given_e= (p_e_given_h * p_h)/p_e
    return p_h_given_e
p_h=float(input("Enter probability of hk having cold: "))
p_e_given_h=float(input("Enter probability of hk observed sneezing when he had cold: "))
p_e_given_not_h=float(input("Enter probability of hk observed sneezing when he did not have cold: "))
result=bayes_theorem(p_h, p_e_given_h, p_e_given_not_h)
print("Hk probability of having cold given that he sneezes is P(H|E)= ", round(result, 2))

Program: 3
def drug_user(prob_th=0.5, sensitivity=0.97, specificity=0.95, prevelance=0.005, verbose=True):
    p_user=prevelance
    p_non_user=1-prevelance
    p_pos_user=sensitivity
    p_neg_user=1-specificity
    p_pos_non_user=1-specificity
    num=p_pos_user*p_user
    den=p_pos_user*p_user+p_pos_non_user*p_non_user
    prob=num/den
    print("Probability of the test-taker being a drug user is ", round(prob, 1))
    if verbose:
        if prob > prob_th:
            print("The test-taker could be an user")
        else:
            print("The test-taker may not be an user")
        return prob
drug_user()
"""
    print(code)


def conditionalProb():
    code=r"""
def conditional_and_joint_probability(A, B, sample_space):
    prob_A_and_B = len(set(A) & set(B))/len(sample_space)
    prob_B = len(B)/len(sample_space)
    prob_A_given_B = prob_A_and_B/prob_B
    return prob_A_and_B, prob_A_given_B
sample_space = range(1, 11)
A = [2, 4, 6, 8, 10]
B = [1, 2, 3, 4, 5]
print("Set(A): ", A)
print("Set(B): ", B)
prob_A_and_B, prob_A_given_B = conditional_and_joint_probability(A, B, sample_space)
print("Joint probability P(A n B) = ", prob_A_and_B)
print("Conditional probability P(A | B) = ", prob_A_given_B)

"""
    print(code)


def familyTree():
    code=r"""
male(j1).    %brother
male(k).     %father
male(a).     %uncle
male(v).    %grandfather
male(s).		%greatgrandfather

female(a1).      %me
female(a2).     %sister
female(j2).     %cousin
female(sk).     %mother
female(aa).     %aunt
female(sv).     %grandmother 
female(ps).     %greatgrandmother 

parent(k,a1).
parent(sk,a1).
parent(k,a2).
parent(sk,a2).
parent(a,j1).
parent(aa,j1).

mother(X,Y):-parent(X,Y),female(X).
father(X,Y):-parent(X,Y), male(X).
sibling(X,Y):-parent(Z,X), parent(Z,Y), X \= Y.
grandparent(X,Y):-parent(X,Z),parent(Z,Y).
greatgrandparent(X,Y):-parent(X,Z),grandparent(Z,Y).
uncle(X,Y):- male(X), sibling(X,P), parent(P,Y).
aunt(X,Y):- female(X), sibling(X,P), parent(P,Y).
"""
    print(code)


def fuzzyOperations():
    code=r"""
Program: 1
A={"a":0.2, "b":0.3, "c":0.6, "d":0.6}
B={"a":0.9, "b":0.9, "c":0.4, "d":0.5}
print("The first fuzzy set: ", A)
print("The second fuzzy set: ", B)
#Union
result={}
for i in A:
    if(A[i]>B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("\nUnion of sets A and B is(A U B): ", result)
#Intersection
result={}
for i in A:
    if(A[i]<B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("\nIntersection of sets A and B is(A n B): ", result)
#Complement
result={}
for i in A:
    result[i]=round(1-A[i], 2)
print("\nComplement of set A is(A'): ", result)
for i in B:
    result[i]=round(1-B[i], 2)
print("Complement of set B is(B'): ", result)
#Difference
result={}
for i in A:
    result[i]=round(min(A[i], 1-B[i]), 2)
print("\nDifference of sets A and B is(A - B):", result)

Program: 2
#pip install fuzzywuzzy
 from fuzzywuzzy import fuzz
from fuzzywuzzy import process
 s1 = "I love GeeksforGeeks"
 s2 = "I am loving GeeksforGeeks"
 print("FuzzyWuzzy Ratio: ", fuzz.ratio(s1, s2))
print("FuzzyWuzzy PartialRatio: ", fuzz.partial_ratio(s1, s2))
print("FuzzyWuzzy TokenSortRatio: ", fuzz.token_sort_ratio(s1, s2))
print("FuzzyWuzzy TokenSetRatio: ", fuzz.token_set_ratio(s1, s2))
print("FuzzyWuzzy Weighted Ratio: ", fuzz.WRatio(s1, s2),'\n\n')
# for process library,
query = 'geeks for geeks'
choices = ['geek for geek', 'geek geek', 'g. for geeks']
print("List of ratios: ")
print(process.extract(query, choices), '\n')
print("Best among the above list: ",process.extractOne(query, choices))
"""
    print(code)


def simulateSupervised():
    code=r"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#Generate random data
np.random.seed(0)
x=2*np.random.rand(100,1)
y=4+3*x+np.random.rand(100,1)

#split data into train and test data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#Instantiate linear model
model = LinearRegression()

#Train the model
model.fit(x_train, y_train)

#Make predictions
predictions=model.predict(x_test)

#Plot training data
plt.scatter(x_train, y_train, color='blue', label='Training data')
plt.scatter(x_test, y_test, color='red', label='Testing data')
plt.plot(x_test, predictions, color='green', linewidth=3, label='Predictions')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear regression')
plt.legend()
plt.show()
"""
    print(code)


def simulateUnsupervised():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
np.random.seed(0)
x=np.random.randn(100, 2)
plt.scatter(x[:, 0], x[:, 1], s=50)
plt.title("Randomly generated data points")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

#Applying k-means clustering
kmeans=KMeans(n_clusters=3)
kmeans.fit(x)

#Getting centroids
centroids=kmeans.cluster_centers_
labels=kmeans.labels_

#Visualizing clustered data points
plt.scatter(x[:,0], x[:,1], s=50, cmap='viridis')
plt.scatter(centroids[:,0], centroids[:,1], marker='*', c='red', s=200, label='Centroids')
plt.title("K-means clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.show()
"""
    print(code)

def clustering():
    code=r"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc

# Load customer data
customer_data = pd.read_csv("Mall_Customers.csv")

# Extract relevant features
data = customer_data[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Perform hierarchical clustering
cluster = AgglomerativeClustering(n_clusters=5)
cluster_labels = cluster.fit_predict(data)

# Plot dendrogram
plt.figure(figsize=(10, 7))
plt.title("Customer Dendrogram")
shc.dendrogram(shc.linkage(data, method='ward'))

# Plot clustered data
plt.figure(figsize=(10, 7))
plt.scatter(data[:, 0], data[:, 1], c=cluster_labels, cmap='rainbow')
plt.show()
"""
    print(code)

def svm():
    code=r"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Titanic dataset
titanic = pd.read_csv('train.csv')

# Preprocessing
titanic.drop(['Name', 'Ticket'], axis=1, inplace=True)
titanic['Cabin'].fillna(titanic['Cabin'].value_counts().idxmax(), inplace=True)
titanic['Embarked'].fillna(titanic['Embarked'].value_counts().idxmax(), inplace=True)
titanic['Age'].fillna(titanic['Age'].mean(), inplace=True)
titanic_cat = titanic.select_dtypes(object).apply(LabelEncoder().fit_transform)
titanic_num = titanic.select_dtypes(np.number).drop('PassengerId', axis=1)
titanic_final = pd.concat([titanic_cat, titanic_num], axis=1)

# Train-test split
X = titanic_final.drop('Survived', axis=1)
Y = titanic_final['Survived']
split_idx = int(0.80 * len(X))
X_train, Y_train = X[:split_idx], Y[:split_idx]
X_test, Y_test = X[split_idx:], Y[split_idx:]

# Model training and evaluation
models = [LogisticRegression(), KNeighborsClassifier(), GaussianNB(), LinearSVC(), SVC(kernel='rbf'),
          DecisionTreeClassifier(), RandomForestClassifier()]
for model in models:
    model_fit = model.fit(X_train, Y_train)
    Y_pred = model_fit.predict(X_test)
    accuracy = accuracy_score(Y_pred, Y_test) * 100
    print(f"{model.__class__.__name__} is {accuracy:.2f}% accurate")
"""
    print(code)


def intelligentClothesAgent():
    code=r"""
class ClothesAgent:
    def __init__(self):
        self.weather = None
    
    def get_weather(self):
        self.weather = input("Enter the weather (Sunny, Rainy, Windy, Snowy): ").lower()
    
    def suggest_clothes(self):
        suggestions = {
            "sunny": "light clothes, sunglasses, and sunscreen",
            "rainy": "an umbrella, raincoat, and waterproof shoes",
            "windy": "layers and a jacket",
            "snowy": "a heavy coat, gloves, and boots"
        }
        if self.weather in suggestions:
            print(f"It is {self.weather} outside. You should wear {suggestions[self.weather]}.")
        else:
            print("Sorry, I don't understand the weather conditions. Please enter sunny, rainy, windy, or snowy.")

def main():
    agent = ClothesAgent()
    agent.get_weather()
    agent.suggest_clothes()

if __name__ == "__main__":
    main()
"""
    print(code)



def simulateLanParser():
    code=r"""
import string
def sentence_segment(text):
    return [sentence.strip() for sentence in text.split('.') + text.split('!') + text.split('?') if sentence.strip()]

def remove_punctuation(input_string):
    return ''.join(char for char in input_string if char not in string.punctuation)

def convert_to_lower(s):
    return s.lower()

def tokenize(s):
    return s.split()

text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."

sentences = sentence_segment(text)
punc_removed_text = remove_punctuation(text)
lower_text = convert_to_lower(punc_removed_text)
tokenized_text = tokenize(lower_text)

print(sentences)
print("\n")
print(tokenized_text)
print("\n")

# Tokenization using str.split()
tokens_split = text.split()
print(tokens_split)
print("\n")

sentence = "We're going to John's house today."
tokens_sentence = sentence.split()
print(tokens_sentence)
"""
    print(code)


def feedforward():
    code=r"""
import numpy as np
def relu(n):
    if n<0:
        return 0
    else:
        return n
inp=np.array([[-1,2],[2,2],[3,3]])
weights=[np.array([3,3]),np.array([1,5]),np.array([3,3]),np.array([1,5]),np.array([2,-1])]
for x in inp :
    node0=relu((x*weights[0]).sum())
    node1=relu((x*weights[1]).sum())
    node2=relu(([node0,node1]*weights[2]).sum())
    node3=relu(([node0,node1]*weights[3]).sum())
    op=relu(([node2,node3]*weights[4]).sum())
    print(x,op)
"""
    print(code)

def allml():
    code=r"""
TrainingInstances
EnjoySportsOrNotFindSAlgo
MultiClassUsingIris
MultiClassUsingWine
CandidateElimination
NaiveAndGaussianClassifier
decision
random
pca
linearreg
logisticreg
euclidean
classificationusingk
backpropagate
textprocessing
"""
    print(code)

def TrainingInstances():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

np.random.seed(2)

x = np.random.normal(3, 1, 100)
y = np.random.normal(150, 40, 100) / x

plt.scatter(x, y)
plt.show()

train_x = x[:80]
train_y = y[:80]
test_x = x[80:]
test_y = y[80:]

plt.scatter(train_x, train_y)
plt.show()

train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3)

# Draw polynomial Regression line through the data points with training data
degree = 4
mymodel_train = np.poly1d(np.polyfit(train_x, train_y, degree))
myline_train = np.linspace(0, 6, 100)

plt.scatter(train_x, train_y)
plt.plot(myline_train, mymodel_train(myline_train))
plt.show()

# Draw polynomial Regression line through the data points with test data
mymodel_test = np.poly1d(np.polyfit(test_x, test_y, degree))
myline_test = np.linspace(0, 6, 100)

plt.scatter(test_x, test_y)
plt.plot(myline_test, mymodel_test(myline_test))
plt.show()

# Measures the relationship between x and y axis for training data
r2_train = r2_score(train_y, mymodel_train(train_x))
print("R2 Score (Training Data):", r2_train)

# Measures the relationship between x and y axis for test data
r2_test = r2_score(test_y, mymodel_test(test_x))
print("R2 Score (Test Data):", r2_test)

# Predict the values
prediction = mymodel_test(5)
print("Prediction for x=5:", prediction)

"""
    print(code)


def EnjoySportsOrNotFindSAlgo():
    code=r"""
import csv
num_attributes=6
a=[]
print("\n Given dataset: \n")
with
open(r'C:\Users\admin\Downloads\EnjoySportOrNot\EnjoySportOrNot.csv', 'r')
as csvfile:
 reader=csv.reader(csvfile)
 count=0
 for row in reader:
 if count==0:
 print(row)
 count+=1
 else:
 a.append(row)
 print(row)
 count+=1
print("\n The initial value of hypothesis: ")
hyp=["0"]*num_attributes
print(hyp)
for j in range(0, num_attributes):
 hyp[j]=a[0][j]
 print(hyp)
print("\n Find S: finding a maximally specific hypothesis \n")
for i in range(0, len(a)):
 if a[i][num_attributes]=='Yes':
 for j in range(0, num_attributes):
 if a[i][j]!=hyp[j]:
 hyp[j]='?'
 else:
 hyp[j]=a[i][j]
 print(" For training example no: {0} the hypothesis is ".format(i), hyp)
print(hyp)

"""
    print(code)


def MultiClassUsingIris():
    code=r"""
from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80,
test_size=0.20, random_state=101)
rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X_train, y_train)
poly = svm.SVC(kernel='poly', degree=3, C=1).fit(X_train, y_train)
poly_pred = poly.predict(X_test)
rbf_pred = rbf.predict(X_test)
poly_accuracy = accuracy_score(y_test, poly_pred)
poly_f1 = f1_score(y_test, poly_pred, average='weighted')
print('Accuracy (Polynomial Kernel): ', "%.2f" % (poly_accuracy*100))
print('F1 (Polynomial Kernel): ', "%.2f" % (poly_f1*100))
rbf_accuracy = accuracy_score(y_test, rbf_pred)
rbf_f1 = f1_score(y_test, rbf_pred, average='weighted')
print('Accuracy (RBF Kernel): ', "%.2f" % (rbf_accuracy*100))
print('F1 (RBF Kernel): ', "%.2f" % (rbf_f1*100))

"""
    print(code)


def MultiClassUsingWine():
    code=r"""
from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
wine = datasets.load_wine()
X = wine.data[:, :2]
y = wine.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80,
test_size=0.20, random_state=101)
rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X_train, y_train)
poly = svm.SVC(kernel='poly', degree=3, C=1).fit(X_train, y_train)
poly_pred = poly.predict(X_test)
rbf_pred = rbf.predict(X_test)
poly_accuracy = accuracy_score(y_test, poly_pred)
poly_f1 = f1_score(y_test, poly_pred, average='weighted')
print('Accuracy (Polynomial Kernel): ', "%.2f" % (poly_accuracy*100))
print('F1 (Polynomial Kernel): ', "%.2f" % (poly_f1*100))
rbf_accuracy = accuracy_score(y_test, rbf_pred)
rbf_f1 = f1_score(y_test, rbf_pred, average='weighted')
print('Accuracy (RBF Kernel): ', "%.2f" % (rbf_accuracy*100))
print('F1 (RBF Kernel): ', "%.2f" % (rbf_f1*100))

"""
    print(code)


def CandidateElimination():
    code=r"""
import numpy as np
import pandas as pd

#Loading data from a csv file.
data = pd.DataFrame(data=pd.read_csv('enjoysport.csv'))
print(data)
#Separating concept features from Target
concepts = np.array(data.iloc[:,0:6])
print(concepts)
#Isolating target into a separate DataFrame
#Copying last column to target  array
target = np.array(data.iloc[:,6])
print(target)
def learn(concepts, target): 
#Initialise S0 with the first instance from concepts.
#.copy()makes sure a new list is created instead of just pointing to the same memory location.
    specific_h = concepts[0].copy()
    print("\nInitialization of specific_h and genearal_h")
    print("\nSpecific Boundary: ", specific_h)
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print("\nGeneric Boundary: ",general_h)
# The learning iterations.
    for i, h in enumerate(concepts):
        print("\nInstance", i+1 , "is ", h)
# Checking if the hypothesis has a positive target.
        if target[i] == "yes":
            print("Instance is Positive ")
            for x in range(len(specific_h)): 
# Change values in S & G only if values change.
                if h[x]!= specific_h[x]:                    
                    specific_h[x] ='?'                     
                    general_h[x][x] ='?'
# Checking if the hypothesis has a positive target.                  
        if target[i] == "no":            
            print("Instance is Negative ")
            for x in range(len(specific_h)): 
# For negative hypothesis change values only in G.
                if h[x]!= specific_h[x]:                    
                    general_h[x][x] = specific_h[x]                
                else:                    
                    general_h[x][x] = '?'        
        print("Specific Bundary after ", i+1, "Instance is ", specific_h)         
        print("Generic Boundary after ", i+1, "Instance is ", general_h)
# find indices where we have empty rows, meaning those that are unchanged.
    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]    
    for i in indices:   
# remove those rows from general_h
        general_h.remove(['?', '?', '?', '?', '?', '?']) 
# Return final values
    return specific_h, general_h 
s_final, g_final = learn(concepts, target)
print("Final Specific_h: ", s_final, sep="\n")
print("Final General_h: ", g_final, sep="\n")

"""
    print(code)


def NaiveAndGaussianClassifier():
    code=r"""
import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv('PlayTennis.csv')
print("The first 5 values of data are: \n", data.head())
x = data.iloc[:, :-1].copy()  # Make a copy of the DataFrame
print("\nThe First 5 values of train data are: \n", x.head())
y = data.iloc[:, -1]
print("\nThe first 5 values of Train output are: \n", y.head())

le_outlook = LabelEncoder()
x['Outlook'] = le_outlook.fit_transform(x['Outlook'])
le_Temperature = LabelEncoder()
x['Temperature'] = le_Temperature.fit_transform(x['Temperature'])
le_Humidity = LabelEncoder()
x['Humidity'] = le_Humidity.fit_transform(x['Humidity'])
le_Wind = LabelEncoder()
x['Wind'] = le_Wind.fit_transform(x['Wind'])

print("\nNow the Train data is : \n", x.head())

le_PlayTennis = LabelEncoder()
y = le_PlayTennis.fit_transform(y)
print("\nNow the Train output is: \n", y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
classifier = GaussianNB()
classifier.fit(x_train, y_train)

print("Accuracy is: ", accuracy_score(classifier.predict(x_test), y_test))

"""
    print(code)

def decision():
    code=r"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
#%matplotlib inline
df = pd.read_csv(r"WA_Fn-UseC_-HR-Employee-Attrition.csv")
df.head()
# Exploratory Data Analysis
sns.countplot(x='Attrition', data=df)
plt.show()
from pandas.core.arrays import categorical
df.drop(['EmployeeCount','EmployeeNumber', 'Over18', 'StandardHours'], axis="columns",
inplace=True)
categorical_col = []
for column in df.columns:
 if df[column].dtype == object:
     categorical_col.append(column)
df['Attrition'] = df.Attrition.astype("category").cat.codes
from sklearn.preprocessing import LabelEncoder
for column in categorical_col:
 df[column] = LabelEncoder().fit_transform(df[column])
from sklearn.model_selection import train_test_split
X = df.drop('Attrition', axis=1)
y = df.Attrition
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
def print_score(clf, X_train, y_train, X_test, y_test, train=True):
 if train:
     pred = clf.predict(X_train)
     clf_report = pd.DataFrame(classification_report(y_train, pred, output_dict=True))
     print("Train Result:\n=======================================")
     print(f"Accuracy Score: {accuracy_score(y_train, pred) * 100:.2f}%")
     print(" ")
     print(f"CLASSIFICATION REPORT:\n{clf_report}")
     print(" ")
     print(f"Confusion Matrix: \n{confusion_matrix(y_train, pred)}\n")
 elif train==False:
     pred = clf.predict(X_test)
     clf_report = pd.DataFrame(classification_report(y_test, pred, output_dict=True))
     print("Test Result:\n=======================================")
     print(f"Accuracy Score: {accuracy_score(y_test, pred) * 100:.2f}%")
     print(" ")
     print(f"CLASSIFICATION REPORT:\n{clf_report}")
     print(" ")
     print(f"Confusion Matrix: \n{confusion_matrix(y_test, pred)}\n")
from sklearn.tree import DecisionTreeClassifier
from pickle import TRUE
from sklearn.tree import DecisionTreeClassifier
tree_clf = DecisionTreeClassifier(random_state=42)
tree_clf.fit(X_train, y_train)
print_score(tree_clf, X_train, y_train, X_test, y_test, train=True)
print_score(tree_clf, X_train, y_train, X_test, y_test, train=False)
from sklearn.ensemble import RandomForestClassifier
rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)
print_score(rf_clf, X_train, y_train, X_test, y_test, train=True)
print_score(rf_clf, X_train, y_train, X_test, y_test, train=False)
"""
    print(code)

def random():
    code=r"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Define the print_score function
def print_score(clf, X_train, y_train, X_test, y_test, train=True):
    if train:
        pred = clf.predict(X_train)
        clf_report = pd.DataFrame(classification_report(y_train, pred, output_dict=True))
        print("Train Result:\n=======================================")
        print(f"Accuracy Score: {accuracy_score(y_train, pred) * 100:.2f}%")
        print(" ")
        print(f"CLASSIFICATION REPORT:\n{clf_report}")
        print(" ")
        print(f"Confusion Matrix: \n{confusion_matrix(y_train, pred)}\n")
    else:
        pred = clf.predict(X_test)
        clf_report = pd.DataFrame(classification_report(y_test, pred, output_dict=True))
        print("Test Result:\n=======================================")
        print(f"Accuracy Score: {accuracy_score(y_test, pred) * 100:.2f}%")
        print(" ")
        print(f"CLASSIFICATION REPORT:\n{clf_report}")
        print(" ")
        print(f"Confusion Matrix: \n{confusion_matrix(y_test, pred)}\n")

# Load the dataset
df = pd.read_csv(r"WA_Fn-UseC_-HR-Employee-Attrition.csv")

# EDA
sns.countplot(x='Attrition', data=df)
plt.show()

# Drop unnecessary columns
df.drop(['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours'], axis="columns", inplace=True)

# Convert categorical columns to numerical
categorical_col = [col for col in df.columns if df[col].dtype == object]
df['Attrition'] = df['Attrition'].astype("category").cat.codes

for column in categorical_col:
    df[column] = LabelEncoder().fit_transform(df[column])

# Split the data
X = df.drop('Attrition', axis=1)
y = df['Attrition']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a RandomForestClassifier
classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

# Call print_score function for both training and testing
print_score(classifier, X_train, y_train, X_test, y_test, train=True)
print_score(classifier, X_train, y_train, X_test, y_test, train=False)
"""
    print(code)

def pca():
    code=r"""
import numpy as np
import pandas as pd
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
dataset = pd.read_csv(url, names=names)
dataset.head()
x = dataset.drop('Class',1)
y = dataset['Class']
y.head()
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train1 = sc.fit_transform(x_train)
x_test1 = sc.transform(x_test)
y_train1 = y_train
y_test1 = y_test
from sklearn.decomposition import PCA
pca = PCA()
x_train1 = pca.fit_transform(x_train1)
x_test1 = pca.transform(x_test1)
explained_variance = pca.explained_variance_ratio_
print ("Explained variance: ", explained_variance)
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(max_depth=2, random_state=0)
classifier.fit(x_train1,y_train1)
y_pred = classifier.predict(x_test1)
#Confusion matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
print('Accuracy', accuracy_score(y_test1, y_pred))
"""
    print(code)


def linearreg():
    code=r"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12.0, 9.0)
# Preprocessing Input data
data = pd.read_csv(r"C:\\Users\\Aditi\\OneDrive\\Documents\\Python Scripts\\data.csv")
X = data.iloc[:, 0]
Y = data.iloc[:, 1]
plt.scatter(X, Y)
plt.show()
# Building the model
X_mean = np.mean(X)
Y_mean = np.mean(Y)
num = 0
den = 0
for i in range(len(X)):
    num += (X[i] - X_mean)*(Y[i] - Y_mean)
    den += (X[i] - X_mean)**2
m = num / den
c = Y_mean - m*X_mean
# Making predictions
Y_pred = m*X + c
plt.scatter(X, Y) 
plt.plot([min(X), max(X)], [min(Y_pred), max(Y_pred)], color='red') # predicted
plt.show()
"""
    print(code)

def logisticreg():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset = pd.read_csv(r"C:\Users\Aditi\OneDrive\Documents\Python Scripts\DMVWrittenTests.csv")
X = dataset.iloc[:, [0, 1]].values
y = dataset.iloc[:, 2].values
dataset.head(5)
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
# Feature Scaling is used to normalize the data within a particular range. It also aids in speeding up the calculations.
# As the data is widely varying, we use this function to limit the range of the data within a small limit ( -2,2).
#For example, the score 62.0730638 is normalized to -0.21231162 and the score 96.51142588 is normalized to 1.55187648. In this way, the scores of X_train and X_test are normalized to a smaller range.
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
# Training the Logistic Regression model on the Training Set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
#predicting the test set results
y_pred = classifier.predict(X_test)
y_pred
#confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
from sklearn.metrics import accuracy_score
print("Accuracy Score of Logistic Regression: ", accuracy_score(y_test,y_pred),"\n")
print("Confusion Matrix: \n",cm)
"""
    print(code)

def euclidean():
    code=r"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
df = pd.read_csv(r"C:\Users\Aditi\OneDrive\Documents\Python Scripts\iris.csv")
df.head(5)
X = df.drop(['variety'], axis=1)
y = df['variety']
X_train, X_test, y_train , y_test = train_test_split(X, y, test_size=0.3, random_state=0)
knn = KNeighborsClassifier(n_neighbors= 6, p = 2, metric='minkowski')
knn.fit(X_train, y_train)
print(knn.score(X_test,y_test))
y_pred = knn.predict(X_test)
from sklearn.metrics import confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm)
knn = KNeighborsClassifier(n_neighbors= 6, p = 1, metric='minkowski')
knn.fit(X_train, y_train)
print(knn.score(X_test,y_test))
from sklearn.metrics import confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm)
"""
    print(code)

def classficationusingk():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
dataset = pd.read_csv(r"C:\Users\Aditi\OneDrive\Documents\Python Scripts\Mall_Customers.csv")
X = dataset.iloc[:, [3,4]].values
from sklearn.cluster import KMeans
wcss=[]
for i in range(1,11):
 kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
 kmeans.fit(X)
 wcss.append(kmeans.inertia_)
plt.plot(range(1,11), wcss)
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
kmeans = KMeans(n_clusters= 5, init= "k-means++", random_state=42)
y_kmeans = kmeans.fit_predict(X)
plt.scatter(X[y_kmeans == 0,0], X[y_kmeans == 0,1], s = 60, c='red', label = 'Cluster1')
plt.scatter(X[y_kmeans == 1,0], X[y_kmeans == 1,1], s = 60, c='blue', label = 'Cluster2')
plt.scatter(X[y_kmeans == 2,0], X[y_kmeans == 2,1], s = 60, c='green', label = 'Cluster3')
plt.scatter(X[y_kmeans == 3,0], X[y_kmeans == 3,1], s = 60, c='violet', label = 'Cluster4')
plt.scatter(X[y_kmeans == 4,0], X[y_kmeans == 4,1], s = 60, c='yellow', label = 'Cluster5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=100, c='black', label = 'Centroids')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()
plt.scatter(X[y_kmeans == 0,0], X[y_kmeans== 0,1], s=100, c='red', label = 'Careful')
plt.scatter(X[y_kmeans == 1,0], X[y_kmeans== 1,1], s=100, c='blue', label = 'Standard')
plt.scatter(X[y_kmeans == 2,0], X[y_kmeans== 2,1], s=100, c='green', label = 'Target')
plt.scatter(X[y_kmeans == 3,0], X[y_kmeans== 3,1], s=100, c='violet', label = 'Careless')
plt.scatter(X[y_kmeans == 4,0], X[y_kmeans== 4,1], s=100, c='yellow', label = 'Sensible')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=100, c='black', label = 'Centroids')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.title('Cluster of Customers')
plt.legend()
plt.show()"""
    print(code)

def backpropagate():
    code=r"""import numpy as np
X=np.array(([2,9],[1,5],[3,6]),dtype=float)
Y=np.array(([92],[86],[89]),dtype=float)
X=X/np.amax(X,axis=0)
Y=Y/100;

class NN(object):
    def __init__(self):
        self.inputsize=2
        self.outputsize=1
        self.hiddensize=3
        self.W1=np.random.randn(self.inputsize,self.hiddensize)
        self.W2=np.random.randn(self.hiddensize,self.outputsize)
    def forward(self,X):
        self.z=np.dot(X,self.W1)
        self.z2=self.sigmoidal(self.z)
        self.z3=np.dot(self.z2,self.W2)
        op=self.sigmoidal(self.z3)
        return op;
    def sigmoidal(self,s):
        return 1/(1+np.exp(-s))
    def sigmoidalprime(self,s):
        return s* (1-s)
    def backward(self,X,Y,o):
        self.o_error=Y-o
        self.o_delta=self.o_error * self.sigmoidalprime(o)
        self.z2_error=self.o_delta.dot(self.W2.T)
        self.z2_delta=self.z2_error * self.sigmoidalprime(self.z2)
        self.W1 = self.W1 + X.T.dot(self.z2_delta)
        self.W2= self.W2+ self.z2.T.dot(self.o_delta)
    def train(self,X,Y):
        o=self.forward(X)
        self.backward(X,Y,o)
obj=NN()
for i in range(4):
    print("input"+str(X))
    print("Actual output"+str(Y))
    print("Predicted output"+str(obj.forward(X)))
    print("loss"+str(np.mean(np.square(Y-obj.forward(X)))))
    obj.train(X,Y)
"""
    print(code)

def textprocessing():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []

for i in range(0,1000):
  review = re.sub('[^a-zA-Z]','',dataset['Review'][i])
  review = review.lower()
  review = review.split()
  ps = PorterStemmer()
  review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
  review = ''.join(review)
  corpus.append(review)


#Creating the bag of words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1500)
X = cv.fit_transform(corpus).toarray()
Y = dataset.iloc[:,1].values

#Splitting the dataset into the training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.25, random_state=100)


#Fitting naive bayes to the training set.
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, Y_train)


# Predicting the test set results.
Y_pred = classifier.predict(X_test)

#Model Accuracy
from sklearn import metrics
from sklearn.metrics import confusion_matrix
print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))


#Making the confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, Y_pred)
print(cm)
"""
    print(code)
    
def amp():
    code=r"""
Image and Background
2.a) Design an Activity with an image and its background colour set.
Main Activity code:
package com.example.prac2

import android.support.v7.app.AppCompatActivity
import android.os.Bundle

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}

Colors.xml code:
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="green">#00FF00</color>
    <color name="yellow"> #FFFF00</color>
    <color name="red">#ff0000</color>
</resources>

Strings.xml code:
<resources>
    <string name="app_name">zoro</string>
</resources>

Xml code:
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/red"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:background="@color/red"
        android:textColor="@color/green"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <ImageView
        android:id="@+id/imageView"
        android:layout_width="309dp"
        android:layout_height="663dp"
        app:srcCompat="@drawable/zoro"
        tools:layout_editor_absoluteX="61dp"
        tools:layout_editor_absoluteY="-156dp"
        tools:ignore="MissingConstraints" />

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="click me"
        android:textColor="@color/green"
        tools:layout_editor_absoluteX="161dp"
        tools:layout_editor_absoluteY="460dp"
        tools:ignore="MissingConstraints" />

</android.support.constraint.ConstraintLayout>

Output:
 

Activity Life Cycle
5.a) To demonstrate the working of Activity and its Life Cycle.
XML FILE:-
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</android.support.constraint.ConstraintLayout>

Main Activity.kt file:-
package com.example.ampprac3

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val toast = Toast.makeText( this,"On Create called",Toast.LENGTH_SHORT).show()

    }

    override fun onStart() {
        super.onStart()
        val toast = Toast.makeText( this,"On Start called",Toast.LENGTH_SHORT).show()
    }

    override fun onStop() {
        super.onStop()
        val toast = Toast.makeText( this,"On Stop called",Toast.LENGTH_SHORT).show()
    }

    override fun onRestart() {
        super.onRestart()
        val toast = Toast.makeText( this,"On Restart called",Toast.LENGTH_SHORT).show()
    }

    override fun onResume() {
        super.onResume()
        val toast = Toast.makeText( this,"On Resume called",Toast.LENGTH_SHORT).show()
    }

    override fun onPause() {
        super.onPause()
        val toast = Toast.makeText( this,"On Pause called",Toast.LENGTH_SHORT).show()
    }

    override fun onDestroy() {
        super.onDestroy()
        val toast = Toast.makeText( this,"On Destroy called",Toast.LENGTH_SHORT).show()

    }
}
OUTPUT: -


Fragment Life Cycle
5.b) To demonstrate the working of Fragments and its Life Cycle.
Main Activity -
package com.example.amp_prac3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    private val fragMgr = supportFragmentManager
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val toast = Toast.makeText(this, "ON CREATE CALLED", Toast.LENGTH_LONG).show()
    }

    fun onClickLogin(view: View){
        val fragTrans = fragMgr.beginTransaction()
        fragTrans.add(R.id.frameLayout, login_fragment())
        fragTrans.addToBackStack(null)
        fragTrans.commit()
    }

    fun onClickSignup(view: View){
        val fragTrans = fragMgr.beginTransaction()
        fragTrans.add(R.id.frameLayout, sign_up_fragment())
        fragTrans.addToBackStack(null)
        fragTrans.commit()
    }

}
Main Activity XML - 
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <LinearLayout
        android:layout_width="409dp"
        android:layout_height="354dp"
        android:orientation="horizontal"
        app:layout_constraintBottom_toTopOf="@+id/frameLayout"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        >

        <Button
            android:id="@+id/button2"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:onClick="onClickLogin"
            android:text="Login" />

        <FrameLayout
            android:id="@+id/frameLayout"
            android:layout_width="wrap_content"
            android:layout_height="match_parent"
            android:layout_weight="1">
        </FrameLayout>

        <Button
            android:id="@+id/button3"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:onClick="onClickSignup"
            android:text="Sign In" />
    </LinearLayout>

    <TextView
        android:id="@+id/textView3"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
Login_fragment.kt File -
package com.example.amp_prac3

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment

class login_fragment:Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.login,container,false)
    }
}
Login.xml File -
TextView “Login” Only.
sign_up_fragment.kt File -
override fun onCreateView(
    inflater: LayoutInflater,
    container: ViewGroup?,
    savedInstanceState: Bundle?
): View? {
    return inflater.inflate(R.layout.sign_up,container,false)
}
Sign_up.xml File -
TextView “Sign Up” Only.


Output -


 Linear Layout
4.a) To demonstrate Linear Layout.

DESIGN:-

add linear layout vertical
textview - login page
editname - name
editpass - password
add linear layout horizontal
btn - submit
btn - reset

 

Main_Activity.xml Code:-

<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <LinearLayout
        android:layout_width="409dp"
        android:layout_height="729dp"
        android:orientation="vertical"
        tools:layout_editor_absoluteX="1dp"
        tools:layout_editor_absoluteY="1dp">

        <TextView
            android:id="@+id/textView2"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Login Page" />

        <EditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/editname"
            android:hint="enter your name"
            android:inputType="text" />

        <EditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/editpass"
            android:hint="enter password"
            android:inputType="text" />


        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="horizontal" >

            <Button
                android:id="@+id/btnsubmit"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="SUBMIT" />

            <Button
                android:id="@+id/btnreset"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="RESET" />
        </LinearLayout>
    </LinearLayout>
</android.support.constraint.ConstraintLayout>


MainActivity.xml Code:-

package com.example.rvprac4

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

    val submitbtn = findViewById<Button>(R.id.btnsubmit)
    val resetbtn = findViewById<Button>(R.id.btnreset)
    val name = findViewById<EditText>(R.id.editname)
    val pass = findViewById<EditText>(R.id.editpass)

    submitbtn.setOnClickListener(){
        Toast.makeText(this, "Data Submitted", Toast.LENGTH_LONG).show()
    }

    resetbtn.setOnClickListener(){
        name.editableText.clear()
        pass.editableText.clear()
    }
  }

}





OUTPUT:-

 

Table Layout
4.b) To demonstrate Table Layout.
Main_Activity.xml Code:-


<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <LinearLayout
        android:layout_width="409dp"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        tools:layout_editor_absoluteX="1dp"
        tools:layout_editor_absoluteY="1dp">

        <TextView
            android:id="@+id/textView"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Login page" />

        <EditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/editname"
            android:hint="enter your name"
            android:inputType="text" />

        <EditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/editpass"
            android:hint="enter password"
            android:inputType="text" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="horizontal">

            <Button
                android:id="@+id/btnsubmit"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="SUBMIT" />

            <Button
                android:id="@+id/btnreset"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="RESET" />
        </LinearLayout>
    </LinearLayout>

</androidx.constraintlayout.widget.ConstraintLayout>

 

MainActivity.xml Code:-

package com.example.randi1

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast

abstract class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val submitbtn = findViewById<Button>(R.id.btnsubmit)
        val resetbtn = findViewById<Button>(R.id.btnreset)
        val name = findViewById<EditText>(R.id.editname)
        val pass = findViewById<EditText>(R.id.editpass)

        submitbtn.setOnClickListener() {

            Toast.makeText(this, "Data Submitted",Toast.LENGTH_SHORT).show()
        }

        resetbtn.setOnClickListener() {
            name.editableText.clear()
            pass.editableText.clear()
        }
    }
}

OUTPUT-


 	
Practical #5

Application Bar
7.a) Design a mobile application to demonstrate working of App Bar

Activity_main.xml File:-

<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</android.support.constraint.ConstraintLayout>


MainActivity.kt File:-

package com.example.prac5

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.support.v7.app.ActionBar
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val ActionBar = supportActionBar
        ActionBar!!.title = "Mera Naya Action Bar"
        ActionBar.subtitle = "Naya Hai Woh"
        ActionBar.setIcon(R.drawable.search)
        ActionBar.setDisplayUseLogoEnabled(true)
        ActionBar.setDisplayShowHomeEnabled(true)

    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu1,menu)
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when(item.itemId){
            R.id.Copy -> Toast.makeText(this,"Copy", Toast.LENGTH_LONG).show()
            R.id.Search -> Toast.makeText(this,"Search", Toast.LENGTH_LONG).show()
            R.id.Location -> Toast.makeText(this,"Location", Toast.LENGTH_LONG).show()
            R.id.call -> Toast.makeText(this,"Call", Toast.LENGTH_LONG).show()
        }
        return super.onOptionsItemSelected(item)
    }


    }



AndroidManiFest.xml File:-


<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.example.prac4b">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@drawable/call"
        android:label="Action Bar"
        android:roundIcon="@drawable/search"
        android:supportsRtl="true"
        android:theme="@style/Theme.Prac4b"
        tools:targetApi="31">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>



Menu1.xml File:-

<?xml version="1.0" encoding="utf-8"?>
<menu
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <item android:id="@+id/Search"
        android:title="Search"
        android:icon="@drawable/search"
        android:orderInCategory="100"
        app:showAsAction="always"/>

    <item android:id="@+id/Copy"
        android:title="Copy"
        android:icon="@drawable/call"
        android:orderInCategory="100"
        app:showAsAction="ifRoom"/>

    <item android:id="@+id/Location"
        android:title="Location"
        android:icon="@drawable/imagesr"
        android:orderInCategory="100"
        app:showAsAction="withText"/>

    <item android:id="@+id/call"
        android:title="call"
        android:icon="@drawable/search"
        android:orderInCategory="100"
        app:showAsAction="never"/>

</menu>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
Strings.xml File:-

<resources>
    <string name="app_name">Action Bar</string>
</resources>

OUTPUT:-
 
 
 
 
 
Login Form
7.b) Design a mobile application to create a login form
Activity_main.xml:
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity">
<LinearLayout
android:layout_width="383dp" android:layout_height="431dp" android:layout_marginStart="8dp" android:layout_marginTop="8dp" android:layout_marginEnd="8dp" android:layout_marginBottom="271dp" android:orientation="vertical" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toTopOf="parent">
<TextView
android:id="@+id/textView1" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="What is your name?" android:textSize="24sp" />
<EditText
android:id="@+id/edtxtname" android:layout_width="match_parent" android:layout_height="wrap_content" android:hint="Enter your name..." android:inputType="text" android:textSize="24sp" />
<TextView
android:id="@+id/textView2" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="What is your E-mail ID?" android:textSize="24sp" />
<EditText
android:id="@+id/edtxtemail" android:layout_width="match_parent" android:layout_height="wrap_content" android:hint="Enter your E-mail..." android:inputType="text" android:textSize="24sp" />
<TextView
android:id="@+id/show" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="" android:textSize="24sp" />
<LinearLayout
android:layout_width="match_parent" android:layout_height="127dp" android:orientation="horizontal">
<Button
android:id="@+id/btnsubmit" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_weight="1" android:text="SUBMIT" />
<Button
android:id="@+id/btnreset" android:layout_width="wrap_content"
android:layout_height="wrap_content" android:layout_weight="1" android:text="RESET" />
</LinearLayout>
</LinearLayout>
</android.support.constraint.ConstraintLayout>

MainActivity.kt File:Tarang Pa
package com.example.practical5
import android.support.v7.app.AppCompatActivity import android.os.Bundle
import android.widget.Button import android.widget.EditText import android.widget.TextView import android.widget.Toast
class MainActivity : AppCompatActivity() {
override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState) setContentView(R.layout.activity_main)
val name = findViewById<EditText>(R.id.edtxtname) val email = findViewById<EditText>(R.id.edtxtemail) val submit = findViewById<Button>(R.id.btnsubmit) val reset = findViewById<Button>(R.id.btnreset)
val show = findViewById<TextView>(R.id.show)
submit.setOnClickListener {
show.setText("Name: "+name.text.toString()+"\nEmail: "+email.text.toString())
Toast.makeText(this,"Record Submitted!",Toast.LENGTH_LONG).show()
}
reset.setOnClickListener { name.text.clear() email.text.clear() show.setText("") Toast.makeText(this,"Record
Cleared!",Toast.LENGTH_LONG).show()
}
}
}

OUTPUT:-


 Intent
7. a) To create a program to implement intent (Implicit and Explicit).
MainActivity.kt

package com.example.amp_7_1

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Finding the button with id 'button' and setting click listener
        val click = findViewById<Button>(R.id.button);

        // Showing a toast message when the button is clicked
        click.setOnClickListener {
            Toast.makeText(this,"Button Click", Toast.LENGTH_SHORT).show();
        }

        // Finding TextView and EditText views by their respective ids
        val disp = findViewById<TextView>(R.id.textView2)
        val fname = findViewById<EditText>(R.id.editText)

        // Adding TextWatcher to the EditText
        fname.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(p0: Editable?) {
            // Not used
            }

            override fun beforeTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
            // Not used
            }

            override fun onTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
                // Setting the text of the TextView based on the input in EditText
                disp.setText("My Name is : "+p0)
            }
        })
    }
}

activity_main.xml 

<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">
        <TextView
            android:id="@+id/textView"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Enter your name"
            tools:layout_editor_absoluteX="50dp"
            tools:layout_editor_absoluteY="138dp" />
        <TextView
            android:id="@+id/textView2"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="TextView"
            tools:layout_editor_absoluteX="50dp"
            tools:layout_editor_absoluteY="49dp" />
        <EditText
            android:id="@+id/editText"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:ems="10"
            android:inputType="textPersonName"
            android:text="Name"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            tools:layout_editor_absoluteY="274dp" />
        <Button
            android:id="@+id/button"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="click Button"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            tools:layout_editor_absoluteY="396dp" />
    </LinearLayout>
</android.support.constraint.ConstraintLayout>

OUTPUT:
     

7. b)
Activity_main,xml:

<?xml version="1.0" encoding="utf-8"?>
 <android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
     xmlns:app="http://schemas.android.com/apk/res-auto"
     xmlns:tools="http://schemas.android.com/tools"
     android:layout_width="match_parent"
     android:layout_height="match_parent"
     tools:context=".MainActivity">
 
    <LinearLayout
         android:layout_width="match_parent"
         android:layout_height="match_parent"
         android:orientation="vertical">
 
        <Button
             android:id="@+id/btnintent1"
             android:layout_width="match_parent"
             android:layout_height="wrap_content"
             android:textStyle="bold"
             android:text="CLICK FOR INTENT" />
 
        <Button
             android:id="@+id/btnintent2"
             android:layout_width="match_parent"
             android:layout_height="wrap_content"
             android:textStyle="bold"
             android:text="CLICK FOR BROWSER" />
 
        <EditText
             android:layout_width="match_parent"
             android:layout_height="wrap_content"
             android:id="@+id/editShare"
             android:text="Type message to share"
             android:textSize="22dp"
             android:layout_marginTop="10dp"/>
 
        <Button
             android:id="@+id/btnintent3"
             android:layout_width="match_parent"
             android:layout_height="wrap_content"
             android:textStyle="bold"
             android:text="CLICK TO SHARE DATA" />
     </LinearLayout>
</android.support.constraint.ConstraintLayout>
 
MainActivity.xml:

package com.example.myapplication
 
import android.support.v7.app.AppCompatActivity
 import android.os.Bundle
 import android.net.Uri
 import android.content.Intent
 import android.widget.EditText
 import android.widget.Button
 
class MainActivity : AppCompatActivity() {
     override fun onCreate(savedInstanceState: Bundle?) {
         super.onCreate(savedInstanceState)
         setContentView(R.layout.activity_main)
         val btnintent1 = findViewById<Button>(R.id.btnintent1)
         val btnintent2 = findViewById<Button>(R.id.btnintent2)
         val btnintent3 = findViewById<Button>(R.id.btnintent3)
         val editshare = findViewById<EditText>(R.id.editShare)
 
        btnintent3.setOnClickListener {
             val msg : String = editshare.text.toString();
             val intent3 = Intent()
             intent3.action = Intent.ACTION_SEND
             intent3.putExtra(Intent.EXTRA_TEXT, msg)
             intent3.type = "text/plain"
             startActivity(Intent.createChooser(intent3,"Share Data"))
         }
 
        btnintent2.setOnClickListener {
             val intent2 = Intent()
             intent2.action = Intent.ACTION_VIEW
             intent2.data = Uri.parse("https://www.rediff.com/")
             startActivity(intent2)
         }
 
        btnintent1.setOnClickListener {
             val intent1 = Intent(this,MainActivity2::class.java)
             startActivity(intent1)
         }
     }
 }
 
Activity_main2.xml:

<?xml version="1.0" encoding="utf-8"?>
 <android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
     xmlns:app="http://schemas.android.com/apk/res-auto"
     xmlns:tools="http://schemas.android.com/tools"
     android:layout_width="match_parent"
     android:layout_height="match_parent"
     tools:context=".MainActivity2">
 
    <RelativeLayout
         android:layout_width="match_parent"
         android:layout_height="match_parent"
         android:orientation="horizontal">
 
        <EditText
             android:layout_width="match_parent"
             android:layout_height="wrap_content"
             android:text="This is Activity 2"
             android:textAlignment="center"
             android:layout_alignParentBottom="true"
             android:layout_alignParentTop="true"
             android:textSize="30dp" />
    </RelativeLayout>
 </android.support.constraint.ConstraintLayout>
 
OUTPUT:


 	
Notification
8.a) Design an Android mobile application to demonstrate the working of notifications. [Hint: create and display the notification with help of button]
Activity_main.xml:-
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
xmlns:app="http://schemas.android.com/apk/res-auto"
xmlns:tools="http://schemas.android.com/tools"
android:layout_width="match_parent"
android:layout_height="match_parent"
tools:context=".MainActivity">
<Button
android:id="@+id/notifyButton"
android:layout_width="wrap_content"
android:layout_height="wrap_content"
android:layout_centerInParent="true"
android:text="Show Notification" />
</RelativeLayout>

MainActivity.kt:-
package com.example.notification1
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.graphics.Color
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
class MainActivity : AppCompatActivity() {
private val channelId = "sample_channel"
private val notificationId = 101
override fun onCreate(savedInstanceState: Bundle?) {
super.onCreate(savedInstanceState)
setContentView(R.layout.activity_main)
val button = findViewById<Button>(R.id.notifyButton)
button.setOnClickListener {
createNotificationChannel()
sendNotification()
}
Vidyalankar School of Information Technology
}
private fun createNotificationChannel() {
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
val name = "Sample Channel"
val descriptionText = "This is a sample notification channel."
val importance = NotificationManager.IMPORTANCE_DEFAULT
val channel = NotificationChannel(channelId, name, importance).apply {
description = descriptionText
}
val notificationManager: NotificationManager =
getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
notificationManager.createNotificationChannel(channel)
}
}
private fun sendNotification() {
val builder = NotificationCompat.Builder(this, channelId)
.setSmallIcon(R.drawable.ic_launcher_background)
.setContentTitle("Sample Notification")
.setContentText("This is a sample notification.")
.setPriority(NotificationCompat.PRIORITY_DEFAULT)
with(NotificationManagerCompat.from(this)) {
notify(notificationId, builder.build())
}
}
}

OUTPUT:-
 
 

Broadcast Receiver
8.b) Design an Android mobile application to show the working of broadcast receiver.
activity_main.xml :-
 
<?xml version="1.0" encoding="utf-8"?>
 <RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
     xmlns:app="http://schemas.android.com/apk/res-auto"
     xmlns:tools="http://schemas.android.com/tools"
     android:layout_width="match_parent"
     android:layout_height="match_parent"
     tools:context=".MainActivity">
     <Button
         android:id="@+id/notifyButton"
         android:layout_width="wrap_content"
         android:layout_height="wrap_content"
         android:layout_centerInParent="true"
         android:text="Show Notification" />
 </RelativeLayout>
 
 
 Design:-
 
MainActivity.kt :-
package com.example.myapplication
 
import android.app.NotificationChannel
 import android.app.NotificationManager
 import android.content.Context
 import android.os.Build
 import android.support.v7.app.AppCompatActivity
 import android.os.Bundle
 import android.support.v4.app.NotificationCompat
 import android.support.v4.app.NotificationManagerCompat
 import android.widget.Button
 
class MainActivity : AppCompatActivity() {
 
    private val channelId = "sample_channel"
     private val notificationId = 101
 
    override fun onCreate(savedInstanceState: Bundle?) {
         super.onCreate(savedInstanceState)
         setContentView(R.layout.activity_main)
 
        val button = findViewById<Button>(R.id.notifyButton)
         button.setOnClickListener {
             createNotificationChannel()
             sendNotification()
         }
     }
 
    private fun createNotificationChannel() {
         if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
             val name = "Sample Channel"
             val descriptionText = "This is a sample notification channel."
             val importance = NotificationManager.IMPORTANCE_DEFAULT
             val channel = NotificationChannel(channelId, name, importance).apply {
                 description = descriptionText
             }
             val notificationManager: NotificationManager =
                 getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
             notificationManager.createNotificationChannel(channel)
         }
     }
 
    private fun sendNotification() {
         val builder = NotificationCompat.Builder(this, channelId)
             .setSmallIcon(R.drawable.ic_launcher_background)
             .setContentTitle("Sample Notification")
             .setContentText("This is a sample notification.")
             .setPriority(NotificationCompat.PRIORITY_DEFAULT)
 
        with(NotificationManagerCompat.from(this)) {
             notify(notificationId, builder.build())
         }
     }
 }


Output :- 
 
 	

 Media API
10.a) To create a program to access music (media) in your mobile phone.
Activity_main.xml :
 
<?xml version="1.0" encoding="utf-8"?> 
<RelativeLayout 
     xmlns:android="http://schemas.android.com/apk/res/android" 
     xmlns:tools="http://schemas.android.com/tools"    
     android:layout_width="match_parent"
     android:layout_height="match_parent"    
     android:gravity="center" 
     tools:context=".MainActivity">
     android:orientation="vertical"
 
     <Button 
         android:id="@+id/button1" 
         android:layout_width="wrap_content" 
         android:layout_height="wrap_content" 
         android:layout_alignParentStart="true"
         android:layout_alignParentTop="true" 
         android:layout_marginStart="122dp" 
         android:layout_marginTop="61dp" 
         tools:ignore="HardcodedText        
         android:text="Play" />

     <Button 
         android:id="@+id/button2" 
         android:layout_width="wrap_content"
         android:layout_height="wrap_content" 
         android:layout_alignStart="@+id/button1" 
         android:layout_alignParentTop="true"
         android:layout_marginTop="128dp"         
         android:text="Pause" />
         
    <Button 
        android:id="@+id/button3"         
        android:layout_width="wrap_content"  
        android:layout_height="wrap_content"  
        android:layout_alignStart="@+id/button1" 
        android:layout_alignParentTop="true" 
        android:layout_marginTop="205dp"
        android:text="Continue" />
                        
   <Button 
       android:id="@+id/button4"
       android:layout_width="wrap_content" 
       android:layout_height="wrap_content"
       android:layout_alignStart="@+id/button1" 
       android:layout_alignParentBottom="true" 
       android:layout_marginBottom="186dp"/>
       android:text="Stop" />
   
   <Button 
       android:id="@+id/button5" 
       android:layout_width="wrap_content"        
       android:layout_height="wrap_content" 
       android:layout_alignParentBottom="true"
       android:layout_alignStart="@+id/button1" 
       android:layout_marginBottom="100dp"/>
       android:text="Button"
</RelativeLayout>

      
MainActivity.kt :
 
package com.example.music 
 
import android.os.Bundle 
Import android.media.MediaPlayer 
import android.widget.Button 
import androidx.appcompat.app.AppCompatActivity 
 
class MainActivity : AppCompatActivity() {    
 private lateinit var mp: MediaPlayer 
     override fun onCreate(savedInstanceState: Bundle?) {         
          super.onCreate(savedInstanceState)      
          setContentView(R.layout.activity_main)         

          mp = MediaPlayer.create (this,R.raw.song1)        
          mp = MediaPlayer.create (this,R.raw.song)         
          var position = 0         
          val button1 = findViewById (R.id.button1) as Button        
          val button2 = findViewById (R.id.button2) as Button         
          val button3 = findViewById (R.id.button3) as Button         
          val button4 = findViewById (R.id.button4) as Button        
          val button5 = findViewById (R.id.button5) as Button
         
          button1.setOnClickListener {            
          mp.start () 
                      if (button5.text == "Do not play in a circular way")                 
                              mp.isLooping = false             
                      else 
                              mp.isLooping = true 
                      }         
          button2.setOnClickListener {             
                      if (mp.isPlaying ()) { 
                            position = mp.getCurrentPosition ()                 
                            mp.pause () 
                    }         
                } 
          button3.setOnClickListener {           
                     if (mp.isPlaying () == false) {                 
                            mp.seekTo (position)                 
                             mp.start () 
                   } 
            }
        button4.setOnClickListener {             
                         position = 0             
                         mp.seekTo (0) 
                      mp.pause ()         
             } 
        button5.setOnClickListener { 
            if (button5.text == "Do not play in a circular way")                 
                        button5.setText ("Play in circular form")             
            else 
                  button5.setText ("Do not play in circular form") 
             }
          }
           override fun onDestroy() {
                    super.onDestroy()
                    mp.release()
             }
        }

OUTPUT:
 



Telephone API
10.b) To create a program that uses the calling feature of android mobile phones.
Design :
 
Activity_main.xml:
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity"
    android:orientation="vertical">

    <Button
        android:id="@+id/placecall"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="200dp"
        android:text="Call Durgesh" />
</LinearLayout>

MainActivity.Kt :
package com.example.practical10a

import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.support.v4.app.ActivityCompat
import android.widget.Button

class MainActivity : AppCompatActivity() {
    val phone_number:String = "7715806795"
    val REQUEST_PHONE_CALL = 1
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val call = findViewById<Button>(R.id.placecall)
        call.setOnClickListener {
            if(ActivityCompat.checkSelfPermission(this,android.Manifest.permission.CALL_PHONE)!= PackageManager.PERMISSION_GRANTED){
                ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.CALL_PHONE),REQUEST_PHONE_CALL)
            }
            else{
                makecall()
            }
        }
    }
    private fun makecall(){
        val intent = Intent(Intent.ACTION_CALL, Uri.fromParts("tel",phone_number,null))
        startActivity(intent)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        if(requestCode==REQUEST_PHONE_CALL){
            makecall()
        }
    }
}
AndroidManifest.xml :
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.example.practical10a">
    <uses-permission android:name="android.permission.CALL_PHONE"></uses-permission>
    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="Telephone API - Sahil"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Practical10A"
        tools:targetApi="31">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
OUTPUT :
 
.

"""
    print(code)


def intent():
    code="""
 Intent
To create a program to implement intent (Implicit and Explicit).

Activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView5"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="37dp"
        android:layout_marginBottom="42dp"
        android:text="My Name is"
        app:layout_constraintBottom_toTopOf="@+id/button2"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.498"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView6" />

    <TextView
        android:id="@+id/textView6"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="44dp"
        android:layout_marginBottom="36dp"
        android:text="Enter your name"
        app:layout_constraintBottom_toTopOf="@+id/textView5"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.498"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/editText" />

    <Button
        android:id="@+id/button2"
        android:layout_width="183dp"
        android:layout_height="39dp"
        android:layout_marginTop="23dp"
        android:layout_marginBottom="430dp"
        android:text="Click here to pop-up"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.442"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView5" />

    <EditText
        android:id="@+id/editText"
        android:layout_width="357dp"
        android:layout_height="87dp"
        android:layout_marginTop="6dp"
        android:layout_marginEnd="36dp"
        android:layout_marginBottom="14dp"
        android:ems="10"
        android:inputType="textPersonName"
        android:text="Intent In Android"
        app:layout_constraintBottom_toTopOf="@+id/textView6"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="1.0"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        tools:text="Enter Name" />


</androidx.constraintlayout.widget.ConstraintLayout>

MainActivity.kt
package com.example.trial5

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val clickme = findViewById<Button>(R.id.button2)
        clickme.setOnClickListener {
            Toast.makeText(this,"Button Clicked", Toast.LENGTH_SHORT).show()
        }

        val display = findViewById<TextView>(R.id.textView5)
        val enteredName  = findViewById<EditText>(R.id.editText)
        enteredName.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {

            }

            override fun afterTextChanged(p0: Editable?) {

            }

            override fun onTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
                display.setText("Your Name in Edit Text is : "+p0)

            }

        })

    }
}

"""
    print(code)

def apbar():
    code="""
Application Bar
a) Design a mobile application to demonstrate working of App Bar

MainActivity.Kt :-
package com.example.practical5
  
 import android.support.v7.app.AppCompatActivity
  import android.os.Bundle
  import android.view.Menu
  import android.view.MenuItem
  import android.widget.Toast
  
 class MainActivity : AppCompatActivity() {
      override fun onCreate(savedInstanceState: Bundle?) {
          super.onCreate(savedInstanceState)
          setContentView(R.layout.activity_main)
  
 
        val myBar = supportActionBar
          myBar!!.title = "My New Action Bar"
          myBar.subtitle = "its new one"
          myBar.setIcon(R.drawable.phone)
          myBar.setDisplayUseLogoEnabled(true)
          myBar.setDisplayShowHomeEnabled(true)
  
     }
  
     override fun onCreateOptionsMenu(menu: Menu?): Boolean {
          menuInflater.inflate(R.menu.menu1,menu)
          return super.onCreateOptionsMenu(menu)
      }
  
     override fun onOptionsItemSelected(item: MenuItem): Boolean {
          when(item.itemId){
              R.id.copy -> Toast.makeText( this, "copy",Toast.LENGTH_SHORT).show()
              R.id.chat -> Toast.makeText( this, "chat",Toast.LENGTH_SHORT).show()
              R.id.football -> Toast.makeText( this, "football",Toast.LENGTH_SHORT).show()
              R.id.location-> Toast.makeText( this, "location",Toast.LENGTH_SHORT).show()
  
         }
          return super.onOptionsItemSelected(item)
      }
  }

AndroidManifest.xml:-
<?xml version="1.0" encoding="utf-8"?>
  <manifest xmlns:android="http://schemas.android.com/apk/res/android"
      xmlns:tools="http://schemas.android.com/tools"
      package="com.example.practical5">
  
     <application
          android:allowBackup="true"
          android:dataExtractionRules="@xml/data_extraction_rules"
          android:fullBackupContent="@xml/backup_rules"
          android:icon="@drawable/football"
          android:label="@string/app_name"
          android:roundIcon="@drawable/football"
          android:supportsRtl="true"
          android:theme="@style/Theme.Practical5"
          tools:targetApi="31">
          <activity
              android:name=".MainActivity"
              android:exported="true">
              <intent-filter>
                  <action android:name="android.intent.action.MAIN" />
  
                 <category android:name="android.intent.category.LAUNCHER" />
              </intent-filter>
          </activity>
      </application>
  
 </manifest>

Menu1.xml :-
<?xml version="1.0" encoding="utf-8"?>
  <menu xmlns:android="http://schemas.android.com/apk/res/android"
      xmlns:app="http://schemas.android.com/apk/res-auto"
      xmlns:tools="http://schemas.android.com/tools">
  
     <item android:id="@+id/football"
          android:title="football"
          android:icon="@drawable/football"
          android:orderInCategory="100"
          app:showAsAction="ifRoom"/>
  
     <item android:id="@+id/chat"
          android:title="chat"
          android:icon="@drawable/chat"
          android:orderInCategory="101"
          app:showAsAction="ifRoom"/>
  
     <item android:id="@+id/location"
          android:title="location"
          android:icon="@drawable/location"
          android:orderInCategory="103"
          app:showAsAction="never"/>
  
     <item android:id="@+id/copy"
          android:title="copy"
          android:icon="@drawable/copy"
          android:orderInCategory="104"
          app:showAsAction="never"/>
  
 </menu>

Strings.xml:-
<resources>
      <string name="app_name">My Action Bar</string>
  </resources>

Login Form
b) Design a mobile application to create a login form

Activity_main.xml:
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <LinearLayout
        android:layout_width="383dp"
        android:layout_height="431dp"
        android:layout_marginStart="8dp"
        android:layout_marginTop="8dp"
        android:layout_marginEnd="8dp"
        android:layout_marginBottom="271dp"
        android:orientation="vertical"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent">

        <TextView
            android:id="@+id/textView1"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="What is your name?"
            android:textSize="24sp" />

        <EditText
            android:id="@+id/edtxtname"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Enter your name..."
            android:inputType="text"
            android:textSize="24sp" />

        <TextView
            android:id="@+id/textView2"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="What is your E-mail ID?"
            android:textSize="24sp" />

        <EditText
            android:id="@+id/edtxtemail"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Enter your E-mail..."
            android:inputType="text"
            android:textSize="24sp" />
        <TextView
            android:id="@+id/show"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text=""
            android:textSize="24sp" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="127dp"
            android:orientation="horizontal">

            <Button
                android:id="@+id/btnsubmit"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="SUBMIT" />
            <Button
                android:id="@+id/btnreset"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="RESET" />
        </LinearLayout>
    </LinearLayout>

</androidx.constraintlayout.widget.ConstraintLayout>

MainActivity.kt File:
package com.example.trial10

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState) setContentView(R.layout.activity_main)
        val name = findViewById<EditText>(R.id.edtxtname)
        val email = findViewById<EditText>(R.id.edtxtemail)
        val submit = findViewById<Button>(R.id.btnsubmit)
        val reset = findViewById<Button>(R.id.btnreset)
        val show = findViewById<TextView>(R.id.show)

        submit.setOnClickListener {
            show.setText("Name: "+name.text.toString()+"\nEmail: "+email.text.toString())
            Toast.makeText(this,"Record Submitted!",Toast.LENGTH_LONG).show()
        }
        reset.setOnClickListener {
            name.text.clear()
            email.text.clear()
            show.setText("")
            Toast.makeText(this,"RecordCleared!",Toast.LENGTH_LONG).show()
        }
    }
}

private infix fun Any.setContentView(activityMain: Int) {

}



Media API
a) To create a program to access music (media) in your mobile phone.

MainActivity.kt:
package com.example.tiral

import android.media.MediaPlayer
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    private lateinit var mp: MediaPlayer
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        mp = MediaPlayer.create(this,R.raw.meramusic)
        var position = 0
        var button = findViewById<Button>(R.id.button)
        var button2 = findViewById<Button>(R.id.button2)
        var button3 = findViewById<Button>(R.id.button3)
        var button4 = findViewById<Button>(R.id.button4)
        var button5 = findViewById<Button>(R.id.button5)

        button.setOnClickListener {
            mp.start()
            mp.isLooping = button5.text != "Do not play in a circular way"
            Toast.makeText(this,"Music is Playing",Toast.LENGTH_LONG).show()
        }

        button2.setOnClickListener {
            if (mp.isPlaying){
                position = mp.currentPosition
                mp.pause()
                Toast.makeText(this,"Music is Paused",Toast.LENGTH_LONG).show()
            }
        }

        button3.setOnClickListener {
            if(!mp.isPlaying){
                mp.seekTo(position)
                mp.start()
            }
        }

        button4.setOnClickListener {
            mp.pause()
            position = 0
            mp.seekTo(0)
        }

        button5.setOnClickListener {
            if (button5.text == "Do not play in a circular way")
                button5.text = "Play in circular form"
            else
                button5.text = "Do not play in circular form"
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        mp.release()
    }
}

Activity_main.xml:
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/black"
    tools:context=".MainActivity">

    <Button
        android:id="@+id/button"
        android:layout_width="109dp"
        android:layout_height="wrap_content"
        android:layout_alignParentStart="true"
        android:layout_marginStart="150dp"
        android:layout_marginTop="65dp"
        android:backgroundTint="#EFC635"
        android:text="Play" />

    <Button
        android:id="@+id/button2"
        android:layout_width="109dp"
        android:layout_height="wrap_content"
        android:layout_alignParentStart="true"
        android:layout_marginStart="150dp"
        android:layout_marginTop="150dp"
        android:backgroundTint="#871353"
        android:text="Pause" />

    <Button
        android:id="@+id/button3"
        android:layout_width="109dp"
        android:layout_height="wrap_content"
        android:layout_alignParentStart="true"
        android:layout_marginStart="150dp"
        android:layout_marginTop="235dp"
        android:backgroundTint="#A6FD05"
        android:text="Continue" />

    <Button
        android:id="@+id/button4"
        android:layout_width="109dp"
        android:layout_height="wrap_content"
        android:layout_alignParentBottom="true"
        android:layout_marginStart="150dp"
        android:layout_marginBottom="280dp"
        android:backgroundTint="#E12222"
        android:text="Stop" />

    <Button
        android:id="@+id/button5"
        android:layout_width="109dp"
        android:layout_height="wrap_content"
        android:layout_alignParentBottom="true"
        android:layout_marginStart="150dp"
        android:layout_marginBottom="200dp"
        android:backgroundTint="#747ED6"
        android:text="Button" />
</RelativeLayout>

Telephone API
b) To create a program that uses the calling feature of android mobile phones.

Activity_main.xml:
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="TYPE YOUR NUMBER"
        android:textAlignment="center"
        android:textSize="36sp"
        android:textStyle="bold"/>

    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/phoneno"
        android:hint="Moblile Number"
        android:inputType="phone"
        tools:ignore="missing"/>

    <Button
        android:id="@+id/btncall"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="CALL"
        tools:ignore="missing"/>

</LinearLayout>

MainActivity.kt:
package com.example.trial2

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {
    private lateinit var btnphonecall: Button
    private lateinit var editphoneNo: EditText
    private val requestCall = 1
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        title = "Time Do"
        editphoneNo = findViewById(R.id.phoneno)
        btnphonecall = findViewById(R.id.btncall)
        btnphonecall.setOnClickListener {
            makeCall()
        }
    }
    private fun makeCall() {
        val callingNo: String = editphoneNo.text.toString()
        if (callingNo.trim { it <= ' ' }.isNotEmpty()) {
            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.CALL_PHONE
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.CALL_PHONE),
                    requestCall
                )
            } else {
                val dial ="tel:$callingNo"
                startActivity(Intent(Intent.ACTION_CALL,Uri.parse(dial)))
            }
        } else {
            Toast.makeText(this, "Enter the Number", Toast.LENGTH_LONG).show()
        }
    }

    @SuppressLint("MissingSuperCall")
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        if (requestCode == requestCall) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                makeCall()
            } else {
                Toast.makeText(this, "Permission denied", Toast.LENGTH_LONG).show()
            }
        }
    }
}


AndroidManifest.xml
<?xml version="1.0" encoding="utf-8"?>
<manifest
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.example.trial2">

    <uses-feature
        android:name="android.hardware.telephony"
        android:required="false"/>

    <uses-permission
        android:name="android.permission.CALL_PHONE"/>

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Trial2"
        tools:targetApi="31">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>



 Intent
To create a program to implement intent (Implicit and Explicit).

Activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView5"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="37dp"
        android:layout_marginBottom="42dp"
        android:text="My Name is"
        app:layout_constraintBottom_toTopOf="@+id/button2"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.498"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView6" />

    <TextView
        android:id="@+id/textView6"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="44dp"
        android:layout_marginBottom="36dp"
        android:text="Enter your name"
        app:layout_constraintBottom_toTopOf="@+id/textView5"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.498"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/editText" />

    <Button
        android:id="@+id/button2"
        android:layout_width="183dp"
        android:layout_height="39dp"
        android:layout_marginTop="23dp"
        android:layout_marginBottom="430dp"
        android:text="Click here to pop-up"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.442"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView5" />

    <EditText
        android:id="@+id/editText"
        android:layout_width="357dp"
        android:layout_height="87dp"
        android:layout_marginTop="6dp"
        android:layout_marginEnd="36dp"
        android:layout_marginBottom="14dp"
        android:ems="10"
        android:inputType="textPersonName"
        android:text="Intent In Android"
        app:layout_constraintBottom_toTopOf="@+id/textView6"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="1.0"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        tools:text="Enter Name" />


</androidx.constraintlayout.widget.ConstraintLayout>

MainActivity.kt
package com.example.trial5

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val clickme = findViewById<Button>(R.id.button2)
        clickme.setOnClickListener {
            Toast.makeText(this,"Button Clicked", Toast.LENGTH_SHORT).show()
        }

        val display = findViewById<TextView>(R.id.textView5)
        val enteredName  = findViewById<EditText>(R.id.editText)
        enteredName.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {

            }

            override fun afterTextChanged(p0: Editable?) {

            }

            override fun onTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
                display.setText("Your Name in Edit Text is : "+p0)

            }

        })

    }
}



Notification 
a) Design an Android mobile application to demonstrate the working of notifications. [Hint: create and display the notification with help of button
MainActivity.kt:
package com.example.myapplication

import android.annotation.SuppressLint
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.graphics.Color
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat

class MainActivity : AppCompatActivity() {

    private val channelId = "sample_channel"
    private val notificationId = 101

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val button = findViewById<Button>(R.id.notifyButton)
        button.setOnClickListener {
            createNotificationChannel()
            sendNotification()
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "Sample Channel"
            val descriptionText = "This is a sample notification channel."
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(channelId, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    @SuppressLint("MissingPermission")
    private fun sendNotification() {
        val builder = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.drawable.ic_launcher_background)
            .setContentTitle("Sample Notification")
            .setContentText("This is a sample notification.")
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)

        with(NotificationManagerCompat.from(this)) {
            notify(notificationId, builder.build())
        }
    }
}


Activity_main.xml:
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">
    <Button
        android:id="@+id/notifyButton"
        android:layout_width="400dp"
        android:layout_height="90dp"
        android:layout_centerInParent="true"
        android:backgroundTint="@color/white"
        android:text="Show Notification"
        android:textSize="35dp"
        android:textColor="#FF0000"/>
</RelativeLayout>

Broadcast Receiver 
b) Design an Android mobile application to show the working of broadcast receiver.
MainActivity.kt:
package com.example.trial4

import android.content.Intent
import android.content.IntentFilter
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

class MainActivity : AppCompatActivity() {
    lateinit var receiver: AirplaneModeChanger
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        receiver = AirplaneModeChanger()
        IntentFilter(Intent.ACTION_AIRPLANE_MODE_CHANGED).also {
            registerReceiver(receiver,it)
        }
    }

    override fun onStop() {
        super.onStop()
        unregisterReceiver(receiver)
    }
}

Activity_main.xml:
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        tools:layout_editor_absolutey="339dp" />

</androidx.constraintlayout.widget.ConstraintLayout>

AirplaneModeChanger.kt
package com.example.trial4

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.widget.Toast


class AirplaneModeChanger : BroadcastReceiver() {
    override fun onReceive(p0: Context?, p1: Intent?) {
        val isAirplaneEnabled = p1?.getBooleanExtra("state",false)?:return
        if (isAirplaneEnabled)
        {
            Toast.makeText(p0,"Airplane Mode Enable", Toast.LENGTH_LONG).show()
        }
        else
        {
            Toast.makeText(p0,"Airplane Mode Disable", Toast.LENGTH_LONG).show()
        }
    }
}


Image and Background
a) Design an Activity with an image and its background colour set.

Activity_main:
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/bg"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/krishna"
        android:textColor="@color/textcolor"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <ImageView
        android:id="@+id/imageView"
        android:layout_width="170dp"
        android:layout_height="320dp"
        app:layout_constraintBottom_toTopOf="@+id/textView"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:srcCompat="@drawable/img1"
        tools:ignore="MissingConstraints" />

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:backgroundTint="@color/buttonbg"
        android:text="@string/click_me"
        android:textColor="@color/textcolor"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView"
        tools:ignore="MissingConstraints" />

</androidx.constraintlayout.widget.ConstraintLayout>

MainActivity:
package com.example.trail7

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}

String:
<resources>
    <string name="app_name">trail7</string>
    <string name="My_Work">pra2.1</string>
    <string name="krishna">Krishna</string>
    <string name="click_me">Click Me</string>
</resources>

Color:
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="bg">#FF000000</color>
    <color name="textcolor">#FFFFFFFF</color>
    <color name="buttonbg">#FF0000</color>
</resources>

On Click of a Button
b) Design an Activity where on Click of a button the image should change.

MainActivity:
package com.example.trial8

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        lateinit var imageView: ImageView

        lateinit var button: Button
        var isImage1 = true



        imageView = findViewById(R.id.imageView)
        button = findViewById(R.id.button)

        button.setOnClickListener {
            // Change the image when the button is clicked
            if (isImage1) {
                imageView.setImageResource(R.drawable.img2)
            } else {
                imageView.setImageResource(R.drawable.img1)
            }

            // Toggle the flag to switch between images
            isImage1 = !isImage1
        }
    }
}






"""
    print(code)



def allnlp():
    code=r"""
def speech_to_text():
def text_to_speech():
def study_of_corpus():
def own_corpora():
def conditionalFrequencyDistribution():
def tagged_corpora():
def frequentNounTags():
def propertiesUsingPythonDict():
def default_Tagger():
def regularExpression_Tagger():
def unigram_Tagger():
def comparingTextWithCorpus():
def wordnet_dictionary():
def lemmas_hyponyms():
def synonym_antonym():
def compare_nouns():
def removingStopWords_NLTK():
def removingStopWords_Gensim():
def removingStopWords_Spacy():
def tokenization_split():
def tokenization_RegEx():
def tokenization_NLTK():
def tokenization_Spacy():
def tokenization_Keras():
def tokenization_Gensim():
def hindi_wordTokenization():
def generate_similarSentences():
def identify_language():
def POS_taggingChunking():
def NamedEntityRecognition():
def NER_treebank():
def grammer_using_NLTK():
def acceptInputString101():
def acceptInputString():
def deductiveChart_CFG():
def stemmers():
def naiveBayes():
def speechTagging_spacy():
def speechTagging_NLTK():
def pennTreebank_statisticalPrasing():
def probabilistic_parser():
def maltParsing():
def multiwordEx():
def normalizedWebDistance():
def wordSenseDisambiguation():
"""
    print(code)
def speech_to_text():
	code=r"""
#pip install SpeechRecognition pydub
import speech_recognition as sr
filename = r"C:\Users\Aditi\Documents\Aditi Files\MScIT-Part2\Semester 4\Natural Language Processing\Practical\archive\harvard.wav"
r = sr.Recognizer()
with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print("Speech to Text output: \n",text)

"""
	print(code)
	
	
def text_to_speech():
	code=r"""
#pip install playsound
#pip install gtts
from playsound import playsound
from gtts import gTTS
myobj=gTTS(text="Hellloooooo Aditi Good morning", lang="en")
myobj.save(r"C:\Users\Aditi\Documents\Aditi Files\MScIT-Part2\Semester 4\Natural Language Processing\Practical\archive\jackhammer.wav")

"""
	print(code)
	
	
def study_of_corpus():
	code=r"""
import nltk
nltk.download('brown')
from nltk.corpus import brown
print ('File ids of brown corpus\n',brown.fileids())
ca01 = brown.words('ca01')
print('\nca01 has following words:\n',ca01)
print('\nca01 has',len(ca01),'words')
print('\n\nCategories or file in brown corpus:\n')
print(brown.categories())
print('\n\nStatistics for each text:\n')
print('AvgWordLen\tAvgSentenceLen\tno.ofTimesEachWordAppearsOnAvg\t\tFileName')
for fileid in brown.fileids():
    num_chars = len(brown.raw(fileid))
    num_words = len(brown.words(fileid))
    num_sents = len(brown.sents(fileid))
    num_vocab = len(set([w.lower() for w in brown.words(fileid)]))
    print (int(num_chars/num_words),'\t\t\t', int(num_words/num_sents),'\t\t\t',int(num_words/num_vocab),'\t\t\t', fileid)

"""
	print(code)
	
	
def own_corpora():
	code=r"""
import nltk
from nltk.corpus import PlaintextCorpusReader
corpus_root = r"C:\Users\Aditi\Documents\Aditi Files\MScIT-Part2\Semester 4\Natural Language Processing\Practical"
filelist = PlaintextCorpusReader(corpus_root, '.*', encoding='latin-1')
print('\n File list: \n')
print(filelist.fileids())
print(filelist.root)
print('\n\nStatistics for each text:\n')
print('AvgWordLen\tAvgSentenceLen\tno.ofTimesEachWordAppearsOnAvg\tFileName')

for fileid in filelist.fileids():
    num_chars = len(filelist.raw(fileid))
    num_words = len(filelist.words(fileid))
    num_sents = len(filelist.sents(fileid))
    num_vocab = len(set([w.lower() for w in filelist.words(fileid)]))
    print(int(num_chars/num_words), '\t\t\t', int(num_words/num_sents), '\t\t\t', int(num_words/num_vocab), '\t\t', fileid)

"""
	print(code)
	
	
def conditionalFrequencyDistribution():
	code=r"""
import nltk
nltk.download('inaugural')
nltk.download('udhr')
from nltk.corpus import brown
text = ['The', 'Fulton', 'County', 'Grand', 'Jury', 'said', ...]
pairs = [('news', 'The'), ('news', 'Fulton'), ('news', 'County'), ...]
fd = nltk.ConditionalFreqDist(
    (genre, word)
    for genre in brown.categories()
    for word in brown.words(categories=genre))
genre_word = [(genre, word)
              for genre in ['news', 'romance']
              for word in brown.words(categories=genre)]
print(len(genre_word))
print(genre_word[:4])
print(genre_word[-4:])
cfd = nltk.ConditionalFreqDist(genre_word)
print(cfd)
print(cfd.conditions())
print(cfd['news'])
print(cfd['romance'])
print(list(cfd['romance']))
from nltk.corpus import inaugural
cfd = nltk.ConditionalFreqDist(
    (target, fileid[:4])
    for fileid in inaugural.fileids()
    for w in inaugural.words(fileid)
    for target in ['america', 'citizen']
    if w.lower().startswith(target))
from nltk.corpus import udhr
languages = ['Chickasaw', 'English', 'German_Deutsch', 'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
cfd = nltk.ConditionalFreqDist(
    (lang, len(word))
    for lang in languages
    for word in udhr.words(lang + '-Latin1'))
cfd.tabulate(conditions=['English', 'German_Deutsch'], samples=range(10), cumulative=True)

"""
	print(code)
	

def tagged_corpora():
	code=r"""
import nltk
from nltk import tokenize
nltk.download('punkt')
nltk.download('words')
para = "Hey! The quick brown fox jumps over the lazy dog."
sents = tokenize.sent_tokenize(para)
print("\nsentence tokenization\n===================\n",sents)
print("\nword tokenization\n===================\n")
for index in range(len(sents)):
    words = tokenize.word_tokenize(sents[index])
    print(words)

"""
	print(code)
	
	
def frequentNounTags():
	code=r"""
import nltk
from collections import defaultdict
text = nltk.word_tokenize("The universe is all of space and time and their contents. It comprises all of existence, any fundamental interaction, physical process and physical constant, and therefore all forms of energy and matter, and the structures they form, from sub-atomic particles to entire galactic filaments.")
tagged = nltk.pos_tag(text)
print(tagged)
addNounWords = []
count=0
for words in tagged:
    val = tagged[count][1]
    if(val == 'NN' or val == 'NNS' or val == 'NNPS' or val == 'NNP'):
        addNounWords.append(tagged[count][0])
    count+=1
print (addNounWords)
temp = defaultdict(int)
for sub in addNounWords:
    for wrd in sub.split():
        temp[wrd] += 1
res = max(temp, key=temp.get)
print("\nWord with maximum frequency : " + str(res))

"""
	print(code)
	
def propertiesUsingPythonDict():
	code=r"""
thisdict = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}
print(thisdict)
print(thisdict["brand"])
print(len(thisdict))
print(type(thisdict))

"""
	print(code)
	
def default_Tagger():
	code=r"""
import nltk
from nltk.tag import DefaultTagger
exptagger = DefaultTagger('NN')
from nltk.corpus import treebank
testsentences = treebank.tagged_sents()[3000:]
print("Accuracy: ", exptagger.accuracy (testsentences))
print(exptagger.tag_sents([['Hi', ','], ['How', 'are', 'you', '?']]))

"""
	print(code)
	
def regularExpression_Tagger():
	code=r"""
from nltk.corpus import brown
from nltk.tag import RegexpTagger
test_sent = brown.sents(categories='news')[0]
regexp_tagger = RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
     ])
print("Regular Expression tagger: ", regexp_tagger)
print(regexp_tagger.tag(test_sent))

"""
	print(code)
	
def unigram_Tagger():
	code=r"""
from nltk.tag import UnigramTagger
from nltk.corpus import treebank

train_sents = treebank.tagged_sents()[:10]
tagger = UnigramTagger(train_sents)

print(treebank.sents()[0])
print('\n',tagger.tag(treebank.sents()[0]))

tagger.tag(treebank.sents()[0])
tagger = UnigramTagger(model ={'Pierre': 'NN'})
print('\n',tagger.tag(treebank.sents()[0]))

"""
	print(code)
	
def comparingTextWithCorpus():
	code=r"""
P2-words.txt	
check       domain
big             rocks
name       cheap
being       human
current     rates
ought        to
go          down
apple        domains
honesty       hour
follow        back
social         media
30      seconds
earth       this
is       insane
it      time
what     is
my       name
let        us
go
	
from __future__ import with_statement 
import re 
words = [] 
testword = [] 
ans = [] 
print("MENU")
print("-----------")
print(" 1 . Hash tag segmentation ")
print(" 2 . URL segmentation ")
print("Enter the input choice for performing word segmentation: ")
choice = int(input())
if choice == 1:
    text = "#whatismyname"
    print("input with HashTag",text)
    pattern=re.compile("[^\w']")
    a = pattern.sub('', text)
elif choice == 2:
    text = "www.whatismyname.com"
    print("input with URL",text)
    a=re.split('\s|(?<!\d)[,.](?!\d)', text)
    splitwords = ["www","com","in"]
    a ="".join([each for each in a if each not in splitwords])
else:
    print("Wrong choice...try again")
print(a)
for each in a:
    testword.append(each) 
test_lenth = len(testword)
with open(r"C:\Users\Aditi\Documents\Python Scripts\MSc_Sem4\NLP Scripts\NLP Datasets\P2-words.txt", 'r') as f:
    lines = f.readlines()
    words =[(e.strip()) for e in lines]
def Seg(a,lenth):
    ans =[]
    for k in range(0,lenth+1):
        if a[0:k] in words:
            print(a[0:k],"-appears in the corpus")
            ans.append(a[0:k])
            break
    if ans != []:
        g = max(ans,key=len)
        return g
test_tot_itr = 0 
answer = [] 
Score = 0 
N = 37 
M = 0
C = 0
while test_tot_itr < test_lenth:
    ans_words = Seg(a,test_lenth)
    if ans_words != 0:
        test_itr = len(ans_words)
        answer.append(ans_words)
        a = a[test_itr:test_lenth]
        test_tot_itr += test_itr
Aft_Seg = " ".join([each for each in answer])

print("Output: ")
print("---------")
print("After segmentation: ", Aft_Seg) 
C = len(answer)
score = C * N / N 
print("Score: ",score)

"""
	print(code)
	
def wordnet_dictionary():
	code=r"""
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
print(wordnet.synsets("sunrise"))
print("My word is Sunrise:- \n", "Definition:", wordnet.synset("sunrise.n.01").definition())
print("Examples:", wordnet.synset("sunrise.n.01").examples())
anto = wordnet.lemma('sunrise.n.01.sunrise')
print("\nAntonym of word Sell (Noun):", anto.antonyms())

"""
	print(code)
	
def lemmas_hyponyms():
	code=r"""
import nltk
from nltk.corpus import wordnet
print(wordnet.synsets("computer"))
print(wordnet.synset("computer.n.01").lemma_names())
for e in wordnet.synsets("computer"):
    print(f'{e} --> {e.lemma_names()}')
print(wordnet.synset('computer.n.01').lemmas())
print(wordnet.lemma('computer.n.01.computing_device').synset())
print(wordnet.lemma('computer.n.01.computing_device').name())
print("\n\n Hyponyms of computer:\n")
syn = wordnet.synset('computer.n.01')
print(syn.hyponyms)
print([lemma.name() for synset in syn.hyponyms() for lemma in synset.lemmas()])
print("\n\n Hyponyms of vehicle:\n")
vehicle = wordnet.synset('vehicle.n.01')
print(vehicle.hyponyms)
print([lemma.name() for synset in vehicle.hyponyms() for lemma in synset.lemmas()])
print("\n\n Hyponyms of car:\n")
car = wordnet.synset('car.n.01')
print(car.hyponyms)
print([lemma.name() for synset in car.hyponyms() for lemma in synset.lemmas()])
print(car.lowest_common_hypernyms(vehicle))
print("\n\nVehi1")
vehi1=wordnet.synset('vehicle.n.01')
print(vehi1.hypernyms)
print([lemma.name() for synset in vehi1.hypernyms() for lemma in synset.lemmas()])

"""
	print(code)
	
def synonym_antonym():
	code=r"""
from nltk.corpus import wordnet
print( wordnet.synsets("active"))
print("\n", wordnet.lemma('active.a.01.active').antonyms())

"""
	print(code)
	
def compare_nouns():
	code=r"""
import nltk
from nltk.corpus import wordnet
syn1 = wordnet.synsets('car')
syn2 = wordnet.synsets('jeep')
for s1 in syn1:
    for s2 in syn2:
        print("Path similarity of: ")
        print(s1, '(', s1.pos(), ')', '[', s1.definition(), ']')
        print(s2, '(', s2.pos(), ')', '[', s2.definition(), ']')
        print(" is", s1.path_similarity(s2))
        print()

"""
	print(code)
	
def removingStopWords_NLTK():
	code=r"""
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
text = "the quick brown fox jumps over the lazy dog but not a cat"
text_tokens = word_tokenize(text)
tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
print(tokens_without_sw)
all_stopwords = stopwords.words('english')
all_stopwords.append('play')
text_tokens = word_tokenize(text)
tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
print(tokens_without_sw)
all_stopwords.remove('not')
text_tokens = word_tokenize(text)
tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
print(tokens_without_sw)

"""
	print(code)
	
def removingStopWords_Gensim():
	code=r"""
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.utils import tokenize
text = "the quick brown fox jumps over the lazy dog but not a playing cat."
# Removing stopwords using Gensim's built-in function
filtered_sentence = remove_stopwords(text)
print("Filtered sentence using Gensim's remove_stopwords function:")
print(filtered_sentence)
# Accessing default stopwords list in Gensim
all_stopwords_gensim = gensim.parsing.preprocessing.STOPWORDS
# Adding custom stopwords to the default Gensim stopwords list
custom_stopwords = {'jumps', 'playing'}
all_stopwords_gensim = all_stopwords_gensim.union(custom_stopwords)
# Tokenizing the text using Gensim
text_tokens = list(tokenize(text))
tokens_without_sw = [word for word in text_tokens if word.lower() not in all_stopwords_gensim]
print("\nTokenized text without custom stopwords:")
print(tokens_without_sw)
# Removing a specific word ('not') from the default Gensim stopwords list
all_stopwords_gensim = gensim.parsing.preprocessing.STOPWORDS
custom_stopwords = {'not'}
all_stopwords_gensim = set(word for word in all_stopwords_gensim if word.lower() not in custom_stopwords)
# Tokenizing the text again using Gensim
text_tokens = list(tokenize(text))
tokens_without_sw = [word for word in text_tokens if word.lower() not in all_stopwords_gensim]
print("\nTokenized text without removing 'not' from default Gensim stopwords list:")
print(tokens_without_sw)

"""
	print(code)
	
def removingStopWords_Spacy():
	code=r"""
#pip install spacy
#python -m spacy download en_core_web_sm
#python -m spacy download en
import spacy
import nltk
from nltk.tokenize import word_tokenize
sp = spacy.load('en_core_web_sm')
#add the word play to the NLTK stop word collection
all_stopwords = sp.Defaults.stop_words
all_stopwords.add("not")
text = "the quick brown fox jumps over the lazy dog but not a playing cat."
print("Original text: ", text, "\n")
text_tokens = word_tokenize(text)
tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
print("Without stopwords(adding not as stopword): ",tokens_without_sw)
#remove 'not' from stop word collection
all_stopwords.remove('not')
tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
print("Without stopwords (removing not as stopword): ",tokens_without_sw)

"""
	print(code)
	
def tokenization_split():
	code=r"""
string = "This is a sentence. Here is another one."
tokens = string.split('.')
print(tokens)

"""
	print(code)
	
def tokenization_RegEx():
	code=r"""
import nltk
from nltk.tokenize import RegexpTokenizer
tk = RegexpTokenizer('\w+')
str1 = "The quick brown fox jumps over the lazy dog."
tokens = tk.tokenize(str1)
print(tokens)

"""
	print(code)
	
def tokenization_NLTK():
	code=r"""
import nltk
from nltk.tokenize import word_tokenize
str = "The quick brown fox jumps over the lazy dog."
print("Tokenized string: ",word_tokenize(str))

"""
	print(code)
	
def tokenization_Spacy():
	code=r"""
import spacy
nlp = spacy.blank("en")
str = "The quick brown fox jumps over the lazy dog."
doc = nlp(str)
words = [word.text for word in doc]
print("Tokenized string using spacy: ",words)

"""
	print(code)
	
def tokenization_Keras():
	code=r"""
#pip install keras
#pip install tensorflow
import keras
from tensorflow.keras.preprocessing.text import text_to_word_sequence
str = "I love to study Natural Language Processing in Python"
tokens = text_to_word_sequence(str)
print("Tokenized string using Keras: ",tokens)

"""
	print(code)
	
def tokenization_Gensim():
	code=r"""
#pip install gensim
from gensim.utils import tokenize
text = "The quick brown fox jumps over the lazy dog."
tokens = list(tokenize(text))
print("Tokenized using Gensim: ",tokens)

"""
	print(code)
	
def hindi_wordTokenization():
	code=r"""
#pip install indic-nlp-library
from indicnlp.tokenize import indic_tokenize

hindi_text = "मुझे संस्कृत पसंद है |"
tokens = indic_tokenize.trivial_tokenize(hindi_text)
print(tokens)

"""
	print(code)
	
def generate_similarSentences():
	code=r"""
synonyms = {
    "खुश": ["प्रसन्न", "आनंदित", "खुशी"],
    "बहुत": ["अधिक", "बहुत ज्यादा", "काफी"] }
 def generate_similar_sentences(input_sentence, num_sentences=5):
    similar_sentences = []
     for word, word_synonyms in synonyms.items():
        for synonym in word_synonyms:
            modified_sentence = input_sentence.replace(word, synonym)
            similar_sentences.append(modified_sentence)
    return similar_sentences[:num_sentences]
 input_sentence = "मैं आज बहुत खुश हूँ।"
similar_sentences = generate_similar_sentences(input_sentence)
print("Original sentence:", input_sentence)
print("Similar sentences:")
for sentence in similar_sentences:
    print("-", sentence)

"""
	print(code)
	
def identify_language():
	code=r"""
from langdetect import detect_langs
text = "मी विद्यार्थी आहे"
languages = detect_langs(text)
for language in languages:
    print("Identified language with probability score: ",language.lang, language.prob)

"""
	print(code)
	
def POS_taggingChunking():
	code=r"""
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import tokenize
from nltk import tag
from nltk import chunk
para = "Natural language processing (NLP) is a machine learning technology that gives computers the ability to interpret, manipulate, and comprehend human language."
sents = tokenize.sent_tokenize(para)
print("\nsentence tokenization\n===================\n",sents)
# word tokenization
print("\nword tokenization\n===================\n")
for index in range(len(sents)):
    words = tokenize.word_tokenize(sents[index])
    print(words)
# POS Tagging
tagged_words = []
for index in range(len(sents)):
    tagged_words.append(tag.pos_tag(words))
print("\nPOS Tagging\n===========\n",tagged_words)
# chunking
tree = []
for index in range(len(sents)):
    tree.append(chunk.ne_chunk(tagged_words[index]))
print("\nchunking\n========\n")
print("Tree: ",tree)

"""
	print(code)
	
def NamedEntityRecognition():
	code=r"""
#pip install -U spacy
#python -m spacy download en_core_web_sm
import spacy
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")
# Process whole documents
text = ("Natural language processing (NLP) is an interdisciplinary subfield of computer science and information retrieval. It is primarily concerned with giving computers the ability to support and manipulate human language. It involves processing natural language datasets, such as text corpora or speech corpora, using either rule-based or probabilistic machine learning approaches.")
print("Original text: ", text, "\n")
doc = nlp(text)
# Analyse syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

"""
	print(code)
	
def NER_treebank():
	code=r"""
import nltk
nltk.download('treebank')
from nltk.corpus import treebank_chunk
treebank_chunk.tagged_sents()[0]
treebank_chunk.chunked_sents()[0]
treebank_chunk.chunked_sents()[0].draw()

"""
	print(code)
	
def grammer_using_NLTK():
	code=r'''
import nltk
from nltk import tokenize
grammar1 = nltk.CFG.fromstring("""
S -> VP
VP -> VP NP
NP -> Det NP
Det -> 'that'
NP -> singular Noun
NP -> 'flight'
VP -> 'Book'
""")
sentence = "Book that flight"
for index in range(len(sentence)):
    all_tokens = tokenize.word_tokenize(sentence)
print(all_tokens)
parser = nltk.ChartParser(grammar1)
for tree in parser.parse(all_tokens):
    print(tree)
    tree.draw()'''
	print(code)
	
def acceptInputString101():
	code=r"""
def FA(s):
    if len(s)<3:
        return "Rejected"
    if s[0]=='1':
        if s[1]=='0':
            if s[2]=='1':
                for i in range(3,len(s)):
                    if s[i]!='1':
                        return "Rejected"
                return "Accepted" # if all 4 nested if true
            return "Rejected" # else of 3rd if
        return "Rejected" # else of 2nd if
    return "Rejected" # else of 1st if
inputs=['1','10101','101','10111','01010','100','','10111101','1011111']
for i in inputs:
    print(FA(i))

"""
	print(code)
	
def acceptInputString():
	code=r"""
def FA(s):
    size=0
    for i in s:
        if i=='a' or i=='b':
            size+=1
        else:
            return "Rejected"
    if size>=3:
        if s[size-3]=='b':
            if s[size-2]=='b':
                if s[size-1]=='a':
                    return "Accepted" # if all 4 if true
                return "Rejected" # else of 4th if
            return "Rejected" # else of 3rd if
        return "Rejected" # else of 2nd if
    return "Rejected" # else of 1st if
inputs=['bba', 'ababbba', 'abba','abb', 'baba','bbb','']
for i in inputs:
    print(FA(i))
#(a+b)*bba

"""
	print(code)
	
def deductiveChart_CFG():
	code=r'''
import nltk
from nltk import tokenize
grammar1 = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'a' | 'my'
N -> 'bird' | 'balcony'
V -> 'saw'
P -> 'in'
""")
sentence = "I saw a bird in my balcony"
for index in range(len(sentence)):
    all_tokens = tokenize.word_tokenize(sentence)
print(all_tokens)
# all_tokens = ['I', 'saw', 'a', 'bird', 'in', 'my', 'balcony']
parser = nltk.ChartParser(grammar1)
for tree in parser.parse(all_tokens):
    print(tree)
    tree.draw()

'''
	print(code)
	
def stemmers():
	code=r"""
# PorterStemmer
import nltk
from nltk.stem import PorterStemmer
word_stemmer = PorterStemmer()
print(word_stemmer.stem('I am writing a letter'))

#LancasterStemmer
import nltk
from nltk.stem import LancasterStemmer
Lanc_stemmer = LancasterStemmer()
print(Lanc_stemmer.stem('I am writing a letter'))

#RegexpStemmer
import nltk
from nltk.stem import RegexpStemmer
Reg_stemmer = RegexpStemmer('ing$|s$|e$|able$', min=4)
print(Reg_stemmer.stem('I am writing a letter'))

#SnowballStemmer
import nltk
from nltk.stem import SnowballStemmer
english_stemmer = SnowballStemmer('english')
print(english_stemmer.stem ('I am writing a letter'))

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
print("word :\tlemma")
print("rocks :", lemmatizer.lemmatize("rocks"))
print("corpora :", lemmatizer.lemmatize("corpora"))
# a denotes adjective in "pos"
print("better :", lemmatizer.lemmatize("better", pos ="a"))

"""
	print(code)
	
def naiveBayes():
	code=r"""
#pip install pandas
#pip install sklearn
import pandas as pd
import numpy as np
import re
import nltk
nltk.download('stopwords')

sms_data = pd.read_csv(r"C:\Users\Aditi\Documents\Python Scripts\MSc_Sem4\NLP Scripts\NLP Datasets\spam.csv", encoding='latin-1')
sms_data.rename(columns={'v1': 'Category', 'v2': 'Message'}, inplace=True)

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

stemming = PorterStemmer()
corpus = []
for i in range(len(sms_data)):
    s1 = re.sub('[^a-zA-Z]', ' ', sms_data['Message'][i])
    s1 = s1.lower()
    s1 = s1.split()
    s1 = [stemming.stem(word) for word in s1 if word not in set(stopwords.words('english'))]
    s1 = ' '.join(s1)
    corpus.append(s1)

from sklearn.feature_extraction.text import CountVectorizer
countvectorizer = CountVectorizer()
x = countvectorizer.fit_transform(corpus).toarray()
print(x)
y = sms_data['Category'].values
print(y)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=2)
from sklearn.naive_bayes import MultinomialNB
multinomialnb = MultinomialNB()
multinomialnb.fit(x_train, y_train)
y_pred = multinomialnb.predict(x_test)
print(y_pred)
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print(classification_report(y_test, y_pred))
print("Accuracy_score: ", accuracy_score(y_test, y_pred))

"""
	print(code)
	
def speechTagging_spacy():
	code=r"""
import spacy
spacy.cli.download("en_core_web_sm")
sp = spacy.load('en_core_web_sm')
sen = sp(u"the quick brown fox jumps over the lazy dog but not a playing cat.")
print(sen.text)
print(sen[7].pos_)
print(sen[7].tag_)
print(spacy.explain(sen[7].tag_))
for word in sen:
    print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
sen = sp(u'Can you google it?')
word = sen[2]
print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
sen = sp(u'Can you search it on google?')
word = sen[5]
print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
#Finding the Number of POS Tags
sen = sp(u"the quick brown fox jumps over the lazy dog but not a playing cat.")
num_pos = sen.count_by(spacy.attrs.POS)
num_pos
for k,v in sorted(num_pos.items()):
      print(f'{k}. {sen.vocab[k].text:{8}}: {v}')
#Visualizing Parts of Speech Tags
from spacy import displacy
sen = sp(u"the quick brown fox jumps over the lazy dog but not a playing cat.")
displacy.serve(sen, style='dep', options={'distance': 120})
#Open browser and type:
#http://127.0.0.1:5000/


"""
	print(code)
	
def speechTagging_NLTK():
	code=r"""
import nltk
nltk.download('state_union')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
#create our training and testing data:
train_text = state_union.raw(r"C:\Users\Aditi\Documents\Python Scripts\MSc_Sem4\NLP Scripts\NLP Datasets\2005-GWBush.txt")
sample_text = state_union.raw(r"C:\Users\Aditi\Documents\Python Scripts\MSc_Sem4\NLP Scripts\NLP Datasets\2006-GWBush.txt")
#train the Punkt tokenizer like:
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
# tokenize:
tokenized = custom_sent_tokenizer.tokenize(sample_text)
def process_content():
    try:
        for i in tokenized[:2]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged,"\n")
    except Exception as e:
        print(str(e))

process_content()

"""
	print(code)
	
def pennTreebank_statisticalPrasing():
	code=r"""
#probabilitistic parser
#Usage of Give and Gave in the Penn Treebank sample
import nltk
import nltk.parse.viterbi
import nltk.parse.pchart
nltk.download('treebank')
def give(t):
    return t.label() == 'VP' and len(t) > 2 and t[1].label() == 'NP'\
           and (t[2].label() == 'PP-DTV' or t[2].label() == 'NP')\
           and ('give' in t[0].leaves() or 'gave' in t[0].leaves())

def sent(t):
    return ' '.join(token for token in t.leaves() if token[0] not in '*-0')
def print_node(t, width):
    output = "%s %s: %s / %s: %s" %\
             (sent(t[0]), t[1].label(), sent(t[1]), t[2].label(), sent(t[2]))
    if len(output) > width:
        output = output[:width] + "..."
    print (output)
for tree in nltk.corpus.treebank.parsed_sents():
    for t in tree.subtrees(give):
        print_node(t, 72)

"""
	print(code)
	
def probabilistic_parser():
	code=r"""
import nltk
from nltk import PCFG
grammar = PCFG.fromstring('''
NP -> NNS [0.5] | JJ NNS [0.3] | NP CC NP [0.2]
NNS -> "men" [0.1] | "women" [0.2] | "children" [0.3] | NNS CC NNS [0.4]
JJ -> "old" [0.4] | "young" [0.6]
CC -> "and" [0.9] | "or" [0.1]
''')
print(grammar)
viterbi_parser = nltk.ViterbiParser(grammar)
token = "old men and women".split()
obj = viterbi_parser.parse(token)
print("Output: ")
for x in obj:
    print(x)

"""
	print(code)
	
def maltParsing():
	code=r"""
Step-1: Install java jdk file from “https://www.oracle.com/in/java/technologies/downloads/#jdk22-windows” and set Environment variable as “JAVA_HOME”.
Step-2: Check whether Java is properly install or not using “java -version” command in cmd
Step-3: Install “maltparser-1.7.2” from https://www.maltparser.org/download.html and “engmalt.linear-1.7.mco” from https://maltparser.org/mco/english_parser/engmalt.html 
Step-4: Unzipped above files and paste those files in python folder
Step-5: Set Environment variable:
“MALT_PARSER” for maltparser-1.7.2
“MALT_MODEL” for engmalt.linear-1.7.mco
Code:
import os
from nltk.parse.malt import MaltParser

maltparser_home = os.getenv('MALT_PARSER')
mp = MaltParser(maltparser_home, 'engmalt.linear-1.7.mco')
sentence = 'Birdwatching is a favorite pastime of mine, especially from my window.'.split()
parsed_sentence = mp.parse_one(sentence).tree()

print(parsed_sentence)
parsed_sentence.draw()

"""
	print(code)
	
def multiwordEx():
	code=r"""
# Multiword Expressions in NLP
from nltk.tokenize import MWETokenizer
from nltk import sent_tokenize, word_tokenize
s = '''Good cake cost Rs.1500\kg in Mumbai. Please buy me one of them.\n\nThanks.'''
mwe = MWETokenizer([('New', 'York'), ('Hong', 'Kong')], separator='_')
for sent in sent_tokenize(s):
    print(mwe.tokenize(word_tokenize(sent)))

"""
	print(code)
	
def normalizedWebDistance():
	code='''
import numpy as np
import re
import textdistance # pip install textdistance
from sklearn.cluster import AgglomerativeClustering

texts = ['Reliance supermarket', 'Reliance hypermarket', 'Reliance', 'Reliance', 'Reliance downtown', 'Relianc market', 'Mumbai', 'Mumbai Hyper', 'Mumbai dxb', 'mumbai airport',
'k.m trading', 'KM Trading', 'KM trade', 'K.M. Trading', 'KM.Trading']
def normalize(text):
    """ Keep only lower-cased text and numbers"""
    return re.sub('[^a-z0-9]+', ' ', text.lower())

def group_texts(texts, threshold=0.4):
    """ Replace each text with the representative of its cluster"""
    normalized_texts = np.array([normalize(text) for text in texts])
    distances = 1 - np.array([[textdistance.jaro_winkler(one, another) for one in normalized_texts] for another in normalized_texts])
    clustering = AgglomerativeClustering(
        linkage="complete",
        distance_threshold=threshold,
        n_clusters=None
    ).fit(distances)
    centers = dict()
    for cluster_id in set(clustering.labels_):
        index = clustering.labels_ == cluster_id
        centrality = distances[:, index][index].sum(axis=1)
        centers[cluster_id] = normalized_texts[index][centrality.argmin()]
    return [centers[i] for i in clustering.labels_]

print(group_texts(texts))

"""
	print(code)
	
def wordSenseDisambiguation():
	code=r"""
#Word Sense Disambiguation
from nltk.corpus import wordnet as wn
def get_first_sense(word, pos=None):
    if pos:
        synsets = wn.synsets(word,pos)
    else:
        synsets = wn.synsets(word)
    return synsets[0]
best_synset = get_first_sense('bank')
print ('%s: %s' % (best_synset.name, best_synset.definition))
best_synset = get_first_sense('set','n')
print ('%s: %s' % (best_synset.name, best_synset.definition))
best_synset = get_first_sense('set','v')
print ('%s: %s' % (best_synset.name, best_synset.definition))'''
	print(code)

def alldl():
	code=r"""
def matrix_multiplication():
def SolvingXORproblemusingdeepfeedforwardnetwork():
def Implementingdeepneuralnetworkforperformingbinaryclassificationtask():
def Usingdeepfeedforwardnetworkwithtwohiddenlayersforperformingmulticlassclassificationandpredictingtheclass():
def Usingdeepfeedforwardnetworkwithtwohiddenlayersforperformingmulticlassclassificationandpredictingtheprobabilityofclass():
def Usingdeepfeedforwardnetworkwithtwohiddenlayersforperforminglinearregressionandpredictingvalues():
def EvaluatingfeedforwarddeepnetworkforregressionusingKFoldcrossvalidation():
def EvaluatingfeedforwarddeepnetworkformulticlassClassificationusingKFoldcrossvalidation():
def Implementingregularizationtoavoidoverfittinginbinaryclassification():
def Implement12regularizationwithalpha():
def Replace12regularizationwithl2regularization():
def Demonstraterecurrentneuralnetworkthatlearnstoperformsequenceanalysisforstockprice():
def Performingencodinganddecodingofimagesusingdeepautoencoder():
def Implementationofconvolutionalneuralnetworktopredictnumbersfromnumberimages():
def Denoisingofimagesusingautoencoder():
"""
	print(code)
	
#ALL CODES DL


def matrix_multiplication():
    code=r"""import tensorflow as tf
print ("Matrix Multiplication")
x = tf.constant([1,2,3,4,5,6], shape=[3,2])
print(x)
y = tf.constant([7,8,9,10,11,12], shape=[2,3])
print(y)
z = tf.matmul(x,y)
print(z)
matrix_A = tf.random.uniform([2,2], minval=1, maxval=10, dtype=tf.float32, name="matrixA")
print("Matrix A :\n{}\n".format(matrix_A))
eigen_values_A,eigen_vectors_A = tf.linalg.eigh(matrix_A)
print("Eigen Value:\n{}\n\n".format(eigen_values_A))
print("Eigen Vector:\n{}\n\n".format(eigen_vectors_A)))
    """
    print(code)

def SolvingXORproblemusingdeepfeedforwardnetwork():
    code=r"""
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

#creating nearual networks
model = Sequential()
model.add(Dense(units=2, activation='relu', input_dim=2))
model.add(Dense(units=1, activation='sigmoid'))

#compiling the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#preparing the data
X = np.array([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
y = np.array([0.,1.,1.,0.])

#training the data
model.fit(X, y, epochs=5)

#making the [redictions
predictions = model.predict(X)
print(predictions)
    """
    print(code)

def Implementingdeepneuralnetworkforperformingbinaryclassificationtask():
    code=r"""
# diabetes_classifier.py

from keras.models import Sequential
from keras.layers import Dense, Input
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.callbacks import LambdaCallback

# Define column names
names = ["No. of pregnancies", "Glucose level", "Blood Pressure", "Skin thickness", "Insulin", "BMI", "Diabetes pedigree", "Age", "Class"]

# Load dataset
df = pd.read_csv("C:/Users/karan/Desktop/M.Sc.IT/KARAN/sem 4 pracs/DL/diabetes.csv", names=names)

# Ensure all data is numeric
df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

# Split features and target
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Split the dataset into training and testing sets
xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.25, random_state=1)

# Define the model
binaryc = Sequential()
binaryc.add(Input(shape=(8,)))
binaryc.add(Dense(units=10, activation='relu'))
binaryc.add(Dense(units=8, activation='relu'))
binaryc.add(Dense(units=1, activation='sigmoid'))

# Compile the model
binaryc.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Custom callback to print each epoch
print_epoch_callback = LambdaCallback(
on_epoch_end=lambda epoch, logs: print(f'Epoch {epoch + 1}/{200} - loss: {logs["loss"]:.4f} - accuracy: {logs["accuracy"]:.4f}')
)

# Train the model
binaryc.fit(xtrain, ytrain, epochs=10, batch_size=20, callbacks=[print_epoch_callback])

# Make predictions
predictions = binaryc.predict(xtest)
class_labels = [1 if i > 0.5 else 0 for i in predictions]

# Print accuracy score
print('Accuracy Score:', accuracy_score(ytest, class_labels))
    """
    print(code)


def Usingdeepfeedforwardnetworkwithtwohiddenlayersforperformingmulticlassclassificationandpredictingtheclass():
    code=r""""
#4a(Aim: Using deep feed forward network with two hidden layers for
#performing classification and predicting the class)

from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler

X,Y=make_blobs(n_samples=100,centers=2,n_features=2,random_state=1)
scalar=MinMaxScaler()
scalar.fit(X)
X=scalar.transform(X)

model=Sequential()
model.add(Dense(4,input_dim=2,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam')
model.fit(X,Y,epochs=500)


Xnew,Yreal=make_blobs(n_samples=3,centers=2,n_features=2,random_state=1)
Xnew=scalar.transform(Xnew)
Ynew=model.predict_step(Xnew)
for i in range(len(Xnew)):
    print("X=%s,Predicted=%s,Desired=%s"%(Xnew[i],Ynew[i],Yreal[i]))
    """
    print(code)


def Usingdeepfeedforwardnetworkwithtwohiddenlayersforperformingmulticlassclassificationandpredictingtheprobabilityofclass():
    code=r""""
#4b(b) Using a deep feed forward network with two hidden layers for performing classification and predicting the probability of class.)
from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
X,Y=make_blobs(n_samples=100,centers=2,n_features=2,random_state=1)
scalar=MinMaxScaler()
scalar.fit(X)
X=scalar.transform(X)
model=Sequential()
model.add(Dense(4,input_dim=2,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam')
model.fit(X,Y,epochs=500)
Xnew,Yreal=make_blobs(n_samples=3,centers=2,n_features=2,random_state=1)
Xnew=scalar.transform(Xnew)
Yclass=model.predict_step(Xnew)
Ynew=model.predict(Xnew)
for i in range(len(Xnew)):
 print("X=%s,Predicted_probability=%s,Predicted_class=%s"%(Xnew[i],Ynew[i],Yclass[i]))
"""
    print(code)

def Usingdeepfeedforwardnetworkwithtwohiddenlayersforperforminglinearregressionandpredictingvalues():
    code=r"""
#4c(c) Using a deep field forward network with two hidden layers for performing linear regression and predicting values.)
from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
X,Y=make_regression(n_samples=100,n_features=2,noise=0.1,random_state=1)
scalarX,scalarY=MinMaxScaler(),MinMaxScaler()
scalarX.fit(X)
scalarY.fit(Y.reshape(100,1))
X=scalarX.transform(X)
Y=scalarY.transform(Y.reshape(100,1))
model=Sequential()
model.add(Dense(4,input_dim=2,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='mse',optimizer='adam')
model.fit(X,Y,epochs=500,verbose=0)
Xnew,a=make_regression(n_samples=3,n_features=2,noise=0.1,random_state=1)
Xnew=scalarX.transform(Xnew)
Ynew=model.predict(Xnew)
for i in range(len(Xnew)):
 print("X=%s,Predicted=%s"%(Xnew[i],Ynew[i]))
"""
    print(code)

def EvaluatingfeedforwarddeepnetworkforregressionusingKFoldcrossvalidation():
    code=r""""
#5a(Evaluating feed forward deep network for regression using KFold cross validation.)
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
# from keras.wrappers.scikit_learn import KerasRegressor
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor

#dataframe = pd.read_csv("C:\Users\karan\Desktop\M.Sc.IT\KARAN\sem 4 pracs\DL\housing.csv")
dataframe = pd.read_csv(r"C:/Users/karan/Desktop/M.Sc.IT/KARAN/sem 4 pracs/DL/housing.csv")
dataset = dataframe.values

# Print the shape of dataset to verify the number of features and samples
print("Shape of dataset:", dataset.shape)

X = dataset[:, :-1]  # Select all columns except the last one as features
Y = dataset[:, -1]   # Select the last column as target variable

def wider_model():
    model = Sequential()
    model.add(Dense(15, input_dim=13, kernel_initializer='normal', activation='relu'))
    # model.add(Dense(20, input_dim=13, kernel_initializer='normal', activation='relu'))
    model.add(Dense(13, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasRegressor(build_fn=wider_model, epochs=10, batch_size=5)))
pipeline = Pipeline(estimators)
kfold = KFold(n_splits=10)

results = cross_val_score(pipeline, X, Y, cv=kfold)
print("Wider: %.2f (%.2f) MSE" % (results.mean(), results.std()))

"""
    print(code)

def EvaluatingfeedforwarddeepnetworkformulticlassClassificationusingKFoldcrossvalidation():
    code=r""""
#5b(b)	Evaluating feed forward deep network for multiclass Classification using KFold cross-validation.)
from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=100,
                           n_features=20,
                           n_informative=2,
                           n_redundant=0,
                           n_classes=2,
                           n_clusters_per_class=2,
                           random_state=42)
# Convert the target variable to categorical format
y = to_categorical(y)
 
# Define the k-fold cross-validator
n_splits = 5
kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
 
# Define the feed-forward deep network model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Perform k-fold cross-validation
fold_accuracies = []
for train_index, val_index in kf.split(X):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = y[train_index], y[val_index]
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))
    y_pred_prob = model.predict(X_val)
    y_pred = y_pred_prob.argmax(axis=1)  # Get the predicted class index with highest probability
    accuracy = accuracy_score(y_val.argmax(axis=1), y_pred)
    fold_accuracies.append(accuracy)
 
# Calculate the mean accuracy across all folds
mean_accuracy = sum(fold_accuracies) / len(fold_accuracies)
print(f'Mean accuracy: {mean_accuracy:.2f}')
"""
    print(code)

def Implementingregularizationtoavoidoverfittinginbinaryclassification():
    code=r""""
from matplotlib import pyplot 
from sklearn.datasets import make_moons 
from keras.models import Sequential 
from keras.layers import Dense 
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1) 
n_train=30 
trainX,testX=X[:n_train,:],X[n_train:] 
trainY,testY=Y[:n_train],Y[n_train:] 

model=Sequential() 
model.add(Dense(500,input_dim=2,activation='relu')) 
model.add(Dense(1,activation='sigmoid')) 
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy']) 
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=10) 
pyplot.plot(history.history['accuracy'],label='train') 
pyplot.plot(history.history['val_accuracy'],label='test') 
pyplot.legend() 
pyplot.show()
"""
    print(code)

def  Implement12regularizationwithalpha():
    code=r""""
from matplotlib import pyplot 
from sklearn.datasets import make_moons 
from keras.models import Sequential 
from keras.layers import Dense 
from keras.regularizers import l2 
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1) 
n_train=30 
trainX,testX=X[:n_train,:],X[n_train:] 
trainY,testY=Y[:n_train],Y[n_train:] 
#print(trainX) 
#print(trainY) 
#print(testX) 
#print(testY) 
model=Sequential() 
model.add(Dense(500,input_dim=2,activation='relu',kernel_regularizer=l2(0.001))) 
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy']) 
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=10) 
pyplot.plot(history.history['accuracy'],label='train') 
pyplot.plot(history.history['val_accuracy'],label='test') 
pyplot.legend() 
pyplot.show() 
"""
    print(code)

def Replace12regularizationwithl2regularization():
    code=r"""
from matplotlib import pyplot 
from sklearn.datasets import make_moons 
from keras.models import Sequential 
from keras.layers import Dense 
from keras.regularizers import l1_l2 
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1) 
n_train=30 
trainX,testX=X[:n_train,:],X[n_train:] 
trainY,testY=Y[:n_train],Y[n_train:] 
#print(trainX) 
#print(trainY) 
#print(testX) 
#print(testY) 
model=Sequential() 
model.add(Dense(500,input_dim=2,activation='relu',kernel_regularizer=l1_l2(l1=0.001,l2=0.001))) 
model.add(Dense(1,activation='sigmoid')) 
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy']) 
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=10) 
pyplot.plot(history.history['accuracy'],label='train') 
pyplot.plot(history.history['val_accuracy'],label='test') 
pyplot.legend() 
pyplot.show() 
"""
    print(code)

def Demonstraterecurrentneuralnetworkthatlearnstoperformsequenceanalysisforstockprice():
    code=r"""
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from keras.models import Sequential 
from keras.layers import Dense 
from keras.layers import LSTM 
from keras.layers import Dropout 
from sklearn.preprocessing import MinMaxScaler 

dataset_train=pd.read_csv(r'C:/Users/karan/Desktop/M.Sc.IT/KARAN/sem 4 pracs/DL/Google_Stock_price_Train.csv')
#print(dataset_train) 
training_set=dataset_train.iloc[:,1:2].values 
#print(training_set) 
sc=MinMaxScaler(feature_range=(0,1)) 
training_set_scaled=sc.fit_transform(training_set) 
#print(training_set_scaled)
X_train=[] 
Y_train=[] 
for i in range(60,1258): 
    X_train.append(training_set_scaled[i-60:i,0]) 
    Y_train.append(training_set_scaled[i,0]) 
X_train,Y_train=np.array(X_train),np.array(Y_train) 
print(X_train) 
print('*********************************************') 
print(Y_train) 
X_train=np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1)) 
print('**********************************************') 
print(X_train) 
regressor=Sequential() 
regressor.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1],1))) 
regressor.add(Dropout(0.2)) 
regressor.add(LSTM(units=50,return_sequences=True)) 
regressor.add(Dropout(0.2)) 
regressor.add(LSTM(units=50,return_sequences=True)) 
regressor.add(Dropout(0.2)) 
regressor.add(LSTM(units=50)) 
regressor.add(Dropout(0.2)) 
regressor.add(Dense(units=1))
regressor.compile(optimizer='adam',loss='mean_squared_error') 
regressor.fit(X_train,Y_train,epochs=10,batch_size=32) 
dataset_test=pd.read_csv(r'C:/Users/karan/Desktop/M.Sc.IT/KARAN/sem 4 pracs/DL/Google_Stock_price_Train.csv') 
real_stock_price=dataset_test.iloc[:,1:2].values 
dataset_total=pd.concat((dataset_train['Open'],dataset_test['Open']),axis=0) 
inputs=dataset_total[len(dataset_total)-len(dataset_test)-60:].values 
inputs=inputs.reshape(-1,1) 
inputs=sc.transform(inputs)
X_test=[] 
for i in range(60,80): 
    X_test.append(inputs[i-60:i,0]) 
X_test=np.array(X_test) 
X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1)) 
predicted_stock_price=regressor.predict(X_test) 
predicted_stock_price=sc.inverse_transform(predicted_stock_price) 
plt.plot(real_stock_price,color='red',label='real google stock price') 
plt.plot(predicted_stock_price,color='blue',label='predicted stock price') 
plt.xlabel('time') 
plt.ylabel('google stock price') 
plt.legend() 
plt.show()
"""
    print(code)

def Performingencodinganddecodingofimagesusingdeepautoencoder():
    code=r"""
#8(Aim: Performing encoding and decoding of images using deep autoencoder.)
import keras
from keras import layers
from keras.datasets import mnist
import numpy as np
encoding_dim=32
#this is our input image
input_img=keras.Input(shape=(784,))
#"encoded" is the encoded representation of the input
encoded=layers.Dense(encoding_dim, activation='relu')(input_img)
#"decoded" is the lossy reconstruction of the input
decoded=layers.Dense(784, activation='sigmoid')(encoded)
#creating autoencoder model
autoencoder=keras.Model(input_img,decoded)
#create the encoder model
encoder=keras.Model(input_img,encoded)
encoded_input=keras.Input(shape=(encoding_dim,))
#Retrive the last layer of the autoencoder model
decoder_layer=autoencoder.layers[-1]
#create the decoder model
decoder=keras.Model(encoded_input,decoder_layer(encoded_input))
autoencoder.compile(optimizer='adam',loss='binary_crossentropy')
#scale and make train and test dataset
(X_train,_),(X_test,_)=mnist.load_data()
X_train=X_train.astype('float32')/255.
X_test=X_test.astype('float32')/255.
X_train=X_train.reshape((len(X_train),np.prod(X_train.shape[1:])))
X_test=X_test.reshape((len(X_test),np.prod(X_test.shape[1:])))
print(X_train.shape)
print(X_test.shape)
#train autoencoder with training dataset
autoencoder.fit(X_train,X_train,
 epochs=50,
 batch_size=256,
 shuffle=True,
 validation_data=(X_test,X_test))
encoded_imgs=encoder.predict(X_test)
decoded_imgs=decoder.predict(encoded_imgs)
import matplotlib.pyplot as plt
n = 10 # How many digits we will display
plt.figure(figsize=(40, 4))
for i in range(10):
 # display original
 ax = plt.subplot(3, 20, i + 1)
 plt.imshow(X_test[i].reshape(28, 28))
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False)
 # display encoded image
 ax = plt.subplot(3, 20, i + 1 + 20)
 plt.imshow(encoded_imgs[i].reshape(8,4))
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False)
 # display reconstruction
 ax = plt.subplot(3, 20, 2*20 +i+ 1)
 plt.imshow(decoded_imgs[i].reshape(28, 28))
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False)
plt.show()
"""
    print(code)

def Implementationofconvolutionalneuralnetworktopredictnumbersfromnumberimages():
    code=r"""
from keras.datasets import mnist 
from keras.utils import to_categorical 
from keras.models import Sequential 
from keras.layers import Dense,Conv2D,Flatten 
import matplotlib.pyplot as plt 
#download mnist data and split into train and test sets 
(X_train,Y_train),(X_test,Y_test)=mnist.load_data() 
#plot the first image in the dataset 
plt.imshow(X_train[0]) 
plt.show() 
print(X_train[0].shape) 
X_train=X_train.reshape(60000,28,28,1) 
X_test=X_test.reshape(10000,28,28,1) 
Y_train=to_categorical(Y_train) 
Y_test=to_categorical(Y_test) 
Y_train[0] 
print(Y_train[0])
model=Sequential() 
#add model layers 
#learn image features 
model.add(Conv2D(64,kernel_size=3,activation='relu',input_shape=(28,28,1))) 
model.add(Conv2D(32,kernel_size=3,activation='relu')) 
model.add(Flatten()) 
model.add(Dense(10,activation='softmax'))
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy']) 
#train 
model.fit(X_train,Y_train,validation_data=(X_test,Y_test),epochs=3) 
print(model.predict(X_test[:4])) 
#actual results for 1st 4 images in the test set 
print(Y_test[:4]) 
"""
    print(code)

def Denoisingofimagesusingautoencoder():
    code=r"""
#10(Denoising of images using autoencoder.)
import keras
from keras.datasets import mnist
from keras import layers
import numpy as np
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt

(X_train,_),(X_test,_)=mnist.load_data()
X_train=X_train.astype('float32')/255.
X_test=X_test.astype('float32')/255.
X_train=np.reshape(X_train,(len(X_train),28,28,1))
X_test=np.reshape(X_test,(len(X_test),28,28,1))
noise_factor=0.5
X_train_noisy=X_train+noise_factor*np.random.normal(loc=0.0,scale=1.0,size=X_train.shape)
X_test_noisy=X_test+noise_factor*np.random.normal(loc=0.0,scale=1.0,size=X_test.shape)
X_train_noisy=np.clip(X_train_noisy,0.,1.)
X_test_noisy=np.clip(X_test_noisy,0.,1.)
n=10
plt.figure(figsize=(20,2))
for i in range(1,n+1):
 ax=plt.subplot(1,n,i)
 plt.imshow(X_test_noisy[i].reshape(28,28))
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False) 
plt.show()
input_img=keras.Input(shape=(28,28,1))
x=layers.Conv2D(32,(3,3),activation='relu',padding='same')(input_img)
x=layers.MaxPooling2D((2,2),padding='same')(x)
x=layers.Conv2D(32,(3,3),activation='relu',padding='same')(x)
encoded=layers.MaxPooling2D((2,2),padding='same')(x)
x=layers.Conv2D(32,(3,3),activation='relu',padding='same')(encoded)
x=layers.UpSampling2D((2,2))(x)
x=layers.Conv2D(32,(3,3),activation='relu',padding='same')(x)
x=layers.UpSampling2D((2,2))(x)
decoded=layers.Conv2D(1,(3,3),activation='sigmoid',padding='same')(x)
autoencoder=keras.Model(input_img,decoded)
autoencoder.compile(optimizer='adam',loss='binary_crossentropy')
autoencoder.fit(X_train_noisy,X_train,
 epochs=3,
 batch_size=128,
 shuffle=True,
 validation_data=(X_test_noisy,X_test), 
callbacks=[TensorBoard(log_dir='/tmo/tb',histogram_freq=0,write_graph=False)])
predictions=autoencoder.predict(X_test_noisy)
m=10
plt.figure(figsize=(20,2))
for i in range(1,m+1):
 ax=plt.subplot(1,m,i)
 plt.imshow(predictions[i].reshape(28,28))
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False) 
plt.show()
"""
    print(code)



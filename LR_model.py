import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# C:\Users\takeoff\Desktop\chat_dataset.xlsx
data = pd.read_excel(r'C:\Users\takeoff\Desktop\chat_dataset.xlsx')
data = data.drop('response_id', axis=1)  # drop 'response_id'

# three labels
print("Unique labels:", data['label'].unique())

# preprocess
def preprocess(text):
    return "" if pd.isna(text) else text.lower()
data['content'] = data['content'].apply(preprocess)

# split data
X = data['content']
y = data['label']

# convert
if y.dtype == 'O':  # data type of y is object
    y = y.astype('category')  # convert to category

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(y_train.value_counts())
print(y_test.value_counts())



# feature extraction
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# train
model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
model.fit(X_train_tfidf, y_train)

# predict
y_pred = model.predict(X_test_tfidf)

# confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# report
report = classification_report(y_test, y_pred)
print(report)
# test set
test_cases = [
    "What is the cooking time for lasagna?",
    "How do I make a chocolate cake?",
    "What ingredients do I need for spaghetti?",
    "Tell me how to make a pizza."
]
# evaluation
test_cases_tfidf = vectorizer.transform(test_cases)
predictions = model.predict(test_cases_tfidf)
print("Predictions:")
for i, pred in enumerate(predictions):
    print(f"Test Case {i+1}: {pred}")

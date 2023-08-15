import requests
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import precision_score, accuracy_score, recall_score

from celery import Celery
import time

myCelery = Celery(
    'worker',
    broker='redis://redis:6379/0',  # Redis broker adresini belirtin
    backend='redis://redis:6379/0'  # Redis backend adresini belirtin
)

log_file = "./train.log"

def create_data(array):
    df = pd.DataFrame(array)
    return df['text'].tolist(), df['label'].tolist()

# feature extraction - creating a tf-idf matrix
def tfidf(data, max_df=0.6, min_df=0.0001):
    tfidf_vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df)
    tfidf_data = tfidf_vectorizer.fit_transform(data)
    return tfidf_data, tfidf_vectorizer

# SVM classifier
def test_SVM(x_train, x_test, y_train, y_test):
    SVM = SVC(kernel='linear', probability=True)
    SVMClassifier = SVM.fit(x_train, y_train)
    predictions = SVMClassifier.predict(x_test)
    a = accuracy_score(y_test, predictions)
    p = precision_score(y_test, predictions, average='weighted')
    r = recall_score(y_test, predictions, average='weighted')
    return SVMClassifier, a, p, r

def dump_model(model, file_output):
    pickle.dump(model, open(file_output, 'wb'))

def load_model(file_input):
    return pickle.load(open(file_input, 'rb'))

# GET DATA
def get_datas():
    datas = requests.get("http://algorithm:8001/get_datas").json()
    text, label = create_data(datas)
    return text, label


# TRAIN
@myCelery.task
def train():
    start = time.time()
    text, label = get_datas()
    training, vectorizer = tfidf(text)
    x_train, x_test, y_train, y_test = train_test_split(training, label, test_size=0.25, random_state=0)
    model, accuracy, precision, recall = test_SVM(x_train, x_test, y_train, y_test)
    dump_model(model, './model.pickle')
    dump_model(vectorizer, './vectorizer.pickle')
    finish = time.time()
    with open(log_file, "a") as f:
        f.write(f"{time.asctime} - INFO - Successfully trained on {(finish - start):.2f} second(s)\n")
    return {'status': 'success'}


# PREDICTION
@myCelery.task
def predict(text):
    model = load_model('./model.pickle')
    vectorizer = load_model('./vectorizer.pickle')
    user_text = text
    tfidf_vector = vectorizer.transform([user_text])
    result = model.predict(tfidf_vector).tolist()[0]
    return result

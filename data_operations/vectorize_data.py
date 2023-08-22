import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import joblib

data_file = open('dataset.json')
# data_file = open('dataset_stopwords.json')
# data_file = open('dataset_custom_stopwords.json')
data = json.load(data_file)

def split_train_test():
    """ Turns dataset into Pandas' data frame 
    then splits into training dataset (70%) and testing dataset (30%). """

    data_pd = pd.DataFrame(data)
    
    # y is the value of predictions we want the model to provid
    # we want a model to predicate the sentiment and another for the stars
    # y = data_pd['sentiment'].values
    y = data_pd['stars'].values
    data_pd.drop(['sentiment'], axis=1, inplace=True)
    data_pd.drop(['stars'], axis=1, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(data_pd, y, test_size=0.3, stratify=y)

    print("Train data:",  X_train.shape, y_train.shape)
    print("Test data:",  X_test.shape, y_test.shape)

    return X_train, X_test, y_train, y_test

def bow(train_data, test_data):
    vect = CountVectorizer(min_df=10)

    # the trining data should be 'fit' while testing data is 'transform'
    X_train_review_vect = vect.fit_transform(X_train['text'])
    X_test_review_vect = vect.transform(X_test['text'])

    print('X_train_review_bow shape: ', X_train_review_vect.shape)
    print('X_test_review_bow shape: ', X_test_review_vect.shape)

    return X_train_review_vect, X_test_review_vect

def tf_idf(train_data, test_data):
    vect = TfidfVectorizer(min_df=10)

    # the trining data should be 'fit' while testing data is 'transform'
    X_train_review_vect = vect.fit_transform(X_train['text'])
    X_test_review_vect = vect.transform(X_test['text'])

    # save vect
    filename = 'vect2.pkl'
    joblib.dump(vect, filename)

    print('X_train_review_tf_idf shape: ', X_train_review_vect.shape)
    print('X_test_review_tf_idf shape: ', X_test_review_vect.shape)

    return X_train_review_vect, X_test_review_vect

def ml_model():
    """ Build and train model then test accuracy using testing dataset. """

    # create model instances
    model = LogisticRegression()
    # model = MultinomialNB()
    # model = KNeighborsClassifier()

    # fit data into model
    model.fit(X_train_review_vect, y_train)

    # make predictions on testing dataset then calcuate accuracy of model
    predictions = model.predict(X_test_review_vect)
    print('Accuracy:\n', accuracy_score(y_test, predictions))
    print('Confusion matrix\n', confusion_matrix(y_test, predictions))
    print('Classification report\n', classification_report(y_test, predictions))

    # save model
    filename = 'stars_model.sav'
    joblib.dump(model, filename)

X_train, X_test, y_train, y_test = split_train_test()
# X_train_review_vect, X_test_review_vect = bow(X_train, X_test)
X_train_review_vect, X_test_review_vect = tf_idf(X_train, X_test)
ml_model()

data_file.close()
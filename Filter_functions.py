import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from keras.models import load_model
import pickle as pk
import tensorflow as tf

ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')


def text_filter(dataset):
    data=[]
    for i in range(0,len(dataset)):
        content=dataset[i]
        content=str(content)
        review = re.sub('[^a-zA-Z]', ' ', content)
        review = review.lower()
        review = review.split()
        review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
        review = ' '.join(review)
        data.append(review) 
    return data

def to_dense(x):
    arrayed_text = x.toarray()
    my_tensor = tf.convert_to_tensor(arrayed_text)
    return my_tensor

def make_prediction(text):
    modified_text = text_filter([text])

    with open('Trained_Models\Count_vectors.pkl', 'rb') as f:
        vectorizer = pk.load(f)

    vectorized_text = vectorizer.transform(modified_text)
    arrayed_text = to_dense(vectorized_text)

    Main_model = load_model('Trained_Models\\ann_model_3000_94.h5')

    result = Main_model.predict(arrayed_text)

    return (result > 0.4).astype(int)

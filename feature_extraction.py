from pickle import load
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model
from PIL import Image

# load the tokenizer
tokenizer = load(open('C:/Users/ACER/Documents/BE Major Project/tokenizer.pkl', 'rb'))
# load the model
model = load_model('C:/Users/ACER/Documents/BE Major Project/model_19.h5')

# extract features from each photo in the directory
# def extract_features(filename):
#     # load the model
#     model = VGG16()
#     # re-structure the model
#     model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
#     # load the photo
#     image = load_img(filename, target_size=(224, 224))
#     # convert the image pixels to a numpy array
#     image = img_to_array(image)
#     # reshape data for the model
#     image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
#     # prepare the image for the VGG model
#     image = preprocess_input(image)
#     # get features
#     feature = model.predict(image, verbose=0)
#     return feature

def extract_features(filename):
    # load the model
    model = VGG16()
    # re-structure the model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    # load the photo
    img = Image.fromarray(filename)
    image = img.resize((224, 224))  # new width & height
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    # get features
    feature = model.predict(image, verbose=0)
    return feature

# map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# generate a description for an image
def generate_desc(model, tokenizer, photo, max_length):
    # seed the generation process
    in_text = 'startseq'
    # iterate over the whole length of the sequence
    for i in range(max_length):
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = model.predict([photo,sequence], verbose=0)
        # convert probability to integer
        yhat = argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += ' ' + word
        # stop if we predict the end of the sequence
        if word == 'endseq':
            break
    return in_text


def clean_description(desc):
    words = ['startseq', 'endseq']
    desc = [word for word in desc.split() if word not in words]
    desc = ' '.join(desc)
    return desc



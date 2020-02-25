import tensorflow as tf
from keras.models import model_from_json,load_model
from tensorflow.keras.models import model_from_json
import numpy as np
import os,pickle

word_index_emp=pickle.load(open("word_index_emp.pkl","rb"))
with open("emp_model.json","r") as emojson:
    emp_model_json=emojson.read()
    emp_loaded_model=model_from_json(emp_model_json)
    emp_loaded_model.load_weights("rushil_drop_lstm_try_train_best.h5")
print("Emp Model Loaded")


def preprocess(sentence):
    sentence=sentence.strip()
    sentence=sentence.lower()
    sentence=sentence.replace("\x92","")
    sentence = sentence.replace("_comma_",",")
    sentence=sentence.replace("'s","")
    sentence=sentence.replace("n't"," not")
    sentence=sentence.replace("'t","ot")
    sentence=sentence.replace("'m"," am")
    sentence=sentence.replace("'ve"," have")
    sen = ""
    for i in range(len(sentence)):
        if not sentence[i].isalpha():
            sen+=" "
        else:
            sen+=sentence[i]
    return sen


def complete_preprocessing(text,intent=0,med=0,emp=0):
    l=[]
    text=preprocess(text)
    for i in text.split():
        try:
            if med:
                l.append(word_index_med[i])
            elif intent:
                l.append(word_index_intent[i])
            elif emp:
                l.append(word_index_emp[i])
            else:
                l.append(word_index_emotion[i]) 
        except:
            l.append(0)

    if intent:
        max_length=200
    else:
        max_length=50

    l=[0]*(max_length-min(len(l),max_length))+l[:max_length]
    return np.array(l)

reversed_word_index_emp=dict()
for i in word_index_emp:
    reversed_word_index_emp[word_index_emp[i]]=i





def generate_empathetic_response(model,input_text,history,emotion):
    user_input= complete_preprocessing(emotion+" "+input_text,emp=1)
    user_input=user_input.reshape((1,50))
    resp=[0]*50
    print(history[0].shape,history[1].shape)
    while True:
        y_pred=model.predict([np.array(user_input),history[0],history[1],np.array([resp])])
        # print(y_pred)
        if np.argmax(y_pred)==word_index_emp["endendend"]-1:
            break
        
        resp=resp[1:]+[np.argmax(y_pred)+1]
        if 0 not in resp:
            break
#         print(resp)
    return convert_to_sentence(reversed_word_index_emp,resp),[np.array([resp]),complete_preprocessing(input_text,emp=1).reshape((1,50))]

history=[np.array([[0]*50]),np.array([[0]*50])]
while True:

    response,history=generate_empathetic_response(emp_loaded_model,input(),history,"sad")
    print(response,history)
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from keras.models import model_from_json,load_model
import numpy as np
import os,pickle
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
word_index_emotion = pickle.load(open("./Model_files/Emotion/word_index_emotion.pkl","rb"))
word_index_intent = pickle.load(open("./Model_files/Intent/word_index_intent.pkl","rb"))
word_index_med=pickle.load(open("./Model_files/Medical_answer/word_index_med.pkl","rb"))
word_index_emp=pickle.load(open("./Model_files/Empathetic/word_index_emp.pkl","rb"))

sess = tf.Session()
graph = tf.get_default_graph()

set_session(sess)
with open("./Model_files/Emotion/emotion_model.json","r") as emojson:
    emotion_model_json=emojson.read()
    emotion_loaded_model=model_from_json(emotion_model_json)
    emotion_loaded_model.load_weights("./Model_files/Emotion/emotion_check_weights_best.h5")
print("Emotion Model Loaded")

with open("./Model_files/Intent/intent_model.json","r") as intentjson:
    intent_model_json=intentjson.read()
    intent_loaded_model=model_from_json(intent_model_json)
    intent_loaded_model.load_weights("./Model_files/Intent/intent_adam.h5")
print("Intent Model Loaded")

from tensorflow.keras.models import model_from_json
with open("./Model_files/Empathetic/emp_model.json","r") as emojson:
    emp_model_json=emojson.read()
    emp_loaded_model=model_from_json(emp_model_json)
    emp_loaded_model.load_weights("./Model_files/Empathetic/rushil_drop_lstm_try_train_best.h5")
print("Emp Model Loaded")

with open("./Model_files/Medical_answer/medical_model.json","r") as medicaljson:
    medical_model_json=medicaljson.read()
    medical_loaded_model=model_from_json(medical_model_json)
    medical_loaded_model.load_weights("./Model_files/Medical_answer/medical_lstm_adam_check_best2.h5")
print("medical Model Loaded")


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


def complete_preprocessing(text,intent,med,emp=0):
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

list_of_common_emotions=[["excited", "surprised", "joyful"],
    ["afraid", "terrified", "anxious", "apprehensive"],
    ["disgusted", "embarrassed", "guilty","ashamed"],
    ["angry", "annoyed","jealous", "furious"],
    [  "faithful", "trusting", "grateful", "caring", "hopeful"],
    ["sad" ,"disappointed", "devastated", "lonely" ,"nostalgic", "sentimental"],
    ["proud", "impressed", "content"],
    ["anticipating", "prepared","confident"]]

def get_emotion(input_text):
    user_input = complete_preprocessing(input_text, intent=0,med=0)
    # user_input.shape
    # print(user_input)
    user_input = user_input.reshape((1,50))
    predicted = emotion_loaded_model.predict(user_input)
    return list_of_common_emotions[np.argmax(predicted)][0]


def get_intent(input_text):
    user_input= complete_preprocessing(input_text,intent=1,med=0)
    user_input=user_input.reshape((1,200))
    output=intent_loaded_model.predict(user_input)
    # output = "hello"
    intent=np.argmax(output)
    return intent

reversed_word_index_med=dict()
for i in word_index_med:
    reversed_word_index_med[word_index_med[i]]=i

def convert_to_sentence(reversed_word_index_med,resp):
    s=[]
    for i in resp:
        if i==0:
            continue
        s.append(reversed_word_index_med[i])
    return s[1:]

def generate_medical_response(input_text):
    user_input= complete_preprocessing(input_text,intent=0,med=1)
    user_input=user_input.reshape((1,50))
    print(user_input)
    resp=[0]*50
    while True:
    # print(np.array(q1_padded).shape,np.array([[0]*50]).shape,np.array([[0]*50]).shape,np.array([resp]).shape)
        y_pred=medical_loaded_model.predict([np.array(user_input),np.array([resp])])
        print(np.argmax(y_pred),word_index_med["endendend"]-1)
        if np.argmax(y_pred)==word_index_med["endendend"]-1:
            break
        resp=resp[1:]+[np.argmax(y_pred)+1]
        if 0 not in resp:
            break
    print(resp)
    out = convert_to_sentence(reversed_word_index_med,resp)
    return out 

# Empathetic Response
reversed_word_index_emp=dict()
for i in word_index_emp:
    reversed_word_index_emp[word_index_emp[i]]=i

def generate_empathetic_response(input_text,history,emotion):
    answer = dict()
    user_input= complete_preprocessing(emotion+" "+input_text,intent=0,med=0,emp=1)
    user_input=user_input.reshape((1,50))
    resp=[0]*50
    # print(history[0].shape,history[1].shape)
    while True:

        y_pred=emp_loaded_model.predict([np.array(user_input),history[0],history[1],np.array([resp])])
        if np.argmax(y_pred)==word_index_emp["endendend"]-1:
            break
        
        resp=resp[1:]+[np.argmax(y_pred)+1]
        if 0 not in resp:
            break

    answer["response"] = convert_to_sentence(reversed_word_index_emp,resp)
    answer["history"] =  [np.array([resp]), complete_preprocessing(input_text,intent=0,med=0,emp=1).reshape((1,50))]
    return answer


from flask import Flask, render_template, request, send_file


app = Flask(__name__)

# def empty_history():
#     return [np.array([[0]*50]),np.array([[0]*50])]

flag=0
# history = empty_history()
history = [np.array([[0]*50]),np.array([[0]*50])]
# english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    print(flag)
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
  global graph
  global flag
  global history
  with graph.as_default():
    print("flag",flag)
    set_session(sess)
    userText = request.args.get('msg')
    print(userText)
    intent = get_intent(str(userText))
    print(intent, "Intent")
    if intent==1:
        emotion = get_emotion(str(userText))
        print("emotion", emotion)
        
        if flag==0:
            # history = empty_history()
            history = [np.array([[0]*50]),np.array([[0]*50])]
            val =  generate_empathetic_response(str(userText), [np.array([[0]*50]),np.array([[0]*50])], emotion)
            # print(val)
            answer = val["response"]
            history = val["history"]
            answer = " ".join(answer)
            flag = 1
        else:
            val =  generate_empathetic_response(str(userText),history,emotion)
            answer = val["response"]
            history = val["history"]
            answer = " ".join(answer)
            
    else:
        answer = " ".join(generate_medical_response(str(userText)))
        print(answer)
        flag=0
        # answer = "You want Medical response."
    # answer = str(emotion)
    # answer = str(answer)
    return answer


if __name__ == "__main__":
    app.run(debug=True,threaded=False)

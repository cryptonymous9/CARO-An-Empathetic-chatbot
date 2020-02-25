# from keras.models import model_from_json
import numpy as np
import os,pickle
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
word_index_emotion = pickle.load(open("./Model_files/Emotion/word_index_emotion.pkl","rb"))
word_index_intent = pickle.load(open("./Model_files/Intent/word_index_intent.pkl","rb"))
word_index_med=pickle.load(open("./Model_files/Medical_answer/word_index_med.pkl","rb"))

from tensorflow.keras.models import model_from_json

with open("./Model_files/Emotion/emotion_model.json","r") as emojson:
	emotion_model_json=emojson.read()
	emotion_loaded_model=model_from_json(emotion_model_json)
	emotion_loaded_model.load_weights("./Model_files/Emotion/emotion_check_weights_best.h5")

with open("./Model_files/Intent/intent_model.json","r") as intentjson:
	intent_model_json=intentjson.read()
	intent_loaded_model=model_from_json(intent_model_json)
	intent_loaded_model.load_weights("./Model_files/Intent/intent_adam.h5")

with open("./Model_files/Medical_answer/medical_model.json","r") as medicaljson:
	medical_model_json=medicaljson.read()
	medical_loaded_model=model_from_json(medical_model_json)
	medical_loaded_model.load_weights("./Model_files/Medical_answer/medical_lstm_adam_check_best.h5")

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


def complete_preprocessing(text,intent,med):
	l=[]
	# print(text)
	text=preprocess(text)
	# print(text)
	for i in text.split():
		try:
			if med:
				a=0
				l.append(word_index_med[i])
			else:
				if intent:
					l.append(word_index_intent[i])
				else:
					l.append(word_index_emotion[i]) 
		except Exception as e:
			# print(e)
			l.append(0)

	if intent:
		max_length=200
	else:
		max_length=50

	l=[0]*(max_length-min(len(l),max_length))+l[:max_length]
	return np.array(l)



def get_emotion(input_text):
	list_of_common_emotions=[["excited", "surprised", "joyful"],
	["afraid", "terrified", "anxious", "apprehensive"],
	["disgusted", "embarrassed", "guilty","ashamed"],
	["angry", "annoyed","jealous", "furious"],
	[  "faithful", "trusting", "grateful", "caring", "hopeful"],
	["sad" ,"disappointed", "devastated", "lonely" ,"nostalgic", "sentimental"],\
	["proud", "impressed", "content"],
	["anticipating", "prepared","confident"]]


	user_input = complete_preprocessing(input_text, intent=0,med=0)
	# user_input.shape
	# print(user_input)
	user_input = user_input.reshape((1,50))
	predicted = emotion_loaded_model.predict(user_input)
	return list_of_common_emotions[np.argmax(predicted)][0]


def get_intent(input_text):
	print("inside get_intent", input_text) 
	user_input= complete_preprocessing(input_text,intent=1,med=0)
	user_input=user_input.reshape((1,200))
	print("predict--------------------------")
	output=intent_loaded_model.predict(user_input)
	# print(output)
	intent=np.argmax(output)
	print("Intent done", intent)
	return intent

def generate_empathetic_response(u1,u2,u3,emotion):
	u1_preprocessed=preprocess(u1)
	u2_preprocessed=preprocess(u2)
	u3_preprocessed=preprocess(u3)

	text=emotion+" "+u3_preprocessed+" . "+u2_preprocessed+" . "+u1_preprocessed+" ."
	# print(text)
	with open("tmp_predict_this.txt","w") as file:
		file.write(text)
	return 0


def generate_medical_response(input_text):
	user_input= complete_preprocessing(input_text)
	user_input=user_input.reshape((1,50))
	# output=



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
#         print(np.array(q1_padded).shape,np.array([[0]*50]).shape,np.array([[0]*50]).shape,np.array([resp]).shape)
		# print("resp",resp)
		y_pred=medical_loaded_model.predict([np.array(user_input),np.array([resp])])
		if np.argmax(y_pred)==word_index_med["endendend"]-1:
			break
		
		resp=resp[1:]+[np.argmax(y_pred)+1]
		if 0 not in resp:
			break
	return resp

while True:
	print(generate_medical_response(input()))



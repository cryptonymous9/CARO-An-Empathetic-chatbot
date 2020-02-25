from keras.models import model_from_json,load_model
import numpy as np
import os,pickle
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
word_index=pickle.load(open("word_index.pkl","rb"))
word_index_intent=pickle.load(open("word_index_intent.pkl","rb"))



with open("emotion_model.json","r") as emojson:
	emotion_model_json=emojson.read()
	emotion_loaded_model=model_from_json(emotion_model_json)
	emotion_loaded_model.load_weights("emotion_check_weights_best.h5")
	print("emotion_model loaded")

with open("intent_model.json","r") as intentjson:
	intent_model_json=intentjson.read()
	intent_loaded_model=model_from_json(intent_model_json)
	intent_loaded_model.load_weights("intent_adam.h5")

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


def complete_preprocessing(text,intent=0):
	l=[]
	text=preprocess(text)
	for i in text.split():
		try:
			if intent:
				l.append(word_index_intent[i])
			else:
				l.append(word_index[i])
		except:
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
	["sad" ,"disappointed", "devastated", "lonely" ,"nostalgic", "sentimental"],
	["proud", "impressed", "content"],
	["anticipating", "prepared","confident"]]


	user_input = complete_preprocessing(input_text)
	# user_input.shape
	print(user_input)
	user_input = user_input.reshape((1,50))
	predicted = emotion_loaded_model.predict(user_input)
	return list_of_common_emotions[np.argmax(predicted)][0]


def get_intent(input_text):
	user_input= complete_preprocessing(input_text,1)
	user_input=user_input.reshape((1,200))
	output=intent_loaded_model.predict(user_input)
	print(output)
	intent=np.argmax(output)
	return intent

def generate_empathetic_response(u1,u2,u3,emotion):
	u1_preprocessed=preprocess(u1)
	u2_preprocessed=preprocess(u2)
	u3_preprocessed=preprocess(u3)

	text=emotion+" "+u3_preprocessed+" . "+u2_preprocessed+" . "+u1_preprocessed+" ."
	print(text)
	with open("tmp_predict_this.txt","w") as file:
		file.write(text)
	# translate()


def generate_medical_response(input_text):
	user_input= complete_preprocessing(input_text)
	user_input=user_input.reshape((1,50))
	# output=

# while True:
# 	print(get_intent(input()))
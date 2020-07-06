# CARO: An Empathetic Health Conversational Chatbot for People with Major Depression

There has been a rise in the number of patients suffering from major depression over the past decade. Most of the patients are reluctant and do not open up for counselling services. Conversational applications such as chatbots have been found efficient in overcoming alcohol addiction. Effective treatments can tackle depression, but only 10% of affected patients are able to avail such treatments mainly due to lack of resources and social stigma associated with mental disorders. We propose CARO, a chatbot app, which is capable of performing empathetic conversations and providing medical advice for people with major depression. CARO will be able to sense the conversational context, its intent and the associated emotions.



## Files

1. **Model_files:**  Saved Model parameters of all the involved subnetworks.
2. **Final:** Defined Pipeline
3. **Static , Templates:** Web files
4. **app.py:** Defined Flask Server 

<!-- ![](screen.PNG) -->

## Requirements

1. Tensorflow = 1.13.1 (recommended)
2. Flask framework

## Usage

To start the app, run the following commands in the terminal:

```shell
python app.py
```

This will start CARO chatbot at `localhost:8888`

> Note: We have not released the weights of individual models yet. 



## Approach

<img src="pipeline.png" style="width: 50%;margin-right: 10px;" />

## CARO chatbot UI

<img src="./screen.PNG" style="width: 50%;margin-right: 10px;" />





## Citation

```latex
@inproceedings{10.1145/3371158.3371220,
author = {Harilal, Nidhin and Shah, Rushil and Sharma, Saumitra and Bhutani, Vedanta},
title = {CARO: An Empathetic Health Conversational Chatbot for People with Major Depression},
doi = {10.1145/3371158.3371220},
booktitle = {Proceedings of the 7th ACM IKDD CoDS and 25th COMAD},
keywords = {Depression, Medical Advice, Empathetic Response, Chatbot}
}
```


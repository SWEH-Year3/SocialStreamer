[sda](sdaad)

# Social Streamer

## Objectives

* Get ReqlTime data Stream from facebook
* Apply Filters on That data
* Prdouce Filtered Data to kafka
* Consume Data with spark
* Apply Aggregate Function on that data

---

## System Architecture
<p>
<img src='./SocialStreamer.png' alt='sys arch' >
</p>

---

## Tools

<p style='text-align: center'>
<img src='./icons/facebook-icon-logo-svgrepo-com.svg' alt='facebook logo' width=150>
<img src='./icons/meta-logo-facebook-svgrepo-com.svg' alt='meta facebook logo' width=150>
<img src='./icons/nodejs-logo-svgrepo-com.svg' alt='nodejs logo' width=150>
<img src='./icons/kafka-svgrepo-com.svg' alt='kafka logo' width=150>
<img src='./icons/python-svgrepo-com.svg' alt='python logo' width=150>
</p>

---

## How To Run

1. Start Docker Container of Kafka ` docker-compose --project-directory=".\docker\" -d up`

2- get new token from [Graph API](https://developers.facebook.com/tools/explorer/)

* token must have __user_likes__ permission
  
3- start either producer or consumer

* make sure that you installed dependencies inside *producer* `npm i ` , inside *pythonSpark* `pip install -r requirements.txt`
   

3.1- Starting Producer ` node .\producer\producer.js `

3.2- start consumer ` python .\spark\pythonSpark\main.py `



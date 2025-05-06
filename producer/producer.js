import axios from 'axios';
import { Kafka } from 'kafkajs';



const publish = async (data) => {

    const kafka = new Kafka({
        clientId: 'social-media-producer',
        brokers: ['localhost:9092'],
    });
    
    const producer = kafka.producer();
    
    await producer.connect();
    
    await producer.send({
        topic: 'pagesLiked',
        messages: [
            { value: data },
        ],
    });
    
    await producer.disconnect();
};

const URL = 'https://graph.facebook.com/v22.0/me/likes';
let nextPage = '';

const app = () => {
    const TOKEN = process.env.TOKEN;
    // console.log(TOKEN)
    // console.log(nextPage);
    axios.get(URL, {
        params: {
            access_token: TOKEN,
            fields: 'category,name,created_time,id',
            limit: 1,
            after: nextPage
        }
    })
        .then((response) => {
            // filter on community service category
            console.log(response.data.data[0]);
            if (!response.data.data[0].category.includes('Community')) {
                const {category} = response.data.data[0];
                const data = JSON.stringify({category});
                publish(data);
                console.log('published');
            };
        
        nextPage = response.data?.paging?.cursors?.after;
        // console.log(nextPage);
    })
    .catch((error) => {
        console.log(error);
    });
};

setInterval(app, 5000);

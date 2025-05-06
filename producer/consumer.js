// consumer.js
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
    clientId: 'my-kafka-consumer',
    brokers: ['localhost:9092'] // adjust as needed
});

const consumer = kafka.consumer({ groupId: 'my-group' });

const run = async () => {
    // Connecting the consumer
    await consumer.connect();

    // Subscribing to a topic
    await consumer.subscribe({ topic: 'social-stream', fromBeginning: true });

    // Start listening for messages
    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            console.log({
                value: message.value.toString(),
                topic,
                partition,
                offset: message.offset,
            });
        },
    });
};

run().catch(console.error);

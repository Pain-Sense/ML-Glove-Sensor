import { Kafka } from 'kafkajs';

const kafka = new Kafka({
    clientId: 'frontend',
    brokers: ['localhost:9092'],
})

const consumer = kafka.consumer({groupId: 'groupFrontend'})

const runConsumer = async() => {
    await consumer.connect();
    await consumer.subscribe({topic: 'eventos', fromBeginning: true});
    await consumer.run({
        eachMessage: async ({message}) => {
            if (message.value){
                const res = message.value.toString()
                const data = JSON.parse(res)
                if (data.sensor === "off") {
                    console.log("Device no %d is offline", data.deviceId)
                }
            }
        }
    })
}

runConsumer()
import { Subscriber, Topic } from "../types/common";

class PubSub {
    private topics: Topic;

    constructor() {
        this.topics = {};
    }

    subscribe(topic: string, subscriber: Subscriber) {
        if (!this.topics[topic]) this.topics[topic] = [];
        if (this.topics[topic].some((sub: Subscriber) => sub.id === subscriber.id)) {
            this.unsubscribe(topic, subscriber.id);
        }
        this.topics[topic].push(subscriber);
    }

    unsubscribe(topic: string, id: string) {
        if (!this.topics[topic]) return;
        this.topics[topic] = this.topics[topic].filter(
            (subscriber: Subscriber) => subscriber.id !== id
        );
    }

    publish(topic: string, message: string) {
        if (!this.topics[topic]) return;
        this.topics[topic].forEach(
            (subscriber: Subscriber) =>
                typeof subscriber.handler === "function" && subscriber.handler(message)
        );
    }
}

export type PubSubType = typeof PubSub;
export const pubsub = new PubSub();
export default PubSub;

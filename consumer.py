cat main.py
import json
import logging
import re
import torch
from quixstreams import Application
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = 'RUSpam/spamNS_v1'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=1).to(DEVICE).eval()
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^А-Яа-я0-9 ]+', ' ', text)
    text = text.lower().strip()
    return text


def classify_message(message):
    message = clean_text(message)
    encoding = tokenizer(message, padding='max_length',
                         truncation=True, max_length=128, return_tensors='pt')
    input_ids = encoding['input_ids'].to(DEVICE)
    attention_mask = encoding['attention_mask'].to(DEVICE)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask).logits
        score = torch.sigmoid(outputs).cpu().numpy()[0][0]

    is_spam = int(score >= 0.5)
    return is_spam, float(score)


def main():
    app = Application(
        broker_address="10.10.127.2:9092",
        loglevel="INFO",
        consumer_group="llm",
    )

    with app.get_consumer() as consumer:
        consumer.subscribe(["raw_messages"])

        while True:
            msg = consumer.poll(1)
            if msg is None:
                continue
            elif msg.error() is not None:
                raise Exception(msg.error())

            value = json.loads(msg.value())
            text = value["text"]

            is_spam, score = classify_message(text)
            if is_spam:
                create_message(session, message)
            
            print(f"Сообщение: {text}")
            print(
                f"Результат: {'СПАМ' if is_spam else 'НЕ СПАМ'} "
                f"(рейтинг спама: {score:.4f})")
            print("-" * 50)



with app.get_consumer() as consumer:
    consumer.subscribe(["rated_messages"])

    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue
        elif msg.error() is not None:
            raise Exception(msg.error())

        value = json.loads(msg.value())
        message = Message(**value)
        if message.spam_score >= 0.4:
            create_message(session, message)
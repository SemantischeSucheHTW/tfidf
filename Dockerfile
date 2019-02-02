FROM python:3.7-stretch

RUN pip install kafka-python pymongo

RUN mkdir /words_by_length_updater
WORKDIR /words_by_length_updater

COPY dao dao
COPY updater updater

COPY main.py main.py

ENV KAFKA_BOOTSTRAP_SERVERS kafka:9092
ENV KAFKA_NEW_WORDLIST_TOPIC new_wordlist
ENV KAFKA_NEW_WORDLIST_GROUP_ID words_by_length_updater

ENV MONGODB_HOST mongo
ENV MONGODB_DB default
ENV MONGODB_WORDS_BY_LENGTH_COLLECTION words_by_length

ENV MONGODB_USERNAME words_by_length_updater
ENV MONGODB_PASSWORD words_by_length_updater

ENV DEBUG true

CMD ["python3", "-u", "main.py"]
import os

from updater.kafkasource import KafkaSource
from updater.updater import Updater
from dao.mongodbdao import MongoDBDao


def env(key):
    value = os.environ.get(key)
    if not value:
        raise Exception(f"environment variable '{key}' not set!")
    return value

debug = env("DEBUG")

kafkaSource = KafkaSource({
    "topic": env("KAFKA_NEW_WORDLIST_TOPIC"),
    "bootstrap_servers": env("KAFKA_BOOTSTRAP_SERVERS"),
    "group_id": env("KAFKA_NEW_WORDLIST_GROUP_ID"),
    "auto_offset_reset": "earliest"
})

#DONE
dao = MongoDBDao({
    "host": env("MONGODB_HOST"),
    "db": env("MONGODB_DB"),
    "words_by_length_collection": env("MONGODB_WORDS_BY_LENGTH_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

updater = Updater(dao)

while True:
    
    wordlist = kafkaSource.getWordList()

    if debug:
        print(f"Got wordlist {wordlist}")
        
    updated = updater.put(wordlist)
    
    if debug:
        print(f"Updated word len matrix")  #with {updated}
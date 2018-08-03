import json
import logging
import os
import sys

import pika

from handlers import handler

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    request = json.loads(body)
    logger.debug(request)
    data = json.loads(request['body'])
    intent = data.get('request', {}).get('intent', {}).get('name')
    logger.debug('intent %s', intent)
    handlers = getattr(handler, 'handlers', {})
    intent_handler = handlers.get(intent)
    if intent_handler is not None:
        response = intent_handler(data)
    else:
        response = {
            "version": "string",
            # "sessionAttributes": {
            #   "key": "value"
            # },
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Sorry, I cannot understand what do you want!",
                },
                "shouldEndSession": True
            }
        }

    response = {
        'response': json.dumps(response)
    }
    ch.basic_publish(exchange='', routing_key=request['answer_queue'], body=json.dumps(response))


def main(config):
    credentials = pika.PlainCredentials(config.get('rabbitmq', 'username'), config.get('rabbitmq', 'password'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.get('rabbitmq', 'host'), credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=config.get('rabbitmq', 'request_queue'))

    channel.basic_consume(callback, queue=config.get('rabbitmq', 'request_queue'), no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    import argparse
    import configparser

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('config')
    args = arg_parser.parse_args()

    if not os.path.exists(args.config):
        logger.critical(f"File {args.config} doesn't exist")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(args.config)

    loglevel = config.get('app', 'log', fallback='INFO')
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logging.basicConfig(format='%(levelname)s:%(message)s')
    logger.setLevel(numeric_level)
    logger.info('info starting...')

    main(config)


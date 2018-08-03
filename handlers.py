import os


def handler(intent):
    handlers = handler.__dict__.setdefault('handlers', {})

    def decorator(func):
        handlers[intent] = func
        return func

    return decorator


@handler('show_processes')
def show_balance(request):
    text = 'You have 23 processes'
    return {
        "version": "string",
        # "sessionAttributes": {
        #   "key": "value"
        # },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text,
            },
            "shouldEndSession": True
        }
    }


@handler('open_terminal')
def show_balance(request):
    os.popen('terminator')
    text = "I'm opening console"
    return {
        "version": "string",
        # "sessionAttributes": {
        #   "key": "value"
        # },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text,
            },
            "shouldEndSession": True
        }
    }


@handler('AMAZON.FallbackIntent')
def fallback(request):
    return {
        "version": "string",
        # "sessionAttributes": {
        #   "key": "value"
        # },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "This gonna be interesting!",
            },
            "shouldEndSession": True
        }
    }


@handler('AMAZON.HelpIntent')
def help(request):
    return {
        "version": "string",
        # "sessionAttributes": {
        #   "key": "value"
        # },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Write to Smartsub in messenger asking about alexa login. It must provide you 4 digit code. Then ask me to login providing this 4 digit code",
            },
            "shouldEndSession": True
        }
    }

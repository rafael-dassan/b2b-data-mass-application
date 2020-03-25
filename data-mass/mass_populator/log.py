import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

MAX_KEY_LENGTH = 30

def log(key, message):
    key_length = MAX_KEY_LENGTH - len(key)

    key_complement = repeat_to_length(".", key_length)
    
    logging.info("{a}{b}: {c}".format(a=key, b=key_complement.strip(), c=message))

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

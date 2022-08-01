import logging

def set_logger():
    # create logger
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    # add ch to logger
    logger.addHandler(ch)

    return logger
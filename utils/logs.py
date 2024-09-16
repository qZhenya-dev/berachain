from loguru import logger
import traceback, sys, os
import time


def error_info():
    errs = traceback.extract_tb(sys.exc_info()[2])
    message = ""
    for err in errs:
        message += f"{os.path.splitext(os.path.basename(err.filename))[0]}:{err.name}:{err.end_lineno}/"
    return message[:-1]

def format_message(record):
    space = 10 - len(record["level"].name)
    if record["level"].name == "ERROR":
        return "<white>[{time:YYYY-MM-DD HH:mm:ss}]</white> | <blue>{level}"+" "*space +"</blue>| " \
               "<cyan>"+error_info()+"</cyan> | <level>{message}</level>\n"
    else:
        return "<white>[{time:YYYY-MM-DD HH:mm:ss}]</white> <level>| {level}"+" "*space +"| <cyan>{function}:{line}</cyan> | {message}</level>\n"

def logging_setup():
    logger.remove()

    title_logs = int(time.time() * 1000)

    logger.add(f"data/logs/{title_logs}.txt", colorize=False, format=format_message, encoding="utf-8", level="INFO")
    logger.add(sys.stdout, colorize=True, format=format_message, level="INFO")

logging_setup()

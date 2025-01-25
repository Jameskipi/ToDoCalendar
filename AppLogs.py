import logging
import os


def start():
    if not os.path.isdir("data"):
        os.makedirs("data")
    logging.basicConfig(
        filename="data/app.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",)
    logging.warning('Main App started')


def warning(text):
    logging.warning(text)


def error(text):
    logging.error(text)

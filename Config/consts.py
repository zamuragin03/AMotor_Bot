from apscheduler.schedulers.asyncio import AsyncIOScheduler
import configparser
from pathlib import Path
import sys
from DB import DataBase
import logging
config = configparser.ConfigParser()
PATH = Path(__file__).resolve().parent
config.read(str(PATH) + '/config.ini')
logger = logging.getLogger(__name__)
logging.basicConfig(filename=Path(__file__).parent.parent.joinpath('db_vol').joinpath("debug.log"), filemode="w", level=logging.DEBUG, encoding='UTF-8', format='%(asctime)s - %(levelname)s - %(message)s', )
DB = DataBase(PATH.parent.joinpath('db_vol').joinpath('db.db'))
BOT_TOKEN = config["Telegram"]["bot_token"]

scheduler = AsyncIOScheduler()


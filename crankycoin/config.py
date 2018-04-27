import logging
import yaml

with open("config/config.yaml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

with open("config/bcinfo.yaml", 'r') as bcfile:
	bcinfo = yaml.load(bcfile)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#client = None


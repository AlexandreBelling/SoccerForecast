from Web_interface.who_scored_browser import WSUrlRobot
from time import sleep
from random import uniform

PROXY_ADRESS = 'https://www.proxysite.com/fr/'
XPATH_INPUT = '//*[@id="url-form-wrap"]/form/div[2]/input'
XPATH_BUTTON = '//*[@id="url-form-wrap"]/form/div[2]/button'

webrobot = WSUrlRobot()

webrobot.set(proxy_adress=PROXY_ADRESS,
             xpath_input=XPATH_INPUT,
             xpath_button=XPATH_BUTTON)

# webrobot.parse_history(proxy=False, verbose=1)

webrobot.get_perf()

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
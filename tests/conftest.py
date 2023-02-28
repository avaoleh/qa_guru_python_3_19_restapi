import pytest
from selene.support.shared import browser
from utils.base_session import BaseSession
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def demoshop():
    demoshop_session = BaseSession(os.getenv("API_URL"))
    return demoshop_session


@pytest.fixture(scope='session')
def register(demoshop):
    browser.config.base_url = "https://demowebshop.tricentis.com/"
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    response = demoshop.post("/login", data={
        'Email': os.getenv('EMAIL'),
        'Password': os.getenv('PASSWORD')
    }, allow_redirects=False)

    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("Themes/DefaultClean/Content/images/logo.png")

    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})

    return browser


@pytest.fixture(scope="session")
def regres():
    regres_session = BaseSession(os.getenv("REG_URL"))
    return regres_session
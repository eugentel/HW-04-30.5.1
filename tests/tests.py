import time

import pytest
import requests
from api import PetFriends
from config import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

class TestMyPets():


    def test_get_my_pets_title(self, driver):
        """ Тест """
        # Вводим email
        driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
        # Вводим пароль
        driver.find_element(By.ID, 'pass').send_keys('12345')
        # Нажимаем на кнопку входа в аккаунт
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    def test_get_my_pets_count(self, driver):
        """ Тест количества питомцев на странице"""
        # Вводим email
        driver.find_element(By.ID, 'email').send_keys('ya1@ya.ru')
        # Вводим пароль
        driver.find_element(By.ID, 'pass').send_keys('ya1')
        # Нажимаем на кнопку входа в аккаунт
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        driver.get('https://petfriends.skillfactory.ru/my_pets')
        table_rows = driver.find_elements(By.XPATH, "//tbody/tr")
        info = driver.find_element(By.XPATH,"//div[@class='.col-sm-4 left']").text
        pets = info.split("\n")
        pets_count = int(pets[1].split()[1])

        assert len(table_rows) == pets_count

    def test_get_my_pets_with_photo_count(self, driver):
        """ Тест количества питомцев с фото на странице больше половины """
        # Вводим email
        driver.find_element(By.ID, 'email').send_keys('ya1@ya.ru')
        # Вводим пароль
        driver.find_element(By.ID, 'pass').send_keys('ya1')
        # Нажимаем на кнопку входа в аккаунт
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        driver.get('https://petfriends.skillfactory.ru/my_pets')
        info = driver.find_element(By.XPATH, "//div[@class='.col-sm-4 left']").text
        pets = info.split("\n")
        pets_count = int(pets[1].split()[1])
        pet_images = driver.find_elements(By.XPATH,"//th[@scope='row']/img")
        photo_count = 0
        for img in pet_images:
            if 'data' in img.get_attribute('src'):
                photo_count = photo_count + 1

        assert photo_count >= pets_count/2
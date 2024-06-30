
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

@pytest.fixture(autouse=True)
def driver():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()


def test_get_my_pets_count(driver):
    """ Тест количества питомцев на странице"""
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('ya1@ya.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('ya1')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    # Получаем записи таблицы питомцев
    table = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "tbody")))
    table_rows = table.find_elements(By.XPATH, "//tbody/tr")
    # Получаем инфоблок статистики
    info = driver.find_element(By.XPATH,"//div[@class='.col-sm-4 left']").text
    # Выделяем запись о питомцах
    pets = info.split("\n")[1]
    # Выделяем обще количество питомцев
    pets_count = int(pets.split()[1])
    # Предполагаем, что количество питомцев соответствует количеству записей в таблице
    assert len(table_rows) == pets_count

def test_get_my_pets_with_photo_count(driver):
    """ Тест количества питомцев с фото на странице больше половины """
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('ya1@ya.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('ya1')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    # Получаем инфоблок статистики
    info = driver.find_element(By.XPATH, "//div[@class='.col-sm-4 left']").text
    pets = info.split("\n")
    # Получаем количество питомцев
    pets_count = int(pets[1].split()[1])
    # Получаем элементы с img
    pet_images = driver.find_elements(By.XPATH,"//th[@scope='row']/img")
    photo_count = 0
    # Подсчитываем количество фото (src имеет данные)
    for img in pet_images:
        if 'data' in img.get_attribute('src'):
            photo_count = photo_count + 1
    # Проверяем, что количество питомцев с фото не меньше половины общего числа питомцев
    assert photo_count >= pets_count/2


def test_get_my_pets_with_name_breed_age(driver):
    """ Тест не пустых name, breed, age  питомцев """
    driver.implicitly_wait(10)  # Задаем неявное ожидание
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('ya1@ya.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('ya1')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Получаем записи таблицы питомцев
    table_rows = driver.find_elements(By.XPATH, "//tbody/tr")
    no_empty_field = True
    for rec in table_rows:
        fields = rec.find_elements(By.TAG_NAME, "td")
        for field in fields:
            if len(field.text) == 0:
                no_empty_field = False
    # Проверяем, что у каждого питомца есть имя, порода и возраст
    assert no_empty_field

def test_get_my_pets_different_name(driver):
    """ Тест не повторяющихся имен питомцев """
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('ya1@ya.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('ya1')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Получаем записи таблицы питомцев
    table_rows = driver.find_elements(By.XPATH, "//tbody/tr")
    names = []
    for rec in table_rows:
        name = rec.find_elements(By.TAG_NAME, "td")[0].text
        names.append(name)
    name_set = set(names)
    # Проверяем, что имя питомца не повторяется
    assert len(names) == len(name_set)


def test_get_my_pets_all_unique(driver):
    """ Тест уникальности питомцев """
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('ya1@ya.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('ya1')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Получаем записи таблицы питомцев
    table_rows = driver.find_elements(By.XPATH, "//tbody/tr")
    pets = set()
    for rec in table_rows:
        name = rec.find_elements(By.TAG_NAME, "td")[0].text
        breed = rec.find_elements(By.TAG_NAME, "td")[1].text
        age = rec.find_elements(By.TAG_NAME, "td")[2].text
        pet = frozenset([name, breed, age])
        pets.add(pet)
    # Проверяем, что данные питомца не повторяются
    assert len(pets) == len(table_rows)

import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wdw
chromedriver_autoinstaller.install()


url = "https://petfriends.skillfactory.ru/login"
email = "panfilivan279@gmail.com"
password = "8357"


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    driver.maximize_window()
    yield driver

    driver.quit()


def test_show_my_pets(driver):
    wdw(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    # assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'
    assert driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'
    # Открываем страницу /my_pets.
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

    # список всех объектов питомца, в котором есть атрибут ".text"
    wdw(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody')))
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody')
    list_data_my_pets = []
    for i in range(len(all_my_pets)):
        list_data = all_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
        list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
    set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество
    assert len(list_data_my_pets) == len(
        set_data_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть


def test_show_all_pets(driver):
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    # assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'
    assert driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'
    # Открываем страницу /my_pets.
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

    # список всех объектов питомца, в котором есть атрибут ".text"
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody')

    # этот список image объектов, которые имееют метод get_attribute('src') ,
    # благодаря которому можно посмотреть есть ли изображение питомца или нет.

    driver.find_element("xpath", "//*[@id=\"all_my_pets\"]/table/tbody/tr[1]/th")

    all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/th')
    for i in range(len(all_pets_images)):
        assert all_pets_images[i].get_attribute('src') != ''

    driver.find_element("xpath", "//*[@id=\"all_my_pets\"]/table/tbody/tr[1]/td[1]")
    all_pets_name = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[1]')
    for i in range(len(all_pets_name)):
        assert all_pets_name[i].text != ''

    all_pets_age = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[2]')
    for i in range(len(all_pets_age)):
        assert all_pets_age[i].text != ''
    driver.find_element("xpath", "//*[@id=\"all_my_pets\"]/table/tbody/tr[1]/td[3]")
    all_pets_breed = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[3]')
    for i in range(len(all_pets_breed)):
        assert all_pets_breed[i].text != ''

    # проверяем что список своих питомцев не пуст
    assert len(all_my_pets) > 0

    pets_info = []
    for i in range(len(all_my_pets)):
        # получаем информацию о питомце из списка всех своих питомцев
        pet_info = all_my_pets[i].text

        # избавляемся от лишних символов '\n×'
        pet_info = pet_info.split("\n")[0]

        # добавляем в список pets_info информацию рода: имя, тип, возраст,  по каждому питомцу
        pets_info.append(pet_info)

    # Проверяем, что у всех питомцев разные имена:
    list_name_my_pets = []
    for i in range(len(all_pets_name)):
        list_name_my_pets.append(all_pets_name[i].text)
    set_name_my_pets = set(list_name_my_pets)  # преобразовываем список в множество
    assert len(list_name_my_pets) == len(
        set_name_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть
    # Проверяем, что в списке нет повторяющихся питомцев:
    list_data_my_pets = []
    for i in range(len(all_my_pets)):
        list_data = all_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
        list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
    set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество
    assert len(list_data_my_pets) == len(
        set_data_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть








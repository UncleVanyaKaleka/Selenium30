import time
import pytest
from main import url, email, password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.get(url=url)
    driver.maximize_window()
    yield driver
    driver.quit()


# Настраиваем переменную явного ожидания:
wait = WebDriverWait(pytest.driver, 10, poll_frequency=1)


@pytest.fixture()
def test_all_pets(driver):
    # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Проверяем, что мы оказались на главной странице сайта.
    # Ожидаем в течение 5с, что на странице есть тег h1 с текстом "PetFriends"
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))
    # Открываем страницу /my_pets.
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    # Проверяем, что мы оказались на странице пользователя.
    # Ожидаем в течение 5с, что на странице есть тег h2 с текстом "All" -именем пользователя
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "All"))

    # assert driver.find_element(By.TAG_NAME, 'h2').text == "JetiMax"
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_number) == len(pets_count)

    # Ищем в теле таблицы все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице:
    image_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert wait.until(EC.visibility_of(image_my_pets[i]))
    # Ищем в теле таблицы все строки с полными данными питомцев (имя, порода, возраст, "х" удаления питомца):
    css_locator = 'tbody>tr'
    data_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, css_locator)

    # Ожидаем, что данные всех питомцев, найденных локатором css_locator = 'tbody>tr', видны на странице:
    for i in range(len(data_my_pets)):
        assert wait.until(EC.visibility_of(data_my_pets[i]))

    # Ищем в теле таблицы все имена питомцев и ожидаем увидеть их на странице:
    name_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert wait.until(EC.visibility_of(name_my_pets[i]))
    # Ищем в теле таблицы все породы питомцев и ожидаем увидеть их на странице:
    type_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert wait.until(EC.visibility_of(type_my_pets[i]))

    # Ищем в теле таблицы все данные возраста питомцев и ожидаем увидеть их на странице:
    age_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert wait.until(EC.visibility_of(age_my_pets[i]))

    # Ищем на странице /my_pets всю статистику пользователя,
    # и вычленяем из полученных данных количество питомцев пользователя:
    all_statistics = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])

    # Проверяем, что количество строк в таблице с моими питомцами равно общему количеству питомцев,
    # указанному в статистике пользователя:
    assert len(data_my_pets) == all_my_pets

    # Проверяем, что хотя бы у половины питомцев есть фото:
    m = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            m += 1
    assert m >= all_my_pets / 2

    # Проверяем, что у всех питомцев есть имя:
    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть порода:
    for i in range(len(type_my_pets)):
        assert type_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть возраст:
    for i in range(len(age_my_pets)):
        assert age_my_pets[i].text != ''

    # Проверяем, что у всех питомцев разные имена:
    list_name_my_pets = []
    for i in range(len(name_my_pets)):
        list_name_my_pets.append(name_my_pets[i].text)
    set_name_my_pets = set(list_name_my_pets)  # преобразовываем список в множество
    assert len(list_name_my_pets) == len(
        set_name_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

    # Проверяем, что в списке нет повторяющихся питомцев:
    list_data_my_pets = []
    for i in range(len(data_my_pets)):
        list_data = data_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
        list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
    set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество
    assert len(list_data_my_pets) == len(
        set_data_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import chromedriver_autoinstaller
import pytest

@pytest.fixture

def driver():
    # Set Chrome to headless mode
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless")              # Run without opening a window
    options.add_argument("--no-sandbox")            # Required in some CI environments
    options.add_argument("--disable-dev-shm-usage") # Prevent shared memory issues
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test1(driver):
    driver.get("http://192.168.176.128")
    sleep(1)
    assert "To-Do List" in driver.title
    input_field = driver.find_element(By.NAME, "task")
    add_task = driver.find_element(By.XPATH, "//button[text()='Add Task']")  # Assumes button text
    input_field.send_keys("Learn Selenium")
    add_task.click()
    sleep(1)
    assert "Learn Selenium"  in driver.page_source
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Learn Selenium')]")))

    # Locate all task rows
    task_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

    # Create a list to hold specific task information
    tasks_info = []

    # Loop through each task row to extract needed information
    for row in task_rows:
        # Extract task details
        task_description = row.find_element(By.XPATH, "td[1]").text  # Assuming task description is in the first column
        added_date = row.find_element(By.XPATH, "td[2]").text  # Assuming added date is in the second column
        completed_status = row.find_element(By.XPATH, "td[3]").text  # Assuming completed status is in the third column

        # Store this information in a dictionary
        task_details = {
            "description": task_description,
            "added_date": added_date,
            "completed": completed_status
        }

        # Append to the list
        tasks_info.append(task_details)

    # Print the task information
    print("Tasks Information:")
    for info in tasks_info:
        print(info)  # Print each task's details

    delete_button = task_rows[-1].find_element(By.XPATH, ".//button[text()='Delete']")
    delete_button.click()

    # Wait for a moment after deletion
    sleep(1)
    task_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")  # Refresh task list
    assert not any("Learn Selenium" in row.find_element(By.XPATH, "td[1]").text for row in task_rows), "Task 'Learn Selenium' was not deleted successfully."


def test2(driver):
    driver.get("http://192.168.176.128")
    sleep(1)
    assert "To-Do List" in driver.title
    input_field = driver.find_element(By.NAME, "task")
    add_task = driver.find_element(By.XPATH, "//button[text()='Add Task']")  # Assumes button text
    input_field.send_keys("Learn Selenium")
    add_task.click()
    sleep(1)
    assert "Learn Selenium"  in driver.page_source
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Learn Selenium')]")))

    # Locate all task rows
    task_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

    # Create a list to hold specific task information
    tasks_info = []

    # Loop through each task row to extract needed information
    for row in task_rows:
        # Extract task details
        task_description = row.find_element(By.XPATH, "td[1]").text  # Assuming task description is in the first column
        added_date = row.find_element(By.XPATH, "td[2]").text  # Assuming added date is in the second column
        completed_status = row.find_element(By.XPATH, "td[3]").text  # Assuming completed status is in the third column

        # Store this information in a dictionary
        task_details = {
            "description": task_description,
            "added_date": added_date,
            "completed": completed_status
        }

        # Append to the list
        tasks_info.append(task_details)

    # Print the task information
    print("Tasks Information:")
    for info in tasks_info:
        print(info)  # Print each task's details

    delete_button = task_rows[-1].find_element(By.XPATH, ".//button[text()='Delete']")
    delete_button.click()

    # Wait for a moment after deletion
    sleep(1)
    task_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")  # Refresh task list
    assert not any("Learn Selenium" in row.find_element(By.XPATH, "td[1]").text for row in task_rows), "Task 'Learn Selenium' was not deleted successfully."

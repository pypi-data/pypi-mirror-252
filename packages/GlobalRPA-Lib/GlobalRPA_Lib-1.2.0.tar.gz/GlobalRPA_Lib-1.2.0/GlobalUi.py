import time

def dummy_send(driver, xpath, word, delay):    
    for c in word:
        driver.find_element('xpath',xpath).send_keys(c)
        time.sleep(delay)

def element_exists(driver, xpath, timeout):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            driver.find_element('xpath', xpath)
            return True
        except Exception as e:
            time.sleep(1)

    return False
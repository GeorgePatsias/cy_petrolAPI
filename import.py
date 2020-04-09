import re
import time
import logging
import datetime
import traceback
from pymongo import MongoClient
from urllib.parse import unquote
from WebDriver import WebDriverObj
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mongo_client = MongoClient('mongodb://localhost:27017/', connect=False)
db = mongo_client['my_information3']
petrol_collec = db['all_petrol']

webDriver = WebDriverObj()

cities_map = {}
petrol_map = {}

date_time_now = datetime.datetime.now()


def dms2latlon(dms_str):
    dms_str = re.sub(r'\s', '', dms_str)

    sign = -1 if re.search('[swSW]', dms_str) else 1

    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'

    second += "." + frac_seconds
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)


def fix_coordinates(coords):
    coords = unquote(coords)

    if 'E' in coords or 'N' in coords:
        if 'N,' in coords:
            lat = dms2latlon(coords.split(',')[0])
            lon = dms2latlon(coords.split(",", 1)[1])
        else:
            lat = dms2latlon(coords.split(' ')[0])
            lon = dms2latlon(coords.split(" ", 1)[1])

    else:
        lat = coords.split(',')[0].strip()
        lon = coords.split(',', 1)[1].strip()

    return lat, lon


def parse_table(table, petrol_type, city):
    try:
        time.sleep(1)

        for row in table.find_elements_by_xpath('./tr'):
            company = {
                "petrol_type": petrol_type,
                "city": city,
                "brand": "",
                "company_name": "",
                "address": "",
                "postal_code": "",
                "telno": "",
                "latitude": "",
                "longitude": "",
                "area": "",
                "price": "",
                "created_at": date_time_now
            }

            td_list = row.find_elements_by_xpath('./td')

            company['brand'] = td_list[0].get_attribute('innerHTML').strip().replace('\n', '')
            company['company_name'] = unquote(td_list[1].get_attribute('innerHTML').strip().replace('\n', '')).replace('&amp;', '&')
            company['area'] = td_list[3].get_attribute('innerHTML').strip().replace('\n', '')
            company['price'] = td_list[4].get_attribute('innerHTML').strip().replace('\n', '')

            coords = td_list[2].get_attribute('innerHTML').strip().replace('\n', '')
            coords = coords.split("coordinates=", 1)[1].split('"')[0]

            lat, lon = fix_coordinates(coords)
            company['latitude'] = lat
            company['longitude'] = lon

            inner_address = td_list[2].text.strip().replace('\n', '')

            company['address'] = inner_address.split(' Τ.Κ')[0]
            company['postal_code'] = inner_address.split("Τ.Κ ", 1)[1].split(' τηλ')[0]
            company['telno'] = inner_address.split("τηλ: ", 1)[1]

            petrol_collec.insert(company)

    except Exception as e:
        logging.exception("[EXCEPTION] parse_table: {}".format(traceback.print_exc(e)))
        webDriver.quit()


def get_selection_mapping(petrol_type_select, city_select):
    try:
        petrol_options = [x for x in petrol_type_select.find_elements_by_tag_name("option")]
        for petrol in petrol_options:
            petrol_map[petrol.text] = petrol.get_attribute("value")

        city_options = [y for y in city_select.find_elements_by_tag_name("option")]
        for city in city_options:
            cities_map[city.text] = city.get_attribute("value")

        petrol_map.pop('--- Επιλέξτε ---')
        cities_map.pop('Όλες')

    except Exception as e:
        logging.exception("[EXCEPTION] get_selection_mapping: {}".format(traceback.print_exc(e)))
        webDriver.quit()


def get_selectDOM():
    try:
        petrol_type_select = WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PetroleumType"]')))
        city_select = WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="StationCity"]')))
        submit_button = WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="assignFiltersBtn"]')))

        return petrol_type_select, city_select, submit_button

    except Exception as e:
        logging.exception("[EXCEPTION] get_selectDOM: {}".format(traceback.print_exc(e)))
        webDriver.quit()
        return None, None, None


def start_scraping(petrol_type, city):
    try:
        webDriver.get('https://mobile.eservices.cyprus.gov.cy/mcit_ccpr/PBL_MCIT_PetroleumPrices')

        petrol_type_select, city_select, submit_button = get_selectDOM()

        petrol_type_select = Select(petrol_type_select)
        city_select = Select(city_select)

        petrol_type_select.select_by_value(petrol_map.get(petrol_type))
        city_select.select_by_value(cities_map.get(city))

        try:
            submit_button.click()

            table = WebDriverWait(webDriver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="table-column-toggle"]/tbody')))

        except Exception as e:
            logging.exception(e)
            webDriver.quit()
            return

        parse_table(table, petrol_type, city)

    except Exception as e:
        logging.exception("[EXCEPTION] start_scraping: {}".format(traceback.print_exc(e)))
        webDriver.quit()


def main():
    try:
        logging.info("STARTED")
        webDriver.get('https://mobile.eservices.cyprus.gov.cy/mcit_ccpr/PBL_MCIT_PetroleumPrices')

        petrol_type_select, city_select, submit_button = get_selectDOM()

        get_selection_mapping(petrol_type_select, city_select)

        for petrol in petrol_map.keys():
            for city in cities_map.keys():
                start_scraping(petrol, city)

        webDriver.quit()
        logging.info("FINISHED!!!!!!!!!!!!!")

    except Exception as e:
        logging.exception("[EXCEPTION] main: {}".format(traceback.print_exc(e)))
        webDriver.quit()


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.INFO)

    main()

    webDriver.quit()

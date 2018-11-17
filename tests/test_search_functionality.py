# -*- coding: UTF-8 -*-
from user import User
from all_imports import *

class Test_search_functionality(unittest.TestCase):

    '''Start web driver'''
    def setUp(self):
        path = os.getcwd() + '/tests/chromedriver/chromedriver'  #chromedriver will be on docker container
        #path = os.getcwd() + '/chromedriver/chromedriver'  #chromedriver will be on docker container

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1366,768')

        self.driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        self.url = 'https://www.autohero.com/de/search/'

    '''Stop web driver'''
    def tearDown(self):
        self.driver.quit()

    '''Filter for 2015 as minimum registration year and sort by descending price'''
    def test_if_items_are_correctly_filtered_and_sorted(self):
        """Test if items are correctly filtered and sorted"""
        driver = self.driver
        user = User(driver)

        user.check_url_status(self.url)

        driver.get(self.url)

        user.click_a_web_element('filter-year')

        user.choose_a_value_in_a_select('yearRange.min', '2015')  # choose 2015 on year select

        user.choose_a_value_in_a_select('sort', 'offerPrice.amountMinorUnits.desc')  # sort by desc price using a select

        current_url = driver.current_url

        '''Verify that items has been filtered by checking: query string on url, applied filter and registration date on cards'''
        self.assertIn('yearMin=2015', current_url, 'Query string is incorrect %s' %current_url)
        time.sleep(2)
        try:
            filter_applied = driver.find_element_by_xpath('//*[@data-qa-selector="active-filter"]')
            value_filter_applied = filter_applied.get_attribute('data-qa-selector-value')
            value_filter_applied = int(value_filter_applied)
            self.assertEqual(value_filter_applied, 2015)
        except:
            self.fail('It\'s not possible to see the active filter \'Registration year\'')

        spec_list = driver.find_elements_by_xpath('//*[@data-qa-selector="spec-list"]')

        reg_dates = []
        for spec in spec_list:
            date = spec.find_elements_by_xpath('//*[@data-qa-selector="spec"]')[0]
            reg_dates.append(date)

        reg_years = []
        for date in reg_dates:
            date_str = str(date.text.encode('ascii', 'replace')).split('/')[1]
            year = int(date_str)
            reg_years.append(year)

        self.assertGreaterEqual(reg_years, 2015)


        '''Verify that items are sorted by descending price by checking: query string and price on cards'''
        self.assertIn('sort=PRICE_DESC', current_url, 'Query string is incorrect %s' %current_url)

        prices = driver.find_elements_by_xpath('//*[@data-qa-selector="price"]')

        price_list = []
        for price in prices:
            p = str(price.text.encode('ascii','replace')).split(' ')[0].replace('.', '')
            p = int(p)
            price_list.append(p)

        self.assertTrue(all(first >= second for first, second in zip(price_list, price_list[1:])))

if __name__ == "__main__":
    path = os.getcwd() + '/../results'
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=path))
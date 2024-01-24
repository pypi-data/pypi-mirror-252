import unittest
from unittest.mock import MagicMock
from main import data_science_central

class TestDataScienceCentral(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_driver.find_element.return_value = MagicMock(text="Mocked HTML")
    
    def test_get_data(self):
        scraper = data_science_central()
        scraper.setup_driver = MagicMock(return_value=self.mock_driver)

        data = scraper.get_data('C:/Users/Chesta/Desktop/data_scraping/chromedriver.exe')
        self.assertIsNotNone(data)

if __name__=='__main__':
    unittest.main()
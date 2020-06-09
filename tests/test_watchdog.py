import unittest
import re

from watchdog import BookWatchDog


class TestScraper(unittest.TestCase):

    link = 'https://www.manning.com/books/flutter-in-action'
    name, price = BookWatchDog(link).get_item()

    def test_get_book_name(self):
        self.assertEqual('Manning | Flutter in Action', self.name)

    def test_get_price(self):
        self.assertIsNotNone(re.match(r'\$\d+.\d{2}', self.price))


if __name__ == '__main__':
    unittest.main()

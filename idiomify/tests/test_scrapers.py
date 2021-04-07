from unittest import TestCase
from idiomify.scrapers import ThefreeRawsScraper


class ThefreeRawsScraperTest(TestCase):

    def test_trojan_horse(self):
        raws = ThefreeRawsScraper.fetch('Trojan-horse')
        self.assertTrue(len(raws) > 0)

    def test_blue_sky_thinking(self):
        raws = ThefreeRawsScraper.fetch('blue-sky thinking')
        self.assertTrue(len(raws) > 0)

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
import argparse

# Define a Scrapy Spider for scraping exchange rates
class RateExchangerSpider(scrapy.Spider):
    name = "exchange_rate"

    # Initialize the spider with date and currency arguments
    def __init__(self, date, currency):
        try:
            # Parse and format the input date
            self.date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
        except ValueError:
            # Handle invalid date format
            print("Invalid input date format")
            return
        self.currency = currency
        self.dictionary = {}
  
    # Start crawling from the currency translation website
    def start_requests(self):
        url_translation = 'https://www.11meigui.com/tools/currency'
        try:
            # Try to make an HTTP request to the currency code translation site
            yield scrapy.Request(url_translation, callback=self.parse_translation_request)
        except Exception as e:
            print(f"An error occurred: {e}")
  
    # Parse the currency translation website's response
    def parse_translation_request(self, response):
        rows = response.xpath('//table/tbody/tr')
        for row in rows[1:]:
            # Extract currency name and code
            currency_name = row.xpath('.//td[2]/text()').get()
            currency_code = row.xpath('.//td[5]/text()').get()
            # Fill in the dictionary with currency code and name
            if currency_code and currency_code not in self.dictionary:
                self.dictionary[currency_code.strip()] = currency_name.strip()

        if self.currency in self.dictionary:
            currency_name = self.dictionary[self.currency]
            # Prepare data for form submission
            try:
                formdata = {
                    'erectDate': self.date,
                    'nothing': self.date,
                    'pjname': currency_name
                }
                url_rate_exchange = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
              
                # Submit the form request for exchange rates
                yield scrapy.FormRequest(
                    url=url_rate_exchange, 
                    formdata=formdata, 
                    callback=self.parse_rateExchange_request
                )
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            # Exit if the input currency code is not correct or not avalible on the website
            print("Currency code is not recognizable")
            return

    # Parse the response from the rate exchange website
    def parse_rateExchange_request(self, response):
        if not response:
            print("Empty response received")
            return
        
        # Extract the sell rate
        sell_rate = response.xpath('//table/tr[2]/td[4]/text()').get()
        if sell_rate is None:
            print("No corresponding Chinese name for your currency code is found")
        else: 
            # Write the sell rate to the result file
            filename = "result.txt"
            with open(filename, 'w') as file:
                file.write(sell_rate)
        
        yield None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Define command line arguments for date and currency
    parser.add_argument('date')
    parser.add_argument('currency')

    # Parse command line arguments
    args = parser.parse_args()
  
    # Start the Scrapy process with project settings and crawling
    process = CrawlerProcess(get_project_settings())
    process.crawl(RateExchangerSpider, date=args.date, currency=args.currency)
    process.start()

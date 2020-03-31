from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from pprint import pprint
import scrapy
import os
import shutil

WATCHLIST = ["USA", "Brazil",
             "China", "S. Korea", "India", "Iran", "Israel"
             "Italy", "UK", 
             "Nigeria", 
             "Australia"]

if os.path.isdir("data"):
    shutil.rmtree("data")

class CoronaSpider(scrapy.Spider):
    # initialize parameters
    name = "corona_spider"
    start_urls = ['https://www.worldometers.info/coronavirus/']

    def parse(self, response):
        table = response.xpath('//*[@id="main_table_countries_today"]//tr')
        assert table is not None
        for country in table[:-1]:
            country_name = country.xpath('td//text()').extract_first()
            if country_name in WATCHLIST:
                country_page = country.xpath('td//a/@href').extract_first()
                if country_page:
                    yield scrapy.Request(
                        response.urljoin(country_page),
                        callback=self.parse_country
                    )
            yield {'name': country_name}

    def parse_country(self, response):
        charts = response.xpath('//*[@class="row graph_row"]')
        total_corona_chart = charts[0]
        script = total_corona_chart.xpath('div/script/text()').extract()[0]
        title = total_corona_chart.xpath('div/h3/text()').extract()[0]
        try:
            country_name = title[title.index(" in ")+4:]
            if country_name[:4] == "the ":
                country_name = country_name[4:]
        except e:
            raise ValueError("Worldometer changed their labels.\
                              Hold your pain, Harold.")

        parser = Parser()
        tree = parser.parse(script)
        data = [None, None] # dates and corresponding number of cases
        for node in nodevisitor.visit(tree):
            if isinstance(node, ast.Assign):
                if getattr(node.left, 'value', '') == 'categories' and not data[0]:
                    print("\nparsing dates\n")
                    data[0] = [eval(getattr(s, 'value', '')) for s in getattr(node.right, 'items', '')]
                elif getattr(node.left, 'value', '') == 'data' and not data[1]:
                    print("\nparsing number of cases\n")
                    data[1] = [int(getattr(n, 'value', '')) for n in getattr(node.right, 'items', '')]
        assert data[0] and data[1] and len(data[0]) == len(data[1])
        with open("data/%s.csv" % country_name, 'w+') as f:
            for k in range(len(data[0])):
                f.write(data[0][k])
                f.write(',')
                f.write(str(data[1][k]))
                f.write('\n')
        
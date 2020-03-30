from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from pprint import pprint
import scrapy
# watchlist = ["USA", "China", "Italy", "Iran", "Germany", "UK", "India", "S. Korea", "Brazil"]
watchlist = ["USA"]

class CoronaSpider(scrapy.Spider):
    # Initialize parameters
    name = "corona_spider"
    start_urls = ['https://www.worldometers.info/coronavirus/']
    my_baby = None

    def parse(self, response):
        table = response.xpath('//*[@id="main_table_countries_today"]//tr')
        assert table is not None
        for country in table[:-1]:
            country_name = country.xpath('td//text()').extract_first()
            if country_name in watchlist:
                my_baby = country_name
                next_page = country.xpath('td//a/@href').extract_first()
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=lambda r: self.parse_country(r, my_baby)
                )
            yield {'name': country_name}

    def parse_country(self, response, country_name):
        charts = response.xpath('//*[@class="row graph_row"]')
        total_corona_chart = charts[0]
        script = total_corona_chart.xpath('div/script/text()').extract()[0]

        parser = Parser()
        tree = parser.parse(script)
        data = [None, None]
        for node in nodevisitor.visit(tree):
            if isinstance(node, ast.Assign):
                if getattr(node.left, 'value', '') == 'categories' and not data[0]:
                    print("\nparsing dates\n")
                    data[0] = [eval(getattr(s, 'value', '')) for s in getattr(node.right, 'items', '')]
                elif getattr(node.left, 'value', '') == 'data' and not data[1]:
                    print("\nparsing values\n")
                    data[1] = [int(getattr(n, 'value', '')) for n in getattr(node.right, 'items', '')]
        assert data[0] and data[1] and len(data[0]) == len(data[1])
        with open("data/%s.csv" % country_name, 'w+') as f:
            for i in range(len(data[0])):
                f.write(data[0][i])
                f.write(',')
                f.write(str(data[1][i]))
                f.write('\n')
        
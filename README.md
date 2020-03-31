# corona-trends
Predict the number of coronavirus cases in major countries in 2020

To crawl data, run ```scrapy runspider scraper.py -o data/countries.csv -t csv``` in your terminal.

To generate models, run ```python3 model.py [number of days you wish to predict after today]``` in your terminal (replace the text in square brackets with number and remove the brackets).
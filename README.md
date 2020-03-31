# Predict number of COVID-19 cases in selected countries

## Motivation

**This project is a nonrigorous yet convenient attempt to estimate the number of COVID-19 cases in selected countries in 2020.** All data used are from [Worldometer](https://www.worldometers.info/coronavirus/). Currently I am working on making the model more predictive specifically for number of coronavirus cases.

**Nobody<sup>*</sup> in the West saw COVID-19 coming for them when the outbreak started in China.** At the inception of this project (end of March), many developing countries, including India and many in Africa, may be similarly unaware of the impending thread. It is troubling to think how much these places, without advanced medical capabilities like the US or China, may suffer when the outbreak hits. Through this project, I hope to contribute to public awareness of the concern and efforts to mitigate it.

## Installation and Use

To use or collaborate, first install ```scrapy```, a popular web scrawler in Python, with
    
    pip install scrapy

Then pull the repo with

    git clone https://github.com/Yijia-Chen/corona-trends/.git

To crawl data from the Worldometer site, run

    scrapy runspider scraper.py -o data/countries.csv -t csv

You should now see a folder named "data" containing case data of countries selected. Select different countries by changing the list at the top of ```scraper.py```. To then fit models to data crawled, run 

    python3 model.py <number of days after today you wish to predict>

Remember to replace the text in triangular brackets above with a number and remove brackets. You should now see "plots" and "preds", which store past data and future predictions respectively. The model in ```model.py``` is a logistic function; you may play with other functions of your choice and see how well it fits the data.

*: By nobody I mean very few who was heard or believed at the time

## Collaboration

If you would like to contribute to this project or just have an cool idea, feel free to contact me at yijia[dot]chen[at]berkeley[dot]edu, and I am more than happy to discuss and we can potentially collaborate.

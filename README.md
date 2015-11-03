# MtG Spider

A simple spider for crawling the results of Magic: The Gathering Online events and generating user stats based on them.

## Requirements

- Splash (http://splash.readthedocs.org/en/latest/install.html).
  - If you're on OS X, be aware that boot2docker is no longer supported and you may need to install Docker Toolbox (http://docs.docker.com/mac/step_one/)
- MongoDB.
- Other than that, just run `pip install -r requirements.txt`.

## Setting it up

### Local development environment

Use the `master` branch. Edit `settings.py` file to point to your own Splash server and MongoDB databases.

* If you don't want to use the MongoDB pipeline, just comment the `mtgspider.pipelines.PlayerStatsPipeline` pipeline in `settings.py`

### ScrapingHub's Scrapy Cloud

Use the `scrapinghub-deployment` branch. Just follow the instructions here to configure it for yourself: http://doc.scrapinghub.com/scrapy-cloud.html#deploying-a-scrapy-spider

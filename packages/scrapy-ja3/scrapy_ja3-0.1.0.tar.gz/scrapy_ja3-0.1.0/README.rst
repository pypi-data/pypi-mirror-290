============
Scrapy-JA3
============


Scrapy-JA3 is used to forge JA3 fingerprints in Scrapy, by modifying DEFAULT_CIPHERS,  which is used in the packaging of Scrapy TLS


* LICENSE: MIT license


Requirements
------------

* ``Python`` >=  3.6.0
* ``Scrapy`` >=  2.6.0
* Works on Linux, Windows, macOS


Installation
------------

From pip 

.. code-block:: bash

    pip install scrapy-ja3

From GitHub

Uninstall
------------

.. code-block:: bash

    pip uninstall scrapy-ja3

Usage
------------

.. code-block:: Python

    from scrapy import Request, Spider


    class Ja3TestSpider(Spider):
        name = 'ja3_test'

        custom_settings = {
            'DOWNLOAD_HANDLERS': {
                'http': 'scrapy_ja3.download_handler.JA3DownloadHandler',
                'https': 'scrapy_ja3.download_handler.JA3DownloadHandler',
            }
        }

        def start_requests(self):
            start_urls = [
                'https://tls.browserleaks.com/json',
            ]
            for url in start_urls:
                yield Request(url=url, callback=self.parse_ja3)

        def parse_ja3(self, response):
            self.logger.info(response.text)
            self.logger.info("ja3_hash: " + response.json()['ja3_hash'])



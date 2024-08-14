import random

from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
from scrapy.core.downloader.handlers.http import HTTPDownloadHandler


def shuffle_ciphers():
    origin_ciphers = ("TLS13-AES-256-GCM-SHA384:TLS13-CHACHA20-POLY1305-SHA256:"
                      "TLS13-AES-128-GCM-SHA256:ECDH+AESGCM:"
                      "ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:"
                      "ECDH+AES256:DH+AES256:"
                      "ECDH+AES128:DH+AES:"
                      "RSA+AESGCM:RSA+AES")

    ciphers = origin_ciphers.split(":")
    random.shuffle(ciphers)
    ciphers.append("!aNULL:!MD5:!DSS")
    return ":".join(ciphers)


class JA3DownloadHandler(HTTPDownloadHandler):
    def download_request(self, request, spider):
        tls_ciphers = shuffle_ciphers()
        self._contextFactory = ScrapyClientContextFactory(tls_ciphers=tls_ciphers)
        return super().download_request(request, spider)

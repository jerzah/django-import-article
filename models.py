from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#import feedparser
#import urllib2                                       
#from BeautifulSoup import BeautifulSoup
import time
import lxml.html
from urlparse import urlparse
import tldextract



class Article(models.Model):
    article_address = models.URLField(max_length=200, default=None)
    article_title = models.CharField(max_length=200)
    authorised_domain = models.BooleanField(default=False)
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.article_address

    #Checks to see the object domain is in the list of allowed domains
    #returns True or False
    def checkDomain(self):
        start = time.time()
        domainName = Domain()
        #tldextract is not effiecient enough
        #address = tldextract.extract(self.article_address)
        address = urlparse(self.article_address)
        end = time.time()
        print(address.hostname, "checkDomain: ", end - start)
        return Domain.objects.filter(registered_domain__contains=address.hostname).exists()

    #returns the extracted title heading from a webpage
    def getTitleFromUrl(self):
        start = time.time()
        t = lxml.html.parse(self.article_address)
        urlTitle = t.find(".//title").text
        end = time.time()
        print("checkTitle: ", end - start)
        return urlTitle

    def setAuthDomain(self):
        self.authorised_domain = self.checkDomain()

    def setTitle(self):
        self.article_title = self.getTitleFromUrl()

    def getTitle(self):
        return self.article_title


class Domain(models.Model):
    #trusted_sources* is for testing of various effeciencies
    trusted_sources_dict = {"bbc" : True,
                       "www.cnn.com" : True,
                       "www.jpost.com": True,
                       "www.ynetnews.com" : True
                            }

    trusted_sources_list = ["bbc",
                       "www.cnn.com",
                       "www.jpost.com",
                       "www.ynetnews.com"
                            ]
    registered_domain = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.registered_domain

'''
    def binarySearch(self, item):
	        if len(self.trusted_sources_list) == 0:
	            return False
	        else:
	            midpoint = len(self.trusted_sources_list)//2
	            if self.trusted_sources_list[midpoint]==item:
	              return True
	            else:
	              if item<self.trusted_sources_list[midpoint]:
	                return self.binarySearch(self.trusted_sources_list[:midpoint],item)
	              else:
	                return self.binarySearch(self.trusted_sources_list[midpoint+1:],item)
            
'''


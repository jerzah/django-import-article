from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#import feedparser
#import urllib2                                       
#from BeautifulSoup import BeautifulSoup
import time
import lxml.html
import urlparse
import tldextract
from django.core.exceptions import ObjectDoesNotExist


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

#Simple function to check if the domain is in the Domains list
    def checkDomain(self):
        #domainName = Domains()
        #return domainName.registered_list.__contains__(address.domain)
        try:
            address = tldextract.extract(self.article_address)
            test = Domain.objects.get(registered_domain__contains=address.domain)
            print(test)
        except ObjectNotExist as error:
            print(test)

        




    def checkTitle(self):
        '''
        start = time.time()
        response = urllib2.urlopen(self.article_address)
        html = response.read()
        soup = BeautifulSoup(html)
        title = soup.html.head.title
        #self.article_title = title
        end = time.time()
        print("urlib2: ", end - start)
        '''

        start = time.time()
        t = lxml.html.parse(self.article_address)
        urlTitle = t.find(".//title").text
        end = time.time()
        print("lxmlParse: ", end - start)
        return urlTitle

    def getTitle(self):
        return self.article_title


class Domain(models.Model):
    registered_domain = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.registered_domain


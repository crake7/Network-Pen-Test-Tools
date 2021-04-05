from burp import IBurpExtender
from burp import IContextMenuFactory

from java.util   import ArrayList
from javax.swing import JMenuItem

from datetime   import datetime
from HTMLParser import HTMLParser

import re

class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

    def handle_data(self, data):
        self.page_text.append(data)
    
    def handle_comment(self, data):
        self.page_text.append(data)
    
    def strip(self, html):
        self.feed(html)
        return "".join(self.page_text)

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()
        self.context    = None
        # No duplicates 
        self.hosts      = set()

        # Start with the goood ol'
        self.wordlist   = set(["password"])

        # Set up your extension
        callbacks.setExtensionName("Make a wordlist")
        callbacks.registerContextMenuFactory(self)

        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list    = ArrayList()
        menu_list.add(JMenuItem(
            "Create a wordlist", actionPerformed = self.wordlist_menu))

        return menu_list

    def wordlist_menu(self, event):
        # grab the details of what the user clicked
        http_traffic = self.context.getSelectedMessages()

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host         = http_service.getHost()
            self.hosts.add(host)
            http_response = traffic.getResponse()
            if http_response:
                self.get_words(http_response)
        
        self.display_wordlist()
        return

    def get_words(self, http_response):
        headers, body = http_response.tostring().split('\r\n\r\n', 1)
        #skip non-text responses
        if headers.lower().find("content-type: text") == -1:
            return

        tag_stripper = TagStripper()
        page_text    = tag_stripper.strip(body)

        # Find all the words that start with an alphabetic char
        # and two or more "word" characters (A-z, a-z, 0-9)
        words = re.findall("[a-zA-Z]\w{2,}", page_text)

        for word in words:
            # filter out long strings
            if len(word) <= 12:
                self.wordlist.add(word.lower())

        return 

    def mangle(self, word):
        year     = datetime.now().year
        suffixes = ["", "1", "!", year]
        mangled  = []

        for password in (word, word.capitalize()):
            for suffix in suffixes:
                mangled.append("%s%s" % (password, suffix))
        
        return mangled

    def display_wordlist(self):
        print( "#!Comment: Wordlist for the site(s) %s" % ", ".join(self.hosts))
        
        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)

        return
        
from burp import IBurpExtender
from burp import IContextMenuFactory

from java.net    import URL
from java.util   import ArrayList
from javax.swing import JMenuItem
from thread      import start_new_thread

import json
import socket
import urllib   # Jython uses Python 2.X implementation

agent    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
# Insert your BING API. "https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/"
api_key  = 12345
api_host = 'api.cognitive.microsoft.com'

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()
        self.context    = None

        # Set up the extension
        callbacks.setExtensionName("Ask Bing")
        callbacks.registerContextMenuFactory(self)

        return

    def createMenuItems(self, context_menu):
        ''' Create a context menu when user right-clicks a request in Burp '''
        # Receives a IContextMenuInvocation object and uses it to determine which HTTP
        # request the user selected.
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem(
            "Send to Bing", actionPerformed=self.bing_menu))
        return menu_list

    def bing_menu(self, event):
        # grab the details of what user clicked
        http_traffic = self.context.getSelectedMessages()

        print("%d requests highlighted" % len(http_traffic))

        for traffic in http_traffic:
            # Methods from IHttpService
            http_service = traffic.getHttpService()
            host         = http_service.getHost()

            print("User selected host: %s" % host)
            self.bing_search(host)

        return
    
    def bing_search(self, host):
        # Check if there is an IP or hostname
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False
        
        if is_ip:
            ip_address = host
            domain     = False
        else:
            ip_address = socket.gethostbyname(host)
            domain     = True
        
        # Queries Bing for all virtual hosts with the same IP address
        start_new_thread(self.bing_query, ('ip:%s' % ip_address,))

        # If a domain is received, we search any subdomains indexed
        if domain:
            start_new_thread(self.bing_query, ('domain:%s' % host,))

    def bing_query(self, bing_query_string):
        print('Performing Bing search: %s' % bing_query_string)
        http_request = 'GET https://%s/bing/v7.0/search?' % api_host
        # encode our query
        http_request += 'q=%s HTTP/1.1\r\n' % urllib.quote(bing_query_string)
        http_request += 'Host: %s\r\n'      % api_host
        http_request += 'Connection:close\r\n'
        http_request += 'Ocp-Apim-Subscription-Key: %s\r\n' % api_key
        http_request += 'User-Agent: %s\r\n\r\n' % agent 

        json_body = self._callbacks.makeHttpRequest(
            api_host, 443, True, http_request).tostring()
        json_body = json_body.split('\r\n\r\n', 1)[1]

        try:
            # Deseralize the response
            response = json.loads(json_body)
        except (TypeError, ValueError) as err:
            print('No results from Bing: %s' % err)
        else:
            sites = list()
            if response.get('webPages'):
                sites = response['webPages']['value']
            if len(sites):
                for site in sites:
                    print('*' * 100) 
                    print('Name: %s     '        % site['name'])  
                    print('URL : %s     '        % site['url'])  
                    print('Description: %s     ' % site['snippet'])
                    print('*' * 100) 

                    java_url = URL(site['url'])
                    if not self._callbacks.isInScope(java_url):
                        print('Adding %s to Burp scope' % site['url'])
                        self._callbacks.includeInScope(java_url)
                    else:
                        print('Empty response from Being.: %s' % bing_query_string)
        return 









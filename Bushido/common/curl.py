import urllib, urllib2, time, os, socket, sys
import xml.dom.minidom

from Bushido.common.out import _log

class curl:
    def __init__(self):
        self.name = None
        self.path = None
        self.cookie = None

    #---------------------------------------------------
    # _curl : Grab the file based on url
    #---------------------------------------------------
    def _curl(self, url, **httpheaders):
        retry = 3
        while retry > 0:
            try:
                return self._do_curl(url, **httpheaders)
            except StandardError:
                _log('[-] Retry...')
            retry = retry - 1
        _log('[-] Failed after retry %d times.' % retry)
        return ("","")
        #raise StandardError('[-] Failed after retry %d times.' % retry)

    #---------------------------------------------------
    # _do_curl : Grab the file contents based on url
    #            Function will return filename and file contents
    #---------------------------------------------------
    def _do_curl(self, url, **httpheaders):
        #' get html text from url. '
        headers = {
                #'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
                'Referer': url
        }
        headers.update(httpheaders)
        req = urllib2.Request(url, None, headers)
        resp = urllib2.urlopen(req)
        self.cookie = resp.headers.get('Set-Cookie')
        content_length = resp.headers.get('Content-Length')
        filename = ""
        if resp.headers.get('Content-Disposition') is None:
            filename = ""
        else:
            filename = _mid(resp.headers.get('Content-Disposition'), 'filename="','"')
        data = resp.read()
        if data is None:
            _log('[*] No download provided.')
            return ''
        return (filename, data)

    #---------------------------------------------------
    # _mid : find substring by start and end.
    #        >>> _mid('some text <h1>header</h1> end...', '<h1>', '</h1>')
    #        It will return 'header'
    #---------------------------------------------------
    def _mid(self, s, start, end):
        n1 = s.find(start)
        if n1 == (-1):
            return u''
        n2 = s.find(end, n1 + len(start))
        if n2 == (-1):
            return u''
        return s[n1 + len(start) : n2]

    #---------------------------------------------------
    # _download_ipa : Downloading of .ipa file
    #---------------------------------------------------
    def _download_dcn_ipa(self, url, referer, basename, **httpheaders):
        print("[+] Downloading .ipa file from %s" % url)
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': referer,
                'Connection': 'keep-alive'
        }
        headers.update(httpheaders)
        req = urllib2.Request(url, None, headers)
        try:
            resp = urllib2.urlopen(req)
            re302 = resp.geturl()
            _log("[+] Redirecting to %s" % re302)
            filename = ""
            filename = urllib.unquote(os.path.basename(re302)).decode('utf8')
            dest_name = filename
            data = resp.read()
            
            if data is None:
                _log('[*] No download provided.')
            else:
                with open(dest_name, 'wb') as fw:
                    fw.write(data)
                _log('[+] Download ok: %s' % os.path.basename(re302))
                time.sleep(10)
        except urllib2.HTTPError, e:
            _log("There was an error: %s" % e)
            sys.exc_clear()
            pass
import re,os,urllib
from urllib2 import unquote

from Bushido.common.out import _log
from Bushido.common.curl import curl

class liqucn(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        
        d = curl()
        filename, download_html = d._curl(self.path)
        _number_pages = re.search("</a><a>...</a><a href='index_(.*?).shtml'>", download_html, re.DOTALL|re.UNICODE)
        _number_pages = int(_number_pages.group(1))
        
        try:
            os.makedirs('./Bushido/downloads/liqucn')
        except OSError:
            pass
        os.chdir("./Bushido/downloads/liqucn")
        for i in range(1, _number_pages+1):
            self.download_url = download_url + str(i) + ".shtml"
            filename, download_html = d._curl(self.download_url)
            _log("[+] Mass downloading from %s" % unquote(self.download_url))

            found = re.findall('<div class="app_name">.*?<a href="/rj/(.*?).shtml" target="_blank">', download_html, re.DOTALL|re.UNICODE)
            for _ipa_link in found:
                _ipa_referer = "http://os-ios.liqucn.com/rj/" + _ipa_link + ".shtml"
                _log("[+] Downloading from %s" % _ipa_referer)
                filename, download_html = d._curl(_ipa_referer)
                found_direct = re.findall('<!--<a href="http://count.liqucn.com/d.php(.*?)" target="_blank">', download_html, re.DOTALL|re.UNICODE)
                _download_link = "http://count.liqucn.com/d.php" + found_direct[0]
                filename, download_html = d._curl(_download_link)
                # Need to revisit this later to check the regular expression
                _direct_link = re.search('http:\/\/[^i][^t](.*?)"', download_html, re.DOTALL|re.UNICODE)
                path = _direct_link.group(0)[:-1]
                _log(path)
                d._download_dcn_ipa(path, _ipa_referer, "")
        os.chdir('../../../')
        
        
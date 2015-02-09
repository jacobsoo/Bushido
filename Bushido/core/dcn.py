import re,os,urllib
from urllib2 import unquote

from Bushido.common.out import _log
from Bushido.common.curl import curl

class dcn(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.download_url = None

    def _download(self, path, download_url):
        self.path = path
        
        d = curl()
        filename, download_html = d._curl(self.path)
        _number_pages = re.search('<span class="total">共(.*?)页</span>', download_html, re.DOTALL)
        _number_pages = int(_number_pages.group(1))
        
        try:
            os.makedirs('./Bushido/downloads/dcn')
        except OSError:
            pass
        os.chdir("./Bushido/downloads/dcn")
        for i in range(9, _number_pages+1):
            self.download_url = download_url + str(i) + ".html"
            filename, download_html = d._curl(self.download_url)
            _log("[+] Mass downloading from %s" % unquote(self.download_url))
            found = re.findall('</a> <a href="/apps/-(.*?).html#divVedio"', download_html, re.DOTALL)
            for _ipa_link in found:
                _ipa_referer = "http://ios.d.cn/apps/-" + _ipa_link + ".html"
                _log("[+] Downloading from %s" % _ipa_referer)
                filename, download_html = d._curl(_ipa_referer)
                found_direct = re.findall('chl=http://ios.d.cn/s-(.*?)&size=3"', download_html, re.DOTALL)
                _download_link = "http://ios.d.cn/apps/download-" + found_direct[0] + "-web.html?js"
                d._download_dcn_ipa(_download_link, _ipa_referer, "")
        os.chdir('../../../')
        
import os, sys, re, time, json, urllib, urllib2
import xml.dom.minidom

from Bushido.common.out import _log
from Bushido.core.dcn import dcn

#-----------------------------------------------------
# List of supported 3rd Party Unofficial iOS AppStore
#-----------------------------------------------------
MarketList = ["ios.d.cn"]
'''
http://ios.d.cn/apps/iphone-soft-------new-.html
http://ios.d.cn/apps/iphone-games-------new-.html
http://app.91.com/soft/
http://app.91.com/game/
http://www.app111.com/home/101024001/
'''
def main(market):
    if market=="ios.d.cn":
        _log("[+] Downloading from %s in progress" % market)
        d = dcn()
        d._download('http://ios.d.cn/apps/iphone-soft-------new-.html', 'http://ios.d.cn/apps/iphone-soft-------new-list-')
        d._download('http://ios.d.cn/apps/iphone-games-------new-.html', 'http://ios.d.cn/apps/iphone-games-------new-list-')
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        _log("[+] Usage: %s [marketplace]" % sys.argv[0])
        _log("[+] Some of the unofficial iOS AppStore:")
        for market in MarketList:
            _log("    %s" % market)
        sys.exit(0)
    else:
        market = sys.argv[1]
        main(market)
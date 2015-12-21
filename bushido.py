import os, sys, re, time, json, urllib, urllib2
import xml.dom.minidom

from Bushido.common.out import _log
from Bushido.core.dcn import dcn
from Bushido.core.liqucn import liqucn

#-----------------------------------------------------
# List of supported 3rd Party Unofficial iOS AppStore
#-----------------------------------------------------
MarketList = ["ios.d.cn","liqucn.com"]

def main(market):
    if market=="ios.d.cn":
        _log("[+] Downloading from %s in progress" % market)
        d = dcn()
        d._download('http://ios.d.cn/apps/iphone-soft-------new-.html', 'http://ios.d.cn/apps/iphone-soft-------new-list-')
        d._download('http://ios.d.cn/apps/iphone-games-------new-.html', 'http://ios.d.cn/apps/iphone-games-------new-list-')
    if market=="liqucn.com":
        _log("[+] Downloading from %s in progress" % market)
        d = liqucn()
        d._download('http://os-ios.liqucn.com/rj/', 'http://os-ios.liqucn.com/rj/index_')
        d._download('http://os-ios.liqucn.com/yx/', 'http://os-ios.liqucn.com/yx/index_')
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
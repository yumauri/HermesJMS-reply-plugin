###
# @author Victor Didenko
# yumaa.verdin@gmail.com
# 05.12.2014
#

import reply_plugin
from hermes.browser import HermesBrowser

# create reply plugin
reply_plugin.plugin.ReplyPlugin(HermesBrowser.getBrowser(), reply_plugin.__file__)

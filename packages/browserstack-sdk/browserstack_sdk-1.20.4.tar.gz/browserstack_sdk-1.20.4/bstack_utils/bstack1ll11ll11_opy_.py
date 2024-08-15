# coding: UTF-8
import sys
bstack111111l_opy_ = sys.version_info [0] == 2
bstack11l1l1_opy_ = 2048
bstack1lll1l_opy_ = 7
def bstack1l11ll_opy_ (bstack1lllll1_opy_):
    global bstack1l11111_opy_
    bstack111l1l_opy_ = ord (bstack1lllll1_opy_ [-1])
    bstack111l1ll_opy_ = bstack1lllll1_opy_ [:-1]
    bstack1ll11l1_opy_ = bstack111l1l_opy_ % len (bstack111l1ll_opy_)
    bstack11l1111_opy_ = bstack111l1ll_opy_ [:bstack1ll11l1_opy_] + bstack111l1ll_opy_ [bstack1ll11l1_opy_:]
    if bstack111111l_opy_:
        bstack1ll1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1_opy_ - (bstack111l111_opy_ + bstack111l1l_opy_) % bstack1lll1l_opy_) for bstack111l111_opy_, char in enumerate (bstack11l1111_opy_)])
    else:
        bstack1ll1l11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1_opy_ - (bstack111l111_opy_ + bstack111l1l_opy_) % bstack1lll1l_opy_) for bstack111l111_opy_, char in enumerate (bstack11l1111_opy_)])
    return eval (bstack1ll1l11_opy_)
class bstack1llllll11_opy_:
    def __init__(self, handler):
        self._1lll1l11l1l_opy_ = None
        self.handler = handler
        self._1lll1l11ll1_opy_ = self.bstack1lll1l11lll_opy_()
        self.patch()
    def patch(self):
        self._1lll1l11l1l_opy_ = self._1lll1l11ll1_opy_.execute
        self._1lll1l11ll1_opy_.execute = self.bstack1lll1l1l111_opy_()
    def bstack1lll1l1l111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᔢ"), driver_command, None, this, args)
            response = self._1lll1l11l1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11ll_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨᔣ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1l11ll1_opy_.execute = self._1lll1l11l1l_opy_
    @staticmethod
    def bstack1lll1l11lll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
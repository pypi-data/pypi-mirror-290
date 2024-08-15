# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11111l_opy_ = 2048
bstack1lll11_opy_ = 7
def bstack1l11ll1_opy_ (bstack11l1l1_opy_):
    global bstack1l1llll_opy_
    bstack1l11111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1111lll_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11ll1_opy_ = bstack1l11111_opy_ % len (bstack1111lll_opy_)
    bstack11l111l_opy_ = bstack1111lll_opy_ [:bstack11ll1_opy_] + bstack1111lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll_opy_:
        bstack1l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l_opy_ - (bstack1ll11ll_opy_ + bstack1l11111_opy_) % bstack1lll11_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack1l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l_opy_ - (bstack1ll11ll_opy_ + bstack1l11111_opy_) % bstack1lll11_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack1l1111_opy_)
class bstack1lllll111l_opy_:
    def __init__(self, handler):
        self._1lll1l1l111_opy_ = None
        self.handler = handler
        self._1lll1l11lll_opy_ = self.bstack1lll1l11ll1_opy_()
        self.patch()
    def patch(self):
        self._1lll1l1l111_opy_ = self._1lll1l11lll_opy_.execute
        self._1lll1l11lll_opy_.execute = self.bstack1lll1l11l1l_opy_()
    def bstack1lll1l11l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11ll1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᔢ"), driver_command, None, this, args)
            response = self._1lll1l1l111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11ll1_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨᔣ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1l11lll_opy_.execute = self._1lll1l1l111_opy_
    @staticmethod
    def bstack1lll1l11ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
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
from collections import deque
from bstack_utils.constants import *
class bstack1ll1111l11_opy_:
    def __init__(self):
        self._1llll11ll11_opy_ = deque()
        self._1llll1l1111_opy_ = {}
        self._1llll11l1ll_opy_ = False
    def bstack1llll11ll1l_opy_(self, test_name, bstack1llll1l1ll1_opy_):
        bstack1llll11lll1_opy_ = self._1llll1l1111_opy_.get(test_name, {})
        return bstack1llll11lll1_opy_.get(bstack1llll1l1ll1_opy_, 0)
    def bstack1llll1l1l1l_opy_(self, test_name, bstack1llll1l1ll1_opy_):
        bstack1llll11llll_opy_ = self.bstack1llll11ll1l_opy_(test_name, bstack1llll1l1ll1_opy_)
        self.bstack1llll1l1lll_opy_(test_name, bstack1llll1l1ll1_opy_)
        return bstack1llll11llll_opy_
    def bstack1llll1l1lll_opy_(self, test_name, bstack1llll1l1ll1_opy_):
        if test_name not in self._1llll1l1111_opy_:
            self._1llll1l1111_opy_[test_name] = {}
        bstack1llll11lll1_opy_ = self._1llll1l1111_opy_[test_name]
        bstack1llll11llll_opy_ = bstack1llll11lll1_opy_.get(bstack1llll1l1ll1_opy_, 0)
        bstack1llll11lll1_opy_[bstack1llll1l1ll1_opy_] = bstack1llll11llll_opy_ + 1
    def bstack1ll1ll11l_opy_(self, bstack1llll1l1l11_opy_, bstack1llll1l111l_opy_):
        bstack1llll1ll111_opy_ = self.bstack1llll1l1l1l_opy_(bstack1llll1l1l11_opy_, bstack1llll1l111l_opy_)
        bstack1llll11l1l1_opy_ = bstack11l1111l1l_opy_[bstack1llll1l111l_opy_]
        bstack1llll1l11l1_opy_ = bstack1l11ll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤᓈ").format(bstack1llll1l1l11_opy_, bstack1llll11l1l1_opy_, bstack1llll1ll111_opy_)
        self._1llll11ll11_opy_.append(bstack1llll1l11l1_opy_)
    def bstack1l1l1l11l1_opy_(self):
        return len(self._1llll11ll11_opy_) == 0
    def bstack11llllll1_opy_(self):
        bstack1llll1l11ll_opy_ = self._1llll11ll11_opy_.popleft()
        return bstack1llll1l11ll_opy_
    def capturing(self):
        return self._1llll11l1ll_opy_
    def bstack111l1l1l1_opy_(self):
        self._1llll11l1ll_opy_ = True
    def bstack11l111ll_opy_(self):
        self._1llll11l1ll_opy_ = False
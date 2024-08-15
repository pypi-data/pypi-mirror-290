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
import sys
class bstack1l111l11ll_opy_:
    def __init__(self, handler):
        self._11l11l1lll_opy_ = sys.stdout.write
        self._11l11l1l1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l11l1ll1_opy_
        sys.stdout.error = self.bstack11l11ll111_opy_
    def bstack11l11l1ll1_opy_(self, _str):
        self._11l11l1lll_opy_(_str)
        if self.handler:
            self.handler({bstack1l11ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ༢"): bstack1l11ll1_opy_ (u"ࠫࡎࡔࡆࡐࠩ༣"), bstack1l11ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༤"): _str})
    def bstack11l11ll111_opy_(self, _str):
        self._11l11l1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack1l11ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༥"): bstack1l11ll1_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭༦"), bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༧"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l11l1lll_opy_
        sys.stderr.write = self._11l11l1l1l_opy_
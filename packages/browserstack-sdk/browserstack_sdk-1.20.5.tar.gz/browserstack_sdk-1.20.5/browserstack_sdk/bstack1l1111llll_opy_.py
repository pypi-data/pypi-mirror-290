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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11ll111lll_opy_, bstack11ll111l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll111lll_opy_ = bstack11ll111lll_opy_
        self.bstack11ll111l1l_opy_ = bstack11ll111l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11llll1l11_opy_(bstack11ll111111_opy_):
        bstack11ll11111l_opy_ = []
        if bstack11ll111111_opy_:
            tokens = str(os.path.basename(bstack11ll111111_opy_)).split(bstack1l11ll1_opy_ (u"ࠤࡢࠦ๝"))
            camelcase_name = bstack1l11ll1_opy_ (u"ࠥࠤࠧ๞").join(t.title() for t in tokens)
            suite_name, bstack11l1llllll_opy_ = os.path.splitext(camelcase_name)
            bstack11ll11111l_opy_.append(suite_name)
        return bstack11ll11111l_opy_
    @staticmethod
    def bstack11ll1111l1_opy_(typename):
        if bstack1l11ll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ๟") in typename:
            return bstack1l11ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ๠")
        return bstack1l11ll1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ๡")
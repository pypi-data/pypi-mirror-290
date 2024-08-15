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
from browserstack_sdk.bstack1lll1ll1l1_opy_ import bstack111111l11_opy_
from browserstack_sdk.bstack1l1111llll_opy_ import RobotHandler
def bstack11llll111_opy_(framework):
    if framework.lower() == bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᇻ"):
        return bstack111111l11_opy_.version()
    elif framework.lower() == bstack1l11ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᇼ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᇽ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11ll1_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᇾ")
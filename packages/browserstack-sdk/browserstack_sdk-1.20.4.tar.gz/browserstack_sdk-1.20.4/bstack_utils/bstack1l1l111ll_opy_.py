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
from browserstack_sdk.bstack1l11l11l11_opy_ import bstack111l11111_opy_
from browserstack_sdk.bstack11ll1ll111_opy_ import RobotHandler
def bstack1ll11lll_opy_(framework):
    if framework.lower() == bstack1l11ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᇻ"):
        return bstack111l11111_opy_.version()
    elif framework.lower() == bstack1l11ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᇼ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᇽ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11ll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᇾ")
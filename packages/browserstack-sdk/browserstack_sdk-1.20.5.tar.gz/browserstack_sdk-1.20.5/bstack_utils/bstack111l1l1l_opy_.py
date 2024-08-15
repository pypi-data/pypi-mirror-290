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
import logging
import os
import threading
from bstack_utils.helper import bstack111ll11ll_opy_
from bstack_utils.constants import bstack11l111l11l_opy_
logger = logging.getLogger(__name__)
class bstack1l11ll11ll_opy_:
    bstack1lll1ll1l11_opy_ = None
    @classmethod
    def bstack1lll1l1l1_opy_(cls):
        if cls.on():
            print(
                bstack1l11ll1_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩᚸ").format(os.environ[bstack1l11ll1_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᚹ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᚺ"), None) is None or os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᚻ")] == bstack1l11ll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᚼ"):
            return False
        return True
    @classmethod
    def bstack1ll1ll1ll1l_opy_(cls, bs_config, framework=bstack1l11ll1_opy_ (u"ࠦࠧᚽ")):
        bstack1ll1ll11111_opy_ = framework in bstack11l111l11l_opy_
        return bstack111ll11ll_opy_(bs_config.get(bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᚾ"), bstack1ll1ll11111_opy_))
    @classmethod
    def bstack1ll1ll111ll_opy_(cls, framework):
        return framework in bstack11l111l11l_opy_
    @classmethod
    def bstack1ll1lll11ll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1ll1ll1l_opy_(bs_config, framework) is True and cls.bstack1ll1ll111ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᚿ"), None)
    @staticmethod
    def bstack11llll1lll_opy_():
        if getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᛀ"), None):
            return {
                bstack1l11ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᛁ"): bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࠧᛂ"),
                bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᛃ"): getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᛄ"), None)
            }
        if getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᛅ"), None):
            return {
                bstack1l11ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫᛆ"): bstack1l11ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᛇ"),
                bstack1l11ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᛈ"): getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᛉ"), None)
            }
        return None
    @staticmethod
    def bstack1ll1l1llll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11ll11ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11llll1l11_opy_(test, hook_name=None):
        bstack1ll1l1lllll_opy_ = test.parent
        if hook_name in [bstack1l11ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᛊ"), bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᛋ"), bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᛌ"), bstack1l11ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᛍ")]:
            bstack1ll1l1lllll_opy_ = test
        scope = []
        while bstack1ll1l1lllll_opy_ is not None:
            scope.append(bstack1ll1l1lllll_opy_.name)
            bstack1ll1l1lllll_opy_ = bstack1ll1l1lllll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1ll1111l_opy_(hook_type):
        if hook_type == bstack1l11ll1_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧᛎ"):
            return bstack1l11ll1_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧᛏ")
        elif hook_type == bstack1l11ll1_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨᛐ"):
            return bstack1l11ll1_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥᛑ")
    @staticmethod
    def bstack1ll1ll111l1_opy_(bstack1l11l11ll1_opy_):
        try:
            if not bstack1l11ll11ll_opy_.on():
                return bstack1l11l11ll1_opy_
            if os.environ.get(bstack1l11ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤᛒ"), None) == bstack1l11ll1_opy_ (u"ࠧࡺࡲࡶࡧࠥᛓ"):
                tests = os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥᛔ"), None)
                if tests is None or tests == bstack1l11ll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᛕ"):
                    return bstack1l11l11ll1_opy_
                bstack1l11l11ll1_opy_ = tests.split(bstack1l11ll1_opy_ (u"ࠨ࠮ࠪᛖ"))
                return bstack1l11l11ll1_opy_
        except Exception as exc:
            print(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥᛗ"), str(exc))
        return bstack1l11l11ll1_opy_
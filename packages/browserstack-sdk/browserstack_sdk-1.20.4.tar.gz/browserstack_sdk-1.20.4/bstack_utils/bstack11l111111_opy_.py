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
import logging
import os
import threading
from bstack_utils.helper import bstack1llll11lll_opy_
from bstack_utils.constants import bstack11l111l111_opy_
logger = logging.getLogger(__name__)
class bstack1lll1lll11_opy_:
    bstack1lll1ll1l11_opy_ = None
    @classmethod
    def bstack1l1lllll1l_opy_(cls):
        if cls.on():
            print(
                bstack1l11ll_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫᚺ").format(os.environ[bstack1l11ll_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣᚻ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l11ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᚼ"), None) is None or os.environ[bstack1l11ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᚽ")] == bstack1l11ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᚾ"):
            return False
        return True
    @classmethod
    def bstack1ll1ll1l1l1_opy_(cls, bs_config, framework=bstack1l11ll_opy_ (u"ࠨࠢᚿ")):
        bstack1ll1ll111l1_opy_ = framework in bstack11l111l111_opy_
        return bstack1llll11lll_opy_(bs_config.get(bstack1l11ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᛀ"), bstack1ll1ll111l1_opy_))
    @classmethod
    def bstack1ll1ll11111_opy_(cls, framework):
        return framework in bstack11l111l111_opy_
    @classmethod
    def bstack1lll111l111_opy_(cls, bs_config, framework):
        return cls.bstack1ll1ll1l1l1_opy_(bs_config, framework) is True and cls.bstack1ll1ll11111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᛁ"), None)
    @staticmethod
    def bstack1l1111l1ll_opy_():
        if getattr(threading.current_thread(), bstack1l11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᛂ"), None):
            return {
                bstack1l11ll_opy_ (u"ࠪࡸࡾࡶࡥࠨᛃ"): bstack1l11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᛄ"),
                bstack1l11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᛅ"): getattr(threading.current_thread(), bstack1l11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᛆ"), None)
            }
        if getattr(threading.current_thread(), bstack1l11ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᛇ"), None):
            return {
                bstack1l11ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᛈ"): bstack1l11ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᛉ"),
                bstack1l11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᛊ"): getattr(threading.current_thread(), bstack1l11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᛋ"), None)
            }
        return None
    @staticmethod
    def bstack1ll1ll111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1lll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11llllll1l_opy_(test, hook_name=None):
        bstack1ll1l1lllll_opy_ = test.parent
        if hook_name in [bstack1l11ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᛌ"), bstack1l11ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᛍ"), bstack1l11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᛎ"), bstack1l11ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᛏ")]:
            bstack1ll1l1lllll_opy_ = test
        scope = []
        while bstack1ll1l1lllll_opy_ is not None:
            scope.append(bstack1ll1l1lllll_opy_.name)
            bstack1ll1l1lllll_opy_ = bstack1ll1l1lllll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1ll1111l_opy_(hook_type):
        if hook_type == bstack1l11ll_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᛐ"):
            return bstack1l11ll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᛑ")
        elif hook_type == bstack1l11ll_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᛒ"):
            return bstack1l11ll_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᛓ")
    @staticmethod
    def bstack1ll1l1llll1_opy_(bstack1l11ll11l_opy_):
        try:
            if not bstack1lll1lll11_opy_.on():
                return bstack1l11ll11l_opy_
            if os.environ.get(bstack1l11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᛔ"), None) == bstack1l11ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᛕ"):
                tests = os.environ.get(bstack1l11ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᛖ"), None)
                if tests is None or tests == bstack1l11ll_opy_ (u"ࠤࡱࡹࡱࡲࠢᛗ"):
                    return bstack1l11ll11l_opy_
                bstack1l11ll11l_opy_ = tests.split(bstack1l11ll_opy_ (u"ࠪ࠰ࠬᛘ"))
                return bstack1l11ll11l_opy_
        except Exception as exc:
            print(bstack1l11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᛙ"), str(exc))
        return bstack1l11ll11l_opy_
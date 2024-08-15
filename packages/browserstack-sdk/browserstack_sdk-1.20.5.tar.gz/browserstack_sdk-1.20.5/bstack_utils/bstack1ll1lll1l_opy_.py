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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111l11lll1_opy_, bstack1l1l111ll_opy_, bstack1l1ll1111_opy_, bstack1llll111_opy_, \
    bstack111l11l1l1_opy_
def bstack11l1l111_opy_(bstack1lll1l11l11_opy_):
    for driver in bstack1lll1l11l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1llll11_opy_(driver, status, reason=bstack1l11ll1_opy_ (u"ࠨࠩᔤ")):
    bstack11l1lll1l_opy_ = Config.bstack1ll1l11l1_opy_()
    if bstack11l1lll1l_opy_.bstack11ll11l111_opy_():
        return
    bstack11l11lll_opy_ = bstack11l111lll_opy_(bstack1l11ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᔥ"), bstack1l11ll1_opy_ (u"ࠪࠫᔦ"), status, reason, bstack1l11ll1_opy_ (u"ࠫࠬᔧ"), bstack1l11ll1_opy_ (u"ࠬ࠭ᔨ"))
    driver.execute_script(bstack11l11lll_opy_)
def bstack1lll1lll_opy_(page, status, reason=bstack1l11ll1_opy_ (u"࠭ࠧᔩ")):
    try:
        if page is None:
            return
        bstack11l1lll1l_opy_ = Config.bstack1ll1l11l1_opy_()
        if bstack11l1lll1l_opy_.bstack11ll11l111_opy_():
            return
        bstack11l11lll_opy_ = bstack11l111lll_opy_(bstack1l11ll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᔪ"), bstack1l11ll1_opy_ (u"ࠨࠩᔫ"), status, reason, bstack1l11ll1_opy_ (u"ࠩࠪᔬ"), bstack1l11ll1_opy_ (u"ࠪࠫᔭ"))
        page.evaluate(bstack1l11ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᔮ"), bstack11l11lll_opy_)
    except Exception as e:
        print(bstack1l11ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᔯ"), e)
def bstack11l111lll_opy_(type, name, status, reason, bstack1ll11ll1l_opy_, bstack1l11lllll1_opy_):
    bstack1lllllll1_opy_ = {
        bstack1l11ll1_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ᔰ"): type,
        bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᔱ"): {}
    }
    if type == bstack1l11ll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᔲ"):
        bstack1lllllll1_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᔳ")][bstack1l11ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᔴ")] = bstack1ll11ll1l_opy_
        bstack1lllllll1_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᔵ")][bstack1l11ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪᔶ")] = json.dumps(str(bstack1l11lllll1_opy_))
    if type == bstack1l11ll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᔷ"):
        bstack1lllllll1_opy_[bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᔸ")][bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᔹ")] = name
    if type == bstack1l11ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᔺ"):
        bstack1lllllll1_opy_[bstack1l11ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᔻ")][bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᔼ")] = status
        if status == bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᔽ") and str(reason) != bstack1l11ll1_opy_ (u"ࠨࠢᔾ"):
            bstack1lllllll1_opy_[bstack1l11ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᔿ")][bstack1l11ll1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᕀ")] = json.dumps(str(reason))
    bstack1ll1ll11l_opy_ = bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᕁ").format(json.dumps(bstack1lllllll1_opy_))
    return bstack1ll1ll11l_opy_
def bstack111ll11l_opy_(url, config, logger, bstack1llll1ll_opy_=False):
    hostname = bstack1l1l111ll_opy_(url)
    is_private = bstack1llll111_opy_(hostname)
    try:
        if is_private or bstack1llll1ll_opy_:
            file_path = bstack111l11lll1_opy_(bstack1l11ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᕂ"), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᕃ"), logger)
            if os.environ.get(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᕄ")) and eval(
                    os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᕅ"))):
                return
            if (bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᕆ") in config and not config[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᕇ")]):
                os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᕈ")] = str(True)
                bstack1lll1l1111l_opy_ = {bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬᕉ"): hostname}
                bstack111l11l1l1_opy_(bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᕊ"), bstack1l11ll1_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪᕋ"), bstack1lll1l1111l_opy_, logger)
    except Exception as e:
        pass
def bstack111ll1111_opy_(caps, bstack1lll1l111ll_opy_):
    if bstack1l11ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᕌ") in caps:
        caps[bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᕍ")][bstack1l11ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᕎ")] = True
        if bstack1lll1l111ll_opy_:
            caps[bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᕏ")][bstack1l11ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᕐ")] = bstack1lll1l111ll_opy_
    else:
        caps[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᕑ")] = True
        if bstack1lll1l111ll_opy_:
            caps[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᕒ")] = bstack1lll1l111ll_opy_
def bstack1llll111111_opy_(bstack11ll1ll1l1_opy_):
    bstack1lll1l111l1_opy_ = bstack1l1ll1111_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᕓ"), bstack1l11ll1_opy_ (u"ࠧࠨᕔ"))
    if bstack1lll1l111l1_opy_ == bstack1l11ll1_opy_ (u"ࠨࠩᕕ") or bstack1lll1l111l1_opy_ == bstack1l11ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᕖ"):
        threading.current_thread().testStatus = bstack11ll1ll1l1_opy_
    else:
        if bstack11ll1ll1l1_opy_ == bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᕗ"):
            threading.current_thread().testStatus = bstack11ll1ll1l1_opy_
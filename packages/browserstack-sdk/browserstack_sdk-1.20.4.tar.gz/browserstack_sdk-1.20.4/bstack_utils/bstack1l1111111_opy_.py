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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l1l1l11l_opy_, bstack1ll1ll1l_opy_, get_host_info, bstack1111ll1l11_opy_, \
 bstack1111lllll_opy_, bstack1l1l1l1ll_opy_, bstack1l11111111_opy_, bstack111l1ll1ll_opy_
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11ll11_opy_
from bstack_utils.bstack11l111111_opy_ import bstack1lll1lll11_opy_
from bstack_utils.percy import bstack1llll1l1l_opy_
from bstack_utils.config import Config
bstack1ll1l111l1_opy_ = Config.bstack1l1ll11l1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack1llll1l1l_opy_()
@bstack1l11111111_opy_(class_method=False)
def bstack1lll111l11l_opy_(bs_config, bstack1l1ll1l1l1_opy_):
  try:
    data = {
        bstack1l11ll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᙿ"): bstack1l11ll_opy_ (u"࠭ࡪࡴࡱࡱࠫ "),
        bstack1l11ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᚁ"): bs_config.get(bstack1l11ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᚂ"), bstack1l11ll_opy_ (u"ࠩࠪᚃ")),
        bstack1l11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᚄ"): bs_config.get(bstack1l11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᚅ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᚆ"): bs_config.get(bstack1l11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᚇ")),
        bstack1l11ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᚈ"): bs_config.get(bstack1l11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᚉ"), bstack1l11ll_opy_ (u"ࠩࠪᚊ")),
        bstack1l11ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚋ"): datetime.datetime.now().isoformat() + bstack1l11ll_opy_ (u"ࠫ࡟࠭ᚌ"),
        bstack1l11ll_opy_ (u"ࠬࡺࡡࡨࡵࠪᚍ"): bstack1111ll1l11_opy_(bs_config),
        bstack1l11ll_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩᚎ"): get_host_info(),
        bstack1l11ll_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨᚏ"): bstack1ll1ll1l_opy_(),
        bstack1l11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᚐ"): os.environ.get(bstack1l11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᚑ")),
        bstack1l11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨᚒ"): os.environ.get(bstack1l11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩᚓ"), False),
        bstack1l11ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧᚔ"): bstack11l1l1l11l_opy_(),
        bstack1l11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚕ"): bstack1ll1ll1l11l_opy_(),
        bstack1l11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫᚖ"): bstack1ll1ll1ll1l_opy_(bstack1l1ll1l1l1_opy_),
        bstack1l11ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᚗ"): bstack1l1l1lll11_opy_(bs_config, bstack1l1ll1l1l1_opy_),
        bstack1l11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᚘ"): bstack1111lllll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l11ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦᚙ").format(str(error)))
    return None
def bstack1ll1ll1ll1l_opy_(framework):
  return {
    bstack1l11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᚚ"): framework.get(bstack1l11ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭᚛"), bstack1l11ll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭᚜")),
    bstack1l11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ᚝"): framework.get(bstack1l11ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᚞")),
    bstack1l11ll_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᚟"): framework.get(bstack1l11ll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᚠ")),
    bstack1l11ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᚡ"): bstack1l11ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᚢ"),
    bstack1l11ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᚣ"): framework.get(bstack1l11ll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᚤ"))
  }
def bstack1l1l1lll11_opy_(bs_config, framework):
  bstack11ll1ll11_opy_ = False
  bstack1ll1l1ll1l_opy_ = False
  if bstack1l11ll_opy_ (u"ࠨࡣࡳࡴࠬᚥ") in bs_config:
    bstack11ll1ll11_opy_ = True
  else:
    bstack1ll1l1ll1l_opy_ = True
  bstack1l111lll1l_opy_ = {
    bstack1l11ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᚦ"): bstack1lll1lll11_opy_.bstack1ll1ll1l1l1_opy_(bs_config, framework),
    bstack1l11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚧ"): bstack1l11ll11_opy_.bstack11l1l1l1ll_opy_(bs_config),
    bstack1l11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᚨ"): bs_config.get(bstack1l11ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᚩ"), False),
    bstack1l11ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᚪ"): bstack1ll1l1ll1l_opy_,
    bstack1l11ll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᚫ"): bstack11ll1ll11_opy_
  }
  return bstack1l111lll1l_opy_
@bstack1l11111111_opy_(class_method=False)
def bstack1ll1ll1l11l_opy_():
  try:
    bstack1ll1ll1ll11_opy_ = json.loads(os.getenv(bstack1l11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᚬ"), bstack1l11ll_opy_ (u"ࠩࡾࢁࠬᚭ")))
    return {
        bstack1l11ll_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬᚮ"): bstack1ll1ll1ll11_opy_
    }
  except Exception as error:
    logger.error(bstack1l11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥᚯ").format(str(error)))
    return {}
def bstack1ll1lll111l_opy_(array, bstack1ll1ll11ll1_opy_, bstack1ll1ll11l11_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1ll11ll1_opy_]
    result[key] = o[bstack1ll1ll11l11_opy_]
  return result
def bstack1ll1lllllll_opy_(bstack1ll11111ll_opy_=bstack1l11ll_opy_ (u"ࠬ࠭ᚰ")):
  bstack1ll1ll11l1l_opy_ = bstack1l11ll11_opy_.on()
  bstack1ll1ll11lll_opy_ = bstack1lll1lll11_opy_.on()
  bstack1ll1ll1l1ll_opy_ = percy.bstack111111l11l_opy_()
  if bstack1ll1ll1l1ll_opy_ and not bstack1ll1ll11lll_opy_ and not bstack1ll1ll11l1l_opy_:
    return bstack1ll11111ll_opy_ not in [bstack1l11ll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᚱ"), bstack1l11ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᚲ")]
  elif bstack1ll1ll11l1l_opy_ and not bstack1ll1ll11lll_opy_:
    return bstack1ll11111ll_opy_ not in [bstack1l11ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᚳ"), bstack1l11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚴ"), bstack1l11ll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᚵ")]
  return bstack1ll1ll11l1l_opy_ or bstack1ll1ll11lll_opy_ or bstack1ll1ll1l1ll_opy_
@bstack1l11111111_opy_(class_method=False)
def bstack1ll1lll1111_opy_(bstack1ll11111ll_opy_, test=None):
  bstack1ll1ll1l111_opy_ = bstack1l11ll11_opy_.on()
  if not bstack1ll1ll1l111_opy_ or bstack1ll11111ll_opy_ not in [bstack1l11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᚶ")] or test == None:
    return None
  return {
    bstack1l11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚷ"): bstack1ll1ll1l111_opy_ and bstack1l1l1l1ll_opy_(threading.current_thread(), bstack1l11ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᚸ"), None) == True and bstack1l11ll11_opy_.bstack1l1lll1111_opy_(test[bstack1l11ll_opy_ (u"ࠧࡵࡣࡪࡷࠬᚹ")])
  }
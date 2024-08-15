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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l1l11lll_opy_, bstack1ll1ll11l1_opy_, get_host_info, bstack111ll1ll11_opy_, \
 bstack1llllllll_opy_, bstack1l1ll1111_opy_, bstack11llll11l1_opy_, bstack111llll11l_opy_
import bstack_utils.bstack1l1lll1l11_opy_ as bstack1l1l1l11l1_opy_
from bstack_utils.bstack111l1l1l_opy_ import bstack1l11ll11ll_opy_
from bstack_utils.percy import bstack1l111ll1l1_opy_
from bstack_utils.config import Config
bstack11l1lll1l_opy_ = Config.bstack1ll1l11l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l111ll1l1_opy_()
@bstack11llll11l1_opy_(class_method=False)
def bstack1lll111l1l1_opy_(bs_config, bstack1llll1ll1l_opy_):
  try:
    data = {
        bstack1l11ll1_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪᙽ"): bstack1l11ll1_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩᙾ"),
        bstack1l11ll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫᙿ"): bs_config.get(bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ "), bstack1l11ll1_opy_ (u"ࠧࠨᚁ")),
        bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚂ"): bs_config.get(bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᚃ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᚄ"): bs_config.get(bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᚅ")),
        bstack1l11ll1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᚆ"): bs_config.get(bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᚇ"), bstack1l11ll1_opy_ (u"ࠧࠨᚈ")),
        bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᚉ"): datetime.datetime.now().isoformat() + bstack1l11ll1_opy_ (u"ࠩ࡝ࠫᚊ"),
        bstack1l11ll1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᚋ"): bstack111ll1ll11_opy_(bs_config),
        bstack1l11ll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᚌ"): get_host_info(),
        bstack1l11ll1_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᚍ"): bstack1ll1ll11l1_opy_(),
        bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᚎ"): os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᚏ")),
        bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ᚐ"): os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᚑ"), False),
        bstack1l11ll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬᚒ"): bstack11l1l11lll_opy_(),
        bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚓ"): bstack1ll1ll11lll_opy_(),
        bstack1l11ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩᚔ"): bstack1ll1ll1l11l_opy_(bstack1llll1ll1l_opy_),
        bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᚕ"): bstack1l11l1l11_opy_(bs_config, bstack1llll1ll1l_opy_),
        bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᚖ"): bstack1llllllll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l11ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤᚗ").format(str(error)))
    return None
def bstack1ll1ll1l11l_opy_(framework):
  return {
    bstack1l11ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᚘ"): framework.get(bstack1l11ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫᚙ"), bstack1l11ll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᚚ")),
    bstack1l11ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᚛"): framework.get(bstack1l11ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᚜")),
    bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ᚝"): framework.get(bstack1l11ll1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᚞")),
    bstack1l11ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ᚟"): bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᚠ"),
    bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᚡ"): framework.get(bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᚢ"))
  }
def bstack1l11l1l11_opy_(bs_config, framework):
  bstack1lll1ll111_opy_ = False
  bstack1l11l1111_opy_ = False
  if bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲࠪᚣ") in bs_config:
    bstack1lll1ll111_opy_ = True
  else:
    bstack1l11l1111_opy_ = True
  bstack1111l1l11_opy_ = {
    bstack1l11ll1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚤ"): bstack1l11ll11ll_opy_.bstack1ll1ll1ll1l_opy_(bs_config, framework),
    bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚥ"): bstack1l1l1l11l1_opy_.bstack11l1l11ll1_opy_(bs_config),
    bstack1l11ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᚦ"): bs_config.get(bstack1l11ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᚧ"), False),
    bstack1l11ll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᚨ"): bstack1l11l1111_opy_,
    bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᚩ"): bstack1lll1ll111_opy_
  }
  return bstack1111l1l11_opy_
@bstack11llll11l1_opy_(class_method=False)
def bstack1ll1ll11lll_opy_():
  try:
    bstack1ll1ll11l11_opy_ = json.loads(os.getenv(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᚪ"), bstack1l11ll1_opy_ (u"ࠧࡼࡿࠪᚫ")))
    return {
        bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪᚬ"): bstack1ll1ll11l11_opy_
    }
  except Exception as error:
    logger.error(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣᚭ").format(str(error)))
    return {}
def bstack1ll1lll1111_opy_(array, bstack1ll1ll1l1ll_opy_, bstack1ll1ll11ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1ll1l1ll_opy_]
    result[key] = o[bstack1ll1ll11ll1_opy_]
  return result
def bstack1ll1lll1lll_opy_(bstack11l11ll1_opy_=bstack1l11ll1_opy_ (u"ࠪࠫᚮ")):
  bstack1ll1ll1l111_opy_ = bstack1l1l1l11l1_opy_.on()
  bstack1ll1ll1ll11_opy_ = bstack1l11ll11ll_opy_.on()
  bstack1ll1ll11l1l_opy_ = percy.bstack1llllll1111_opy_()
  if bstack1ll1ll11l1l_opy_ and not bstack1ll1ll1ll11_opy_ and not bstack1ll1ll1l111_opy_:
    return bstack11l11ll1_opy_ not in [bstack1l11ll1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᚯ"), bstack1l11ll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᚰ")]
  elif bstack1ll1ll1l111_opy_ and not bstack1ll1ll1ll11_opy_:
    return bstack11l11ll1_opy_ not in [bstack1l11ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᚱ"), bstack1l11ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᚲ"), bstack1l11ll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᚳ")]
  return bstack1ll1ll1l111_opy_ or bstack1ll1ll1ll11_opy_ or bstack1ll1ll11l1l_opy_
@bstack11llll11l1_opy_(class_method=False)
def bstack1lll11111l1_opy_(bstack11l11ll1_opy_, test=None):
  bstack1ll1ll1l1l1_opy_ = bstack1l1l1l11l1_opy_.on()
  if not bstack1ll1ll1l1l1_opy_ or bstack11l11ll1_opy_ not in [bstack1l11ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚴ")] or test == None:
    return None
  return {
    bstack1l11ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚵ"): bstack1ll1ll1l1l1_opy_ and bstack1l1ll1111_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᚶ"), None) == True and bstack1l1l1l11l1_opy_.bstack1lllll1lll_opy_(test[bstack1l11ll1_opy_ (u"ࠬࡺࡡࡨࡵࠪᚷ")])
  }
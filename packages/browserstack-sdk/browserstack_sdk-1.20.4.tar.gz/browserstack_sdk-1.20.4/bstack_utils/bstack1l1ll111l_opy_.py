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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l1l111l1_opy_, bstack11l1l1lll1_opy_, bstack1lll11ll1_opy_, bstack1l11111111_opy_, bstack111l1l1l1l_opy_, bstack1111ll11l1_opy_, bstack111l1ll1ll_opy_
from bstack_utils.bstack1lll1ll1l11_opy_ import bstack1lll1l1l11l_opy_
import bstack_utils.bstack1l1111111_opy_ as bstack1lll1l1ll1_opy_
from bstack_utils.bstack11l111111_opy_ import bstack1lll1lll11_opy_
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11ll11_opy_
from bstack_utils.bstack111l1111l_opy_ import bstack111l1111l_opy_
from bstack_utils.bstack1l111111l1_opy_ import bstack11lll1lll1_opy_
bstack1ll1llll1l1_opy_ = bstack1l11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᖖ")
logger = logging.getLogger(__name__)
class bstack1ll1llllll_opy_:
    bstack1lll1ll1l11_opy_ = None
    bs_config = None
    bstack1l1ll1l1l1_opy_ = None
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l1ll1l1l1_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1ll1l1l1_opy_ = bstack1l1ll1l1l1_opy_
        try:
            cls.bstack1ll1llllll1_opy_()
            bstack11l1l111ll_opy_ = bstack11l1l111l1_opy_(bs_config)
            bstack11l1lll11l_opy_ = bstack11l1l1lll1_opy_(bs_config)
            data = bstack1lll1l1ll1_opy_.bstack1lll111l11l_opy_(bs_config, bstack1l1ll1l1l1_opy_)
            config = {
                bstack1l11ll_opy_ (u"ࠫࡦࡻࡴࡩࠩᖗ"): (bstack11l1l111ll_opy_, bstack11l1lll11l_opy_),
                bstack1l11ll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᖘ"): cls.default_headers()
            }
            response = bstack1lll11ll1_opy_(bstack1l11ll_opy_ (u"࠭ࡐࡐࡕࡗࠫᖙ"), cls.request_url(bstack1l11ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧᖚ")), data, config)
            if response.status_code != 200:
                bstack1ll1lll1lll_opy_ = response.json()
                if bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᖛ")] == False:
                    cls.bstack1lll1111111_opy_(bstack1ll1lll1lll_opy_)
                    return
                cls.bstack1lll111111l_opy_(bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᖜ")])
                cls.bstack1lll111l1l1_opy_(bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᖝ")])
                return None
            bstack1ll1lll1ll1_opy_ = cls.bstack1lll111ll1l_opy_(response)
            return bstack1ll1lll1ll1_opy_
        except Exception as error:
            logger.error(bstack1l11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤᖞ").format(str(error)))
            return None
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def stop(cls, bstack1lll1111l11_opy_=None):
        if not bstack1lll1lll11_opy_.on() and not bstack1l11ll11_opy_.on():
            return
        if os.environ.get(bstack1l11ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᖟ")) == bstack1l11ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᖠ") or os.environ.get(bstack1l11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᖡ")) == bstack1l11ll_opy_ (u"ࠣࡰࡸࡰࡱࠨᖢ"):
            logger.error(bstack1l11ll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᖣ"))
            return {
                bstack1l11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᖤ"): bstack1l11ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᖥ"),
                bstack1l11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖦ"): bstack1l11ll_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫᖧ")
            }
        try:
            cls.bstack1lll1ll1l11_opy_.shutdown()
            data = {
                bstack1l11ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᖨ"): datetime.datetime.now().isoformat() + bstack1l11ll_opy_ (u"ࠨ࡜ࠪᖩ")
            }
            if not bstack1lll1111l11_opy_ is None:
                data[bstack1l11ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭ᖪ")] = [{
                    bstack1l11ll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᖫ"): bstack1l11ll_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩᖬ"),
                    bstack1l11ll_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬᖭ"): bstack1lll1111l11_opy_
                }]
            config = {
                bstack1l11ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᖮ"): cls.default_headers()
            }
            bstack111ll1l1l1_opy_ = bstack1l11ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᖯ").format(os.environ[bstack1l11ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨᖰ")])
            bstack1ll1lll1l1l_opy_ = cls.request_url(bstack111ll1l1l1_opy_)
            response = bstack1lll11ll1_opy_(bstack1l11ll_opy_ (u"ࠩࡓ࡙࡙࠭ᖱ"), bstack1ll1lll1l1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l11ll_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᖲ"))
        except Exception as error:
            logger.error(bstack1l11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣᖳ") + str(error))
            return {
                bstack1l11ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᖴ"): bstack1l11ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᖵ"),
                bstack1l11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖶ"): str(error)
            }
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def bstack1lll111ll1l_opy_(cls, response):
        bstack1ll1lll1lll_opy_ = response.json()
        bstack1ll1lll1ll1_opy_ = {}
        if bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"ࠨ࡬ࡺࡸࠬᖷ")) is None:
            os.environ[bstack1l11ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᖸ")] = bstack1l11ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᖹ")
        else:
            os.environ[bstack1l11ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᖺ")] = bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"ࠬࡰࡷࡵࠩᖻ"), bstack1l11ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᖼ"))
        os.environ[bstack1l11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᖽ")] = bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᖾ"), bstack1l11ll_opy_ (u"ࠩࡱࡹࡱࡲࠧᖿ"))
        if bstack1lll1lll11_opy_.bstack1lll111l111_opy_(cls.bs_config, cls.bstack1l1ll1l1l1_opy_.get(bstack1l11ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᗀ"), bstack1l11ll_opy_ (u"ࠫࠬᗁ"))) is True:
            bstack1ll1llll1ll_opy_, bstack1lll11111ll_opy_, bstack1lll1111lll_opy_ = cls.bstack1lll1111ll1_opy_(bstack1ll1lll1lll_opy_)
            if bstack1ll1llll1ll_opy_ != None and bstack1lll11111ll_opy_ != None:
                bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᗂ")] = {
                    bstack1l11ll_opy_ (u"࠭ࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠩᗃ"): bstack1ll1llll1ll_opy_,
                    bstack1l11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᗄ"): bstack1lll11111ll_opy_,
                    bstack1l11ll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᗅ"): bstack1lll1111lll_opy_
                }
            else:
                bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᗆ")] = {}
        else:
            bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᗇ")] = {}
        if bstack1l11ll11_opy_.bstack11l1l1l1ll_opy_(cls.bs_config) is True:
            bstack1ll1lllll11_opy_, bstack1lll11111ll_opy_ = cls.bstack1lll1111l1l_opy_(bstack1ll1lll1lll_opy_)
            if bstack1ll1lllll11_opy_ != None and bstack1lll11111ll_opy_ != None:
                bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᗈ")] = {
                    bstack1l11ll_opy_ (u"ࠬࡧࡵࡵࡪࡢࡸࡴࡱࡥ࡯ࠩᗉ"): bstack1ll1lllll11_opy_,
                    bstack1l11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᗊ"): bstack1lll11111ll_opy_,
                }
            else:
                bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᗋ")] = {}
        else:
            bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᗌ")] = {}
        if bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᗍ")].get(bstack1l11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᗎ")) != None or bstack1ll1lll1ll1_opy_[bstack1l11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᗏ")].get(bstack1l11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᗐ")) != None:
            cls.bstack1ll1lllll1l_opy_(bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"࠭ࡪࡸࡶࠪᗑ")), bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᗒ")))
        return bstack1ll1lll1ll1_opy_
    @classmethod
    def bstack1lll1111ll1_opy_(cls, bstack1ll1lll1lll_opy_):
        if bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᗓ")) == None:
            cls.bstack1lll111111l_opy_()
            return [None, None, None]
        if bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᗔ")][bstack1l11ll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᗕ")] != True:
            cls.bstack1lll111111l_opy_(bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᗖ")])
            return [None, None, None]
        logger.debug(bstack1l11ll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩᗗ"))
        os.environ[bstack1l11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᗘ")] = bstack1l11ll_opy_ (u"ࠧࡵࡴࡸࡩࠬᗙ")
        if bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"ࠨ࡬ࡺࡸࠬᗚ")):
            os.environ[bstack1l11ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᗛ")] = bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠪ࡮ࡼࡺࠧᗜ")]
            os.environ[bstack1l11ll_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨᗝ")] = json.dumps({
                bstack1l11ll_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧᗞ"): bstack11l1l111l1_opy_(cls.bs_config),
                bstack1l11ll_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨᗟ"): bstack11l1l1lll1_opy_(cls.bs_config)
            })
        if bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᗠ")):
            os.environ[bstack1l11ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᗡ")] = bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᗢ")]
        if bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᗣ")].get(bstack1l11ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᗤ"), {}).get(bstack1l11ll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᗥ")):
            os.environ[bstack1l11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᗦ")] = str(bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᗧ")][bstack1l11ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗨ")][bstack1l11ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᗩ")])
        return [bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠪ࡮ࡼࡺࠧᗪ")], bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᗫ")], os.environ[bstack1l11ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᗬ")]]
    @classmethod
    def bstack1lll1111l1l_opy_(cls, bstack1ll1lll1lll_opy_):
        if bstack1ll1lll1lll_opy_.get(bstack1l11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᗭ")) == None:
            cls.bstack1lll111l1l1_opy_()
            return [None, None]
        if bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᗮ")][bstack1l11ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᗯ")] != True:
            cls.bstack1lll111l1l1_opy_(bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᗰ")])
            return [None, None]
        if bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗱ")].get(bstack1l11ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᗲ")):
            logger.debug(bstack1l11ll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩᗳ"))
            parsed = json.loads(os.getenv(bstack1l11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᗴ"), bstack1l11ll_opy_ (u"ࠧࡼࡿࠪᗵ")))
            capabilities = bstack1lll1l1ll1_opy_.bstack1ll1lll111l_opy_(bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᗶ")][bstack1l11ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᗷ")][bstack1l11ll_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᗸ")], bstack1l11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᗹ"), bstack1l11ll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫᗺ"))
            bstack1ll1lllll11_opy_ = capabilities[bstack1l11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫᗻ")]
            os.environ[bstack1l11ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᗼ")] = bstack1ll1lllll11_opy_
            parsed[bstack1l11ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗽ")] = capabilities[bstack1l11ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗾ")]
            os.environ[bstack1l11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᗿ")] = json.dumps(parsed)
            scripts = bstack1lll1l1ll1_opy_.bstack1ll1lll111l_opy_(bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘀ")][bstack1l11ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘁ")][bstack1l11ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᘂ")], bstack1l11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᘃ"), bstack1l11ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩᘄ"))
            bstack111l1111l_opy_.bstack11l1l1ll1l_opy_(scripts)
            commands = bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘅ")][bstack1l11ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᘆ")][bstack1l11ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬᘇ")].get(bstack1l11ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᘈ"))
            bstack111l1111l_opy_.bstack11l1l1ll11_opy_(commands)
            bstack111l1111l_opy_.store()
        return [bstack1ll1lllll11_opy_, bstack1ll1lll1lll_opy_[bstack1l11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᘉ")]]
    @classmethod
    def bstack1lll111111l_opy_(cls, response=None):
        os.environ[bstack1l11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᘊ")] = bstack1l11ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᘋ")
        os.environ[bstack1l11ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᘌ")] = bstack1l11ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᘍ")
        os.environ[bstack1l11ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᘎ")] = bstack1l11ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᘏ")
        os.environ[bstack1l11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᘐ")] = bstack1l11ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᘑ")
        os.environ[bstack1l11ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᘒ")] = bstack1l11ll_opy_ (u"ࠤࡱࡹࡱࡲࠢᘓ")
        os.environ[bstack1l11ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᘔ")] = bstack1l11ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᘕ")
        cls.bstack1lll1111111_opy_(response, bstack1l11ll_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᘖ"))
        return [None, None, None]
    @classmethod
    def bstack1lll111l1l1_opy_(cls, response=None):
        os.environ[bstack1l11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᘗ")] = bstack1l11ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᘘ")
        os.environ[bstack1l11ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘙ")] = bstack1l11ll_opy_ (u"ࠩࡱࡹࡱࡲࠧᘚ")
        os.environ[bstack1l11ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᘛ")] = bstack1l11ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᘜ")
        cls.bstack1lll1111111_opy_(response, bstack1l11ll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᘝ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1lllll1l_opy_(cls, bstack1ll1lll11ll_opy_, bstack1lll11111ll_opy_):
        os.environ[bstack1l11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᘞ")] = bstack1ll1lll11ll_opy_
        os.environ[bstack1l11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᘟ")] = bstack1lll11111ll_opy_
    @classmethod
    def bstack1lll1111111_opy_(cls, response=None, product=bstack1l11ll_opy_ (u"ࠣࠤᘠ")):
        if response == None:
            logger.error(product + bstack1l11ll_opy_ (u"ࠤࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠦᘡ"))
        for error in response[bstack1l11ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᘢ")]:
            bstack111ll111l1_opy_ = error[bstack1l11ll_opy_ (u"ࠫࡰ࡫ࡹࠨᘣ")]
            error_message = error[bstack1l11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘤ")]
            if error_message:
                match bstack111ll111l1_opy_:
                    case bstack1l11ll_opy_ (u"ࠨࡅࡓࡔࡒࡖࡤࡏࡎࡗࡃࡏࡍࡉࡥࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࠦᘥ"):
                        logger.error(error_message)
                    case bstack1l11ll_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨᘦ"):
                        logger.info(error_message)
                    case bstack1l11ll_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡔࡆࡎࡣࡉࡋࡐࡓࡇࡆࡅ࡙ࡋࡄࠣᘧ"):
                        logger.error(error_message)
                    case _:
                        logger.error(error_message)
            else:
                logger.error(bstack1l11ll_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥᘨ") + product + bstack1l11ll_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᘩ"))
    @classmethod
    def bstack1ll1llllll1_opy_(cls):
        if cls.bstack1lll1ll1l11_opy_ is not None:
            return
        cls.bstack1lll1ll1l11_opy_ = bstack1lll1l1l11l_opy_(cls.bstack1lll111l1ll_opy_)
        cls.bstack1lll1ll1l11_opy_.start()
    @classmethod
    def bstack1l1111ll1l_opy_(cls):
        if cls.bstack1lll1ll1l11_opy_ is None:
            return
        cls.bstack1lll1ll1l11_opy_.shutdown()
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def bstack1lll111l1ll_opy_(cls, bstack11lll11l1l_opy_, bstack1ll1ll1lll1_opy_=bstack1l11ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᘪ")):
        config = {
            bstack1l11ll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᘫ"): cls.default_headers()
        }
        response = bstack1lll11ll1_opy_(bstack1l11ll_opy_ (u"࠭ࡐࡐࡕࡗࠫᘬ"), cls.request_url(bstack1ll1ll1lll1_opy_), bstack11lll11l1l_opy_, config)
        bstack11l1llll1l_opy_ = response.json()
    @classmethod
    def bstack11llll111l_opy_(cls, bstack11lll11l1l_opy_, bstack1ll1ll1lll1_opy_=bstack1l11ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᘭ")):
        if not bstack1lll1l1ll1_opy_.bstack1ll1lllllll_opy_(bstack11lll11l1l_opy_[bstack1l11ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᘮ")]):
            return
        bstack1l111lll1l_opy_ = bstack1lll1l1ll1_opy_.bstack1ll1lll1111_opy_(bstack11lll11l1l_opy_[bstack1l11ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᘯ")], bstack11lll11l1l_opy_.get(bstack1l11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᘰ")))
        if bstack1l111lll1l_opy_ != None:
            bstack11lll11l1l_opy_[bstack1l11ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩᘱ")] = bstack1l111lll1l_opy_
        if bstack1ll1ll1lll1_opy_ == bstack1l11ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᘲ"):
            cls.bstack1ll1llllll1_opy_()
            cls.bstack1lll1ll1l11_opy_.add(bstack11lll11l1l_opy_)
        elif bstack1ll1ll1lll1_opy_ == bstack1l11ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᘳ"):
            cls.bstack1lll111l1ll_opy_([bstack11lll11l1l_opy_], bstack1ll1ll1lll1_opy_)
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def bstack1lll1ll11_opy_(cls, bstack11lllll1l1_opy_):
        bstack1lll11111l1_opy_ = []
        for log in bstack11lllll1l1_opy_:
            bstack1ll1lll11l1_opy_ = {
                bstack1l11ll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᘴ"): bstack1l11ll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪᘵ"),
                bstack1l11ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᘶ"): log[bstack1l11ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᘷ")],
                bstack1l11ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᘸ"): log[bstack1l11ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᘹ")],
                bstack1l11ll_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ᘺ"): {},
                bstack1l11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘻ"): log[bstack1l11ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᘼ")],
            }
            if bstack1l11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘽ") in log:
                bstack1ll1lll11l1_opy_[bstack1l11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘾ")] = log[bstack1l11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘿ")]
            elif bstack1l11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙀ") in log:
                bstack1ll1lll11l1_opy_[bstack1l11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᙁ")] = log[bstack1l11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᙂ")]
            bstack1lll11111l1_opy_.append(bstack1ll1lll11l1_opy_)
        cls.bstack11llll111l_opy_({
            bstack1l11ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᙃ"): bstack1l11ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᙄ"),
            bstack1l11ll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᙅ"): bstack1lll11111l1_opy_
        })
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def bstack1lll111ll11_opy_(cls, steps):
        bstack1ll1lll1l11_opy_ = []
        for step in steps:
            bstack1ll1ll1llll_opy_ = {
                bstack1l11ll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᙆ"): bstack1l11ll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨᙇ"),
                bstack1l11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᙈ"): step[bstack1l11ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᙉ")],
                bstack1l11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᙊ"): step[bstack1l11ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᙋ")],
                bstack1l11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙌ"): step[bstack1l11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙍ")],
                bstack1l11ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᙎ"): step[bstack1l11ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᙏ")]
            }
            if bstack1l11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᙐ") in step:
                bstack1ll1ll1llll_opy_[bstack1l11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᙑ")] = step[bstack1l11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᙒ")]
            elif bstack1l11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᙓ") in step:
                bstack1ll1ll1llll_opy_[bstack1l11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᙔ")] = step[bstack1l11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙕ")]
            bstack1ll1lll1l11_opy_.append(bstack1ll1ll1llll_opy_)
        cls.bstack11llll111l_opy_({
            bstack1l11ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᙖ"): bstack1l11ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᙗ"),
            bstack1l11ll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᙘ"): bstack1ll1lll1l11_opy_
        })
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def bstack11ll1l111_opy_(cls, screenshot):
        cls.bstack11llll111l_opy_({
            bstack1l11ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᙙ"): bstack1l11ll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᙚ"),
            bstack1l11ll_opy_ (u"ࠫࡱࡵࡧࡴࠩᙛ"): [{
                bstack1l11ll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᙜ"): bstack1l11ll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨᙝ"),
                bstack1l11ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᙞ"): datetime.datetime.utcnow().isoformat() + bstack1l11ll_opy_ (u"ࠨ࡜ࠪᙟ"),
                bstack1l11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙠ"): screenshot[bstack1l11ll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᙡ")],
                bstack1l11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᙢ"): screenshot[bstack1l11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙣ")]
            }]
        }, bstack1ll1ll1lll1_opy_=bstack1l11ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᙤ"))
    @classmethod
    @bstack1l11111111_opy_(class_method=True)
    def bstack1llllll111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11llll111l_opy_({
            bstack1l11ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᙥ"): bstack1l11ll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᙦ"),
            bstack1l11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᙧ"): {
                bstack1l11ll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᙨ"): cls.current_test_uuid(),
                bstack1l11ll_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᙩ"): cls.bstack1l11111l11_opy_(driver)
            }
        })
    @classmethod
    def bstack1l111111ll_opy_(cls, event: str, bstack11lll11l1l_opy_: bstack11lll1lll1_opy_):
        bstack11lll1111l_opy_ = {
            bstack1l11ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᙪ"): event,
            bstack11lll11l1l_opy_.bstack11lll1l1l1_opy_(): bstack11lll11l1l_opy_.bstack1l111l11l1_opy_(event)
        }
        cls.bstack11llll111l_opy_(bstack11lll1111l_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᙫ"), None) is None or os.environ[bstack1l11ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᙬ")] == bstack1l11ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ᙭")) and (os.environ.get(bstack1l11ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᙮"), None) is None or os.environ[bstack1l11ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᙯ")] == bstack1l11ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᙰ")):
            return False
        return True
    @staticmethod
    def bstack1ll1llll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1llllll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l11ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᙱ"): bstack1l11ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᙲ"),
            bstack1l11ll_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪᙳ"): bstack1l11ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᙴ")
        }
        if os.environ.get(bstack1l11ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᙵ"), None):
            headers[bstack1l11ll_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᙶ")] = bstack1l11ll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᙷ").format(os.environ[bstack1l11ll_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨᙸ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l11ll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᙹ").format(bstack1ll1llll1l1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l11ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᙺ"), None)
    @staticmethod
    def bstack1l11111l11_opy_(driver):
        return {
            bstack111l1l1l1l_opy_(): bstack1111ll11l1_opy_(driver)
        }
    @staticmethod
    def bstack1ll1llll111_opy_(exception_info, report):
        return [{bstack1l11ll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᙻ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11l1llllll_opy_(typename):
        if bstack1l11ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᙼ") in typename:
            return bstack1l11ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᙽ")
        return bstack1l11ll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᙾ")
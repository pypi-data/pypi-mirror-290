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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11111l1111_opy_
bstack11l1lll1l_opy_ = Config.bstack1ll1l11l1_opy_()
def bstack1llll1111ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llll11l11l_opy_(bstack1llll111l1l_opy_, bstack1llll111l11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llll111l1l_opy_):
        with open(bstack1llll111l1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1llll1111ll_opy_(bstack1llll111l1l_opy_):
        pac = get_pac(url=bstack1llll111l1l_opy_)
    else:
        raise Exception(bstack1l11ll1_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨᓉ").format(bstack1llll111l1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11ll1_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥᓊ"), 80))
        bstack1llll11l111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llll11l111_opy_ = bstack1l11ll1_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫᓋ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llll111l11_opy_, bstack1llll11l111_opy_)
    return proxy_url
def bstack1lll11lll_opy_(config):
    return bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᓌ") in config or bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᓍ") in config
def bstack1l1l11l1_opy_(config):
    if not bstack1lll11lll_opy_(config):
        return
    if config.get(bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᓎ")):
        return config.get(bstack1l11ll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᓏ"))
    if config.get(bstack1l11ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᓐ")):
        return config.get(bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᓑ"))
def bstack1l1llll1ll_opy_(config, bstack1llll111l11_opy_):
    proxy = bstack1l1l11l1_opy_(config)
    proxies = {}
    if config.get(bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᓒ")) or config.get(bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᓓ")):
        if proxy.endswith(bstack1l11ll1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪᓔ")):
            proxies = bstack111l11lll_opy_(proxy, bstack1llll111l11_opy_)
        else:
            proxies = {
                bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᓕ"): proxy
            }
    bstack11l1lll1l_opy_.bstack111ll1l1l_opy_(bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᓖ"), proxies)
    return proxies
def bstack111l11lll_opy_(bstack1llll111l1l_opy_, bstack1llll111l11_opy_):
    proxies = {}
    global bstack1llll111lll_opy_
    if bstack1l11ll1_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫᓗ") in globals():
        return bstack1llll111lll_opy_
    try:
        proxy = bstack1llll11l11l_opy_(bstack1llll111l1l_opy_, bstack1llll111l11_opy_)
        if bstack1l11ll1_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤᓘ") in proxy:
            proxies = {}
        elif bstack1l11ll1_opy_ (u"ࠥࡌ࡙࡚ࡐࠣᓙ") in proxy or bstack1l11ll1_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥᓚ") in proxy or bstack1l11ll1_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦᓛ") in proxy:
            bstack1llll111ll1_opy_ = proxy.split(bstack1l11ll1_opy_ (u"ࠨࠠࠣᓜ"))
            if bstack1l11ll1_opy_ (u"ࠢ࠻࠱࠲ࠦᓝ") in bstack1l11ll1_opy_ (u"ࠣࠤᓞ").join(bstack1llll111ll1_opy_[1:]):
                proxies = {
                    bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᓟ"): bstack1l11ll1_opy_ (u"ࠥࠦᓠ").join(bstack1llll111ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᓡ"): str(bstack1llll111ll1_opy_[0]).lower() + bstack1l11ll1_opy_ (u"ࠧࡀ࠯࠰ࠤᓢ") + bstack1l11ll1_opy_ (u"ࠨࠢᓣ").join(bstack1llll111ll1_opy_[1:])
                }
        elif bstack1l11ll1_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨᓤ") in proxy:
            bstack1llll111ll1_opy_ = proxy.split(bstack1l11ll1_opy_ (u"ࠣࠢࠥᓥ"))
            if bstack1l11ll1_opy_ (u"ࠤ࠽࠳࠴ࠨᓦ") in bstack1l11ll1_opy_ (u"ࠥࠦᓧ").join(bstack1llll111ll1_opy_[1:]):
                proxies = {
                    bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᓨ"): bstack1l11ll1_opy_ (u"ࠧࠨᓩ").join(bstack1llll111ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᓪ"): bstack1l11ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᓫ") + bstack1l11ll1_opy_ (u"ࠣࠤᓬ").join(bstack1llll111ll1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᓭ"): proxy
            }
    except Exception as e:
        print(bstack1l11ll1_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᓮ"), bstack11111l1111_opy_.format(bstack1llll111l1l_opy_, str(e)))
    bstack1llll111lll_opy_ = proxies
    return proxies
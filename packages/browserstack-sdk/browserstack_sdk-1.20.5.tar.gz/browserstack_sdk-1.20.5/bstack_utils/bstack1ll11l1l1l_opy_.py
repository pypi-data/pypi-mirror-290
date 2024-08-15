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
class bstack11l11ll1ll_opy_(object):
  bstack1ll1llll1l_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠪࢂࠬ།")), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ༎"))
  bstack11l11lll1l_opy_ = os.path.join(bstack1ll1llll1l_opy_, bstack1l11ll1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬ༏"))
  bstack11l11ll11l_opy_ = None
  perform_scan = None
  bstack111l1lll_opy_ = None
  bstack1111ll111_opy_ = None
  bstack11l1l1lll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11ll1_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨ༐")):
      cls.instance = super(bstack11l11ll1ll_opy_, cls).__new__(cls)
      cls.instance.bstack11l11ll1l1_opy_()
    return cls.instance
  def bstack11l11ll1l1_opy_(self):
    try:
      with open(self.bstack11l11lll1l_opy_, bstack1l11ll1_opy_ (u"ࠧࡳࠩ༑")) as bstack1lll1ll1l_opy_:
        bstack11l11lll11_opy_ = bstack1lll1ll1l_opy_.read()
        data = json.loads(bstack11l11lll11_opy_)
        if bstack1l11ll1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ༒") in data:
          self.bstack11l1llll11_opy_(data[bstack1l11ll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ༓")])
        if bstack1l11ll1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ༔") in data:
          self.bstack11l1ll1ll1_opy_(data[bstack1l11ll1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ༕")])
    except:
      pass
  def bstack11l1ll1ll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1l11ll1_opy_ (u"ࠬࡹࡣࡢࡰࠪ༖")]
      self.bstack111l1lll_opy_ = scripts[bstack1l11ll1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪ༗")]
      self.bstack1111ll111_opy_ = scripts[bstack1l11ll1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼ༘ࠫ")]
      self.bstack11l1l1lll1_opy_ = scripts[bstack1l11ll1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ༙࠭")]
  def bstack11l1llll11_opy_(self, bstack11l11ll11l_opy_):
    if bstack11l11ll11l_opy_ != None and len(bstack11l11ll11l_opy_) != 0:
      self.bstack11l11ll11l_opy_ = bstack11l11ll11l_opy_
  def store(self):
    try:
      with open(self.bstack11l11lll1l_opy_, bstack1l11ll1_opy_ (u"ࠩࡺࠫ༚")) as file:
        json.dump({
          bstack1l11ll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧ༛"): self.bstack11l11ll11l_opy_,
          bstack1l11ll1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧ༜"): {
            bstack1l11ll1_opy_ (u"ࠧࡹࡣࡢࡰࠥ༝"): self.perform_scan,
            bstack1l11ll1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥ༞"): self.bstack111l1lll_opy_,
            bstack1l11ll1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦ༟"): self.bstack1111ll111_opy_,
            bstack1l11ll1_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨ༠"): self.bstack11l1l1lll1_opy_
          }
        }, file)
    except:
      pass
  def bstack1111ll1l1_opy_(self, bstack11l11llll1_opy_):
    try:
      return any(command.get(bstack1l11ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ༡")) == bstack11l11llll1_opy_ for command in self.bstack11l11ll11l_opy_)
    except:
      return False
bstack1ll11l1l1l_opy_ = bstack11l11ll1ll_opy_()
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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1111l1_opy_, bstack1lll11ll1_opy_
class bstack1llll1l1l_opy_:
  working_dir = os.getcwd()
  bstack11l11l111_opy_ = False
  config = {}
  binary_path = bstack1l11ll_opy_ (u"ࠩࠪᑡ")
  bstack1lllll1l1ll_opy_ = bstack1l11ll_opy_ (u"ࠪࠫᑢ")
  bstack1l1l11l1l1_opy_ = False
  bstack1llllllllll_opy_ = None
  bstack1llllllll11_opy_ = {}
  bstack1lllllll1l1_opy_ = 300
  bstack1lllll1111l_opy_ = False
  logger = None
  bstack1llll1ll1l1_opy_ = False
  bstack111111ll11_opy_ = bstack1l11ll_opy_ (u"ࠫࠬᑣ")
  bstack1lllllllll1_opy_ = {
    bstack1l11ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᑤ") : 1,
    bstack1l11ll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᑥ") : 2,
    bstack1l11ll_opy_ (u"ࠧࡦࡦࡪࡩࠬᑦ") : 3,
    bstack1l11ll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᑧ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lllll11l11_opy_(self):
    bstack11111111ll_opy_ = bstack1l11ll_opy_ (u"ࠩࠪᑨ")
    bstack1llllll11ll_opy_ = sys.platform
    bstack1lllll111ll_opy_ = bstack1l11ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᑩ")
    if re.match(bstack1l11ll_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᑪ"), bstack1llllll11ll_opy_) != None:
      bstack11111111ll_opy_ = bstack11l11l111l_opy_ + bstack1l11ll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᑫ")
      self.bstack111111ll11_opy_ = bstack1l11ll_opy_ (u"࠭࡭ࡢࡥࠪᑬ")
    elif re.match(bstack1l11ll_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᑭ"), bstack1llllll11ll_opy_) != None:
      bstack11111111ll_opy_ = bstack11l11l111l_opy_ + bstack1l11ll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᑮ")
      bstack1lllll111ll_opy_ = bstack1l11ll_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᑯ")
      self.bstack111111ll11_opy_ = bstack1l11ll_opy_ (u"ࠪࡻ࡮ࡴࠧᑰ")
    else:
      bstack11111111ll_opy_ = bstack11l11l111l_opy_ + bstack1l11ll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᑱ")
      self.bstack111111ll11_opy_ = bstack1l11ll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᑲ")
    return bstack11111111ll_opy_, bstack1lllll111ll_opy_
  def bstack1111111ll1_opy_(self):
    try:
      bstack111111111l_opy_ = [os.path.join(expanduser(bstack1l11ll_opy_ (u"ࠨࡾࠣᑳ")), bstack1l11ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᑴ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111111111l_opy_:
        if(self.bstack1lllll1ll1l_opy_(path)):
          return path
      raise bstack1l11ll_opy_ (u"ࠣࡗࡱࡥࡱࡨࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᑵ")
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᑶ").format(e))
  def bstack1lllll1ll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lllll1ll11_opy_(self, bstack11111111ll_opy_, bstack1lllll111ll_opy_):
    try:
      bstack1lllll111l1_opy_ = self.bstack1111111ll1_opy_()
      bstack111111l1ll_opy_ = os.path.join(bstack1lllll111l1_opy_, bstack1l11ll_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ᑷ"))
      bstack1lllll11l1l_opy_ = os.path.join(bstack1lllll111l1_opy_, bstack1lllll111ll_opy_)
      if os.path.exists(bstack1lllll11l1l_opy_):
        self.logger.info(bstack1l11ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᑸ").format(bstack1lllll11l1l_opy_))
        return bstack1lllll11l1l_opy_
      if os.path.exists(bstack111111l1ll_opy_):
        self.logger.info(bstack1l11ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᑹ").format(bstack111111l1ll_opy_))
        return self.bstack1111111lll_opy_(bstack111111l1ll_opy_, bstack1lllll111ll_opy_)
      self.logger.info(bstack1l11ll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᑺ").format(bstack11111111ll_opy_))
      response = bstack1lll11ll1_opy_(bstack1l11ll_opy_ (u"ࠧࡈࡇࡗࠫᑻ"), bstack11111111ll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111111l1ll_opy_, bstack1l11ll_opy_ (u"ࠨࡹࡥࠫᑼ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11ll_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢᑽ").format(bstack111111l1ll_opy_))
        return self.bstack1111111lll_opy_(bstack111111l1ll_opy_, bstack1lllll111ll_opy_)
      else:
        raise(bstack1l11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨᑾ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᑿ").format(e))
  def bstack1111111l11_opy_(self, bstack11111111ll_opy_, bstack1lllll111ll_opy_):
    try:
      retry = 2
      bstack1lllll11l1l_opy_ = None
      bstack1lllll11ll1_opy_ = False
      while retry > 0:
        bstack1lllll11l1l_opy_ = self.bstack1lllll1ll11_opy_(bstack11111111ll_opy_, bstack1lllll111ll_opy_)
        bstack1lllll11ll1_opy_ = self.bstack11111111l1_opy_(bstack11111111ll_opy_, bstack1lllll111ll_opy_, bstack1lllll11l1l_opy_)
        if bstack1lllll11ll1_opy_:
          break
        retry -= 1
      return bstack1lllll11l1l_opy_, bstack1lllll11ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤᒀ").format(e))
    return bstack1lllll11l1l_opy_, False
  def bstack11111111l1_opy_(self, bstack11111111ll_opy_, bstack1lllll111ll_opy_, bstack1lllll11l1l_opy_, bstack1lllll1l11l_opy_ = 0):
    if bstack1lllll1l11l_opy_ > 1:
      return False
    if bstack1lllll11l1l_opy_ == None or os.path.exists(bstack1lllll11l1l_opy_) == False:
      self.logger.warn(bstack1l11ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᒁ"))
      return False
    bstack1llllllll1l_opy_ = bstack1l11ll_opy_ (u"ࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࡟࠳ࡨࡲࡩࠡ࡞ࡧ࠲ࡡࡪࠫ࠯࡞ࡧ࠯ࠧᒂ")
    command = bstack1l11ll_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧᒃ").format(bstack1lllll11l1l_opy_)
    bstack1lllll1l1l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1llllllll1l_opy_, bstack1lllll1l1l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᒄ"))
      return False
  def bstack1111111lll_opy_(self, bstack111111l1ll_opy_, bstack1lllll111ll_opy_):
    try:
      working_dir = os.path.dirname(bstack111111l1ll_opy_)
      shutil.unpack_archive(bstack111111l1ll_opy_, working_dir)
      bstack1lllll11l1l_opy_ = os.path.join(working_dir, bstack1lllll111ll_opy_)
      os.chmod(bstack1lllll11l1l_opy_, 0o755)
      return bstack1lllll11l1l_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᒅ"))
  def bstack111111l11l_opy_(self):
    try:
      percy = str(self.config.get(bstack1l11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᒆ"), bstack1l11ll_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᒇ"))).lower()
      if percy != bstack1l11ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᒈ"):
        return False
      self.bstack1l1l11l1l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᒉ").format(e))
  def bstack1lllll1l111_opy_(self):
    try:
      bstack1lllll1l111_opy_ = str(self.config.get(bstack1l11ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᒊ"), bstack1l11ll_opy_ (u"ࠤࡤࡹࡹࡵࠢᒋ"))).lower()
      return bstack1lllll1l111_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᒌ").format(e))
  def init(self, bstack11l11l111_opy_, config, logger):
    self.bstack11l11l111_opy_ = bstack11l11l111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111111l11l_opy_():
      return
    self.bstack1llllllll11_opy_ = config.get(bstack1l11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᒍ"), {})
    self.bstack1lllll11lll_opy_ = config.get(bstack1l11ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᒎ"), bstack1l11ll_opy_ (u"ࠨࡡࡶࡶࡲࠦᒏ"))
    try:
      bstack11111111ll_opy_, bstack1lllll111ll_opy_ = self.bstack1lllll11l11_opy_()
      bstack1lllll11l1l_opy_, bstack1lllll11ll1_opy_ = self.bstack1111111l11_opy_(bstack11111111ll_opy_, bstack1lllll111ll_opy_)
      if bstack1lllll11ll1_opy_:
        self.binary_path = bstack1lllll11l1l_opy_
        thread = Thread(target=self.bstack1lllll1lll1_opy_)
        thread.start()
      else:
        self.bstack1llll1ll1l1_opy_ = True
        self.logger.error(bstack1l11ll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᒐ").format(bstack1lllll11l1l_opy_))
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᒑ").format(e))
  def bstack1llllll1l1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11ll_opy_ (u"ࠩ࡯ࡳ࡬࠭ᒒ"), bstack1l11ll_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭ᒓ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11ll_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣᒔ").format(logfile))
      self.bstack1lllll1l1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᒕ").format(e))
  def bstack1lllll1lll1_opy_(self):
    bstack1llllll1ll1_opy_ = self.bstack1lllllll11l_opy_()
    if bstack1llllll1ll1_opy_ == None:
      self.bstack1llll1ll1l1_opy_ = True
      self.logger.error(bstack1l11ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤᒖ"))
      return False
    command_args = [bstack1l11ll_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣᒗ") if self.bstack11l11l111_opy_ else bstack1l11ll_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬᒘ")]
    bstack1lllllll1ll_opy_ = self.bstack1llll1ll1ll_opy_()
    if bstack1lllllll1ll_opy_ != None:
      command_args.append(bstack1l11ll_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣᒙ").format(bstack1lllllll1ll_opy_))
    env = os.environ.copy()
    env[bstack1l11ll_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣᒚ")] = bstack1llllll1ll1_opy_
    env[bstack1l11ll_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦᒛ")] = os.environ.get(bstack1l11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᒜ"), bstack1l11ll_opy_ (u"࠭ࠧᒝ"))
    bstack1lllll1llll_opy_ = [self.binary_path]
    self.bstack1llllll1l1l_opy_()
    self.bstack1llllllllll_opy_ = self.bstack1llllll1l11_opy_(bstack1lllll1llll_opy_ + command_args, env)
    self.logger.debug(bstack1l11ll_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣᒞ"))
    bstack1lllll1l11l_opy_ = 0
    while self.bstack1llllllllll_opy_.poll() == None:
      bstack1llll1lllll_opy_ = self.bstack1llllll11l1_opy_()
      if bstack1llll1lllll_opy_:
        self.logger.debug(bstack1l11ll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦᒟ"))
        self.bstack1lllll1111l_opy_ = True
        return True
      bstack1lllll1l11l_opy_ += 1
      self.logger.debug(bstack1l11ll_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧᒠ").format(bstack1lllll1l11l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣᒡ").format(bstack1lllll1l11l_opy_))
    self.bstack1llll1ll1l1_opy_ = True
    return False
  def bstack1llllll11l1_opy_(self, bstack1lllll1l11l_opy_ = 0):
    try:
      if bstack1lllll1l11l_opy_ > 10:
        return False
      bstack1lllll11111_opy_ = os.environ.get(bstack1l11ll_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫᒢ"), bstack1l11ll_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭ᒣ"))
      bstack1llllll1lll_opy_ = bstack1lllll11111_opy_ + bstack11l111ll1l_opy_
      response = requests.get(bstack1llllll1lll_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1lllllll11l_opy_(self):
    bstack1llll1lll11_opy_ = bstack1l11ll_opy_ (u"࠭ࡡࡱࡲࠪᒤ") if self.bstack11l11l111_opy_ else bstack1l11ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᒥ")
    bstack111ll1l1l1_opy_ = bstack1l11ll_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠢᒦ").format(self.config[bstack1l11ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᒧ")], bstack1llll1lll11_opy_)
    uri = bstack1l1111l1_opy_(bstack111ll1l1l1_opy_)
    try:
      response = bstack1lll11ll1_opy_(bstack1l11ll_opy_ (u"ࠪࡋࡊ࡚ࠧᒨ"), uri, {}, {bstack1l11ll_opy_ (u"ࠫࡦࡻࡴࡩࠩᒩ"): (self.config[bstack1l11ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᒪ")], self.config[bstack1l11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᒫ")])})
      if response.status_code == 200:
        bstack1lllllll111_opy_ = response.json()
        if bstack1l11ll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᒬ") in bstack1lllllll111_opy_:
          return bstack1lllllll111_opy_[bstack1l11ll_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᒭ")]
        else:
          raise bstack1l11ll_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᒮ").format(bstack1lllllll111_opy_)
      else:
        raise bstack1l11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᒯ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᒰ").format(e))
  def bstack1llll1ll1ll_opy_(self):
    bstack111111l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᒱ"))
    try:
      if bstack1l11ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᒲ") not in self.bstack1llllllll11_opy_:
        self.bstack1llllllll11_opy_[bstack1l11ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᒳ")] = 2
      with open(bstack111111l1l1_opy_, bstack1l11ll_opy_ (u"ࠨࡹࠪᒴ")) as fp:
        json.dump(self.bstack1llllllll11_opy_, fp)
      return bstack111111l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᒵ").format(e))
  def bstack1llllll1l11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111111ll11_opy_ == bstack1l11ll_opy_ (u"ࠪࡻ࡮ࡴࠧᒶ"):
        bstack1111111111_opy_ = [bstack1l11ll_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᒷ"), bstack1l11ll_opy_ (u"ࠬ࠵ࡣࠨᒸ")]
        cmd = bstack1111111111_opy_ + cmd
      cmd = bstack1l11ll_opy_ (u"࠭ࠠࠨᒹ").join(cmd)
      self.logger.debug(bstack1l11ll_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᒺ").format(cmd))
      with open(self.bstack1lllll1l1ll_opy_, bstack1l11ll_opy_ (u"ࠣࡣࠥᒻ")) as bstack1llll1llll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll1llll1_opy_, text=True, stderr=bstack1llll1llll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llll1ll1l1_opy_ = True
      self.logger.error(bstack1l11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᒼ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lllll1111l_opy_:
        self.logger.info(bstack1l11ll_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᒽ"))
        cmd = [self.binary_path, bstack1l11ll_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᒾ")]
        self.bstack1llllll1l11_opy_(cmd)
        self.bstack1lllll1111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᒿ").format(cmd, e))
  def bstack1llll1l11l_opy_(self):
    if not self.bstack1l1l11l1l1_opy_:
      return
    try:
      bstack1llllll111l_opy_ = 0
      while not self.bstack1lllll1111l_opy_ and bstack1llllll111l_opy_ < self.bstack1lllllll1l1_opy_:
        if self.bstack1llll1ll1l1_opy_:
          self.logger.info(bstack1l11ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᓀ"))
          return
        time.sleep(1)
        bstack1llllll111l_opy_ += 1
      os.environ[bstack1l11ll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᓁ")] = str(self.bstack1111111l1l_opy_())
      self.logger.info(bstack1l11ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᓂ"))
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᓃ").format(e))
  def bstack1111111l1l_opy_(self):
    if self.bstack11l11l111_opy_:
      return
    try:
      bstack1llll1ll11l_opy_ = [platform[bstack1l11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᓄ")].lower() for platform in self.config.get(bstack1l11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᓅ"), [])]
      bstack1llllll1111_opy_ = sys.maxsize
      bstack1llll1lll1l_opy_ = bstack1l11ll_opy_ (u"ࠬ࠭ᓆ")
      for browser in bstack1llll1ll11l_opy_:
        if browser in self.bstack1lllllllll1_opy_:
          bstack111111l111_opy_ = self.bstack1lllllllll1_opy_[browser]
        if bstack111111l111_opy_ < bstack1llllll1111_opy_:
          bstack1llllll1111_opy_ = bstack111111l111_opy_
          bstack1llll1lll1l_opy_ = browser
      return bstack1llll1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᓇ").format(e))
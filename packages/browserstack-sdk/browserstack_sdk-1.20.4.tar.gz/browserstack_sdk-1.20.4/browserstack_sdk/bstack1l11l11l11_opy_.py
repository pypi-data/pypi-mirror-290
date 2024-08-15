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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11ll11_opy_
from browserstack_sdk.bstack1lll111ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l111llll_opy_
class bstack111l11111_opy_:
    def __init__(self, args, logger, bstack11ll11l111_opy_, bstack11ll1l1111_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll11l111_opy_ = bstack11ll11l111_opy_
        self.bstack11ll1l1111_opy_ = bstack11ll1l1111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l11ll11l_opy_ = []
        self.bstack11ll11llll_opy_ = None
        self.bstack1l1l11l1ll_opy_ = []
        self.bstack11ll11l1l1_opy_ = self.bstack1ll1ll1l11_opy_()
        self.bstack1l1l1ll1ll_opy_ = -1
    def bstack1l11llll11_opy_(self, bstack11ll111l11_opy_):
        self.parse_args()
        self.bstack11ll111lll_opy_()
        self.bstack11ll11l1ll_opy_(bstack11ll111l11_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll11ll11_opy_():
        import importlib
        if getattr(importlib, bstack1l11ll_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡰࡴࡧࡤࡦࡴࠪ฽"), False):
            bstack11ll11ll1l_opy_ = importlib.find_loader(bstack1l11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ฾"))
        else:
            bstack11ll11ll1l_opy_ = importlib.util.find_spec(bstack1l11ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ฿"))
    def bstack11ll11l11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1l1ll1ll_opy_ = -1
        if self.bstack11ll1l1111_opy_ and bstack1l11ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨเ") in self.bstack11ll11l111_opy_:
            self.bstack1l1l1ll1ll_opy_ = int(self.bstack11ll11l111_opy_[bstack1l11ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩแ")])
        try:
            bstack11ll11lll1_opy_ = [bstack1l11ll_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬโ"), bstack1l11ll_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧใ"), bstack1l11ll_opy_ (u"ࠬ࠳ࡰࠨไ")]
            if self.bstack1l1l1ll1ll_opy_ >= 0:
                bstack11ll11lll1_opy_.extend([bstack1l11ll_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧๅ"), bstack1l11ll_opy_ (u"ࠧ࠮ࡰࠪๆ")])
            for arg in bstack11ll11lll1_opy_:
                self.bstack11ll11l11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll111lll_opy_(self):
        bstack11ll11llll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11ll11llll_opy_ = bstack11ll11llll_opy_
        return bstack11ll11llll_opy_
    def bstack1ll11ll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11ll11ll11_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l111llll_opy_)
    def bstack11ll11l1ll_opy_(self, bstack11ll111l11_opy_):
        bstack1ll1l111l1_opy_ = Config.bstack1l1ll11l1l_opy_()
        if bstack11ll111l11_opy_:
            self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ็"))
            self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"ࠩࡗࡶࡺ࡫่ࠧ"))
        if bstack1ll1l111l1_opy_.bstack11ll1111ll_opy_():
            self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴ้ࠩ"))
            self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"࡙ࠫࡸࡵࡦ๊ࠩ"))
        self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"ࠬ࠳ࡰࠨ๋"))
        self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫ์"))
        self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩํ"))
        self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ๎"))
        if self.bstack1l1l1ll1ll_opy_ > 1:
            self.bstack11ll11llll_opy_.append(bstack1l11ll_opy_ (u"ࠩ࠰ࡲࠬ๏"))
            self.bstack11ll11llll_opy_.append(str(self.bstack1l1l1ll1ll_opy_))
    def bstack11ll1l111l_opy_(self):
        bstack1l1l11l1ll_opy_ = []
        for spec in self.bstack1l11ll11l_opy_:
            bstack1lll11l11l_opy_ = [spec]
            bstack1lll11l11l_opy_ += self.bstack11ll11llll_opy_
            bstack1l1l11l1ll_opy_.append(bstack1lll11l11l_opy_)
        self.bstack1l1l11l1ll_opy_ = bstack1l1l11l1ll_opy_
        return bstack1l1l11l1ll_opy_
    def bstack1ll1ll1l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll11l1l1_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll11l1l1_opy_ = False
        return self.bstack11ll11l1l1_opy_
    def bstack1ll1ll1l1_opy_(self, bstack11ll111ll1_opy_, bstack1l11llll11_opy_):
        bstack1l11llll11_opy_[bstack1l11ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ๐")] = self.bstack11ll11l111_opy_
        multiprocessing.set_start_method(bstack1l11ll_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪ๑"))
        bstack1l11ll11ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l111lll1_opy_ = manager.list()
        if bstack1l11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๒") in self.bstack11ll11l111_opy_:
            for index, platform in enumerate(self.bstack11ll11l111_opy_[bstack1l11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ๓")]):
                bstack1l11ll11ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11ll111ll1_opy_,
                                                            args=(self.bstack11ll11llll_opy_, bstack1l11llll11_opy_, bstack1l111lll1_opy_)))
            bstack11ll111l1l_opy_ = len(self.bstack11ll11l111_opy_[bstack1l11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ๔")])
        else:
            bstack1l11ll11ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11ll111ll1_opy_,
                                                        args=(self.bstack11ll11llll_opy_, bstack1l11llll11_opy_, bstack1l111lll1_opy_)))
            bstack11ll111l1l_opy_ = 1
        i = 0
        for t in bstack1l11ll11ll_opy_:
            os.environ[bstack1l11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ๕")] = str(i)
            if bstack1l11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ๖") in self.bstack11ll11l111_opy_:
                os.environ[bstack1l11ll_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ๗")] = json.dumps(self.bstack11ll11l111_opy_[bstack1l11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๘")][i % bstack11ll111l1l_opy_])
            i += 1
            t.start()
        for t in bstack1l11ll11ll_opy_:
            t.join()
        return list(bstack1l111lll1_opy_)
    @staticmethod
    def bstack111l1l1ll_opy_(driver, bstack111lll1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ๙"), None)
        if item and getattr(item, bstack1l11ll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࠨ๚"), None) and not getattr(item, bstack1l11ll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࡣࡩࡵ࡮ࡦࠩ๛"), False):
            logger.info(
                bstack1l11ll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠢ๜"))
            bstack11ll1l11l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11ll11_opy_.bstack1111l11l_opy_(driver, bstack11ll1l11l1_opy_, item.name, item.module.__name__, item.path, bstack111lll1l_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
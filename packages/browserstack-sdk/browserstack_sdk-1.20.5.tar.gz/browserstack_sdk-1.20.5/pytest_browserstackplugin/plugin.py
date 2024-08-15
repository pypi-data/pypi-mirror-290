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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11l1l11l_opy_, bstack1ll1l11lll_opy_, update, bstack1l1lll111l_opy_,
                                       bstack1l1ll1l1ll_opy_, bstack1111111l_opy_, bstack1lllll1ll_opy_, bstack11l1ll111_opy_,
                                       bstack11l1l1ll1_opy_, bstack1l1llll1l1_opy_, bstack1l11111ll_opy_, bstack1llll11l11_opy_,
                                       bstack11llll1ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11111l1l1_opy_)
from browserstack_sdk.bstack1lll1ll1l1_opy_ import bstack111111l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11ll1ll1l_opy_
from bstack_utils.capture import bstack1l111l11ll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11ll1l1l1_opy_, bstack11lll11l_opy_, bstack11111ll1l_opy_, \
    bstack1lll11ll11_opy_
from bstack_utils.helper import bstack1l1ll1111_opy_, bstack1111ll1l1l_opy_, bstack11ll1ll1ll_opy_, bstack1l11llll11_opy_, bstack1111lll1l1_opy_, bstack1l1l1l1l11_opy_, \
    bstack111lll1ll1_opy_, \
    bstack111lllllll_opy_, bstack1llll1111l_opy_, bstack11l11l11l_opy_, bstack111l11ll11_opy_, bstack1l111111_opy_, Notset, \
    bstack11ll11l1_opy_, bstack1111lllll1_opy_, bstack1111ll1l11_opy_, Result, bstack111lll1lll_opy_, bstack111ll1llll_opy_, bstack11llll11l1_opy_, \
    bstack1111ll11_opy_, bstack1ll11l1l_opy_, bstack111ll11ll_opy_, bstack111l1111l1_opy_
from bstack_utils.bstack1111l11lll_opy_ import bstack1111l1l1l1_opy_
from bstack_utils.messages import bstack1l11l1l1ll_opy_, bstack11l1lll11_opy_, bstack1l1ll1ll1_opy_, bstack1ll1ll1ll1_opy_, bstack111l11ll_opy_, \
    bstack1llllll111_opy_, bstack1llllll1l_opy_, bstack1l1ll1111l_opy_, bstack1ll1111l11_opy_, bstack1l1ll1l1l1_opy_, \
    bstack1l1l11ll_opy_, bstack1l1l11lll_opy_
from bstack_utils.proxy import bstack1l1l11l1_opy_, bstack111l11lll_opy_
from bstack_utils.bstack1l1111ll1_opy_ import bstack1lll1ll1ll1_opy_, bstack1lll1lllll1_opy_, bstack1lll1lll11l_opy_, bstack1llll11111l_opy_, \
    bstack1lll1ll1l1l_opy_, bstack1lll1llll1l_opy_, bstack1lll1ll1lll_opy_, bstack1lll111ll_opy_, bstack1lll1lll1ll_opy_
from bstack_utils.bstack1ll1lllll_opy_ import bstack1lllll111l_opy_
from bstack_utils.bstack1ll1lll1l_opy_ import bstack11l111lll_opy_, bstack111ll11l_opy_, bstack111ll1111_opy_, \
    bstack1l1llll11_opy_, bstack1lll1lll_opy_
from bstack_utils.bstack11llllll1l_opy_ import bstack11lllll111_opy_
from bstack_utils.bstack111l1l1l_opy_ import bstack1l11ll11ll_opy_
import bstack_utils.bstack1l1lll1l11_opy_ as bstack1l1l1l11l1_opy_
from bstack_utils.bstack1ll1l111_opy_ import bstack1l1111111_opy_
from bstack_utils.bstack1ll11l1l1l_opy_ import bstack1ll11l1l1l_opy_
bstack1l1lll1l1l_opy_ = None
bstack1111111ll_opy_ = None
bstack11ll11111_opy_ = None
bstack1ll11llll1_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1lllllll11_opy_ = None
bstack1111ll1ll_opy_ = None
bstack111l111l1_opy_ = None
bstack1ll1l1l1_opy_ = None
bstack1l1ll11l1l_opy_ = None
bstack1ll111lll1_opy_ = None
bstack1l111l1ll_opy_ = None
bstack1ll1111l1_opy_ = None
bstack1l1l1lll_opy_ = bstack1l11ll1_opy_ (u"ࠪࠫᛘ")
CONFIG = {}
bstack1ll11l1ll1_opy_ = False
bstack1l1ll1l111_opy_ = bstack1l11ll1_opy_ (u"ࠫࠬᛙ")
bstack1ll1l1l111_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠭ᛚ")
bstack1ll1lll11_opy_ = False
bstack1llll11ll1_opy_ = []
bstack1l11l111ll_opy_ = bstack11ll1l1l1_opy_
bstack1ll1l1ll1l1_opy_ = bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᛛ")
bstack1ll1l1l1l11_opy_ = False
bstack1ll11l111_opy_ = {}
bstack1l11lll1l_opy_ = False
logger = bstack11ll1ll1l_opy_.get_logger(__name__, bstack1l11l111ll_opy_)
store = {
    bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᛜ"): []
}
bstack1ll1l11111l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11ll1llll1_opy_ = {}
current_test_uuid = None
def bstack1ll1l111l1_opy_(page, bstack11l111ll_opy_):
    try:
        page.evaluate(bstack1l11ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᛝ"),
                      bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᛞ") + json.dumps(
                          bstack11l111ll_opy_) + bstack1l11ll1_opy_ (u"ࠥࢁࢂࠨᛟ"))
    except Exception as e:
        print(bstack1l11ll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᛠ"), e)
def bstack1ll1l11l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1l11ll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᛡ"), bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫᛢ") + json.dumps(
            message) + bstack1l11ll1_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪᛣ") + json.dumps(level) + bstack1l11ll1_opy_ (u"ࠨࡿࢀࠫᛤ"))
    except Exception as e:
        print(bstack1l11ll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧᛥ"), e)
def pytest_configure(config):
    bstack11l1lll1l_opy_ = Config.bstack1ll1l11l1_opy_()
    config.args = bstack1l11ll11ll_opy_.bstack1ll1ll111l1_opy_(config.args)
    bstack11l1lll1l_opy_.bstack11ll111ll_opy_(bstack111ll11ll_opy_(config.getoption(bstack1l11ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᛦ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll1l111l1l_opy_ = item.config.getoption(bstack1l11ll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᛧ"))
    plugins = item.config.getoption(bstack1l11ll1_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᛨ"))
    report = outcome.get_result()
    bstack1ll1l11l1l1_opy_(item, call, report)
    if bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᛩ") not in plugins or bstack1l111111_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l11ll1_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᛪ"), None)
    page = getattr(item, bstack1l11ll1_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢ᛫"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll1l1111ll_opy_(item, report, summary, bstack1ll1l111l1l_opy_)
    if (page is not None):
        bstack1ll1l111111_opy_(item, report, summary, bstack1ll1l111l1l_opy_)
def bstack1ll1l1111ll_opy_(item, report, summary, bstack1ll1l111l1l_opy_):
    if report.when == bstack1l11ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᛬") and report.skipped:
        bstack1lll1lll1ll_opy_(report)
    if report.when in [bstack1l11ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ᛭"), bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᛮ")]:
        return
    if not bstack1111lll1l1_opy_():
        return
    try:
        if (str(bstack1ll1l111l1l_opy_).lower() != bstack1l11ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪᛯ")):
            item._driver.execute_script(
                bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᛰ") + json.dumps(
                    report.nodeid) + bstack1l11ll1_opy_ (u"ࠧࡾࡿࠪᛱ"))
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᛲ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l11ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤᛳ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11ll1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᛴ")))
    bstack1l1ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠦࠧᛵ")
    bstack1lll1lll1ll_opy_(report)
    if not passed:
        try:
            bstack1l1ll111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l11ll1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᛶ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l11ll1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᛷ")))
        bstack1l1ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠢࠣᛸ")
        if not passed:
            try:
                bstack1l1ll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ᛹").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭᛺")
                    + json.dumps(bstack1l11ll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦ᛻"))
                    + bstack1l11ll1_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢ᛼")
                )
            else:
                item._driver.execute_script(
                    bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ᛽")
                    + json.dumps(str(bstack1l1ll111ll_opy_))
                    + bstack1l11ll1_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ᛾")
                )
        except Exception as e:
            summary.append(bstack1l11ll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧ᛿").format(e))
def bstack1ll1l1111l1_opy_(test_name, error_message):
    try:
        bstack1ll1l11l1ll_opy_ = []
        bstack11l111l1l_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᜀ"), bstack1l11ll1_opy_ (u"ࠩ࠳ࠫᜁ"))
        bstack1llll111l_opy_ = {bstack1l11ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᜂ"): test_name, bstack1l11ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᜃ"): error_message, bstack1l11ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᜄ"): bstack11l111l1l_opy_}
        bstack1ll1l11l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᜅ"))
        if os.path.exists(bstack1ll1l11l11l_opy_):
            with open(bstack1ll1l11l11l_opy_) as f:
                bstack1ll1l11l1ll_opy_ = json.load(f)
        bstack1ll1l11l1ll_opy_.append(bstack1llll111l_opy_)
        with open(bstack1ll1l11l11l_opy_, bstack1l11ll1_opy_ (u"ࠧࡸࠩᜆ")) as f:
            json.dump(bstack1ll1l11l1ll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ᜇ") + str(e))
def bstack1ll1l111111_opy_(item, report, summary, bstack1ll1l111l1l_opy_):
    if report.when in [bstack1l11ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᜈ"), bstack1l11ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᜉ")]:
        return
    if (str(bstack1ll1l111l1l_opy_).lower() != bstack1l11ll1_opy_ (u"ࠫࡹࡸࡵࡦࠩᜊ")):
        bstack1ll1l111l1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11ll1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᜋ")))
    bstack1l1ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠨࠢᜌ")
    bstack1lll1lll1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1ll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11ll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᜍ").format(e)
                )
        try:
            if passed:
                bstack1lll1lll_opy_(getattr(item, bstack1l11ll1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᜎ"), None), bstack1l11ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᜏ"))
            else:
                error_message = bstack1l11ll1_opy_ (u"ࠪࠫᜐ")
                if bstack1l1ll111ll_opy_:
                    bstack1ll1l11l1l_opy_(item._page, str(bstack1l1ll111ll_opy_), bstack1l11ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᜑ"))
                    bstack1lll1lll_opy_(getattr(item, bstack1l11ll1_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᜒ"), None), bstack1l11ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᜓ"), str(bstack1l1ll111ll_opy_))
                    error_message = str(bstack1l1ll111ll_opy_)
                else:
                    bstack1lll1lll_opy_(getattr(item, bstack1l11ll1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ᜔࠭"), None), bstack1l11ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤ᜕ࠣ"))
                bstack1ll1l1111l1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l11ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨ᜖").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l11ll1_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ᜗"), default=bstack1l11ll1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ᜘"), help=bstack1l11ll1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ᜙"))
    parser.addoption(bstack1l11ll1_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ᜚"), default=bstack1l11ll1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ᜛"), help=bstack1l11ll1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ᜜"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l11ll1_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ᜝"), action=bstack1l11ll1_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ᜞"), default=bstack1l11ll1_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦᜟ"),
                         help=bstack1l11ll1_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦᜠ"))
def bstack11lll1l11l_opy_(log):
    if not (log[bstack1l11ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜡ")] and log[bstack1l11ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᜢ")].strip()):
        return
    active = bstack11llll1lll_opy_()
    log = {
        bstack1l11ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᜣ"): log[bstack1l11ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᜤ")],
        bstack1l11ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᜥ"): bstack11ll1ll1ll_opy_().isoformat() + bstack1l11ll1_opy_ (u"ࠫ࡟࠭ᜦ"),
        bstack1l11ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᜧ"): log[bstack1l11ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜨ")],
    }
    if active:
        if active[bstack1l11ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬᜩ")] == bstack1l11ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᜪ"):
            log[bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜫ")] = active[bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜬ")]
        elif active[bstack1l11ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩᜭ")] == bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࠪᜮ"):
            log[bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜯ")] = active[bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜰ")]
    bstack1l1111111_opy_.bstack1l1l1ll11l_opy_([log])
def bstack11llll1lll_opy_():
    if len(store[bstack1l11ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᜱ")]) > 0 and store[bstack1l11ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᜲ")][-1]:
        return {
            bstack1l11ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᜳ"): bstack1l11ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬᜴ࠩ"),
            bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᜵"): store[bstack1l11ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ᜶")][-1]
        }
    if store.get(bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ᜷"), None):
        return {
            bstack1l11ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭᜸"): bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺࠧ᜹"),
            bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᜺"): store[bstack1l11ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ᜻")]
        }
    return None
bstack1l11111ll1_opy_ = bstack1l111l11ll_opy_(bstack11lll1l11l_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll1l1l1l11_opy_
        item._1ll11llll1l_opy_ = True
        bstack1l111ll111_opy_ = bstack1l1l1l11l1_opy_.bstack1lllll1lll_opy_(bstack111lllllll_opy_(item.own_markers))
        item._a11y_test_case = bstack1l111ll111_opy_
        if bstack1ll1l1l1l11_opy_:
            driver = getattr(item, bstack1l11ll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᜼"), None)
            item._a11y_started = bstack1l1l1l11l1_opy_.bstack1l1l1111l1_opy_(driver, bstack1l111ll111_opy_)
        if not bstack1l1111111_opy_.on() or bstack1ll1l1ll1l1_opy_ != bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᜽"):
            return
        global current_test_uuid, bstack1l11111ll1_opy_
        bstack1l11111ll1_opy_.start()
        bstack11ll1lll1l_opy_ = {
            bstack1l11ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᜾"): uuid4().__str__(),
            bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᜿"): bstack11ll1ll1ll_opy_().isoformat() + bstack1l11ll1_opy_ (u"ࠩ࡝ࠫᝀ")
        }
        current_test_uuid = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᝁ")]
        store[bstack1l11ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᝂ")] = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᝃ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11ll1llll1_opy_[item.nodeid] = {**_11ll1llll1_opy_[item.nodeid], **bstack11ll1lll1l_opy_}
        bstack1ll1l1ll111_opy_(item, _11ll1llll1_opy_[item.nodeid], bstack1l11ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᝄ"))
    except Exception as err:
        print(bstack1l11ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᝅ"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll1l11111l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111l11ll11_opy_():
        atexit.register(bstack11l1l111_opy_)
        if not bstack1ll1l11111l_opy_:
            try:
                bstack1ll1l11lll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111l1111l1_opy_():
                    bstack1ll1l11lll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1l11lll1_opy_:
                    signal.signal(s, bstack1ll11llll11_opy_)
                bstack1ll1l11111l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l11ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤᝆ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll1ll1ll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l11ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᝇ")
    try:
        if not bstack1l1111111_opy_.on():
            return
        bstack1l11111ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll1lll1l_opy_ = {
            bstack1l11ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᝈ"): uuid,
            bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᝉ"): bstack11ll1ll1ll_opy_().isoformat() + bstack1l11ll1_opy_ (u"ࠬࡠࠧᝊ"),
            bstack1l11ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫᝋ"): bstack1l11ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᝌ"),
            bstack1l11ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᝍ"): bstack1l11ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᝎ"),
            bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᝏ"): bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᝐ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l11ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᝑ")] = item
        store[bstack1l11ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᝒ")] = [uuid]
        if not _11ll1llll1_opy_.get(item.nodeid, None):
            _11ll1llll1_opy_[item.nodeid] = {bstack1l11ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᝓ"): [], bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ᝔"): []}
        _11ll1llll1_opy_[item.nodeid][bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᝕")].append(bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᝖")])
        _11ll1llll1_opy_[item.nodeid + bstack1l11ll1_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫ᝗")] = bstack11ll1lll1l_opy_
        bstack1ll1l1l1l1l_opy_(item, bstack11ll1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᝘"))
    except Exception as err:
        print(bstack1l11ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ᝙"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1ll11l111_opy_
        bstack11l111l1l_opy_ = 0
        if bstack1ll1lll11_opy_ is True:
            bstack11l111l1l_opy_ = int(os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᝚")))
        if CONFIG.get(bstack1l11ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᝛"), False):
            if CONFIG.get(bstack1l11ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ᝜"), bstack1l11ll1_opy_ (u"ࠥࡥࡺࡺ࡯ࠣ᝝")) == bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᝞"):
                bstack1ll1l1l11l1_opy_ = bstack1l1ll1111_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᝟"), None)
                bstack1l1llll1l_opy_ = bstack1ll1l1l11l1_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤᝠ")
                driver = getattr(item, bstack1l11ll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᝡ"), None)
                bstack1l1l111l_opy_ = item.get(bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᝢ")) or bstack1l11ll1_opy_ (u"ࠩࠪᝣ")
                bstack1ll11l1l11_opy_ = item.get(bstack1l11ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᝤ")) or bstack1l11ll1_opy_ (u"ࠫࠬᝥ")
                PercySDK.screenshot(driver, bstack1l1llll1l_opy_, bstack1l1l111l_opy_=bstack1l1l111l_opy_, bstack1ll11l1l11_opy_=bstack1ll11l1l11_opy_, bstack1ll11lll_opy_=bstack11l111l1l_opy_)
        if getattr(item, bstack1l11ll1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᝦ"), False):
            bstack111111l11_opy_.bstack1l11lll11_opy_(getattr(item, bstack1l11ll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᝧ"), None), bstack1ll11l111_opy_, logger, item)
        if not bstack1l1111111_opy_.on():
            return
        bstack11ll1lll1l_opy_ = {
            bstack1l11ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᝨ"): uuid4().__str__(),
            bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᝩ"): bstack11ll1ll1ll_opy_().isoformat() + bstack1l11ll1_opy_ (u"ࠩ࡝ࠫᝪ"),
            bstack1l11ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᝫ"): bstack1l11ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᝬ"),
            bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᝭"): bstack1l11ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᝮ"),
            bstack1l11ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᝯ"): bstack1l11ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᝰ")
        }
        _11ll1llll1_opy_[item.nodeid + bstack1l11ll1_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬ᝱")] = bstack11ll1lll1l_opy_
        bstack1ll1l1l1l1l_opy_(item, bstack11ll1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᝲ"))
    except Exception as err:
        print(bstack1l11ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᝳ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l1111111_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1llll11111l_opy_(fixturedef.argname):
        store[bstack1l11ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ᝴")] = request.node
    elif bstack1lll1ll1l1l_opy_(fixturedef.argname):
        store[bstack1l11ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ᝵")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l11ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᝶"): fixturedef.argname,
            bstack1l11ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᝷"): bstack111lll1ll1_opy_(outcome),
            bstack1l11ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ᝸"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l11ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ᝹")]
        if not _11ll1llll1_opy_.get(current_test_item.nodeid, None):
            _11ll1llll1_opy_[current_test_item.nodeid] = {bstack1l11ll1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭᝺"): []}
        _11ll1llll1_opy_[current_test_item.nodeid][bstack1l11ll1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ᝻")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l11ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ᝼"), str(err))
if bstack1l111111_opy_() and bstack1l1111111_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11ll1llll1_opy_[request.node.nodeid][bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ᝽")].bstack1lll11l1ll1_opy_(id(step))
        except Exception as err:
            print(bstack1l11ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭᝾"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11ll1llll1_opy_[request.node.nodeid][bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ᝿")].bstack11lll11l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l11ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧក"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11llllll1l_opy_: bstack11lllll111_opy_ = _11ll1llll1_opy_[request.node.nodeid][bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧខ")]
            bstack11llllll1l_opy_.bstack11lll11l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l11ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩគ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1l1ll1l1_opy_
        try:
            if not bstack1l1111111_opy_.on() or bstack1ll1l1ll1l1_opy_ != bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪឃ"):
                return
            global bstack1l11111ll1_opy_
            bstack1l11111ll1_opy_.start()
            driver = bstack1l1ll1111_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ង"), None)
            if not _11ll1llll1_opy_.get(request.node.nodeid, None):
                _11ll1llll1_opy_[request.node.nodeid] = {}
            bstack11llllll1l_opy_ = bstack11lllll111_opy_.bstack1lll11l11ll_opy_(
                scenario, feature, request.node,
                name=bstack1lll1llll1l_opy_(request.node, scenario),
                bstack11lll1l1ll_opy_=bstack1l1l1l1l11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l11ll1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪច"),
                tags=bstack1lll1ll1lll_opy_(feature, scenario),
                bstack11lll11l1l_opy_=bstack1l1111111_opy_.bstack11llll111l_opy_(driver) if driver and driver.session_id else {}
            )
            _11ll1llll1_opy_[request.node.nodeid][bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬឆ")] = bstack11llllll1l_opy_
            bstack1ll1l11l111_opy_(bstack11llllll1l_opy_.uuid)
            bstack1l1111111_opy_.bstack11lllll11l_opy_(bstack1l11ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫជ"), bstack11llllll1l_opy_)
        except Exception as err:
            print(bstack1l11ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ឈ"), str(err))
def bstack1ll1l1lll1l_opy_(bstack1ll1l1l1ll1_opy_):
    if bstack1ll1l1l1ll1_opy_ in store[bstack1l11ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩញ")]:
        store[bstack1l11ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪដ")].remove(bstack1ll1l1l1ll1_opy_)
def bstack1ll1l11l111_opy_(bstack1ll1l1lll11_opy_):
    store[bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫឋ")] = bstack1ll1l1lll11_opy_
    threading.current_thread().current_test_uuid = bstack1ll1l1lll11_opy_
@bstack1l1111111_opy_.bstack1ll1lllll11_opy_
def bstack1ll1l11l1l1_opy_(item, call, report):
    global bstack1ll1l1ll1l1_opy_
    bstack11llll1l1_opy_ = bstack1l1l1l1l11_opy_()
    if hasattr(report, bstack1l11ll1_opy_ (u"ࠨࡵࡷࡳࡵ࠭ឌ")):
        bstack11llll1l1_opy_ = bstack111lll1lll_opy_(report.stop)
    elif hasattr(report, bstack1l11ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨឍ")):
        bstack11llll1l1_opy_ = bstack111lll1lll_opy_(report.start)
    try:
        if getattr(report, bstack1l11ll1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨណ"), bstack1l11ll1_opy_ (u"ࠫࠬត")) == bstack1l11ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪថ"):
            bstack1l11111ll1_opy_.reset()
        if getattr(report, bstack1l11ll1_opy_ (u"࠭ࡷࡩࡧࡱࠫទ"), bstack1l11ll1_opy_ (u"ࠧࠨធ")) == bstack1l11ll1_opy_ (u"ࠨࡥࡤࡰࡱ࠭ន"):
            if bstack1ll1l1ll1l1_opy_ == bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩប"):
                _11ll1llll1_opy_[item.nodeid][bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨផ")] = bstack11llll1l1_opy_
                bstack1ll1l1ll111_opy_(item, _11ll1llll1_opy_[item.nodeid], bstack1l11ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ព"), report, call)
                store[bstack1l11ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩភ")] = None
            elif bstack1ll1l1ll1l1_opy_ == bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥម"):
                bstack11llllll1l_opy_ = _11ll1llll1_opy_[item.nodeid][bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪយ")]
                bstack11llllll1l_opy_.set(hooks=_11ll1llll1_opy_[item.nodeid].get(bstack1l11ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧរ"), []))
                exception, bstack11lll1ll11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll1ll11_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨល"), bstack1l11ll1_opy_ (u"ࠪࠫវ"))]
                bstack11llllll1l_opy_.stop(time=bstack11llll1l1_opy_, result=Result(result=getattr(report, bstack1l11ll1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬឝ"), bstack1l11ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬឞ")), exception=exception, bstack11lll1ll11_opy_=bstack11lll1ll11_opy_))
                bstack1l1111111_opy_.bstack11lllll11l_opy_(bstack1l11ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨស"), _11ll1llll1_opy_[item.nodeid][bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪហ")])
        elif getattr(report, bstack1l11ll1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ឡ"), bstack1l11ll1_opy_ (u"ࠩࠪអ")) in [bstack1l11ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩឣ"), bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ឤ")]:
            bstack11lll111l1_opy_ = item.nodeid + bstack1l11ll1_opy_ (u"ࠬ࠳ࠧឥ") + getattr(report, bstack1l11ll1_opy_ (u"࠭ࡷࡩࡧࡱࠫឦ"), bstack1l11ll1_opy_ (u"ࠧࠨឧ"))
            if getattr(report, bstack1l11ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩឨ"), False):
                hook_type = bstack1l11ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧឩ") if getattr(report, bstack1l11ll1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨឪ"), bstack1l11ll1_opy_ (u"ࠫࠬឫ")) == bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫឬ") else bstack1l11ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪឭ")
                _11ll1llll1_opy_[bstack11lll111l1_opy_] = {
                    bstack1l11ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬឮ"): uuid4().__str__(),
                    bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬឯ"): bstack11llll1l1_opy_,
                    bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬឰ"): hook_type
                }
            _11ll1llll1_opy_[bstack11lll111l1_opy_][bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨឱ")] = bstack11llll1l1_opy_
            bstack1ll1l1lll1l_opy_(_11ll1llll1_opy_[bstack11lll111l1_opy_][bstack1l11ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩឲ")])
            bstack1ll1l1l1l1l_opy_(item, _11ll1llll1_opy_[bstack11lll111l1_opy_], bstack1l11ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧឳ"), report, call)
            if getattr(report, bstack1l11ll1_opy_ (u"࠭ࡷࡩࡧࡱࠫ឴"), bstack1l11ll1_opy_ (u"ࠧࠨ឵")) == bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧា"):
                if getattr(report, bstack1l11ll1_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪិ"), bstack1l11ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪី")) == bstack1l11ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫឹ"):
                    bstack11ll1lll1l_opy_ = {
                        bstack1l11ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪឺ"): uuid4().__str__(),
                        bstack1l11ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪុ"): bstack1l1l1l1l11_opy_(),
                        bstack1l11ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬូ"): bstack1l1l1l1l11_opy_()
                    }
                    _11ll1llll1_opy_[item.nodeid] = {**_11ll1llll1_opy_[item.nodeid], **bstack11ll1lll1l_opy_}
                    bstack1ll1l1ll111_opy_(item, _11ll1llll1_opy_[item.nodeid], bstack1l11ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩួ"))
                    bstack1ll1l1ll111_opy_(item, _11ll1llll1_opy_[item.nodeid], bstack1l11ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫើ"), report, call)
    except Exception as err:
        print(bstack1l11ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨឿ"), str(err))
def bstack1ll1l111lll_opy_(test, bstack11ll1lll1l_opy_, result=None, call=None, bstack11l11ll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11llllll1l_opy_ = {
        bstack1l11ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩៀ"): bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪេ")],
        bstack1l11ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫែ"): bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࠬៃ"),
        bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ោ"): test.name,
        bstack1l11ll1_opy_ (u"ࠩࡥࡳࡩࡿࠧៅ"): {
            bstack1l11ll1_opy_ (u"ࠪࡰࡦࡴࡧࠨំ"): bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫះ"),
            bstack1l11ll1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪៈ"): inspect.getsource(test.obj)
        },
        bstack1l11ll1_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ៉"): test.name,
        bstack1l11ll1_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭៊"): test.name,
        bstack1l11ll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ់"): bstack1l11ll11ll_opy_.bstack11llll1l11_opy_(test),
        bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ៌"): file_path,
        bstack1l11ll1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ៍"): file_path,
        bstack1l11ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ៎"): bstack1l11ll1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭៏"),
        bstack1l11ll1_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ័"): file_path,
        bstack1l11ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ៑"): bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸ្ࠬ")],
        bstack1l11ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ៓"): bstack1l11ll1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ។"),
        bstack1l11ll1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ៕"): {
            bstack1l11ll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ៖"): test.nodeid
        },
        bstack1l11ll1_opy_ (u"࠭ࡴࡢࡩࡶࠫៗ"): bstack111lllllll_opy_(test.own_markers)
    }
    if bstack11l11ll1_opy_ in [bstack1l11ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ៘"), bstack1l11ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ៙")]:
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠩࡰࡩࡹࡧࠧ៚")] = {
            bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ៛"): bstack11ll1lll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ៜ"), [])
        }
    if bstack11l11ll1_opy_ == bstack1l11ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭៝"):
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭៞")] = bstack1l11ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ៟")
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ០")] = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ១")]
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ២")] = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ៣")]
    if result:
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ៤")] = result.outcome
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ៥")] = result.duration * 1000
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ៦")] = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭៧")]
        if result.failed:
            bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ៨")] = bstack1l1111111_opy_.bstack11ll1111l1_opy_(call.excinfo.typename)
            bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ៩")] = bstack1l1111111_opy_.bstack1ll1lll1ll1_opy_(call.excinfo, result)
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ៪")] = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ៫")]
    if outcome:
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭៬")] = bstack111lll1ll1_opy_(outcome)
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ៭")] = 0
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭៮")] = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ៯")]
        if bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ៰")] == bstack1l11ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ៱"):
            bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ៲")] = bstack1l11ll1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ៳")  # bstack1ll1l111ll1_opy_
            bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ៴")] = [{bstack1l11ll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ៵"): [bstack1l11ll1_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭៶")]}]
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ៷")] = bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ៸")]
    return bstack11llllll1l_opy_
def bstack1ll1l11ll1l_opy_(test, bstack1l1111l1ll_opy_, bstack11l11ll1_opy_, result, call, outcome, bstack1ll1l1l1lll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ៹")]
    hook_name = bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ៺")]
    hook_data = {
        bstack1l11ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៻"): bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭៼")],
        bstack1l11ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ៽"): bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ៾"),
        bstack1l11ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ៿"): bstack1l11ll1_opy_ (u"ࠬࢁࡽࠨ᠀").format(bstack1lll1lllll1_opy_(hook_name)),
        bstack1l11ll1_opy_ (u"࠭ࡢࡰࡦࡼࠫ᠁"): {
            bstack1l11ll1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ᠂"): bstack1l11ll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ᠃"),
            bstack1l11ll1_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ᠄"): None
        },
        bstack1l11ll1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ᠅"): test.name,
        bstack1l11ll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ᠆"): bstack1l11ll11ll_opy_.bstack11llll1l11_opy_(test, hook_name),
        bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ᠇"): file_path,
        bstack1l11ll1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ᠈"): file_path,
        bstack1l11ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᠉"): bstack1l11ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ᠊"),
        bstack1l11ll1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ᠋"): file_path,
        bstack1l11ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᠌"): bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᠍")],
        bstack1l11ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᠎"): bstack1l11ll1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ᠏") if bstack1ll1l1ll1l1_opy_ == bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ᠐") else bstack1l11ll1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ᠑"),
        bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᠒"): hook_type
    }
    bstack1ll1l11ll11_opy_ = bstack11ll1l1l1l_opy_(_11ll1llll1_opy_.get(test.nodeid, None))
    if bstack1ll1l11ll11_opy_:
        hook_data[bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ᠓")] = bstack1ll1l11ll11_opy_
    if result:
        hook_data[bstack1l11ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᠔")] = result.outcome
        hook_data[bstack1l11ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭᠕")] = result.duration * 1000
        hook_data[bstack1l11ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᠖")] = bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᠗")]
        if result.failed:
            hook_data[bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᠘")] = bstack1l1111111_opy_.bstack11ll1111l1_opy_(call.excinfo.typename)
            hook_data[bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᠙")] = bstack1l1111111_opy_.bstack1ll1lll1ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l11ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᠚")] = bstack111lll1ll1_opy_(outcome)
        hook_data[bstack1l11ll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᠛")] = 100
        hook_data[bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᠜")] = bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᠝")]
        if hook_data[bstack1l11ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᠞")] == bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᠟"):
            hook_data[bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᠠ")] = bstack1l11ll1_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᠡ")  # bstack1ll1l111ll1_opy_
            hook_data[bstack1l11ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᠢ")] = [{bstack1l11ll1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᠣ"): [bstack1l11ll1_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᠤ")]}]
    if bstack1ll1l1l1lll_opy_:
        hook_data[bstack1l11ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᠥ")] = bstack1ll1l1l1lll_opy_.result
        hook_data[bstack1l11ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᠦ")] = bstack1111lllll1_opy_(bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᠧ")], bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᠨ")])
        hook_data[bstack1l11ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᠩ")] = bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᠪ")]
        if hook_data[bstack1l11ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᠫ")] == bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᠬ"):
            hook_data[bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᠭ")] = bstack1l1111111_opy_.bstack11ll1111l1_opy_(bstack1ll1l1l1lll_opy_.exception_type)
            hook_data[bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᠮ")] = [{bstack1l11ll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᠯ"): bstack1111ll1l11_opy_(bstack1ll1l1l1lll_opy_.exception)}]
    return hook_data
def bstack1ll1l1ll111_opy_(test, bstack11ll1lll1l_opy_, bstack11l11ll1_opy_, result=None, call=None, outcome=None):
    bstack11llllll1l_opy_ = bstack1ll1l111lll_opy_(test, bstack11ll1lll1l_opy_, result, call, bstack11l11ll1_opy_, outcome)
    driver = getattr(test, bstack1l11ll1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᠰ"), None)
    if bstack11l11ll1_opy_ == bstack1l11ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᠱ") and driver:
        bstack11llllll1l_opy_[bstack1l11ll1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᠲ")] = bstack1l1111111_opy_.bstack11llll111l_opy_(driver)
    if bstack11l11ll1_opy_ == bstack1l11ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᠳ"):
        bstack11l11ll1_opy_ = bstack1l11ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᠴ")
    bstack11lll11ll1_opy_ = {
        bstack1l11ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᠵ"): bstack11l11ll1_opy_,
        bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᠶ"): bstack11llllll1l_opy_
    }
    bstack1l1111111_opy_.bstack11ll1ll111_opy_(bstack11lll11ll1_opy_)
def bstack1ll1l1l1l1l_opy_(test, bstack11ll1lll1l_opy_, bstack11l11ll1_opy_, result=None, call=None, outcome=None, bstack1ll1l1l1lll_opy_=None):
    hook_data = bstack1ll1l11ll1l_opy_(test, bstack11ll1lll1l_opy_, bstack11l11ll1_opy_, result, call, outcome, bstack1ll1l1l1lll_opy_)
    bstack11lll11ll1_opy_ = {
        bstack1l11ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᠷ"): bstack11l11ll1_opy_,
        bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᠸ"): hook_data
    }
    bstack1l1111111_opy_.bstack11ll1ll111_opy_(bstack11lll11ll1_opy_)
def bstack11ll1l1l1l_opy_(bstack11ll1lll1l_opy_):
    if not bstack11ll1lll1l_opy_:
        return None
    if bstack11ll1lll1l_opy_.get(bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᠹ"), None):
        return getattr(bstack11ll1lll1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᠺ")], bstack1l11ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᠻ"), None)
    return bstack11ll1lll1l_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᠼ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l1111111_opy_.on():
            return
        places = [bstack1l11ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᠽ"), bstack1l11ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᠾ"), bstack1l11ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᠿ")]
        bstack11lll1111l_opy_ = []
        for bstack1ll11lllll1_opy_ in places:
            records = caplog.get_records(bstack1ll11lllll1_opy_)
            bstack1ll1l111l11_opy_ = bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᡀ") if bstack1ll11lllll1_opy_ == bstack1l11ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᡁ") else bstack1l11ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᡂ")
            bstack1ll1l1ll11l_opy_ = request.node.nodeid + (bstack1l11ll1_opy_ (u"ࠩࠪᡃ") if bstack1ll11lllll1_opy_ == bstack1l11ll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᡄ") else bstack1l11ll1_opy_ (u"ࠫ࠲࠭ᡅ") + bstack1ll11lllll1_opy_)
            bstack1ll1l1lll11_opy_ = bstack11ll1l1l1l_opy_(_11ll1llll1_opy_.get(bstack1ll1l1ll11l_opy_, None))
            if not bstack1ll1l1lll11_opy_:
                continue
            for record in records:
                if bstack111ll1llll_opy_(record.message):
                    continue
                bstack11lll1111l_opy_.append({
                    bstack1l11ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᡆ"): bstack1111ll1l1l_opy_(record.created).isoformat() + bstack1l11ll1_opy_ (u"࡚࠭ࠨᡇ"),
                    bstack1l11ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᡈ"): record.levelname,
                    bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡉ"): record.message,
                    bstack1ll1l111l11_opy_: bstack1ll1l1lll11_opy_
                })
        if len(bstack11lll1111l_opy_) > 0:
            bstack1l1111111_opy_.bstack1l1l1ll11l_opy_(bstack11lll1111l_opy_)
    except Exception as err:
        print(bstack1l11ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ᡊ"), str(err))
def bstack1llll111l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l11lll1l_opy_
    bstack1l11ll1ll_opy_ = bstack1l1ll1111_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᡋ"), None) and bstack1l1ll1111_opy_(
            threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᡌ"), None)
    bstack1111lll1_opy_ = getattr(driver, bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᡍ"), None) != None and getattr(driver, bstack1l11ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᡎ"), None) == True
    if sequence == bstack1l11ll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᡏ") and driver != None:
      if not bstack1l11lll1l_opy_ and bstack1111lll1l1_opy_() and bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᡐ") in CONFIG and CONFIG[bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᡑ")] == True and bstack1ll11l1l1l_opy_.bstack1111ll1l1_opy_(driver_command) and (bstack1111lll1_opy_ or bstack1l11ll1ll_opy_) and not bstack11111l1l1_opy_(args):
        try:
          bstack1l11lll1l_opy_ = True
          logger.debug(bstack1l11ll1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬᡒ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l11ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩᡓ").format(str(err)))
        bstack1l11lll1l_opy_ = False
    if sequence == bstack1l11ll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᡔ"):
        if driver_command == bstack1l11ll1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᡕ"):
            bstack1l1111111_opy_.bstack1ll1l1111l_opy_({
                bstack1l11ll1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᡖ"): response[bstack1l11ll1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᡗ")],
                bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᡘ"): store[bstack1l11ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᡙ")]
            })
def bstack11l1l111_opy_():
    global bstack1llll11ll1_opy_
    bstack11ll1ll1l_opy_.bstack1l1ll11ll1_opy_()
    logging.shutdown()
    bstack1l1111111_opy_.bstack11ll1lll11_opy_()
    for driver in bstack1llll11ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11llll11_opy_(*args):
    global bstack1llll11ll1_opy_
    bstack1l1111111_opy_.bstack11ll1lll11_opy_()
    for driver in bstack1llll11ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l1lll_opy_(self, *args, **kwargs):
    bstack11l1111l1_opy_ = bstack1l1lll1l1l_opy_(self, *args, **kwargs)
    bstack1l1111111_opy_.bstack1l1l111ll1_opy_(self)
    return bstack11l1111l1_opy_
def bstack1llll1lll_opy_(framework_name):
    global bstack1l1l1lll_opy_
    global bstack1l111l1ll1_opy_
    bstack1l1l1lll_opy_ = framework_name
    logger.info(bstack1l1l11lll_opy_.format(bstack1l1l1lll_opy_.split(bstack1l11ll1_opy_ (u"ࠫ࠲࠭ᡚ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1111lll1l1_opy_():
            Service.start = bstack1lllll1ll_opy_
            Service.stop = bstack11l1ll111_opy_
            webdriver.Remote.__init__ = bstack1ll1l1llll_opy_
            webdriver.Remote.get = bstack1l1ll11lll_opy_
            if not isinstance(os.getenv(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᡛ")), str):
                return
            WebDriver.close = bstack11l1l1ll1_opy_
            WebDriver.quit = bstack1llll1l1ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1111lll1l1_opy_() and bstack1l1111111_opy_.on():
            webdriver.Remote.__init__ = bstack1lll1l1lll_opy_
        bstack1l111l1ll1_opy_ = True
    except Exception as e:
        pass
    bstack1l1lllll_opy_()
    if os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᡜ")):
        bstack1l111l1ll1_opy_ = eval(os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᡝ")))
    if not bstack1l111l1ll1_opy_:
        bstack1l11111ll_opy_(bstack1l11ll1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᡞ"), bstack1l1l11ll_opy_)
    if bstack1l1l11111l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll11l111_opy_
        except Exception as e:
            logger.error(bstack1llllll111_opy_.format(str(e)))
    if bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᡟ") in str(framework_name).lower():
        if not bstack1111lll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1ll1l1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1111111l_opy_
            Config.getoption = bstack1l1ll11111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1l1l11ll_opy_
        except Exception as e:
            pass
def bstack1llll1l1ll_opy_(self):
    global bstack1l1l1lll_opy_
    global bstack1llll1l111_opy_
    global bstack1111111ll_opy_
    try:
        if bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᡠ") in bstack1l1l1lll_opy_ and self.session_id != None and bstack1l1ll1111_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᡡ"), bstack1l11ll1_opy_ (u"ࠬ࠭ᡢ")) != bstack1l11ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᡣ"):
            bstack11l1l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᡤ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᡥ")
            bstack1ll11l1l_opy_(logger, True)
            if self != None:
                bstack1l1llll11_opy_(self, bstack11l1l1l1l_opy_, bstack1l11ll1_opy_ (u"ࠩ࠯ࠤࠬᡦ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1l11ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᡧ"), None)
        if item is not None and bstack1ll1l1l1l11_opy_:
            bstack111111l11_opy_.bstack1l11lll11_opy_(self, bstack1ll11l111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l11ll1_opy_ (u"ࠫࠬᡨ")
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨᡩ") + str(e))
    bstack1111111ll_opy_(self)
    self.session_id = None
def bstack1ll1l1llll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll1l111_opy_
    global bstack1l1ll1l11l_opy_
    global bstack1ll1lll11_opy_
    global bstack1l1l1lll_opy_
    global bstack1l1lll1l1l_opy_
    global bstack1llll11ll1_opy_
    global bstack1l1ll1l111_opy_
    global bstack1ll1l1l111_opy_
    global bstack1ll1l1l1l11_opy_
    global bstack1ll11l111_opy_
    CONFIG[bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᡪ")] = str(bstack1l1l1lll_opy_) + str(__version__)
    command_executor = bstack11l11l11l_opy_(bstack1l1ll1l111_opy_)
    logger.debug(bstack1ll1ll1ll1_opy_.format(command_executor))
    proxy = bstack11llll1ll_opy_(CONFIG, proxy)
    bstack11l111l1l_opy_ = 0
    try:
        if bstack1ll1lll11_opy_ is True:
            bstack11l111l1l_opy_ = int(os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᡫ")))
    except:
        bstack11l111l1l_opy_ = 0
    bstack111lll1l1_opy_ = bstack11l1l11l_opy_(CONFIG, bstack11l111l1l_opy_)
    logger.debug(bstack1l1ll1111l_opy_.format(str(bstack111lll1l1_opy_)))
    bstack1ll11l111_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᡬ"))[bstack11l111l1l_opy_]
    if bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᡭ") in CONFIG and CONFIG[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᡮ")]:
        bstack111ll1111_opy_(bstack111lll1l1_opy_, bstack1ll1l1l111_opy_)
    if bstack1l1l1l11l1_opy_.bstack1llll1l1_opy_(CONFIG, bstack11l111l1l_opy_) and bstack1l1l1l11l1_opy_.bstack1l1lllllll_opy_(bstack111lll1l1_opy_, options, desired_capabilities):
        bstack1ll1l1l1l11_opy_ = True
        bstack1l1l1l11l1_opy_.set_capabilities(bstack111lll1l1_opy_, CONFIG)
    if desired_capabilities:
        bstack111l11ll1_opy_ = bstack1ll1l11lll_opy_(desired_capabilities)
        bstack111l11ll1_opy_[bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᡯ")] = bstack11ll11l1_opy_(CONFIG)
        bstack1l1lll11l1_opy_ = bstack11l1l11l_opy_(bstack111l11ll1_opy_)
        if bstack1l1lll11l1_opy_:
            bstack111lll1l1_opy_ = update(bstack1l1lll11l1_opy_, bstack111lll1l1_opy_)
        desired_capabilities = None
    if options:
        bstack1l1llll1l1_opy_(options, bstack111lll1l1_opy_)
    if not options:
        options = bstack1l1lll111l_opy_(bstack111lll1l1_opy_)
    if proxy and bstack1llll1111l_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᡰ")):
        options.proxy(proxy)
    if options and bstack1llll1111l_opy_() >= version.parse(bstack1l11ll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᡱ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1llll1111l_opy_() < version.parse(bstack1l11ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᡲ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack111lll1l1_opy_)
    logger.info(bstack1l1ll1ll1_opy_)
    if bstack1llll1111l_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᡳ")):
        bstack1l1lll1l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1111l_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᡴ")):
        bstack1l1lll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1111l_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᡵ")):
        bstack1l1lll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1lll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1ll11ll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠫࠬᡶ")
        if bstack1llll1111l_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ᡷ")):
            bstack1ll11ll1l1_opy_ = self.caps.get(bstack1l11ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᡸ"))
        else:
            bstack1ll11ll1l1_opy_ = self.capabilities.get(bstack1l11ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ᡹"))
        if bstack1ll11ll1l1_opy_:
            bstack1111ll11_opy_(bstack1ll11ll1l1_opy_)
            if bstack1llll1111l_opy_() <= version.parse(bstack1l11ll1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ᡺")):
                self.command_executor._url = bstack1l11ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ᡻") + bstack1l1ll1l111_opy_ + bstack1l11ll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ᡼")
            else:
                self.command_executor._url = bstack1l11ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ᡽") + bstack1ll11ll1l1_opy_ + bstack1l11ll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ᡾")
            logger.debug(bstack11l1lll11_opy_.format(bstack1ll11ll1l1_opy_))
        else:
            logger.debug(bstack1l11l1l1ll_opy_.format(bstack1l11ll1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ᡿")))
    except Exception as e:
        logger.debug(bstack1l11l1l1ll_opy_.format(e))
    bstack1llll1l111_opy_ = self.session_id
    if bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᢀ") in bstack1l1l1lll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l11ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᢁ"), None)
        if item:
            bstack1ll1l1l11ll_opy_ = getattr(item, bstack1l11ll1_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧᢂ"), False)
            if not getattr(item, bstack1l11ll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᢃ"), None) and bstack1ll1l1l11ll_opy_:
                setattr(store[bstack1l11ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᢄ")], bstack1l11ll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᢅ"), self)
        bstack1l1111111_opy_.bstack1l1l111ll1_opy_(self)
    bstack1llll11ll1_opy_.append(self)
    if bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᢆ") in CONFIG and bstack1l11ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᢇ") in CONFIG[bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᢈ")][bstack11l111l1l_opy_]:
        bstack1l1ll1l11l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᢉ")][bstack11l111l1l_opy_][bstack1l11ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᢊ")]
    logger.debug(bstack1l1ll1l1l1_opy_.format(bstack1llll1l111_opy_))
def bstack1l1ll11lll_opy_(self, url):
    global bstack1ll1l1l1_opy_
    global CONFIG
    try:
        bstack111ll11l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll1111l11_opy_.format(str(err)))
    try:
        bstack1ll1l1l1_opy_(self, url)
    except Exception as e:
        try:
            bstack111l11l11_opy_ = str(e)
            if any(err_msg in bstack111l11l11_opy_ for err_msg in bstack11111ll1l_opy_):
                bstack111ll11l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll1111l11_opy_.format(str(err)))
        raise e
def bstack1l1l1lll1l_opy_(item, when):
    global bstack1l111l1ll_opy_
    try:
        bstack1l111l1ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1l1l11ll_opy_(item, call, rep):
    global bstack1ll1111l1_opy_
    global bstack1llll11ll1_opy_
    name = bstack1l11ll1_opy_ (u"ࠫࠬᢋ")
    try:
        if rep.when == bstack1l11ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᢌ"):
            bstack1llll1l111_opy_ = threading.current_thread().bstackSessionId
            bstack1ll1l111l1l_opy_ = item.config.getoption(bstack1l11ll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᢍ"))
            try:
                if (str(bstack1ll1l111l1l_opy_).lower() != bstack1l11ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬᢎ")):
                    name = str(rep.nodeid)
                    bstack11l11lll_opy_ = bstack11l111lll_opy_(bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᢏ"), name, bstack1l11ll1_opy_ (u"ࠩࠪᢐ"), bstack1l11ll1_opy_ (u"ࠪࠫᢑ"), bstack1l11ll1_opy_ (u"ࠫࠬᢒ"), bstack1l11ll1_opy_ (u"ࠬ࠭ᢓ"))
                    os.environ[bstack1l11ll1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᢔ")] = name
                    for driver in bstack1llll11ll1_opy_:
                        if bstack1llll1l111_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11lll_opy_)
            except Exception as e:
                logger.debug(bstack1l11ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧᢕ").format(str(e)))
            try:
                bstack1lll111ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l11ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᢖ"):
                    status = bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᢗ") if rep.outcome.lower() == bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᢘ") else bstack1l11ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᢙ")
                    reason = bstack1l11ll1_opy_ (u"ࠬ࠭ᢚ")
                    if status == bstack1l11ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᢛ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l11ll1_opy_ (u"ࠧࡪࡰࡩࡳࠬᢜ") if status == bstack1l11ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᢝ") else bstack1l11ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᢞ")
                    data = name + bstack1l11ll1_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬᢟ") if status == bstack1l11ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᢠ") else name + bstack1l11ll1_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨᢡ") + reason
                    bstack111l111l_opy_ = bstack11l111lll_opy_(bstack1l11ll1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᢢ"), bstack1l11ll1_opy_ (u"ࠧࠨᢣ"), bstack1l11ll1_opy_ (u"ࠨࠩᢤ"), bstack1l11ll1_opy_ (u"ࠩࠪᢥ"), level, data)
                    for driver in bstack1llll11ll1_opy_:
                        if bstack1llll1l111_opy_ == driver.session_id:
                            driver.execute_script(bstack111l111l_opy_)
            except Exception as e:
                logger.debug(bstack1l11ll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧᢦ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨᢧ").format(str(e)))
    bstack1ll1111l1_opy_(item, call, rep)
notset = Notset()
def bstack1l1ll11111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll111lll1_opy_
    if str(name).lower() == bstack1l11ll1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬᢨ"):
        return bstack1l11ll1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ᢩࠧ")
    else:
        return bstack1ll111lll1_opy_(self, name, default, skip)
def bstack1lll11l111_opy_(self):
    global CONFIG
    global bstack1111ll1ll_opy_
    try:
        proxy = bstack1l1l11l1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l11ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᢪ")):
                proxies = bstack111l11lll_opy_(proxy, bstack11l11l11l_opy_())
                if len(proxies) > 0:
                    protocol, bstack11111111l_opy_ = proxies.popitem()
                    if bstack1l11ll1_opy_ (u"ࠣ࠼࠲࠳ࠧ᢫") in bstack11111111l_opy_:
                        return bstack11111111l_opy_
                    else:
                        return bstack1l11ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ᢬") + bstack11111111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l11ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ᢭").format(str(e)))
    return bstack1111ll1ll_opy_(self)
def bstack1l1l11111l_opy_():
    return (bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᢮") in CONFIG or bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᢯") in CONFIG) and bstack1l11llll11_opy_() and bstack1llll1111l_opy_() >= version.parse(
        bstack11lll11l_opy_)
def bstack1l11ll11l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1ll1l11l_opy_
    global bstack1ll1lll11_opy_
    global bstack1l1l1lll_opy_
    CONFIG[bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᢰ")] = str(bstack1l1l1lll_opy_) + str(__version__)
    bstack11l111l1l_opy_ = 0
    try:
        if bstack1ll1lll11_opy_ is True:
            bstack11l111l1l_opy_ = int(os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᢱ")))
    except:
        bstack11l111l1l_opy_ = 0
    CONFIG[bstack1l11ll1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᢲ")] = True
    bstack111lll1l1_opy_ = bstack11l1l11l_opy_(CONFIG, bstack11l111l1l_opy_)
    logger.debug(bstack1l1ll1111l_opy_.format(str(bstack111lll1l1_opy_)))
    if CONFIG.get(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᢳ")):
        bstack111ll1111_opy_(bstack111lll1l1_opy_, bstack1ll1l1l111_opy_)
    if bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᢴ") in CONFIG and bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᢵ") in CONFIG[bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᢶ")][bstack11l111l1l_opy_]:
        bstack1l1ll1l11l_opy_ = CONFIG[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᢷ")][bstack11l111l1l_opy_][bstack1l11ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᢸ")]
    import urllib
    import json
    bstack11l11l1l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪᢹ") + urllib.parse.quote(json.dumps(bstack111lll1l1_opy_))
    browser = self.connect(bstack11l11l1l_opy_)
    return browser
def bstack1l1lllll_opy_():
    global bstack1l111l1ll1_opy_
    global bstack1l1l1lll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1l1l1ll_opy_
        if not bstack1111lll1l1_opy_():
            global bstack1ll11111_opy_
            if not bstack1ll11111_opy_:
                from bstack_utils.helper import bstack1l1l1l1lll_opy_, bstack1l11l1l111_opy_
                bstack1ll11111_opy_ = bstack1l1l1l1lll_opy_()
                bstack1l11l1l111_opy_(bstack1l1l1lll_opy_)
            BrowserType.connect = bstack1ll1l1l1ll_opy_
            return
        BrowserType.launch = bstack1l11ll11l_opy_
        bstack1l111l1ll1_opy_ = True
    except Exception as e:
        pass
def bstack1ll11llllll_opy_():
    global CONFIG
    global bstack1ll11l1ll1_opy_
    global bstack1l1ll1l111_opy_
    global bstack1ll1l1l111_opy_
    global bstack1ll1lll11_opy_
    global bstack1l11l111ll_opy_
    CONFIG = json.loads(os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨᢺ")))
    bstack1ll11l1ll1_opy_ = eval(os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᢻ")))
    bstack1l1ll1l111_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫᢼ"))
    bstack1llll11l11_opy_(CONFIG, bstack1ll11l1ll1_opy_)
    bstack1l11l111ll_opy_ = bstack11ll1ll1l_opy_.bstack1l111ll1ll_opy_(CONFIG, bstack1l11l111ll_opy_)
    global bstack1l1lll1l1l_opy_
    global bstack1111111ll_opy_
    global bstack11ll11111_opy_
    global bstack1ll11llll1_opy_
    global bstack1l111l1l1_opy_
    global bstack1lllllll11_opy_
    global bstack111l111l1_opy_
    global bstack1ll1l1l1_opy_
    global bstack1111ll1ll_opy_
    global bstack1ll111lll1_opy_
    global bstack1l111l1ll_opy_
    global bstack1ll1111l1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1lll1l1l_opy_ = webdriver.Remote.__init__
        bstack1111111ll_opy_ = WebDriver.quit
        bstack111l111l1_opy_ = WebDriver.close
        bstack1ll1l1l1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᢽ") in CONFIG or bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᢾ") in CONFIG) and bstack1l11llll11_opy_():
        if bstack1llll1111l_opy_() < version.parse(bstack11lll11l_opy_):
            logger.error(bstack1llllll1l_opy_.format(bstack1llll1111l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1111ll1ll_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1llllll111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll111lll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1l111l1ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack111l11ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll1111l1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨᢿ"))
    bstack1ll1l1l111_opy_ = CONFIG.get(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᣀ"), {}).get(bstack1l11ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᣁ"))
    bstack1ll1lll11_opy_ = True
    bstack1llll1lll_opy_(bstack1lll11ll11_opy_)
if (bstack111l11ll11_opy_()):
    bstack1ll11llllll_opy_()
@bstack11llll11l1_opy_(class_method=False)
def bstack1ll1l1l111l_opy_(hook_name, event, bstack1ll1l1l1111_opy_=None):
    if hook_name not in [bstack1l11ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᣂ"), bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᣃ"), bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᣄ"), bstack1l11ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᣅ"), bstack1l11ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᣆ"), bstack1l11ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᣇ"), bstack1l11ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᣈ"), bstack1l11ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᣉ")]:
        return
    node = store[bstack1l11ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᣊ")]
    if hook_name in [bstack1l11ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᣋ"), bstack1l11ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᣌ")]:
        node = store[bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᣍ")]
    elif hook_name in [bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᣎ"), bstack1l11ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᣏ")]:
        node = store[bstack1l11ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᣐ")]
    if event == bstack1l11ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᣑ"):
        hook_type = bstack1lll1lll11l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l1111l1ll_opy_ = {
            bstack1l11ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᣒ"): uuid,
            bstack1l11ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᣓ"): bstack1l1l1l1l11_opy_(),
            bstack1l11ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬᣔ"): bstack1l11ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᣕ"),
            bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᣖ"): hook_type,
            bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᣗ"): hook_name
        }
        store[bstack1l11ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᣘ")].append(uuid)
        bstack1ll1l11llll_opy_ = node.nodeid
        if hook_type == bstack1l11ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᣙ"):
            if not _11ll1llll1_opy_.get(bstack1ll1l11llll_opy_, None):
                _11ll1llll1_opy_[bstack1ll1l11llll_opy_] = {bstack1l11ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᣚ"): []}
            _11ll1llll1_opy_[bstack1ll1l11llll_opy_][bstack1l11ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᣛ")].append(bstack1l1111l1ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᣜ")])
        _11ll1llll1_opy_[bstack1ll1l11llll_opy_ + bstack1l11ll1_opy_ (u"ࠩ࠰ࠫᣝ") + hook_name] = bstack1l1111l1ll_opy_
        bstack1ll1l1l1l1l_opy_(node, bstack1l1111l1ll_opy_, bstack1l11ll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᣞ"))
    elif event == bstack1l11ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᣟ"):
        bstack11lll111l1_opy_ = node.nodeid + bstack1l11ll1_opy_ (u"ࠬ࠳ࠧᣠ") + hook_name
        _11ll1llll1_opy_[bstack11lll111l1_opy_][bstack1l11ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᣡ")] = bstack1l1l1l1l11_opy_()
        bstack1ll1l1lll1l_opy_(_11ll1llll1_opy_[bstack11lll111l1_opy_][bstack1l11ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᣢ")])
        bstack1ll1l1l1l1l_opy_(node, _11ll1llll1_opy_[bstack11lll111l1_opy_], bstack1l11ll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᣣ"), bstack1ll1l1l1lll_opy_=bstack1ll1l1l1111_opy_)
def bstack1ll11lll1ll_opy_():
    global bstack1ll1l1ll1l1_opy_
    if bstack1l111111_opy_():
        bstack1ll1l1ll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᣤ")
    else:
        bstack1ll1l1ll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᣥ")
@bstack1l1111111_opy_.bstack1ll1lllll11_opy_
def bstack1ll1l1ll1ll_opy_():
    bstack1ll11lll1ll_opy_()
    if bstack1l11llll11_opy_():
        bstack1lllll111l_opy_(bstack1llll111l1_opy_)
    try:
        bstack1111l1l1l1_opy_(bstack1ll1l1l111l_opy_)
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧᣦ").format(e))
bstack1ll1l1ll1ll_opy_()
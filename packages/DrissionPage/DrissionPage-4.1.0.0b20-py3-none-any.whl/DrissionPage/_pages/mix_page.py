# -*- coding:utf-8 -*-
"""
@Author   : g1879
@Contact  : g1879@qq.com
@Copyright: (c) 2024 by g1879, Inc. All Rights Reserved.
@License  : BSD 3-Clause.
"""
from .chromium_page import ChromiumPage
from .session_page import SessionPage
from .._base.base import BasePage
from .._configs.chromium_options import ChromiumOptions
from .._functions.cookies import set_session_cookies, set_tab_cookies
from .._functions.settings import Settings
from .._units.setter import MixPageSetter


class MixPage(SessionPage, ChromiumPage, BasePage):
    """整合浏览器和request的页面类"""

    def __new__(cls, mode='d', timeout=None, chromium_options=None, session_or_options=None):
        """初始化函数
        :param mode: 'd' 或 's'，即driver模式和session模式
        :param timeout: 超时时间（秒），d模式时为寻找元素时间，s模式时为连接时间，默认10秒
        :param chromium_options: Driver对象，只使用s模式时应传入False
        :param session_or_options: Session对象或SessionOptions对象，只使用d模式时应传入False
        """
        return super().__new__(cls, chromium_options)

    def __init__(self, mode='d', timeout=None, chromium_options=None, session_or_options=None):
        if hasattr(self, '_created'):
            return

        self._mode = mode.lower()
        if self._mode not in ('s', 'd'):
            raise ValueError('mode参数只能是s或d。')
        self._has_driver = True
        self._has_session = True

        super().__init__(session_or_options=session_or_options)
        if not chromium_options:
            chromium_options = ChromiumOptions(read_file=chromium_options)
            chromium_options.set_timeouts(base=self._timeout).set_paths(download_path=self.download_path)
        super(SessionPage, self).__init__(addr_or_opts=chromium_options, timeout=timeout)
        self._type = 'MixPage'
        self.change_mode(self._mode, go=False, copy_cookies=False)

    def __call__(self, locator, index=1, timeout=None):
        if self._mode == 'd':
            return super(SessionPage, self).__call__(locator, index=index, timeout=timeout)
        elif self._mode == 's':
            return super().__call__(locator, index=index)

    @property
    def latest_tab(self):
        return self.browser.get_mix_tab(self.tab_ids[0], as_id=not Settings.singleton_tab_obj)

    @property
    def set(self):
        if self._set is None:
            self._set = MixPageSetter(self)
        return self._set

    @property
    def url(self):
        if self._mode == 'd':
            return self._browser_url
        elif self._mode == 's':
            return self._session_url

    @property
    def _browser_url(self):
        return super(SessionPage, self).url if self._driver else None

    @property
    def title(self):
        if self._mode == 's':
            return super().title
        elif self._mode == 'd':
            return super(SessionPage, self).title

    @property
    def raw_data(self):
        if self._mode == 's':
            return super().raw_data
        elif self._mode == 'd':
            return super(SessionPage, self).html if self._has_driver else ''

    @property
    def html(self):
        if self._mode == 's':
            return super().html
        elif self._mode == 'd':
            return super(SessionPage, self).html if self._has_driver else ''

    @property
    def json(self):
        if self._mode == 's':
            return super().json
        elif self._mode == 'd':
            return super(SessionPage, self).json

    @property
    def response(self):
        return self._response

    @property
    def mode(self):
        return self._mode

    @property
    def user_agent(self):
        if self._mode == 's':
            return super().user_agent
        elif self._mode == 'd':
            return super(SessionPage, self).user_agent

    @property
    def session(self):
        if self._session is None:
            self._create_session()
        return self._session

    @property
    def _session_url(self):
        return self._response.url if self._response else None

    @property
    def timeout(self):
        return self._timeout if self._mode == 's' else self.timeouts.base

    def get(self, url, show_errmsg=False, retry=None, interval=None, timeout=None, **kwargs):
        if self._mode == 'd':
            return super(SessionPage, self).get(url, show_errmsg, retry, interval, timeout)
        elif self._mode == 's':
            if timeout is None:
                timeout = self.timeouts.page_load if self._has_driver else self.timeout
            return super().get(url, show_errmsg, retry, interval, timeout, **kwargs)

    def post(self, url, show_errmsg=False, retry=None, interval=None, **kwargs):
        if self.mode == 'd':
            self.cookies_to_session()
            super().post(url, show_errmsg, retry, interval, **kwargs)
            return self.response
        return super().post(url, show_errmsg, retry, interval, **kwargs)

    def ele(self, locator, index=1, timeout=None):
        if self._mode == 's':
            return super().ele(locator, index=index)
        elif self._mode == 'd':
            return super(SessionPage, self).ele(locator, index=index, timeout=timeout)

    def eles(self, locator, timeout=None):
        if self._mode == 's':
            return super().eles(locator)
        elif self._mode == 'd':
            return super(SessionPage, self).eles(locator, timeout=timeout)

    def s_ele(self, locator=None, index=1):
        if self._mode == 's':
            return super().s_ele(locator, index=index)
        elif self._mode == 'd':
            return super(SessionPage, self).s_ele(locator, index=index)

    def s_eles(self, locator):
        if self._mode == 's':
            return super().s_eles(locator)
        elif self._mode == 'd':
            return super(SessionPage, self).s_eles(locator)

    def change_mode(self, mode=None, go=True, copy_cookies=True):
        if mode is not None and mode.lower() == self._mode:
            return

        self._mode = 's' if self._mode == 'd' else 'd'

        # s模式转d模式
        if self._mode == 'd':
            if self._driver is None:
                self._connect_browser(self._chromium_options)

            self._url = None if not self._has_driver else super(SessionPage, self).url
            self._has_driver = True

            if self._session_url:
                if copy_cookies:
                    self.cookies_to_browser()

                if go:
                    self.get(self._session_url)

        # d模式转s模式
        elif self._mode == 's':
            self._has_session = True
            self._url = self._session_url

            if self._has_driver:
                if copy_cookies:
                    self.cookies_to_session()

                if go and not self.get(super(SessionPage, self).url):
                    raise ConnectionError('s模式访问失败，请设置go=False，自行构造连接参数进行访问。')

    def cookies_to_session(self, copy_user_agent=True):
        if not self._has_session:
            return

        if copy_user_agent:
            user_agent = self._run_cdp('Runtime.evaluate', expression='navigator.userAgent;')['result']['value']
            self._headers.update({"User-Agent": user_agent})

        set_session_cookies(self.session, super(SessionPage, self).cookies())

    def cookies_to_browser(self):
        if not self._has_driver:
            return
        set_tab_cookies(self, super().cookies())

    def cookies(self, all_domains=False, all_info=False):
        if self._mode == 's':
            return super().cookies(all_domains, all_info)
        elif self._mode == 'd':
            return super(SessionPage, self).cookies(all_domains, all_info)

    def get_tab(self, id_or_num=None, title=None, url=None, tab_type='page', as_id=False):
        return self.browser._get_tab(id_or_num=id_or_num, title=title, url=url,
                                     tab_type=tab_type, mix=True, as_id=as_id)

    def get_tabs(self, title=None, url=None, tab_type='page', as_id=False):
        return self.browser._get_tabs(title=title, url=url, tab_type=tab_type, mix=True, as_id=as_id)

    def new_tab(self, url=None, new_window=False, background=False, new_context=False):
        return self.browser.new_mix_tab(url=url, new_window=new_window, background=background, new_context=new_context)

    def close_driver(self):
        if self._has_driver:
            self.change_mode('s')
            try:
                self.driver.run('Browser.close')
            except Exception:
                pass
            self._driver.stop()
            self._driver = None
            self._has_driver = None

    def close_session(self):
        if self._has_session:
            self.change_mode('d')
            self._session.close()
            if self._response is not None:
                self._response.close()
            self._session = None
            self._response = None
            self._has_session = None

    def close(self):
        if self._has_driver:
            self.close_tabs(self.tab_id)
        if self._session:
            self._session.close()
            if self._response is not None:
                self._response.close()

    def _find_elements(self, locator, timeout=None, index=1, relative=False, raise_err=None):
        if self._mode == 's':
            return super()._find_elements(locator, index=index)
        elif self._mode == 'd':
            return super(SessionPage, self)._find_elements(locator, timeout=timeout, index=index, relative=relative)

    def quit(self, timeout=5, force=True, del_data=False):
        if self._has_session:
            self._session.close()
            self._session = None
            self._response = None
            self._has_session = None
        if self._has_driver:
            super(SessionPage, self).quit(timeout, force, del_data=del_data)
            self._driver = None
            self._has_driver = None

    def __repr__(self):
        return f'<MixPage browser_id={self.browser.id} tab_id={self.tab_id}>'

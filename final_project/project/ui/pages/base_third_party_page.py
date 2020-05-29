from ui.pages.base import BaseActions


class BaseThirdPartyPage(BaseActions):
    active_tab = False

    def get_current_url(self):
        if not self.active_tab:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.active_tab = True
        return self.driver.current_url

    def close_tab(self, home_page_object):
        if self.active_tab:
            base_tab = self.driver.window_handles[0]
            self.driver.close()
            self.driver.switch_to.window(base_tab)
        else:
            default_tab = self.driver.current_window_handle
            flask_page_tab = self.driver.window_handles[-1]
            self.driver.switch_to.window(flask_page_tab)
            self.driver.close()
            self.driver.switch_to.window(default_tab)
        return home_page_object

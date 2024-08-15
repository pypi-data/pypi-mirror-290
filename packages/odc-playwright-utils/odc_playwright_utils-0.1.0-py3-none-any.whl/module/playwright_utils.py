import platform
from playwright.sync_api import sync_playwright

class PlaywrightUtils:
    def __init__(self, page):
        self.page = page

    # 等待元素可见
    def wait_for_element_to_be_visible(self, selector, timeout=10000):
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    # 等待元素可点击
    def wait_for_element_to_be_clickable(self, selector, timeout=10000):
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.wait_for_function(
            "element => !element.disabled",
            self.page.query_selector(selector),
            timeout=timeout
        )

    # 点击元素前等待其可点击
    def click(self, selector):
        # self.wait_for_element_to_be_clickable(selector)
        self.page.click(selector, timeout=20000)

    # 清除文本框内容
    def clear(self, selector):
        self.wait_for_element_to_be_clickable(selector)
        element = self.page.query_selector(selector)
        element.fill("")

    # 输入文本前等待元素可见
    def send_keys(self, selector, text):
        self.wait_for_element_to_be_visible(selector)
        element = self.page.query_selector(selector)
        element.fill(text)

    # 获取文本前等待元素可见
    def get_text(self, selector):
        self.wait_for_element_to_be_visible(selector)
        return self.page.inner_text(selector)

    # 检查元素是否显示
    def is_element_displayed(self, selector):
        try:
            return self.page.is_visible(selector)
        except:
            return False

    # 获取一组元素中的特定元素
    def get_element(self, selector, index):
        elements = self.page.query_selector_all(selector)
        return elements[index]

    # 选择下拉菜单中的选项
    def select_dropdown_option(self, selector, value):
        self.wait_for_element_to_be_visible(selector)
        element = self.page.query_selector(selector)
        element.select_option(value)

    # 检查元素是否存在
    def is_element_present(self, selector):
        try:
            self.page.query_selector(selector)
            return True
        except:
            return False

    # 等待页面导航完成
    def wait_for_navigation(self, url=None, timeout=30000):
        self.page.wait_for_navigation(url=url, timeout=timeout)

    # 滚动到元素可见
    def scroll_to_element(self, selector):
        self.page.evaluate(f'document.querySelector("{selector}").scrollIntoView()')

    # 获取页面的标题
    def get_page_title(self):
        return self.page.title()

    # 获取页面URL
    def get_current_url(self):
        return self.page.url

    # 等待并点击元素
    def wait_and_click(self, selector, timeout=10000):
        self.wait_for_element_to_be_clickable(selector, timeout)
        self.click(selector)

    # 截图
    def take_screenshot(self, path):
        self.page.screenshot(path=path)

    # 上传文件
    def upload_file(self, selector, file_path):
        self.wait_for_element_to_be_visible(selector)
        self.page.set_input_files(selector, file_path)

    # 执行JavaScript代码
    def execute_script(self, script):
        return self.page.evaluate(script)

    # 获取元素属性
    def get_element_attribute(self, selector, attribute):
        self.wait_for_element_to_be_visible(selector)
        element = self.page.query_selector(selector)
        return element.get_attribute(attribute)

    # 等待元素不可见
    def wait_for_element_to_be_hidden(self, selector, timeout=10000):
        self.page.wait_for_selector(selector, state="hidden", timeout=timeout)

    # 等待文本出现
    def wait_for_text(self, selector, text, timeout=10000):
        self.page.wait_for_function(
            f"element => element.innerText.includes('{text}')",
            self.page.query_selector(selector),
            timeout=timeout
        )

    # 双击元素
    def double_click(self, selector):
        self.wait_for_element_to_be_clickable(selector)
        self.page.dblclick(selector)

    # 右击元素
    def right_click(self, selector):
        self.wait_for_element_to_be_clickable(selector)
        self.page.click(selector, button='right')

    # 拖动元素到目标位置
    def drag_and_drop(self, source_selector, target_selector):
        self.wait_for_element_to_be_visible(source_selector)
        self.wait_for_element_to_be_visible(target_selector)
        source = self.page.query_selector(source_selector)
        target = self.page.query_selector(target_selector)
        source.drag_to(target)
    # 等待并清除文本框内容
    def wait_and_clear(self, selector, timeout=10000):
        self.wait_for_element_to_be_clickable(selector, timeout)
        element = self.page.query_selector(selector)
        element.fill("")

    # 等待元素消失
    def wait_for_element_to_disappear(self, selector, timeout=10000):
        self.page.wait_for_selector(selector, state="detached", timeout=timeout)

    # 等待页面加载完成
    def wait_for_page_load(self, timeout=30000):
        self.page.wait_for_load_state("load", timeout=timeout)

    # 切换到指定的iframe
    def switch_to_frame(self, frame_selector):
        frame_element = self.page.query_selector(frame_selector)
        return frame_element.content_frame()

    # 切换回主内容
    def switch_to_default_content(self):
        self.page.main_frame()

    # 执行鼠标悬停操作
    def hover_over_element(self, selector):
        self.wait_for_element_to_be_visible(selector)
        self.page.hover(selector)

    # 获取元素CSS属性值
    def get_css_property(self, selector, property_name):
        self.wait_for_element_to_be_visible(selector)
        element = self.page.query_selector(selector)
        return self.page.evaluate(f"element => window.getComputedStyle(element).getPropertyValue('{property_name}')", element)

    # 强制点击元素，即使不可点击
    def force_click(self, selector):
        self.page.evaluate(f'document.querySelector("{selector}").click()')

    # 检查复选框是否被选中
    def is_checkbox_checked(self, selector):
        self.wait_for_element_to_be_visible(selector)
        return self.page.is_checked(selector)

    # 全选文本框内容
    def select_all_text(self, selector):
        element = self.page.query_selector(selector)
        element.click()
        self.page.keyboard.press("Control+A" if platform.system() == "Windows" else "Command+A")

    # 检查元素是否在视口中
    def is_element_in_viewport(self, selector):
        element = self.page.query_selector(selector)
        return self.page.evaluate(f"""
            (element) => {{
                const rect = element.getBoundingClientRect();
                return (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                );
            }}
        """, element)

    # 等待指定的元素数量
    def wait_for_number_of_elements(self, selector, number, timeout=10000):
        self.page.wait_for_function(
            f'document.querySelectorAll("{selector}").length === {number}',
            timeout=timeout
        )
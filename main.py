from datetime import datetime
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.core.provider.entities import ProviderRequest


@register(
    "astrbot_plugin_timeline",
    "ctrlkk",
    "一个非常简单的插件，在请求中插入当前时间",
    "1.0",
)
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

    @filter.on_llm_request(priority=-1)
    async def on_llm_request2(self, event: AstrMessageEvent, req: ProviderRequest):
        """处理时间"""
        if not req.prompt:
            req.prompt = ""

        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        req.prompt = f"[玩家时间:{formatted_time}]\n{req.prompt.strip()}"

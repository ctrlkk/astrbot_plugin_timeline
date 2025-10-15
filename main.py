from datetime import datetime, timezone
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.provider.entities import ProviderRequest


@register(
    "astrbot_plugin_timeline",
    "ctrlkk",
    "一个非常简单的插件，在请求中插入当前时间",
    "1.1",
)
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.time_format = config.get("time_format", "[玩家时间:%Y-%m-%d %H:%M:%S]")
        self.timezone = config.get("timezone", "local")
        self.prefix = config.get("prefix", "")
        self.suffix = config.get("suffix", "")
        self.position = config.get("position", "before")

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用该方法。"""

    def get_formatted_time(self):
        """根据配置获取格式化的时间"""
        if self.timezone == "utc":
            now = datetime.now(timezone.utc)
        else:
            now = datetime.now()
        formatted_time = now.strftime(self.time_format)
        return f"{self.prefix}{formatted_time}{self.suffix}"

    @filter.on_llm_request(priority=-1)
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """处理时间"""
        formatted_time = self.get_formatted_time()
        prompt = (req.prompt or "").strip()
        if self.position == "after":
            req.prompt = f"{prompt}\n{formatted_time}".strip()
        else:
            req.prompt = f"{formatted_time}\n{prompt}".strip()

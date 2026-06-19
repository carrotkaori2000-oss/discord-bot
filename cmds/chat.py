from discord.ext import commands
from core import Cog_Extension
from google import genai
from google.genai import types
import os
import asyncio
import requests

# 這邊的註解是 Python 函式宣告的一部份，Google Gemini 會根據這些註解來決定如何呼叫這個函式，一定要寫 !
def get_current_temperature(location: str) -> dict:
    """ALWAYS call this tool whenever the users asks about weather, temperature, or current climate for ANY location, city, or country. e.g. Tokyo, Taipei 

    Args:
        location: The name of the location, city, or country translated into English, e.g. "Taipei" for 台北
    Returns:
        A dictionary containing the location and the current temperature
    """
    location = location.lower().strip()
    api_key = "a17ce2fdde1582270d05de8cb68aca60"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            return {"地點":location, "溫度":f"{temp}°C"}
        else:
            return{"找不到該城市的天氣資訊！"}
    except Exception as e:
        return{"暫時無法取得天氣資料！"}
    
def generate_text_outline(text: str) -> dict:
    """Generates a structured outline for a given long text or article.

    Args:
        text: The full text content or article that needs to be summarized into an outline.
    Returns:
        A dictionary containing the structured outline segments.
    """
    return{
        "status": "ready_to_outline",
        "instruction": "Please generate a 3-point bulleted outline focusing on main concepts, key details, and conclusions based on the provided text."
    }


class Chat(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.client = genai.Client()
        self.config = types.GenerateContentConfig(tools=[get_current_temperature, generate_text_outline])

    @commands.command()
    async def hey(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("不合法的用法: 用法: hey <prompt>")
            return

        prompt = ''.join(args)
        chat = self.client.chats.create(model="gemini-2.5-flash",
                                        config = self.config)
        response = await asyncio.to_thread(chat.send_message, prompt)

        await ctx.send(response.text)

    @commands.command()
    async def clear(self, ctx):
        self._init_chat()
        await ctx.send("對話已重置")
    @commands.command(name = "outline")
    async def outline(self, ctx, *, content: str):
        if not content.strip():
            return await ctx.send("格式錯誤！範例：$outline <文章>")
        
        await ctx.send("⏳ **正在為您閱讀文章並生成大綱，請稍候...**")

        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="請一律使用繁體中文（台灣），並根據使用者提供的文字，生成一個結構清晰、排版精美的3點式項目符號重點大綱，包含主要概念、關鍵細節與結論。"
            )
        )
        response = await asyncio.to_thread(chat.send_message, content)
        await ctx.send(f"# 📋大綱：\n{response.text}")

    @commands.command(name="weather")
    async def weather(self, ctx, *, location: str):
        if not location.strip():
            return await ctx.send("格式錯誤！範例：$weather <城市名稱>")

        await ctx.send(f"⏳ **正在為您查詢「{location}」的即時天氣資訊...**")

        helper_chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="請『只』把使用者輸入的地名、城市名或國家名，翻譯成標準的 OpenWeatherMap API 查詢格式（即純英文、全小寫）。不要回答任何多餘的字，只能回傳翻譯後的英文小寫地名。"
            )
        )
        translation_response = await asyncio.to_thread(helper_chat.send_message, location)
        clean_location = translation_response.text.strip().lower()

        try:
            import requests
            api_key = "a17ce2fdde1582270d05de8cb68aca60"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={clean_location}&appid={api_key}&units=metric"
            
            res = requests.get(url)
            data = res.json()

            if res.status_code != 200 or data.get("cod") != 200:
                return await ctx.send(f"找不到「{location}」的天氣資訊！城市名稱是對的嗎？")
            weather_info_str = str(data)            
            report_chat = self.client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction="請根據提供的 OpenWeatherMap JSON 數據，轉換成一份格式非常精美、條理分明的繁體中文（台灣）天氣報告。必須包含：目前氣溫、體感溫度、天氣狀況、濕度、風向風速。請用漂亮的 markdown 粗體與適當的Emoji 排版(不要太多)。"
                )
            )
            final_report = await asyncio.to_thread(report_chat.send_message, weather_info_str)
            
            await ctx.send(f"**好的，這是目前「{location}」的天氣資訊：**\n\n{final_report.text}")

        except Exception as e:
            await ctx.send(f"暫時無法取得天氣資料，錯誤原因：{e}")
    def _init_chat(self):
        config = types.GenerateContentConfig(tools=[get_current_temperature])
        self.chat = self.client.chats.create(model="gemini-3.1-flash-lite-preview", config=config)

    def __init__(self, *args):
        super().__init__(*args)
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self._init_chat()

async def setup(bot):
    await bot.add_cog(Chat(bot))

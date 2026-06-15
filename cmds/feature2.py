import discord
from discord.ext import commands
from core import Cog_Extension
import random

# ==================== 指令一的下拉選單介面 ====================
class SituationSelect(discord.ui.Select):
    def __init__(self, pool):
        self.pool = pool
        options = [
            discord.SelectOption(label="喜悅", emoji="🥳", description="雀躍、開心、充滿能量的時刻"),
            discord.SelectOption(label="心動", emoji="🦋", description="曖昧、小鹿亂撞的甜蜜感"),
            discord.SelectOption(label="思念", emoji="💭", description="想起某個人、某段回憶的時候"),
            discord.SelectOption(label="失落", emoji="😢", description="心情低落、需要音樂共鳴的時刻"),
            discord.SelectOption(label="希望", emoji="✨", description="迎接新挑戰、充滿正能量"),
            discord.SelectOption(label="深夜獨處", emoji="🌌", description="夜深人靜，屬於自己的時間"),
            discord.SelectOption(label="通勤路上", emoji="🚌", description="上學、放學路上的陪伴"),
            discord.SelectOption(label="讀書／寫作業", emoji="✍️", description="專注學習、寫作業的背景音"),
            discord.SelectOption(label="運動熱血", emoji="⚡", description="揮灑汗水、極限轟炸的節奏"),
            discord.SelectOption(label="放空療癒", emoji="🍃", description="什麼都不想，純粹放鬆緊繃的神經")
        ]
        super().__init__(placeholder="🎵 請選擇你想聽的心情或狀態...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        # 從該分類的 2 首歌曲中，隨機二選一抽出「一首」
        random_song = random.choice(self.pool[selected])
        
        embed = discord.Embed(
            title=f"🎬 情境推薦：【{selected}】",
            description="已從該情境的歌單中為你隨機二選一抽出一首好歌！",
            color=discord.Color.blue()
        )
        embed.add_field(name="🔗 點擊歌名直接前往 YouTube", value=f"🎶 {random_song}", inline=False)
        
        # 移除選單，只顯示最終美觀的結果
        await interaction.response.edit_message(embed=embed, view=None)

# ==================== 指令三的下拉選單介面 ====================
class GenreSelect(discord.ui.Select):
    def __init__(self, pool):
        self.pool = pool
        options = [
            discord.SelectOption(label="流行", emoji="🎤"),
            discord.SelectOption(label="搖滾", emoji="🎸"),
            discord.SelectOption(label="嘻哈／饒舌", emoji="🧢"),
            discord.SelectOption(label="節奏藍調", emoji="🎷"),
            discord.SelectOption(label="電子音樂", emoji="🎛️"),
            discord.SelectOption(label="民謠", emoji="🎻"),
            discord.SelectOption(label="鄉村音樂", emoji="🤠"),
            discord.SelectOption(label="爵士", emoji="🎹"),
            discord.SelectOption(label="交響改編 / 浪漫弦樂", emoji="🎼"),
            discord.SelectOption(label="獨立音樂", emoji="🛸")
        ]
        super().__init__(placeholder="🎼 請選擇你想探索的曲風...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        # 從該曲風的 2 首歌曲中，隨機二選一抽出「一首」
        random_song = random.choice(self.pool[selected])
        
        embed = discord.Embed(
            title=f"🎼 曲風推薦：【{selected}】",
            description="已從該曲風的歌單中為你隨機二選一抽出一首好歌！",
            color=discord.Color.purple()
        )
        embed.add_field(name="🔗 點擊歌名直接前往 YouTube", value=f"🎤 {random_song}", inline=False)
        
        # 移除選單，只顯示最終美觀的結果
        await interaction.response.edit_message(embed=embed, view=None)

# ==================== 主 Cog 類別 ====================
class Feature2(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        
        # ==================== 第一部分：心情與狀態（10個分類 × 2首 = 共 20 首） ====================
        self.mood_situation_pool = {
            "喜悅": [
                "[Bruno Mars — 24K Magic](https://www.youtube.com/watch?v=UqyT8IEBkvY)",
                "[Taylor Swift — Cruel Summer](https://www.youtube.com/watch?v=ic8j13piAhQ)"
            ],
            "心動": [
                "[JVKE — golden hour](https://www.youtube.com/watch?v=Pem1u8GgG6w)",
                "[Charlie Puth — Left and Right (feat. Jung Kook)](https://www.youtube.com/watch?v=a7GITgqwDVg)"
            ],
            "思念": [
                "[Peder Elias — Loving You Girl](https://www.youtube.com/watch?v=by3yRdlQvzs)",
                "[Shawn Mendes — Treat You Better](https://www.youtube.com/watch?v=lY2yjAdbvdQ)"
            ],
            "失落": [
                "[Sombr — back to friends](https://www.youtube.com/watch?v=Yf1eNWe0fEM)",
                "[Olivia Rodrigo — drivers license](https://www.youtube.com/watch?v=ZmDBpeDNnNJ)"
            ],
            "希望": [
                "[Ed Sheeran — Castle on the Hill](https://www.youtube.com/watch?v=K0ibBPhiaG0)",
                "[Justin Bieber — Holy](https://www.youtube.com/watch?v=pvPsJFRGleA)"
            ],
            "深夜獨處": [
                "[Billie Eilish — ocean eyes](https://www.youtube.com/watch?v=viimfQi_pUw)",
                "[Sombr — undressed](https://www.youtube.com/watch?v=gT8BfGstXis)"
            ],
            "通勤路上": [
                "[Lauv — Paris in the Rain](https://www.youtube.com/watch?v=kOCkne-Bku4)",
                "[Drake — Hotline Bling](https://www.youtube.com/watch?v=uxpDa-c-4Mc)"
            ],
            "讀書／寫作業": [
                "[Ed Sheeran — Thinking Out Loud](https://www.youtube.com/watch?v=lp-EO5I60KA)",
                "[Lauv — Breathe](https://www.youtube.com/watch?v=7zVp97SgG68)"
            ],
            "運動熱血": [
                "[Taylor Swift — ...Ready For It?](https://www.youtube.com/watch?v=wIft-t-MQuE)",
                "[Bruno Mars & Mark Ronson — Uptown Funk](https://www.youtube.com/watch?v=OPf0YbXqDm0)"
            ],
            "放空療癒": [
                "[JVKE — this is what falling in love feels like](https://www.youtube.com/watch?v=A8vN67Vb_kU)",
                "[Peder Elias — Paper Plane](https://www.youtube.com/watch?v=m1wXsh2P7B4)"
            ]
        }

        # ==================== 第二部分：每日純享好歌推薦（共 10 首） ====================
        self.daily_pool = [
            "[1. Lauv — Modern Loneliness](https://www.youtube.com/watch?v=vv-8vKCHmF0)",
            "[2. JVKE — i can't help it](https://www.youtube.com/watch?v=D-aV5vWz9yM)",
            "[3. Olivia Rodrigo — vampire](https://www.youtube.com/watch?v=RlPNh_PB6Bk)",
            "[4. Billie Eilish — L'AMOUR DE MA VIE](https://www.youtube.com/watch?v=8M6pE_t_tms)",
            "[5. Peder Elias — MS. SEROTONIN](https://www.youtube.com/watch?v=jW018i769kE)",
            "[6. Taylor Swift — Style](https://www.youtube.com/watch?v=BFfdq7S0uRE)",
            "[7. Ed Sheeran — Bloodstream](https://www.youtube.com/watch?v=Orq_7wS9MOM)",
            "[8. Justin Bieber — Die For You (feat. Dominic Fike)](https://www.youtube.com/watch?v=C7D_6pZ8Gpk)",
            "[9. Charlie Puth — Loser](https://www.youtube.com/watch?v=70f7fMAnp_M)",
            "[10. Drake — Passionfruit](https://www.youtube.com/watch?v=COz9lDCFHjw)"
        ]

        # ==================== 第三部分：曲風推薦（10種曲風 × 2首 = 共 20 首） ====================
        self.genre_pool = {
            "流行": [
                "[Charlie Puth — Light Switch](https://www.youtube.com/watch?v=WFsAon_TWPQ)",
                "[Shawn Mendes — There's Nothing Holdin' Me Back](https://www.youtube.com/watch?v=dT2owtxkU8k)"
            ],
            "搖滾": [
                "[Olivia Rodrigo — brutal](https://www.youtube.com/watch?v=OGUX0A0Q9mE)",
                "[Billie Eilish — Happier Than Ever](https://www.youtube.com/watch?v=5GJWxDKykBY)"
            ],
            "嘻哈／饒舌": [
                "[Drake — God's Plan](https://www.youtube.com/watch?v=xpVfcZ0ZcFM)",
                "[Justin Bieber — As Long As You Love Me (feat. Big Sean)](https://www.youtube.com/watch?v=R4em3LKQCAY)"
            ],
            "節奏藍調": [
                "[Bruno Mars — That's What I Like](https://www.youtube.com/watch?v=PMivT7MJ41M)",
                "[Charlie Puth — We Don't Talk Anymore (feat. Selena Gomez)](https://www.youtube.com/watch?v=3AtDnEC4zak)"
            ],
            "電子音樂": [
                "[Lauv — I Like Me Better](https://www.youtube.com/watch?v=BcqxLCb7dKU)",
                "[Justin Bieber — What Do You Mean?](https://www.youtube.com/watch?v=DK_00HDNFcY)"
            ],
            "民謠": [
                "[Ed Sheeran — The A Team](https://www.youtube.com/watch?v=UAWcs5H-qgQ)",
                "[Taylor Swift — Cardigan](https://www.youtube.com/watch?v=K-a8s8OLBSE)"
            ],
            "鄉村音樂": [
                "[Taylor Swift — Love Story](https://www.youtube.com/watch?v=8xg3vE8Ie_E)",
                "[Ed Sheeran — Galway Girl](https://www.youtube.com/watch?v=nkqVm5aiC28)"
            ],
            "爵士": [
                "[Bruno Mars — Smokin Out The Window (as Silk Sonic)](https://www.youtube.com/watch?v=GG7fLOmlhYg)",
                "[Billie Eilish — my future](https://www.youtube.com/watch?v=Dm9Zf1WYQ_A)"
            ],
            "交響改編 / 浪漫弦樂": [
                "[JVKE — this is what falling in love feels like (Orchestral Version)](https://www.youtube.com/watch?v=34gLg9O-Wv0)",
                "[Taylor Swift — Lover (First Dance Remix)](https://www.youtube.com/watch?v=686A_7DscX0)"
            ],
            "獨立音樂": [
                "[Sombr — Caroline](https://www.youtube.com/watch?v=nE-k39vI5K4)",
                "[Peder Elias — Best Friend](https://www.youtube.com/watch?v=O1m_wE66Z8A)"
            ]
        }

    # ==================== 指令一：情境點歌（選狀態再二選一） ====================
    @commands.command(name="推薦情境")
    async def mood_recommend(self, ctx):
        """跳出下拉選單供使用者選擇情境，並從中二選一推薦歌曲"""
        embed = discord.Embed(
            title="🎬 情境與狀態音樂點播",
            description="請從下方下拉選單中選擇你目前的心情或所處狀態：",
            color=discord.Color.blue()
        )
        # 建立帶有下拉選單的 View
        view = discord.ui.View(timeout=60)
        view.add_item(SituationSelect(self.mood_situation_pool))
        
        await ctx.send(embed=embed, view=view)

    # ==================== 指令二：每日推薦（維持盲抽多取一） ====================
    @commands.command(name="每日推薦")
    async def daily_recommend(self, ctx):
        """從 10 首每日推薦中隨機盲抽一首"""
        random_song = random.choice(self.daily_pool)
        
        embed = discord.Embed(
            title="💿 每日純享好歌推薦 (共 10 首庫存)",
            description="今日嚴選精選輯，隨機盲盒為你推薦：",
            color=discord.Color.orange()
        )
        embed.add_field(name="🔗 點擊歌名直接前往 YouTube 聽歌", value=f"🎵 {random_song}", inline=False)
        embed.set_footer(text="輸入 $每日推薦 可以重新抽取")
        
        await ctx.send(embed=embed)

    # ==================== 指令三：曲風推薦（選曲風再二選一） ====================
    @commands.command(name="推薦曲風")
    async def genre_recommend(self, ctx):
        """跳出下拉選單供使用者選擇曲風，並從中二選一推薦歌曲"""
        embed = discord.Embed(
            title="🎼 豐富曲風探索",
            description="請從下方下拉選單中選擇你想探索的音樂風格類型：",
            color=discord.Color.purple()
        )
        # 建立帶有下拉選單的 View
        view = discord.ui.View(timeout=60)
        view.add_item(GenreSelect(self.genre_pool))
        
        await ctx.send(embed=embed, view=view)

# 載入 Cog
async def setup(bot):
    await bot.add_cog(Feature2(bot))
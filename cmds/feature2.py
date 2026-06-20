import discord
from discord.ext import commands
from core import Cog_Extension
import random

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
        random_song = random.choice(self.pool[selected])
        
        embed = discord.Embed(
            title=f"🎬 情境推薦：【{selected}】",
            description="已從該情境的歌單中為你隨機二選一抽出一首好歌！",
            color=discord.Color.blue()
        )
        embed.add_field(name="🔗 點擊歌名直接前往 YouTube", value=f"🎶 {random_song}", inline=False)
        await interaction.response.edit_message(embed=embed, view=None)

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
        random_song = random.choice(self.pool[selected])
        
        embed = discord.Embed(
            title=f"🎼 曲風推薦：【{selected}】",
            description="已從該曲風的歌單中為你隨機二選一抽出一首好歌！",
            color=discord.Color.purple()
        )
        embed.add_field(name="🔗 點擊歌名直接前往 YouTube", value=f"🎤 {random_song}", inline=False)
        
        await interaction.response.edit_message(embed=embed, view=None)

class Feature2(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)

        self.mood_situation_pool = {
            "喜悅": [
                "[Bruno Mars — 24K Magic](https://www.youtube.com/watch?v=UqyT8IEBkvY)",
                "[Taylor Swift — Cruel Summer](https://www.youtube.com/watch?v=ic8j13piAhQ)"
            ],
            "心動": [
                "[JVKE — golden hour](https://www.youtube.com/watch?v=PEM0Vs8jf1w)",
                "[Charlie Puth — Left and Right (feat. Jung Kook)](https://www.youtube.com/watch?v=a7GITgqwDVg)"
            ],
            "思念": [
                "[Peder Elias — Loving You Girl](https://www.youtube.com/watch?v=uZbB9DssRlA)",
                "[Shawn Mendes — Treat You Better](https://www.youtube.com/watch?v=lY2yjAdbvdQ)"
            ],
            "失落": [
                "[Sombr — back to friends](https://www.youtube.com/watch?v=c8zq4kAn_O0)",
                "[Olivia Rodrigo — drivers license](https://www.youtube.com/watch?v=ZmDBbnmKpqQ)"
            ],
            "希望": [
                "[Ed Sheeran — Castle on the Hill](https://www.youtube.com/watch?v=K0ibBPhiaG0)",
                "[Justin Bieber — Holy (feat. Chance The Rapper)](https://www.youtube.com/watch?v=pvPsJFRGleA)"
            ],
            "深夜獨處": [
                "[Billie Eilish — ocean eyes](https://www.youtube.com/watch?v=viimfQi_pUw)",
                "[Sombr — undressed](https://www.youtube.com/watch?v=CtRn6eqVnvY)"
            ],
            "通勤路上": [
                "[Lauv — Paris in the Rain](https://www.youtube.com/watch?v=kOCkne-Bku4)",
                "[Drake — Hotline Bling](https://www.youtube.com/watch?v=uxpDa-c-4Mc)"
            ],
            "讀書／寫作業": [
                "[Ed Sheeran — Thinking Out Loud](https://www.youtube.com/watch?v=lp-EO5I60KA)",
                "[Lauv — Breathe](https://www.youtube.com/watch?v=Tkc_9OPC20E)"
            ],
            "運動熱血": [
                "[Taylor Swift — ...Ready For It?](https://www.youtube.com/watch?v=wIft-t-MQuE)",
                "[Bruno Mars & Mark Ronson — Uptown Funk](https://www.youtube.com/watch?v=OPf0YbXqDm0)"
            ],
            "放空療癒": [
                "[JVKE — this is what falling in love feels like](https://www.youtube.com/watch?v=BOyO8sZOaOQ)",
                "[Peder Elias — Paper Plane](https://www.youtube.com/watch?v=YbqZsvWC2lU)"
            ]
        }

        self.daily_pool = [
            "[1. Lauv — Modern Loneliness](https://www.youtube.com/watch?v=bDidwMxir4o)",
            "[2. JVKE — i can't help it](https://www.youtube.com/watch?v=PFiynNbmeLI)",
            "[3. Olivia Rodrigo — vampire](https://www.youtube.com/watch?v=RlPNh_PBZb4)",
            "[4. Billie Eilish — L'AMOUR DE MA VIE](https://www.youtube.com/watch?v=GLpdY-57Dro)",
            "[5. Peder Elias — MS. SEROTONIN](https://www.youtube.com/watch?v=XpeGw8MDMcI)",
            "[6. Taylor Swift — Style](https://www.youtube.com/watch?v=-CmadmM5cOk)",
            "[7. Ed Sheeran — Bloodstream](https://www.youtube.com/watch?v=XIJHg1XWR7o)",
            "[8. The Weeknd & Ariana Grande — Die For You](https://www.youtube.com/watch?v=YQ-qToZUybM)",
            "[9. Charlie Puth — Loser](https://www.youtube.com/watch?v=Sp6BS-rSr98)",
            "[10. Drake — Passionfruit](https://www.youtube.com/watch?v=COz9lDCFHjw)"
        ]

        self.genre_pool = {
            "流行": [
                "[Charlie Puth — Light Switch](https://www.youtube.com/watch?v=WFsAon_TWPQ)",
                "[Shawn Mendes — There's Nothing Holdin' Me Back](https://www.youtube.com/watch?v=dT2owtxkU8k)"
            ],
            "搖滾": [
                "[Olivia Rodrigo — brutal](https://www.youtube.com/watch?v=OGUy2UmRxJ0)",
                "[Billie Eilish — Happier Than Ever](https://www.youtube.com/watch?v=5GJWxDKyk3A)"
            ],
            "嘻哈／饒舌": [
                "[Drake — God's Plan](https://www.youtube.com/watch?v=xpVfcZ0ZcFM)",
                "[Drake — One Dance (feat. Wizkid & Kyla)](https://www.youtube.com/watch?v=ki0Ocze98U8&list=RDki0Ocze98U8&start_radio=1)"
            ],
            "節奏藍調": [
                "[Bruno Mars — That's What I Like](https://www.youtube.com/watch?v=PMivT7MJ41M)",
                "[Bruno Mars — Versace on the Floor](https://www.youtube.com/watch?v=-FyjEnoIgTM)"
            ],
            "電子音樂": [
                "[Lauv — I Like Me Better](https://www.youtube.com/watch?v=a7fzkqLozwA)",
                "[Charlie Puth — Attention](https://www.youtube.com/watch?v=nfs8NYg7yQM)"
            ],
            "民謠": [
                "[Ed Sheeran — The A Team](https://www.youtube.com/watch?v=UAWcs5H-qgQ)",
                "[Taylor Swift — Cardigan](https://www.youtube.com/watch?v=K-a8s8OLBSE)"
            ],
            "鄉村音樂": [
                "[Taylor Swift — Love Story](https://www.youtube.com/watch?v=8xg3vE8Ie_E)",
                "[Taylor Swift — Our Song](https://www.youtube.com/watch?v=Jb2stN7kH28)"
            ],
            "爵士": [
                "[Silk Sonic — Smokin Out The Window](https://www.youtube.com/watch?v=GG7fLOmlhYg)",
                "[Billie Eilish — my future](https://www.youtube.com/watch?v=Dm9Zf1WYQ_A)"
            ],
            "交響改編 / 浪漫弦樂": [
                "[Ed Sheeran — Perfect Symphony](https://www.youtube.com/watch?v=eiDiKwbGfIY)",
                "[Taylor Swift — Lover ](https://www.youtube.com/watch?v=-BjZmE2gtdo)"
            ],
            "獨立音樂": [
                "[Peder Elias — Row Your Boat](https://www.youtube.com/watch?v=ynQ6bEnewu0)",
                "[Peder Elias — Bonfire](https://www.youtube.com/watch?v=A1DFnqzF8-o)"
            ]
        }

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

    @commands.command(name="推薦曲風")
    async def genre_recommend(self, ctx):
        """跳出下拉選單供使用者選擇曲風，並從中二選一推薦歌曲"""
        embed = discord.Embed(
            title="🎼 豐富曲風探索",
            description="請從下方下拉選單中選擇你想探索的音樂風格類型：",
            color=discord.Color.purple()
        )
        view = discord.ui.View(timeout=60)
        view.add_item(GenreSelect(self.genre_pool))
        
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Feature2(bot))
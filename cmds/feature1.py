import discord
from discord.ext import commands
from core import Cog_Extension
from datetime import datetime

class Feature1(Cog_Extension):
        
    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello, world")
    
    @commands.command(name="set_grades")
    async def set_grades(self, ctx, 國文: int, 英文: int, 數學: int, 社會1: int, 社會2: int, 社會3: int, 自然1: int, 自然2: int):
        scores = [國文, 英文, 數學, 社會1, 社會2, 社會3, 自然1, 自然2]

        if any(s < 0 or s > 100 for s in scores):
            await ctx.send("❌ 輸入失敗！分數必須介於 0 到 100 之間。")
            return

        total = sum(scores)
        avg = total / len(scores)

        embed = discord.Embed(title="📊 個人成績結算單", color=discord.Color.green())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.add_field(name="核心主科", value=f"國文: {國文} | 英文: {英文} | 數學: {數學}", inline=False)
        embed.add_field(name="社會三科", value=f"{社會1}分, {社會2}分, {社會3}分", inline=True)
        embed.add_field(name="自然兩科", value=f"{自然1}分, {自然2}分", inline=True)
        embed.add_field(name="總合成績", value=f"📈 **總分: {total}**\n📋 **平均: {avg:.2f}**", inline=False)
        
        comment = "表現太棒了！繼續保持！" if avg >= 80 else "有進步的空間，加油，你可以的！"
        embed.set_footer(text=comment)
        await ctx.send(embed=embed)

    @set_grades.error
    async def set_grades_error(self, ctx, error):
        await ctx.send("❌ 格式錯誤！請依照此格式輸入：\n`!set_grades 國文 英文 數學 社會1 社會2 社會3 自然1 自然2` (皆為數字並用空格隔開)")

    @commands.command(name="countdown")
    async def countdown(self, ctx, 考試名稱: str, 日期: str):
        try:
            target_date = datetime.strptime(日期, "%Y-%m-%d")
            today = datetime.now()
            delta = target_date - today
            days_left = delta.days + 1

            embed = discord.Embed(title="📅 考試倒數計時器", color=discord.Color.orange())
            if days_left > 0:
                embed.description = f"距離 🎯 **{考試名稱}** 還有\n\n# 🕒 {days_left} 天"
                embed.set_footer(text=f"目標日期：{日期}")
            elif days_left == 0:
                embed.description = f"🔔 🎉 **{考試名稱}** 就是今天了！祝你全力以赴！"
            else:
                embed.description = f"⌛ **{考試名稱}** 已經結束 {-days_left} 天囉。"
            await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("❌ 日期格式錯誤！請使用 `YYYY-MM-DD` 格式（例如：`2026-06-20`）。")

    @countdown.error
    async def countdown_error(self, ctx, error):
        await ctx.send("❌ 格式錯誤！請依照此格式輸入：\n`!countdown 考試名稱 YYYY-MM-DD`\n(例如：`!countdown 學測 2027-01-22`)")

    @commands.command(name="set_timetable")
    async def set_timetable(self, ctx, 星期: str, 課1: str, 課2: str, 課3: str, 課4: str, 課5: str, 課6: str, 課7: str):
        valid_days = ["週一", "週二", "週三", "週四", "週五", "星期一", "星期二", "星期三", "星期四", "星期五"]
        if 星期 not in valid_days:
            await ctx.send("❌ 星期輸入錯誤！請輸入『週一』到『週五』。")
            return

        if not hasattr(self, 'timetable_data'):
            self.timetable_data = {}

        user_id = str(ctx.author.id)
        if user_id not in self.timetable_data:
            self.timetable_data[user_id] = {}
        
        self.timetable_data[user_id][星期] = [課1, 課2, 課3, 課4, 課5, 課6, 課7]
        await ctx.send(f"✅ 成功儲存 {ctx.author.display_name} 的 **{星期}** 課表！")

    @set_timetable.error
    async def set_timetable_error(self, ctx, error):
        await ctx.send("❌ 格式錯誤！請務必輸入完整七節課：\n`!set_timetable 週一 國文 英文 數學 體育 歷史 地理 地科`")

    @commands.command(name="show_timetable")
    async def show_timetable(self, ctx, 星期: str):
        if not hasattr(self, 'timetable_data'):
            self.timetable_data = {}
            
        user_id = str(ctx.author.id)
        if user_id not in self.timetable_data or 星期 not in self.timetable_data[user_id]:
            await ctx.send(f"❓ 找不到你 **{星期}** 的課表。請先使用 `!set_timetable` 設定喔！")
            return

        classes = self.timetable_data[user_id][星期]
        embed = discord.Embed(title=f"🏫 {ctx.author.display_name} 的 {星期} 課表", color=discord.Color.purple())
        
        schedule_text = ""
        for i, class_name in enumerate(classes, 1):
            schedule_text += f"第 {i} 節：**{class_name}**\n"
        
        embed.description = schedule_text
        await ctx.send(embed=embed)

    @show_timetable.error
    async def show_timetable_error(self, ctx, error):
        await ctx.send("❌ 格式錯誤！請輸入想要查詢的星期，例如：`!show_timetable 週一`")

async def setup(bot):
    await bot.add_cog(Feature1(bot))
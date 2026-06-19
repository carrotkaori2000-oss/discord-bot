from discord.ext import commands
from core import Cog_Extension
import json
import os
import datetime
import discord

class Task():
    def __init__(self, name: str, description: str, deadline: datetime.datetime):
        self.name: str = name
        self.deadline: datetime.datetime = deadline
        self.description: str = description

class Scheduler(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.todo_list = self.load_todo_list()
    def load_todo_list(self):
        if not os.path.exists("todo_list.json"):
            return []
        try:
            with open("todo_list.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded_list = []
            for item in data:
                deadline_obj = datetime.datetime.strptime(item["deadline"], "%Y-%m-%d %H:%M")
                task = Task(item["name"], item["description"], deadline_obj)
                loaded_list.append(task)
            return loaded_list
        except Exception as e:
            print(f"讀取檔案失敗: {e}")
            return []

    def save_todo_list(self):
        data = []
        for task in self.todo_list:
            data.append({
                "name": task.name,
                "description": task.description,
                "deadline": task.deadline.strftime("%Y-%m-%d %H:%M")
            })
        with open("todo_list.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    


    @commands.command(name="AddTodoList", aliases=["add"])
    async def AddTodoList(self, ctx, *args):
        print("收到了!")
   
        try:
            name, description, date, deadline = args        
            deadline_object = datetime.datetime.strptime(f"{date} {deadline}", "%Y-%m-%d %H:%M")
        
            if not any (task.name == name for task in self.todo_list):
                new_task = Task(name, description, deadline_object)
                self.todo_list.append(new_task)
                self.save_todo_list()
                await ctx.send(f"已新增Todo List:**{name}**!")
            else:
                await ctx.send(f"已經有**{name}**了喔!" )

        except ValueError:
            await ctx.send("輸入格式錯誤!範例：$add <事項名稱> <詳細資訊> 2025-05-18 23:59")
            return
    @commands.command(name = "remove")
    async def RemoveTodoList(self, ctx, *args):
        if len(args) != 1:
            await ctx.send("不合法的用法: 用法: $remove <事項名稱>")
            return
        else:
            name = args[0]
            task_to_remove = None
            for task in self.todo_list:
                if task.name == name:
                    task_to_remove = task
                    break

        if task_to_remove is not None:
            self.todo_list.remove(task_to_remove)
            self.save_todo_list
            await ctx.send(f"已移除**{name}**!")
        else:
            await ctx.send(f"找不到名為**{name}**的事項喔!")


    @commands.command(name = "clear_list")
    async def ClearTodoList(self, ctx):
        self.todo_list.clear()
        await ctx.send("已清空Todo List!")
        

    @commands.command(name = "show")
    async def ShowTodoList(self, ctx):
        if not self.todo_list:
            await ctx.send("目前沒有任何代辦事項喔!")
            return
            
        sorted_list = sorted(self.todo_list, key = lambda task: task.deadline)
        reply_message = "# 目前的代辦事項清單：\n"
        for index, task in enumerate(sorted_list, start = 1):
            time_str = task.deadline.strftime("%Y-%m-%d %H:%M")
            reply_message += f"{index}. **{task.name}** - {task.description} 截止時間：{time_str}\n"
        await ctx.send(reply_message)
        await ctx.send("以上是目前的代辦事項!")
        



async def setup(bot):
    await bot.add_cog(Scheduler(bot))


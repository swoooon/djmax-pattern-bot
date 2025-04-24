from interactions import Client, Intents, SlashContext, OptionType, slash_command, SlashCommandOption, File
import httpx
import os
from io import BytesIO
from dotenv import load_dotenv
import sys



load_dotenv()
bot = Client(token=os.getenv("BOT_TOKEN"), intents=Intents.DEFAULT)


@slash_command(
    name="graph",
    description="유저 닉네임의 태그별 실력 그래프를 생성합니다",
    options=[
        SlashCommandOption(
            name="nickname",
            description="조회할 유저 닉네임",
            type=OptionType.STRING,
            required=True
        )
    ]
)
async def graph(ctx: SlashContext, nickname: str):
    await ctx.defer()
    try:

        async with httpx.AsyncClient() as client:
            res = await client.get(f"{os.getenv('MY_API')}/varchive/{nickname}/tag-skill-image")
            res.raise_for_status()
            img_bytes = BytesIO(res.content)
            print(nickname)
            await ctx.send(
                content=f"🎵 `{nickname}`님의 태그별 실력 그래프입니다!",
                files=File(file=img_bytes, file_name="skill.png")
            )
    except Exception as e:
        await ctx.send("❌ 데이터를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.", ephemeral=True)
        print(e)




@bot.listen()
async def on_ready():
    print(f"✅ 봇 시작됨 - {len(bot.guilds)}개의 서버에 참여 중입니다.")

bot.start()

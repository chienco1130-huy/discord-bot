import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

TOKEN = "MTQ4MjM1NTA0MDYwMDU5MjQ4Nw.GN-54Q.onI2Qw18FxyTJ0TJJjt_wrV1hw4Ea4YCueeTCg"

WELCOME_CHANNEL = 1482552289108693155

CHAT_CHANNEL = [
1435598881181274114,
1480874990151663626,
1482282139125940370,
1481175414641655978,
1481176423765901372,
1480877610060742776,
1481257701420961863,
1481168883204358176
]

SUPERIORS = [
753829917677977643,
1102278875360264263,
1357951504530804837
]

bad_words = ["ngu","óc chó","đồ ngu","thằng ngu","con ngu","lồn","cặc"]

warnings = {}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"🤖 Bot đã sẵn sàng! {bot.user}")


# ===============================
# WELCOME MEMBER
# ===============================
@bot.event
async def on_member_join(member):

    channel = bot.get_channel(WELCOME_CHANNEL)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    banner_path = os.path.join(base_dir,"welcome_banner.jpg")
    bg_path = os.path.join(base_dir,"background.jpg")

    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)

    avatar = Image.open(BytesIO(response.content)).convert("RGBA")
    background = Image.open(bg_path).convert("RGBA")

    avatar = avatar.resize((250,250))

    mask = Image.new("L",(250,250),0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,250,250),fill=255)

    avatar.putalpha(mask)

    background.paste(avatar,(835,300),avatar)

    draw = ImageDraw.Draw(background)

    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf",60)

    text = f"LÍNH MỚI\n{member.name}"

    draw.text((650,600),text,font=font,fill="white")

    background = background.convert("RGB")
    background.save(banner_path)

    embed = discord.Embed(
        title="🎖 THÔNG BÁO TÂN BINH",
        description="Hãy đọc luật tại <#1481880483770925127> rồi react ✅ để có thể vào chat trong server!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="SỐ LƯỢNG THÀNH VIÊN",
        value=f"Hiện tại đơn vị có {member.guild.member_count} THÀNH VIÊN.",
        inline=False
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    embed.set_image(url="attachment://welcome_banner.jpg")

    await channel.send(
        content=f"# ĐỒNG CHÍ {member.mention} ĐÃ GIA NHẬP ĐƠN VỊ!🎉🎉🎉\n# Chào mừng đồng chí đến với sư đoàn!",
        embed=embed,
        file=discord.File(banner_path,"welcome_banner.jpg")
    )


# ===============================
# CHAT + WARN SYSTEM
# ===============================
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    msg = message.content.strip().lower()
    user = message.author.id

    if message.channel.id not in CHAT_CHANNEL:
        await bot.process_commands(message)
        return

    if any(word in msg for word in bad_words):

        if user not in warnings:
            warnings[user] = 1
        else:
            warnings[user] += 1

        if user in SUPERIORS:

            if warnings[user] == 1:
                await message.channel.send("Chú ý lời nói của mình thưa lãnh đạo")

            elif warnings[user] == 2:
                await message.channel.send("😔")

            return

        else:

            if warnings[user] == 1:
                await message.channel.send(
                f"⚠ Đồng chí {message.author.mention} XIN VUI LÒNG CHÚ Ý LỜI NÓI CỦA MÌNH VỚI CẤP TRÊN"
                )

            elif warnings[user] == 2:
                await message.channel.send(
                f"⚠ Đồng chí {message.author.mention}, đây là lần cảnh báo thứ 2. Nếu tiếp tục xúc phạm cấp trên đồng chí sẽ bị xử lý."
                )

            elif warnings[user] == 3:
                await message.channel.send(
                f"⚠ Đồng chí {message.author.mention}, cảnh báo lần cuối cùng việc liên tục vi phạm sẽ khiến đồng chí bị cấp trên xử phạt theo quy định cộng đồng. Không có ai, kể cả tôi, ngăn được đâu."
                )

            return


# ===============================
# CHAT ĐƠN GIẢN
# ===============================

    if msg == "!chào":
        await message.channel.send(
        f"Chào {message.author.mention}!"
        )

    ROLE_ID = 1482566487171530927
    if message.role_mentions:
        role = message.role_mentions[0]

        if role.id == ROLE_ID:
            await message.channel.send(
            f"Xin thưa {message.author.mention}! Tôi có thể giúp gì?"
        )

    elif "!luật sử dụng bot" in msg:
        await message.channel.send(
        "📜 Hãy đọc luật tại kênh:\n<#1482295806655598622>"
        )

    elif "!luật" in msg:
        await message.channel.send(
        "📜 Hãy đọc luật tại kênh:\n<#1481880483770925127>"
        )

    await bot.process_commands(message)


bot.run(TOKEN)

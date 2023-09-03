import interactions
import discord
import os
import platform
import random
import requests
from interactions import *
from keepAlive import keep_alive
import time
#delete_after=20 (ห้ามลบ)
intents = discord.Intents.default(
)  # ใช้ค่า default หรือปรับแต่งตามความต้องการ [เพิ่มเติมมันเอาไว้ไม่ต้อง init]
token = os.environ['ICE_SHOP']
ICE_SHOP = interactions.Client(token=token,
                               intents=Intents.ALL)  # ห้ามแก้เด็ดขาด !!!

ch_id = "1147504472080252958"  # ใส่ ID ช่องที่จะให้ซื้อยศ

phone = "0972626018"  # ใส่เบอร์มือถือที่ใช้สมัครบัญชี ทรูมันนี่วอเลท

log_id = "1147504472080252958"  # ใส่ไอดีช่องประวัติการซื้อ

# ห้ามนำไปแจกต่อ เจอปรับ 10 เท่าของราคา src ที่ขาย !!!

# ชื่อร้าน หรือชื่อ อื่นๆ...
m_title = "ICE SHOP"

# ลิ้งค์รูปเล็ก By Ice Shop
m_tn = "https://cdn.discordapp.com/attachments/1101236843900588043/1107341553971769415/IMG_1032.jpg"

# ลิ้งค์รููปใหญ่ By Ice Shop
m_img = "https://cdn.discordapp.com/attachments/1135392389721231490/1135405104451817552/IMG_2507.gif"

product_name01 = "ts"  # ชื่อสินค้า
product_01 = "https://cdn.discordapp.com/attachments/1147504472080252958/1147772155208138883/keepAlive.py"  # ลิ้งค์สินค้า
product_01p = "10.00"  # ราคาสินค้า
product_name02 = "ts"  # ชื่อสินค้า

# Link สินค้า
link = [
  "none", 
  "ex@gmail.com", 
  "ex2@gmail.com", 
  3, 
  4, 
  5, 
  6, 
  7, 
  "ex1@gmail.com",
  "ex2@gmail.com", 
  "ex3@gmail.com"
]
# จำนวน
n = 1
num = 10 + n
# Clinet Event
mClient = 0
idCurremt = 0
#MainGui 
def GetMainEmbed():
  main_embed = interactions.Embed(
      title=f"**{m_title} ซื้อสินค้าผ่านบอทอัตโนมัติ**",
      description="",
      color=0x7300ff)
  main_embed.set_image(m_img)
  main_embed.set_footer("© 2023", f'{m_tn}')
  return main_embed
# Menubar
def GetMenubar():
  components: list[ActionRow] = [
      ActionRow(
          StringSelectMenu(
              [
                  interactions.StringSelectOption(
                      emoji="<a:36:1136315227605045502>",
                      label=f"{product_name01} {num-1}",
                      description=f"{product_01p} BAHT",
                      value="10"),
                  interactions.StringSelectOption(
                      emoji="<a:36:1136315227605045502>",
                      label=f"{product_name01}",
                      description=f"-",
                      value="-"),
              ],
              custom_id="buy_cb",
              placeholder="🛒 เลือกสินค้าที่ต้องการซื้อ",
              min_values=1,
              max_values=1,
          ))
  ]
  return components
# DestroyId
def productDestroy(nLength):
  global num
  print(nLength)
  if nLength <= 11 and nLength != 0:
    link[num - 1] == ""
    num -= 1
    print(num)
# GetLink
def getLink():
  return link[num]
  # Void start 
@interactions.listen()
async def on_ready():
  global idCurrent
  global mClient
  ch = await ICE_SHOP.fetch_channel(channel_id=ch_id)
   # Keep Message Id
  mClient = await ch.send(embeds=GetMainEmbed(), components=GetMenubar())
  idCurrent = mClient.id
   # Alive time log
  if platform.system() == 'Windows':
    os.system('clear')
    print("ICE SHOP ACTIVE ")
  else:
    os.system('clear')
    print("ICE SHOP ACTIVE ")
# Callback func
@component_callback("buy_cb")
async def buy_cb(ctx: ComponentContext):
  rolebuy = ctx.values[0]
  topup_modal = Modal(
      ShortText(
          label='''ซื้อสินค้าผ่านบอทอัตโนมัติไม่ต้องรอแอดมิน''',
          custom_id="giftLink",
          required=True,
          placeholder="🧧 ใส่ลิ้งค์ซองอั่งเปา",
          max_length=80,
      ),
      title=f"{m_title} ซื้อสินค้าผ่านบอท",
  )
  await ctx.send_modal(modal=topup_modal)
  modal_ctx: ModalContext = await ctx.bot.wait_for_modal(topup_modal)
  giftLink = modal_ctx.responses['giftLink']
  print("successed Item")
  try:
    auth = requests.get(
        f"https://zamex-hub.000webhostapp.com/index.php?phone={phone}&link{giftLink}"
    )
    gotji = auth.json()
  except error:
    print("req fail http 404")
  if gotji["status"] == "SUCCESS":
    if gotji["amount"] == product_01p:
      productDestroy(len(link))
      await mClient.edit(components=GetMenubar())
      main_embed = interactions.Embed(
          title=f"**{m_title} ซื้อสินค้าผ่านบอทอัตโนมัติ**",
          description="",
          color=0x7300ff)
      main_embed.set_image(m_img)
      main_embed.set_footer("© 2023", f'{m_tn}')
      product_01s = interactions.Embed(
          title=f"**{m_title} ประวัติการซื้อสินค้า**",
          description="**ลิ้งค์ดาวโหลดสินค้า**",
          color=0x33FF99)
      product_01s.add_field(name=f"{getLink()}", value=f" ")
      await modal_ctx.send(embeds=product_01s, ephemeral=True)
      
      log_01 = await ICE_SHOP.fetch_channel(channel_id=log_id)
      log_01eb = interactions.Embed(
          title=f"**{m_title} ประวัติการซื้อสินค้า**",
          description="_ _",
          color=0x33FF99)
      log_01eb.add_field(
          name="ข้อมูลถูกต้อง",
          value=
          f"_ _\n> <a:7y4badgesrole:1135479816280358984> **สินค้าที่ซื้อ {product_name01}**",
      )
      await log_01.send(f"<@{ctx.author.id}>", embeds=log_01eb)
  else:
    print("fail")
    fail = interactions.Embed(title=f"**{m_title} ประวัติการซื้อสินค้า**",
                              description="_ _",
                              color=0xFF0033)

    fail.add_field(
        name="ข้อมูลผิดผลาด",
        value=
        "_ _\n> **<a:50_:1135481101914214431>  ซื้อสินค้าไม่สำเร็จโปรดลองอีกครั้ง**"
    )
    await modal_ctx.send(embeds=fail, ephemeral=True)

    fail_x = await ICE_SHOP.fetch_channel(channel_id=log_id)

    faileb = interactions.Embed(title=f"**{m_title} ประวัติการซื้อสินค้า**",
                                description="_ _",
                                color=0xFF0033)

    faileb.add_field(
        name="ข้อมูลผิดผลาด",
        value=
        "_ _\n> **<a:50_:1135481101914214431>  ซื้อสินค้าไม่สำเร็จโปรดลองอีกครั้ง**"
    )

    await fail_x.send(f"<@{ctx.author.id}>", embeds=faileb)


keep_alive()

ICE_SHOP.start(token)

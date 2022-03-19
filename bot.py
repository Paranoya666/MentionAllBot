import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "**Salam 👋 Men @Mr_KABUS_13 terefinden yaradılmış tağ botuyam**, Qrupda ve Kanallarda Hamını tağ ede bilerem 👻\nBas **/help** daha çox melumatı elde ede bilersiniz",
    link_preview=False,
    buttons=(
      [
        Button.url('🇦🇿 IMP Resmi', 'https://t.me/IMPRESMI'),
        Button.url('⚜️ Developer', 'https://t.me/Mr_KABUS_13')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Botun menyusuna xoş gelmisiz**\n\nKamandalar: /all\n__Bu komandanı Tağ etmek sebebi ile işlede bilersiniz.__\n`Meselen: /all Sabahınız xeyir!`\n__Bu komandanı kimese yanıt olaraq istifade edin ve yaxud tağ sebebini yazın botu dayandırmaq /𝖢𝖺𝗇𝖼𝖾𝗅__."
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('🇦🇿 IMP Resmi', 'https://t.me/Xxaosresmi'),
        Button.url('⚜️ Developer', 'https://t.me/Mr_KABUS_13')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__Bu kamanda yalnız Qrup ve Kanallarda istifade edile biler!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Yalnız adminler tağ ede bilerler!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Tağ sebebini yaz!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__Men köhne mesajlara tağ ede bilmerem! (Men qrupa elave edilmemişden evvel gönderilen mesajlar)__")
  else:
    return await event.respond("__Hansısa bir mesajı yanıtla ve yaxud tağ sebebini yaz!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__Heç bir proses baş vermir...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Dayandırıldı.__')

print(">> BOT STARTED <<")
client.run_until_disconnected()

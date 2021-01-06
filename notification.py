import users, config
# import discord, asyncio, queue, threading
import smtplib
from email.message import EmailMessage

# messages = queue.Queue()
# client = discord.Client()

def SendEmail(subject="No subject", body="No message"):
    admins = users.getAdmins()
    adminEmails = []

    for admin in admins:
        adminEmails.append(admin["email"])

    msg = EmailMessage()
    msg['Subject'] = f'KBot Notification - {subject}'
    msg['From'] = config.KBOT_EMAIL_USERNAME
    msg['To'] = adminEmails
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(config.KBOT_EMAIL_USERNAME, config.KBOT_EMAIL_PASSWORD)
            server.send_message(msg)
    except:
        print(body)

# def SendDiscord(message=""):
#     messages.put(message)
#
# async def sendMessage():
#     await client.wait_until_ready()
#     while True:
#         if not messages.empty():
#             message = messages.get()
#             channel = client.get_channel(config.DISCORD_KBOT_CHANNEL)
#             await channel.send(message)
#         await asyncio.sleep(10)
#
# async def discordbot():
#     await client.start(config.DISCORD_API_TOKEN)
#
# def botloop(loop):
#      loop.run_until_complete(client.start(config.DISCORD_API_TOKEN))
#
# asyncio.get_child_watcher()
# loop = asyncio.get_event_loop()
# loop.create_task(sendMessage())
#
# thread = threading.Thread(target=botloop, args=(loop,))
# thread.start()

if __name__ == "__main__":
    SendEmail("test", "test");

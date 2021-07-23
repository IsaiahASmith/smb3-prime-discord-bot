import discord

from replit import db

from translate import translate, Language

client = discord.Client()

def add_listener(channel, name):
    if "listeners" in db.keys():
        listeners = db["listeners"]

        listeners.append((name, channel))
        db["listeners"] = listeners
    else:
        db["listeners"] = [(name, channel)]


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$P"):
        await message.channel.send("Hello!")

    if message.content.startswith("$ES"):
        s = message.content[3:]
        print("message", s)
        await message.channel.send(translate
        (s, Language.spanish))

if __name__ == "__main__":
    from keep_alive import keep_alive
    keep_alive()  # Runs a random server so the bot doesn't go to sleep.

    from os import environ
    client.run(environ['TOKEN'])
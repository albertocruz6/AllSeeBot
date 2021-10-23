import discord
import os
from keep_alive import keep_alive


client = discord.Client()


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith("$hello"):
		await message.channel.send("Hello!")

def main():
	# keep_alive()
	client.run(os.getenv('BOT_TOKEN'))
	print("Hello there! -> Bot is ONLINE")

if __name__ == "__main__":
	main()
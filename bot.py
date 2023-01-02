import re
import requests
import discord

TOKEN = 'YOUR-TOKEN-HERE'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('bot ready')

@client.event
async def on_message(message):
  youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
  youtube_link = message.content
  video_id = re.search(youtube_regex, youtube_link)
  if video_id is not None:
    video_id = video_id.group(6)
    
    api_url = f'https://finder.madiator.com/api/v1/resolve?video_ids={video_id}'
    response = requests.get(api_url)
    data = response.json()
    
    odysee_url = data['data']['videos'].get(video_id)
    if odysee_url is None:
      await message.delete()
      await message.channel.send(f'{message.author.mention}, YouTube links are not allowed.')
    else:
      message_text = f'Here is Odysee.com link to your video:\nhttps://odysee.com/{odysee_url}'
      
      await message.delete()
      await message.channel.send(f'{message.author.mention} {message_text}')

client.run(TOKEN)


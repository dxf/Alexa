from discord.ext import commands
import discord
from credentials import DiscordToken
from credentials import WolframAppID
import sys
import asyncio
import wolframalpha

client = wolframalpha.Client(WolframAppID)
bot = commands.Bot(command_prefix='Alexa, ', case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)


@bot.command(name="play", brief="Makes a \"Now Playing\" meme in Discord.")
async def play(ctx, song):
    nowplayinembed = discord.Embed(title=f"ɴᴏᴡ ᴘʟᴀʏɪɴɢ: {song}",
                                   description="\n───────────:white_circle:────── ◄◄⠀▐▐ ⠀►►⠀⠀ ⠀ 𝟸:𝟷𝟾 / 𝟹:𝟻𝟼 ⠀ ─○─ :loud_sound:⠀ ᴴᴰ :gear:️ ❐ ⊏⊐",
                                   color=0x00afff)
    await ctx.send(embed=nowplayinembed)


@bot.command()
async def Wolfram(ctx, *, userquery):
    res = client.query(userquery)
    result = next(res.results).text
    wolframembed = discord.Embed(title=f"**Wolfram Result for {userquery}**", color=0x00afff, description=result)
    await ctx.send(embed=wolframembed)


@bot.command()
@commands.is_owner()
async def kill(ctx):
    sys.exit()


@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title="**Commands**", color=0x00afff, type="rich", url="https://github.com/dxf/Alexa",
                               footer="*All commands are prefixed with \"Alexa, \"")
    help_embed.add_field(name="**All Users**",
                         value="Help - This Command\nPlay - Make a \"Now Playing\" meme in Discord.\nWolfram - Query [Wolfram Alpha](https://wolframalpha.com) in Discord.")
    help_embed.add_field(name="**Bot Owner**", value="Kill - Kills the bot.")
    help_embed.set_footer(text='All commands are prefixed with \"Alexa, \"')
    await ctx.send(embed=help_embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        nopermsembed = discord.Embed(title=f"**No Permission**", color=0x00afff, description="Try \"Alexa, help\".")
        return await ctx.send(embed=nopermsembed)
    if isinstance(error, commands.CommandNotFound):
        commandnotfoundembed = discord.Embed(title=f"**Command Not Found**", color=0x00afff,
                                             description="Try \"Alexa, help\".")
        return await ctx.send(embed=commandnotfoundembed)
    else:
        errorembed = discord.Embed(title=f"**Error Occurred**", color=0x00afff,
                                   description="Please report [here!](https://discord.gg/tUr8ywd)")
        return await ctx.send(embed=errorembed)

bot.run(DiscordToken)

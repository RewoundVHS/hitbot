#! /usr/bin/python3

import discord
from discord.ext import commands
import hitbot_query

DESCRIPTION = '''Prints helpful frame data for Super Smash Bros Ultimate.'''
BOT = commands.Bot(command_prefix='hb!')

# Print bot information
@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
    print('------')
    # game = discord.Game('hb!help for command list')
    game = discord.Game('Alpha build: don\'t touch!')
    await BOT.change_presence(status=discord.Status.online, activity=game)

# TODO account for multiword character names, potentially split on a -
# TODO finish generalizing embed generator
# TODO account for multiple moves (bair early, bair late etc)
# TODO account for moves like throws where hitbox is null
# TODO refactor frames command
# TODO add movement data
# TODO add docstrings for each command

# Adds a course to the spreadsheet
@BOT.command()
async def frames(ctx, *, char_and_move: str):
    words = char_and_move.split('-')
    fighter_name = str(words[0]).strip()
    move_search = str(words[1]).strip()

    print("Character:", fighter_name)
    print("Move:", move_search)

    frame_data = hitbot_query.GetFrameData(fighter_name, move_search)

    move_name = frame_data[0][0]

    title_string = '**' + move_name + '**'
    embed = discord.Embed(title=title_string,
            colour=discord.Colour(0x1e8488))

    embed.set_image(url=
            "http://kuroganehammer.com/images/ultimate/character/"
            + fighter_name + ".png")

    embed.add_field(name="Active Frames", value="10-12", inline=True)
    embed.add_field(name="Shield Advantage", value="-4", inline=True)
    embed.add_field(name="Damage", value="20.4/22.2/20.4", inline=True)
    embed.add_field(name="Angle", value="361", inline=True)
    embed.add_field(name="Base Knockback", value="40", inline=True)
    embed.add_field(name="Knockback Growth", value="86", inline=True)

    await ctx.send(embed=embed)


BOT.run('TOKEN')

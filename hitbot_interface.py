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
    game = discord.Game('Alpha build: play nice!')
    await BOT.change_presence(status=discord.Status.online, activity=game)

# TODO finish generalizing embed generator
# TODO account for multiple moves (bair early, bair late etc)
# TODO account for moves like throws where hitbox is null
# TODO refactor frames command
# TODO add movement data
# TODO add docstrings for each command

@BOT.command()
async def frames(ctx, *, char_and_move: str):
    words = char_and_move.split(' ')
    fighter_name = str(words[0]).strip()
    move_search = str(words[1]).strip()

    print("Character:", fighter_name)
    print("Move:", move_search)

    frame_data = hitbot_query.GetFrameData(fighter_name, move_search)
    print(frame_data)

    if (frame_data != '404'):
        title_string = '**' + FormatField(0, frame_data) + '**'
        embed = discord.Embed(title=title_string,
                colour=discord.Colour(0x1e8488))

        embed.set_image(url=
                "http://kuroganehammer.com/images/ultimate/character/"
                + fighter_name + ".png")

        embed.add_field(name="Active Frames", value=FormatField(1, frame_data), inline=True)
        embed.add_field(name="Shield Advantage", value=FormatField(2, frame_data), inline=True)
        embed.add_field(name="Damage", value=FormatField(3, frame_data), inline=True)
        embed.add_field(name="Angle", value=FormatField(4, frame_data), inline=True)
        embed.add_field(name="Base Knockback", value=FormatField(5, frame_data), inline=True)
        embed.add_field(name="Knockback Growth", value=FormatField(6, frame_data), inline=True)
    else:
        embed = discord.Embed(title='**Error**',
                colour=discord.Colour(0x1e8488))
        embed.add_field(name="404", value='Could not find fighter, please check https://kuroganehammer.com/Ultimate/ for the current list of fighters', inline=True)

    await ctx.send(embed=embed)

def FormatField(index, frame_data):
    return ' → '.join([item[index] for item in frame_data])


BOT.run('TOKEN')

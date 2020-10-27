import discord
import random
import os
from discord.ext import commands

from utils import *

client = commands.Bot(command_prefix='.')

'''Variables'''
id_bot = os.environ["ID_BOT"]
liste_id_participant = []
current_id_vote = None
h = None

'''Event'''
@client.event
async def on_ready():
    print("Go")

@client.event
async def on_reaction_add(reaction, user):
    print("react!!!")
    msg_id = reaction.message.id
    if reaction.emoji == "🏃":
        if (belong(liste_id_participant, user.id)==False) and (msg_id == current_id_vote) and (user.id != id_bot):
            liste_id_participant.append(user.id)
            print(liste_id_participant)


'''Commands'''
@client.command(aliases=['self'])
async def me(msg, arg):
    identifiant = msg.author.id
    reponse = time_to_int(arg, identifiant)
    await msg.send(f'Hey <@{identifiant}> si tu veux arriver à {arg} tu vas devoir partir à **{reponse}**')

@client.command(aliases=['create'])
async def new(msg, arg):
    global current_id_vote
    global liste_id_participant
    global h
    liste_id_participant = []
    h = arg

    vote = await msg.send(f'Nouveau Pedibus pour {arg}, qui vient ?')
    await vote.add_reaction("🏃")
    current_id_vote = vote.id
    
@client.command(aliases=['recap'])
async def resume(msg):
    reponse = message(liste_id_participant, h)
    await msg.send(f'{reponse}')

client.run(os.environ["DISCORD_TOKEN"])

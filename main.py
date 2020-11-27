import discord
from discord.ext import commands
import asyncio

from data import USERS
from utils import bcolors, add_dico, time_to_int, belong,\
     message, print_ruler, printd


print(f"{bcolors.OKGREEN}Lancement du Pedibot{bcolors.ENDC}")
token = input("Veuillez entrer le token du bot : \n")
client = commands.Bot(command_prefix='.')

# Variables

liste_id_participant = []
current_id_vote = None
h = None


# Event


@client.event
async def on_ready():
    print_ruler()
    print(bcolors.BOLD +"Pedibot Initialisé :)"+ bcolors.ENDC)
    print(f'{bcolors.WARNING}NOM: {bcolors.ENDC}{client.user.name}')
    print(f'{bcolors.OKCYAN}ID: {bcolors.ENDC}{client.user.id}')
    print_ruler()
    await client.change_presence(activity=discord.Game(name=".aled"))


@client.event
async def on_reaction_add(reaction, user):
    msg_id = reaction.message.id
    if reaction.emoji == "🏃":
        if (user.id not in USERS):
            await user.send("Hey, <@{user.id}> il semblerait que tu"
                            + "ne fasse pas partie de ma base de donnée, "
                            + "ajoute toi avec la commande"
                            + "**.add <nom> <distance>**")

        elif (belong(liste_id_participant, user.id) is False) \
            and (msg_id == current_id_vote) \
                and (user.id != client.user.id):
            liste_id_participant.append(user.id)
            print(f'Liste des participants au vote : {liste_id_participant}')       


# Commands


@client.command(aliases=['self'])
async def me(msg, *args):
    identifiant = msg.author.id

    if (identifiant not in USERS):
        await msg.author.send("Hey, il semblerait que tu ne fasse"
                              + "pas partie de ma base de donnée,"
                              + "ajoute toi avec la commande "
                              + "**.add <nom> <distance>**")

    if (len(args) != 1):
        await msg.author.send("Format souhaité .self <heure>")

    else:
        reponse = time_to_int(args[0], identifiant)
        await msg.author.send(f'Hey <@{msg.author.id}> si tu veux arriver à {args[0]} \
                    tu vas devoir partir à **{reponse}**')


@client.command(aliases=['create'])
async def new(msg, *args):
    if (len(args) != 1):
        await msg.send("Format souhaité .new <heure>")

    else:
        if (USERS == {}):
            await msg.send("Personne dans ma base de donnée, ajoute toi avec la commande **.add <nom> <distance>**")

        else:
            global current_id_vote
            global liste_id_participant
            global h
            liste_id_participant = []
            h = args[0]
            vote = await msg.send(f'Nouveau Pedibus pour {args[0]}, qui vient ?')
            await vote.add_reaction("🏃")
            current_id_vote = vote.id


@client.command()
async def add(msg, *args):
    if (len(args) != 2):
        await msg.send(".add <nom> <distance>")
    else:
        id = msg.author.id
        add_dico(args[0], id, args[1])
        printd()


@client.command(aliases=['recap'])
async def resume(ctx):
    reponse = message(liste_id_participant, h)
    x = await ctx.send('Chargement')
    await asyncio.sleep(0.3)
    await x.edit(content=reponse)


@client.command()
async def aled(ctx):
    reponse = """
Voici les commandes que tu peux utiliser :
**.new** *hour* : Create a new pedibus and start a vote
**.recap** : Sum up who participate
**.add** *name* *distance* : Add you to the database
**.me** *hour* : Tell you what hour you need to leave"""
    await ctx.author.send(reponse)


client.run(f"{token}")

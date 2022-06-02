import discord
import time
import youtube_dl
import random
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException

# Clef api de giphy
api_key= ""
api_instance = giphy_client.DefaultApi()

# Récupération du token correspondant au bot ainsi que la mise en place du client
client = commands.Bot(command_prefix = '!',intents=discord.Intents.all())
TOKEN = ''

# Quand le bot est prêt
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("!aide"))
    print(f"{client.user.name} est connecté au serveur") 

# Quand un utilisateur discord rejoint le serveur on envoit en mp le mode d'emploi du bot
@client.event
async def on_member_join(member):
    await member.send("**Commandes Général :**\n"
                   "`!delete nombre` supprime le nombre de messages donné\n"
                   "\n"
                   "**Commandes Fun :**\n"
                   "`!octogone @utilisateur` créera un octogone entre toi et lui\n"
                   "`!chinese text` écrira ton text en caractère chinois\n"
                   "`!love @utilisateur @utilisateur` revoie le pourcentage de compatibilité entre deux personnes\n"
                   "`!meme text` trouve un meme par rapport au text rentré\n"
                   "`!de` lance un dé\n"
                   "`!piece` lance une pièce\n"
                   "`!kiss @utilisateur` envoie de l'amour à l'utilisateur choisit\n"
                   "`!slap @utilisateur` gifle l'utilisateur choisit\n"
                   "`!battle @utilisateur @utilisateur` Lance un combat entre deux utilisateurs\n"
                   "`!bruno` La phrase célèbre de Bruno Simon\n"
                   "\n"
                   "**Commandes De Musique :**\n"
                   "`!play lien vidéo youtube` lance la musique\n"
                   "`!pause` met en pause\n"
                   "`!resume` remet la musique si elle était en pause\n"
                   "`!leave` quitte le salon vocal\n"
                   "\n"
                   "**Commandes De Discution :**\n"
                   "`!chat init` Commencera la conversation\n"
                   "`!chat reponse` Pour choisir ce que vous voulez\n"
                   "`!chat retour` Pour retourner à la question d'avant\n"
                   "`!chat reset` Pour recommancer la discussion jusqu'au début\n")

# Dit bonjour avec un tts
@client.command(pass_context=True)
async def bonjour(ctx):
    await ctx.send("Hello everybody", tts=True)

# permet d'avoir la liste des commands
@client.command(pass_context=True)
async def aide(ctx):
    await ctx.send("**Commandes Général :**\n"
                   "`!delete nombre` supprime le nombre de messages donné\n"
                   "\n"
                   "**Commandes Fun :**\n"
                   "`!octogone @utilisateur` créera un octogone entre toi et lui\n"
                   "`!chinese text` écrira ton text en caractère chinois\n"
                   "`!love @utilisateur @utilisateur` revoie le pourcentage de compatibilité entre deux personnes\n"
                   "`!meme text` trouve un meme par rapport au text rentré\n"
                   "`!de` lance un dé\n"
                   "`!piece` lance une pièce\n"
                   "`!kiss @utilisateur` envoie de l'amour à l'utilisateur choisit\n"
                   "`!slap @utilisateur` gifle l'utilisateur choisit\n"
                   "`!battle @utilisateur @utilisateur` Lance un combat entre deux utilisateurs\n"
                   "`!bruno` La phrase célèbre de Bruno Simon\n"
                   "\n"
                   "**Commandes De Musique :**\n"
                   "`!play lien vidéo youtube` lance la musique\n"
                   "`!pause` met en pause\n"
                   "`!resume` remet la musique si elle était en pause\n"
                   "`!leave` quitte le salon vocal\n"
                   "\n"
                   "**Commandes De Discution :**\n"
                   "`!chat init` Commencera la conversation\n"
                   "`!chat reponse` Pour choisir ce que vous voulez\n"
                   "`!chat retour` Pour retourner à la question d'avant\n"
                   "`!chat reset` Pour recommancer la discussion jusqu'au début\n")
    
# fouine bot quitte le vocal
@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Tu n'es pas dans le channel vocal")

# à l'appel de la fonction suivi d'un lien youtube on connecte au vocal de l'utilisateur et on lance la musique
@client.command(pass_context=True)
async def play(ctx,url):
    if (ctx.author.voice):
        await ctx.message.author.voice.channel.connect()
    else:
        await client.get_channel(977523840018182198).connect()
    if (ctx.voice_client):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options':'-vn'}
        YDL_OPTIONS = {'format':"bestaudio"}
        player = ctx.voice_client
        # grace à la bibliothèque youtube_dl on va extraire pui load la vidéo
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
            player.play(source)

# mettre en pause la vidéo jouée dans le vocal
@client.command(pass_context=True)
async def pause(ctx):
    await ctx.voice_client.pause()

# remet en route la vidéo
@client.command(pass_context=True)
async def resume(ctx):
    await ctx.voice_client.resume()

# delete un nombre de messages envoyés
@client.command(pass_context=True)
async def delete(ctx, arg: int):
    messages = await ctx.channel.history(limit = arg + 1).flatten()
    for each_message in messages:
        await each_message.delete()

# envoie un meme gifi selon la catégorie souhaité
@client.command(pass_context=True)
async def meme(ctx,q="random"):
    try:
        api_responce = api_instance.gifs_search_get(api_key, q, limit=50, rating='R')
        lst = list(api_responce.data)
        giff = random.choice(lst)
        await ctx.channel.send(giff.embed_url)
    except ApiException as e :
        print("Problème d'appel API")

# envoie un meme octogone entre deux l'utisateur et un autre utilisateur 
@client.command()
async def octogone(ctx, user : discord.User):
    await ctx.send(f"**{ctx.author.name}** propose un octogone sans règles contre **{user.name}** ?\n"
                    "On attend la date, l'heure, le jour, pas d'arbitre.\n"
                    "https://media.giphy.com/media/WXB88TeARFVvi/giphy.gif")

# traduit avec des caractères asiatiques votre texte
@client.command(pass_context=True)
async def chinese(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))

# calcule randomly la compatibilité entre deux users
@client.command(pass_context=True)
async def love(ctx, user1 : discord.User, user2 : discord.User):
    lov = random.randint(0, 100)
    if (lov >= 60):
        await ctx.send(f"**{user1.name}** + **{user2.name}** = __{lov}%__ d'amour :sparkling_heart:")
    elif (lov >= 40):
        await ctx.send(f"**{user1.name}** + **{user2.name}** = __{lov}%__ d'amour :heart:")     
    else:
        await ctx.send(f"**{user1.name}** + **{user2.name}** = __{lov}%__ d'amour :broken_heart:")     

# lance un dé
@client.command(pass_context=True)
async def de(ctx):
    await ctx.send(f"**{random.randint(1, 6)}** :game_die:")

# lance une piece
@client.command(pass_context=True)
async def piece(ctx):
    coin = ["Pile", "Face"]
    await ctx.send(f"**{random.choice(coin)}** :coin:")

# donne un bisou à un autre utilisateur
@client.command(pass_context=True)
async def kiss(ctx, user : discord.User):
    kiss_list = ["https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif", "https://media.giphy.com/media/11k3oaUjSlFR4I/giphy.gif", "https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif"]
    await ctx.send(f"**{ctx.author.name}** kiss **{user.name}**\n"
                    f"{random.choice(kiss_list)}")

# claque un autre utilsateur
@client.command(pass_context=True)
async def slap(ctx, user : discord.User):
    slap_list = ["https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif", "https://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif", "https://media.giphy.com/media/xUO4t2gkWBxDi/giphy.gif", "https://media.giphy.com/media/tX29X2Dx3sAXS/giphy.gif", "https://media.giphy.com/media/AlsIdbTgxX0LC/giphy.gif", "https://media.giphy.com/media/k1uYB5LvlBZqU/giphy.gif"]
    await ctx.send(f"**{ctx.author.name}** slap **{user.name}**\n"
                    f"{random.choice(slap_list)}")

# deux utilisateurs se battent
@client.command(pass_context=True)
async def battle(ctx, user1 : discord.User, user2 : discord.User):
    battle_list = [user1.name, user2.name]
    await ctx.send(f"Un combat a été déclenché entre **{user1.name}** et **{user2.name}**")
    time.sleep(2)
    await ctx.send(f"Le vainqueur est **{random.choice(battle_list)}**")

# renvoie une phrase de bruno simon
@client.command(pass_context=True)
async def bruno(ctx):
    await ctx.send("Rare sont les écoles à pouvoir se vanter d'une telle proximité entre les étudiants et le groupe enseignant, que ce soit les intervenants ou l'administration.", tts=True)

# classe Arbre 
class Node :
    def __init__(self,keyword,question,list_child_node):
        self.keyword = keyword
        self.question = question  
        self.list_child_node = list_child_node


node = Node("help","Sur quel langague puis-je vous aider (`python`, `javascript` ou `php`)?",
    [
    Node("python", "`débutant` ou `confirmé`?",
        [
        Node("débutant", "Documentation `écrite` ou en `vidéo` en python?",
        [
            Node("écrite", "https://docs.python.org/3/", []),
            Node("vidéo", "https://www.youtube.com/watch?v=LamjAFnybo0", [])
        ]),
        Node("confirmé", "Documentation `écrite` ou en `vidéo` en python?",
        [
           Node("écrite", "https://docs.python.org/3/", []),
            Node("vidéo", "https://www.youtube.com/watch?v=p_dE8DD-oNs", []) 
        ])
        ]),
    Node("javascript", "`débutant` ou `confirmé`?",
        [
        Node("débutant", "Documentation `écrite` ou en `vidéo` en javascript?",
        [
            Node("écrite", "https://developer.mozilla.org/fr/docs/Web/JavaScript", []),
            Node("vidéo", "https://www.youtube.com/watch?v=QB1DTl7HFnc", [])
        ]),
        Node("confirmé", "Documentation `écrite` ou en `vidéo` en javascript?",
        [
           Node("écrite", "https://developer.mozilla.org/fr/docs/Web/JavaScript", []),
            Node("vidéo", "https://www.youtube.com/watch?v=JmbZBZhOtl8", []) 
        ])
        ]),
    Node("php", "`débutant` ou `confirmé`?",
        [
        Node("débutant", "Documentation `écrite` ou en `vidéo` en php?",
        [
            Node("écrite", "https://www.php.net/", []),
            Node("vidéo", "https://www.youtube.com/watch?v=fIOidjf1y5I", [])
        ]),
    Node("confirmé", "Documentation `écrite` ou en `vidéo` en php?",
        [
           Node("écrite", "https://www.php.net/", []),
            Node("vidéo", "https://www.youtube.com/watch?v=Zd5HgzemEms", []) 
        ])
        ])
    ])

# les variables historique, place qui correspond au node actuel et state pour savoir 
# si c'est la première fois qu'on lance la commande
histo=[]
place = node
state = False

# retourne vers le node parent
def retour(arbre, list):
    if len(list)==1 or list == []:
        return True
    for child in arbre.list_child_node:
        if child.keyword == list[-1][0]:
            return child
        else:
            retour(child, histo)
            
# command permetant de lancer le chat
@client.command()
async def chat(ctx, *arg):
    global node, place, histo, state
    txt = " ".join(arg)
    # première commande permetant de lancer le chat
    if txt == "init":
        state = True
        await ctx.send(place.question)
        return
    elif state == True:
        # revient au tout 1er node
        if txt == "reset":
            place = node
            await ctx.send(place.question)
        # remonte vers le node parent
        elif txt == "retour":
            print("true")
            back = retour(node, histo)
            if back == True:
                place = node
                await ctx.send(place.question)
            else:
                place = back
                await ctx.send(place.question)
        else:
            # selon le choix de l'user on se dirige vers le node enfant
            for child in place.list_child_node:
                if child.keyword in txt:
                    histo.append([place.keyword, place.question, place.list_child_node])
                    place = child
                    await ctx.send(place.question)
                    # si il n'y a plus de node on reset les variables
                    if place.list_child_node == []:
                        place = node
                        histo =[]
                        state = False
                        await ctx.send("Le chat s'est arrêté")
                    return
            await ctx.send("Je n'ai pas compris")

client.run(TOKEN)


# On s'est basé sur les deux fonctions récursives pour réaliser la commande chat

# histo=[]

# def retour(A, list):
#     if len(list)==1 or list == []:
#         return True
#     for child in A.list_child_node:
#         print(child.keyword)
#         print(list[-1][0])
#         if child.keyword == list[-1][0]:
#             return child
#         else:
#             retour(child, histo)

# def parcours(A):
#     print(A.question)
#     if A.list_child_node == []:
#         print("stop")
#         return
#     txt = input()
#     if txt == "reset":
#         parcours(first_node)
#     elif txt == "retour":
#         temp = retour(first_node, histo)
#         if temp == True:
#             parcours(first_node)
#         else:
#             parcours(temp)
#     else:
#         for child in A.list_child_node:
#             if child.keyword in txt:
#                 histo.append([A.keyword, A.question, A.list_child_node])
#                 parcours(child)

# parcours(first_node)
# print(histo)

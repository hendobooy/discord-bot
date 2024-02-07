import discord
from riotwatcher import LolWatcher, ApiError
import requests
from champs_dictionary import champion_names

#Configuração da API do LoL
key = 'SUA_KEY_AQUI' #Key da API do LoL
watcher = LolWatcher(key)
regiao = 'br1' #Região que será feito as consultas
base_url = 'https://americas.api.riotgames.com' #Link base para encurtar as APIS
base_url2 = 'https://br1.api.riotgames.com' #Outro link base para encurtar as APIS (Sim, cada um tem funções diferentes)
headers = {'X-Riot-Token': key}             #Executar em headers, senão irá ocorrer erro 401 (Não Autorizado)


#Ligar bot
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Olá Mundo, sou {self.user} (ID: {self.user.id})')
        print('--------------------------------------------------')


    # Script para ver top maestrias do invocador
    async def on_message(self, message):   

        if message.author == self.user.id: #Bot não irá se responder
           return

        if message.content.startswith('!main'):
            #Forneça as informações corretas
            try:
                summoner_name = message.content.split('!main')[1].strip() #Essa linha funciona como um input para pegar o nome do invocador
                summoner = watcher.summoner.by_name(regiao, summoner_name)
                puuid = summoner['puuid'] #Pega o PUUID do invocador
                champion_response = requests.get(f'{base_url2}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}', headers=headers)
                champion_data = champion_response.json() # Extrai as 5 primeiras datas consultadas
                champions_maestry = []
                champion_icon = []


                for maestry_champions in champion_data:
                    champion_id = maestry_champions['championId']
                    champion_lvl = maestry_champions['championLevel']
                    champion_points = maestry_champions['championPoints']
                    champion_name = champion_names.get(champion_id, 'Desconhecido')
                    champion_icon.append(champion_name)
                    champion_url = f"https://ddragon.leagueoflegends.com/cdn/14.3.1/img/champion/{champion_icon[0]}.png"
                    champions_maestry.append(f"**Campeão**: {champion_name}\n **Maestria:** {champion_lvl}\n **Pontos de Maestria:** {champion_points}\n")

                embed = discord.Embed(
                    title=f"Maestria de campeões - {summoner_name}",
                    color=discord.Color.purple()
                )
                embed.set_thumbnail(url=champion_url)
                embed.add_field(name="Top 1 Champion", value=champions_maestry[0], inline=False)
                embed.add_field(name="Top 2 Champion", value=champions_maestry[1], inline=False)
                embed.add_field(name="Top 3 Champion", value=champions_maestry[2], inline=False)
                embed.add_field(name="Top 4 Champion", value=champions_maestry[3], inline=False)
                embed.add_field(name="Top 5 Champion", value=champions_maestry[4], inline=False)
                
                await message.channel.send(embed=embed)
            except ApiError as e:
                await message.channel.send(f"Erro ao obter informações do invocador: {e}")
            except Exception as e:
                await message.channel.send(f"Há algo de errado com este jogador. Erro ao obter informações. _{e}_")




#Configuração e Key do Bot

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = MyClient(intents=intents)
client.run('SUA_KEY_AQUI') #Key do bot do discord
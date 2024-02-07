import discord
from riotwatcher import LolWatcher, ApiError
import requests

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



#Script para ver rank, winrate, KDA e campeões recem jogados no LoL

    async def on_message(self, message):
        if message.author == self.user.id:  #Bot não irá se responder
           return
            
        if message.content.startswith('!rank'):
            #Forneça as informações corretas
            try:
                summoner_name = message.content.split('!rank')[1].strip() #Essa linha funciona como um input para pegar o nome do invocador
                summoner = watcher.summoner.by_name(regiao, summoner_name)
                summoner_id = summoner['id']
                summoner_icon_id = summoner['profileIconId']
                puuid = summoner['puuid'] #Pega o PUUID do invocador
                matchs_ids_response = requests.get(f'{base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids', headers=headers) #Link da API matches
                match_ids = matchs_ids_response.json()[:5] # Extrai a data dos primeiros 5 IDs de partida

                champions = [] #Cria uma lista para armazenar todos os campeões das partidas
                KDA = [] #Cria uma lista para armazenar todos o KDA das partidas

                icon_url = f"http://ddragon.leagueoflegends.com/cdn/14.2.1/img/profileicon/{summoner_icon_id}.png" #Construir o icone do invocador
                
                stats = watcher.league.by_summoner(regiao, summoner['id'])
                #Verifica se o player é unranked
                if stats:
                    tier = stats[0]['tier']
                    rank = stats[0]['rank']
                    pdl = stats[0]['leaguePoints']
                    wins = stats[0]['wins']
                    losses = stats[0]['losses']
                
                    winrate = ((wins / (wins + losses) * 100))
                
                else:                      
                    tier = "Unranked"
                    rank = ""
                    pdl = 0
                    wins = 0
                    losses = 0
                    winrate = 0

                for match_id in match_ids:
                    match_response = requests.get(f'{base_url}/lol/match/v5/matches/{match_id}', headers=headers) #Busca as informações pelo id da partida
                    match_data = match_response.json() #Extrai a data da API requisitada
                    
                    
                    for participant in match_data['info']['participants']: #Acessa as infos e participantes na partida
                        if participant['puuid'] == puuid: #Verifica se o PUUID é o mesmo do jogador consultado
                            champions.append(participant['championName']) #Puxa os campeões da lista criada
                            champions_str = ', '.join(champions) #Arruma a formatação na hora de imprimir o nome dos campeões
                            KDA.append(f"{participant['kills']}/{participant['deaths']}/{participant['assists']}")
                            KDA_str = ', '.join(KDA)
                

                # Criar uma mensagem embed
                embed = discord.Embed(
                    title=f"Rank Status - {summoner_name}",
                    color=discord.Color.purple()
                )
                embed.add_field(name="Nome", value=summoner['name'], inline=False)
                embed.add_field(name="Nível", value=summoner['summonerLevel'], inline=False)

                embed.add_field(name= "Elo Solo/Duo", value=f"{tier} {rank}, {pdl} PDL", inline=True)
                
                embed.add_field(name="Vitórias", value=wins, inline=False)
                embed.add_field(name="Derrotas", value=losses, inline=False)
                embed.add_field(name='Campeoes recentes', value=champions_str, inline=False)
                embed.add_field(name='K/D/A', value=KDA_str, inline=False)
                
                #If e else feitos para não conflitar na hora de imprimir a porcetagem (tentar tirar porcetagem de 0 irá gerar um erro)

                if winrate == 0:
                    embed.add_field(name="Winrate", value=f"{winrate}%", inline=False)
                    embed.set_thumbnail(url=icon_url)
                    await message.channel.send(embed=embed)
                
                else:
                    embed.add_field(name="Winrate", value=f"{winrate :.4}%", inline=False)
                    embed.set_thumbnail(url=icon_url)
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
import discord

#Ligar bot
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Olá Mundo, sou {self.user} (ID: {self.user.id})')
        print('--------------------------------------------------')

    #Script para limpar x numeros de mensagens no chat
    async def on_message_delete(self, message):
        if message.author == self.user.id: #Bot não irá se responder
            return
        
        if message.content.startswith('!clear'):
            
            if message.author.guild_permissions.manage_messages: #Verifica se quem ativou o script tem permissão para gerenciar mensagens
                try:
                    amount = int(message.content.split()[1])  # Obtém o número de mensagens a serem excluídas
                    if amount > 10: #Põe limite no clear
                        await message.channel.send(f"Você não pode exeder o limite de mensagens, o limite é 10")
                        return
                    await message.delete()  # Exclui o comando
                    await message.channel.purge(limit=amount)  # Exclui as mensagens
                    await message.channel.send(f"{amount} mensagens foram limpas por {message.author.mention}.", delete_after=5)  # Mensagem de confirmação que será excluída após 5 segundos
                except IndexError:
                    await message.channel.send("Por favor, forneça um número de mensagens para limpar.")
                except ValueError:
                        await message.channel.send("Por favor, forneça um número válido de mensagens para limpar.")
            else:
                await message.channel.send("Você não tem permissão para gerenciar mensagens.")




#Configuração e Key do Bot

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = MyClient(intents=intents)
client.run('SUA_KEY_AQUI') #Key do Bot      
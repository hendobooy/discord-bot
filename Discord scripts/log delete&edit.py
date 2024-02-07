import discord

#Ligar bot
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Olá Mundo, sou {self.user} (ID: {self.user.id})')
        print('--------------------------------------------------')

    #Script para guardar log de mensagem editada ou apagada
    async def on_message_delete(self, message):
        if message.author == self.user.id: #Bot não irá se responder
            return

        if message.attachments == []:
            embed = discord.Embed(
                title="Log de mensagem apagada",
                color=discord.Color.red()
            )
            embed.set_author(name=(message.author.name) ,icon_url=(message.author.avatar_url))
            embed.add_field(name=(f'Mensagem de {message.author.name}'), value=(f'Deletada em {message.channel.name}'), inline=False)
            embed.add_field(name=(f'Mensagem deletada'), value=(message.content), inline=True)
            embed.set_footer(text=(f'Servidor que a mensagem foi deletada: {message.guild.name}'))

            await self.get_channel('ID_DO_CANAL').send(embed=embed) #Canal que a Embed vai ser enviada

        else:
            embed = discord.Embed(
                title="Log de imagem apagada",
                color=discord.Color.red()
            )
            embed.set_author(name=(message.author.name) ,icon_url=(message.author.avatar_url))
            embed.add_field(name=(f'Mensagem de {message.author.name}'), value=(f'Deletada em {message.channel.name}'), inline=False)
            embed.set_image(url = message.attachments[0].url)
            embed.set_footer(text=(f'Servidor que a mensagem foi deletada: {message.guild.name}'))

            await self.get_channel('ID_DO_CANAL').send(embed=embed) #Canal que a Embed vai ser enviada
        

    async def on_message_edit(self, before, after):
        if before.author.id == self.user.id:
            return
        
        else:
            embed = discord.Embed(
                title="Log de mensagem editada",
                color=discord.Color.red()
            )
            embed.set_author(name=(before.author.name) ,icon_url=(before.author.avatar_url))
            embed.add_field(name=(f'Mensagem de {before.author.name}'), value=(f'Editada em {before.channel.name}'), inline=False)
            embed.add_field(name=(f'Mensagem Original'), value=(before.content), inline=True)
            embed.add_field(name=(f'Mensagem Editada'), value=(f'_{after.content}_'), inline=True)
            embed.set_footer(text=(f'Servidor que a mensagem foi deletada: {before.guild.name}'))

            await self.get_channel('ID_DO_CANAL').send(embed=embed)




#Configuração e Key do Bot

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = MyClient(intents=intents)
client.run('SUA_KEY_AQUI') #Key do Bot
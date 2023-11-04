
import datetime
import json
import os
import discord
import constants

def init():
    if not os.path.exists('data/femboy_of_the_month.json'):
        with open('data/femboy_of_the_month.json', 'w') as f:
            f.write('[]')
            
def vote_femboy_of_the_month(user_id: int, voted_femboy: int):
    with open('data/femboy_of_the_month.json', 'r') as f:
        data = json.load(f)
        
    for i in data:
        if i['femboy_id'] == voted_femboy:
            i['voted_by'].append(user_id)
    else:
        data.append({'femboy_id': voted_femboy, 'voted_by': [user_id]})
        
    with open('data/femboy_of_the_month.json', 'w') as f:
        json.dump(data, f)
        
def has_user_voted(user_id: int):
    with open('data/femboy_of_the_month.json', 'r') as f:
        data = json.load(f)
        
    for i in data:
        if user_id in i['voted_by']:
            return True
        
    return False

def get_femboys():
    with open('data/femboy_of_the_month.json', 'r') as f:
        data = json.load(f)
        
    data = sorted(data, key=lambda x: len(x['voted_by']), reverse=True)
    return data

def clear_femboys():
    with open('data/femboy_of_the_month.json', 'w') as f:
        f.write('[]')

def month_to_word(month: int) -> str:
    if month == 1:
        return 'January'
    elif month == 2:
        return 'February'
    elif month == 3:
        return 'March'
    elif month == 4:
        return 'April'
    elif month == 5:
        return 'May'
    elif month == 6:
        return 'June'
    elif month == 7:
        return 'July'
    elif month == 8:
        return 'August'
    elif month == 9:
        return 'September'
    elif month == 10:
        return 'October'
    elif month == 11:
        return 'November'
    elif month == 12:
        return 'December'
    else:
        return 'Invalid month'


class FemboyOfTheMonth(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        init()
        super().__init__()
    
    @discord.slash_command(guild_ids=[constants.guild_id])
    async def vote_femboy_of_the_month(self, ctx: discord.ApplicationContext, femboy: discord.Member):
        if constants.femboy_stage_0_role not in [i.id for i in femboy.roles]:
            await ctx.respond('The user you tried to vote for is not a femboy', ephemeral=True)
        
        if has_user_voted(ctx.user.id):
            await ctx.respond('You have already voted for a femboy this month', ephemeral=True)
            return
        
        vote_femboy_of_the_month(ctx.user.id, femboy.id)
        await ctx.respond('Successfully voted for the femboy', ephemeral=True)
        
    async def submit_results(self):
        femboys = get_femboys()
        clear_femboys()
        
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        message = f'# Femboys of the month {month_to_word(yesterday.month)}\n'
        
        for i in range(min(3, len(femboys))):
            femboy = femboys[i]
            member = self.bot.get_guild(constants.guild_id).get_member(femboy['femboy_id'])
            if member is None:
                message += f'{i + 1}. User({femboy["femboy_id"]}) - {len(femboy["voted_by"])} votes\n'
            else:
                message += f'{i + 1}. {member.mention} - {len(femboy["voted_by"])} votes\n'
                
        message += '\n'
        message += 'Start voting for next month by using /vote_femboy_of_the_month'
        
        general = self.bot.get_guild(constants.guild_id).get_channel(constants.general_channel)
        await general.send(message)

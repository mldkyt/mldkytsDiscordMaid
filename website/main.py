import json
import subprocess
import discord
import constants
from flask import Flask, redirect, request

bot: discord.Bot = None
app = Flask('astolfo/Website')

@app.route('/widget')
def widget():
    with open('website/html/widget.html', 'r') as f:
        web = f.read()
        
    with open('changelog.md') as f:
        ver_data = f.read()

    ver_data = ver_data.split('\n')[0]
    ver_data = ver_data[2:]
    
    web = web.replace('%ver%', ver_data)
    
    guild = bot.get_guild(constants.guild_id)
    if guild is not None:
        web = web.replace('%members%', str(guild.member_count))
        web = web.replace('%online%', str(len([m for m in guild.members if m.status != discord.Status.offline])))
    else:
        web = web.replace('%members%', 'Offline')
        web = web.replace('%online%', 'Offline')    
    
    return web

@app.route('/')
def hello_world():
    with open('website/html/index.html', 'r') as f:
        web = f.read()
        
    return web

@app.route('/api/uptime')
def uptime():
    uptime_output = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()
    uptime_dict = {'uptime': uptime_output}
    return json.dumps(uptime_dict)

@app.route('/botideas')
def bot_ideas():
    with open('website/html/bot_ideas.html', 'r') as f:
        return f.read()
    
@app.route('/api/botideas')
def bot_ideas_api():
    with open('data/ideas.json', 'r') as f:
        return f.read()

@app.route('/botideas/<int:id>/delete')
def delete_idea(id: int):
    
    with open('data/ideas.json', 'r') as f:
        ideas: list = json.load(f)
    if id < 0 or id >= len(ideas):
        return redirect('/botideas')
    
    confirm = request.args.get('confirm')
    if confirm != '1':
        with open('website/html/idea_delete_confirm.html', 'r') as f:
            web = f.read()
            web = web.replace('%idea%', str(ideas[id]['idea']))
            web = web.replace('%id%', str(id))
            web = web.replace('%userid%', str(ideas[id]['user_id']))
            web = web.replace('%delurl%', str('/botideas/' + str(id) + '/delete?confirm=1'))
            return web
        
    del ideas[id]
    with open('data/ideas.json', 'w') as f:
        json.dump(ideas, f)
    return redirect('/botideas')


def run_app(bot_param: discord.Bot):
    global bot
    bot = bot_param
    app.run(port=7576)



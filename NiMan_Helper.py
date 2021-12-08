import discord
import requests
import random
import requests
import json
import time

# Custom
import NiMan_Constants as constants

# Helpers
global focused_user

def find_all(str, sub):
    start = 0
    returns = []
    while True:
        start = str.find(sub, start)
        if start == -1:
            break;
        returns.append(start)
        start += len(sub)
    return(returns)

def get_name(user):
    if '#' in user:
        return(user[:user.find('#')])
    return(user)

def get_id(members, username):
    for user in members:
        print(user.name)
        print(username)
        print('--')
        if user.name == username:
            return(user.id)
    return('')

def is_user(m):
    return m.author.name == focused_user.name

async def purge(channel, users):
    if len(users) == 0:
        focused_user = client.user.name
        users.append(client.user)
    print("trying to purge messages in" + channel.name + "by the following authors:")
    print(users)
    for user in users:
        print(user.name)
        print(focused_user.name)
        focused_user = user
        deleted = await channel.purge(limit=100, check=is_user)
        await channel.send('Deleted {} message(s) from '.format(len(deleted)) + focused_user)

async def exec_command(payload):
    if (payload.lower() == 'greet'):
        payload = constants.script_greeting
    if '.py' in payload:
        await exec_py_command(payload)
        return
    print('Executing payload: ' + payload)
    p = multiprocessing.Process(target=os.system, name="os.system", args=(payload,))
    print('Created process')
    print('Joining...')
    p.start()
    p.join(10)
    if p.is_alive():
        print('Execution still running, terminating...')
        p.terminate()
        p.join()
    print('Finished execution')

async def exec_py_command(py_payload):
    os.system(py_payload)

async def process_message(message, bot):
    if message.author == bot.user:
        print('ignored self'.format(message))
        return

    if message.author.name in constants.ignore_list:
        print('ignored {0.author.name}'.format(message))
        return

    if '`' in message.content:
        print('ignored {0.author.name} using `'.format(message))
        return

    if message.content.startswith('http'):
        print('ignored {0.author.name}\'s link to {0.content}'.format(message))
        return

    if len(message.content) > 250:
        print('ignored large message')
        return

    if bot.user in message.mentions and 'purge' not in message.content:
        await message.channel.send('Why you @ me bitch? No use in that... use a command lazy ass. If you really need help and are still reading this, I guess I\'ll tell you to use ' + constants.symbol + 'help. Now go make use of your life you dumbass piece of shit and get some help for your stupidity. :stuck_out_tongue:')
        return

    if 'cock' in message.content.lower():
        print('{0.author} said \'{0.content}\''.format(message))
        print('said nice cock!')
        gif = get_gif('nice', 20)
        await message.channel.send(gif[random.randint(0,19)])
        gif = get_gif('cock', 20)
        await message.channel.send(gif[random.randint(0,19)])
        await message.channel.send('NICE COCK!')
        return(False)

    if 'cock' not in message.content.lower() and ('nice' in message.content.lower()) or ('noice' in message.content.lower()):
        print('{0.author} said \'{0.content}\''.format(message))
        print('said noice!')
        gif = get_gif('nice', 20)
        await message.channel.send(gif[random.randint(0,19)])
        return(False)

    if 'ni' in message.content.lower():
        print('{0.author} said \'{0.content}\''.format(message))
        print('said ni!'.format(message))
        await message.channel.send('ni')
        return(False)

    if constants.symbol + 'n' in message.content.lower() or '!n' in message.content.lower():
        print('{0.author} said \'{0.content}\''.format(message))
        print('replaced ' + constants.symbol + 'n')
        await message.delete()
        await message.channel.send(message.content.replace(constants.symbol + 'n', 'nigga').replace('!n', 'nigga').replace(constants.symbol + 'N', "nigger").replace('!N', 'nigger'))
        return(False)

    return(False)

# Web APIs
def get_inspirational_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    print(json_data)
    return(json_data[0]['q'] + " -" + json_data[0]['a'])

def get_rs_quote():
    response = requests.get("http://ron-swanson-quotes.herokuapp.com/v2/quotes")
    print(response)
    return(response.text.replace("[","").replace("]","") + ' -Ron Swanson')

def get_cn_quote():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    print(response)
    return(response.text[response.text.find('value') + 7 : len(response.text) - 1])

def get_joke(type):
    if type.lower() not in ['any', 'misc', 'programming', 'dark', 'pun', 'spooky', 'christmas']:
        type = 'any'
    returns = []
    response = requests.get("https://v2.jokeapi.dev/joke/" + type)
    #print(response.text)
    if '\"type\": \"single\"' in response.text:
        joke = response.text[response.text.find('joke') + 6 : response.text.find('flags') - 5].replace("\\n","")
        #print(joke)
        returns.append(joke)
    elif '\"type\": \"twopart\"' in response.text:
        setup = response.text[response.text.find('setup') + 7 : response.text.find('delivery') - 5].replace("\\n","")
        delivery = response.text[response.text.find('delivery') + 10 : response.text.find('flags') - 5].replace("\\n","")
        #print(setup)
        #print(delivery)
        returns.append(setup)
        returns.append(delivery)
    print(returns)
    return(returns)

def get_gif(search_term, limit = 1):
    if limit <= 0 or limit > 30:
        limit = tenor_limit
    search_term_cleaned = ""
    for c in search_term:
        if c.isalnum():
            search_term_cleaned += c
    returns = []
    response = requests.get("https://g.tenor.com/v1/search?q=" + search_term_cleaned + "&key=" + constants.tenor_key + "&limit=" + str(limit))
    urls = find_all(response.text, '\"itemurl\":')
    print(urls)
    if len(urls) != limit:
        print('limit length mismatch')
        return
    for url in urls:
        start = url + 12
        end = response.text.find('\",', start + 1)
        returns.append(response.text[start:end:])
    print(returns)
    return(returns)

import discord
import json
from math import ceil
import random
from link_api import LinkApi
from ai import get_custom_resume, get_possible_questions, set_params
from pdf import render_pdf
import configparser
import warnings
import asyncio

client = discord.Client(intents=discord.Intents.default())
all_jobs = {}
all_posts = []

config = configparser.ConfigParser()
config.read('files/config.ini')
print("Config Loaded")


@client.event
async def on_ready():
    """
       Event handler triggered when the bot is ready and connected to Discord.

       It prints a message indicating the successful connection.
    """
    print(f'{client.user} has connected to Discord!')


async def send_message(message, content, title, max_length=4096):
    """
       Sends a message with embeds, splitting the content if necessary.

       Args:
           message (discord.Message): The original message triggering the action.
           content (str): The content of the message.
           title (str): The title of the embed.
           max_length (int, optional): The maximum length of each split message. Defaults to 4096.
    """
    for i in range(ceil(len(content) / max_length)):
        embed = discord.Embed(title=title)
        embed.description = (content[(max_length * i):(max_length * (i + 1))])
        await message.channel.send(embed=embed)


async def activate_alert(message, keywords, timeout):
    """
       Activates an alert by retrieving jobs from an API based on given keywords.

       Args:
           message (discord.Message): The original message triggering the action.
           keywords (list): A list of keywords for job searching.
           timeout (int): The timeout for the alert in seconds.
    """
    try:
        all_posts_local = []
        for key in keywords:
            jobs = link_api.get_jobs(key, limit=100, listed_time=86400)
            [all_posts_local.append(b) for b in jobs if b['post_id'] not in [a['post_id'] for a in all_posts]]

        for ind, post in enumerate(all_posts_local):
            rand_id = random.randint(1, 9999)
            if rand_id in all_jobs.keys():
                while rand_id in all_jobs.keys():
                    rand_id = random.randint(1, 9999)

            message_post = "Company: {} Job description: {} URL: {}".format(post['company_name'], post['job_post_text'],
                                                                            post['post_url'])
            all_jobs[rand_id] = post
            await send_message(message, message_post, str(rand_id) + " | " + post['post_title'])

        [all_posts.append(a) for a in all_posts_local]
        loop = asyncio.get_event_loop()
        loop.call_later(timeout, lambda: asyncio.ensure_future(activate_alert(message, keywords, timeout)))
    except:
        loop = asyncio.get_event_loop()
        loop.call_later(timeout, lambda: asyncio.ensure_future(activate_alert(message, keywords, timeout)))


async def trigger_alert(timeout, message, keywords):
    """
        Triggers an alert to periodically retrieve jobs based on given keywords.

        Args:
            timeout (int): The timeout for the alert in seconds.
            message (discord.Message): The original message triggering the action.
            keywords (list): A list of keywords for job searching.
    """
    await activate_alert(message, keywords, timeout)


@client.event
async def on_message(message):
    """
        Event handler triggered when a message is received.

        Args:
            message (discord.Message): The received message.
    """
    message.author.id = str(message.author.id)
    # if already registered user
    if str(message.author.id) in users:
        user_stats = users[message.author.id]
        if user_stats['is_registered'] == 0 and len(user_stats['name']) == 0:
            user_stats['name'] = message.content
            await message.channel.send(
                'Whats your job keywords? example: data scientist, machine learning engineer, python engineer')

        elif user_stats['is_registered'] == 0 and len(user_stats['job_key']) == 0:
            keywords = message.content.split(",")
            user_stats['job_key'] = keywords

            await message.channel.send(
                'Write your life story regarding work experience, personal projects, education and what ever you think is worth to mention or write your resume')

        elif user_stats['is_registered'] == 0 and len(user_stats['description']) == 0:
            user_stats['description'] = message.content
            user_stats['is_registered'] = 1

            save_users()
            await message.channel.send('You finally registered! now you can use the bot commands!')

    if message.content.startswith("!generate"):
        if message.author.id not in users:
            await message.channel.send('You have to register first, use !register command')
            return

        job_id = int(message.content.split("!generate")[1])
        if job_id not in all_jobs:
            await message.channel.send('Job id wasnt found')
            return

        job_description = all_jobs[job_id]['post_title'] + ' ' + all_jobs[job_id]['job_post_text']

        resume = "My name is " + users[message.author.id]['name'] + " " + users[message.author.id]['description']
        await message.channel.send('Generate custom resume based on your information and job description')
        res = get_custom_resume(config['AI'], resume, job_description, enhance_end=config['AI']['enhance_end'],
                                enhance_start=config['AI']['enhance_start'])
        json_object = json.dumps(res)

        # Writing to sample.json
        with open("edited_resume.json", "w") as outfile:
            outfile.write(json_object)
        out = render_pdf(res)
        if out:
            await message.channel.send(file=discord.File("resume.pdf"))
            await message.channel.send('Note: ' + res['note'])
            return

        await message.channel.send(file=discord.File("edited_resume.json"))
        await message.channel.send('Note: ' + res['note'])


    elif message.content == '!stats':
        if message.author.id not in users:
            await message.channel.send('You are not registered')
            return

        await message.channel.send(users[message.author.id])


    elif message.content == '!register':
        if message.author.id in users:
            await message.channel.send('You already have registered')
            return

        users[message.author.id] = {'name': '', 'job_key': [], 'description': '', 'is_registered': 0}

        await message.channel.send('Whats your name?')

    elif message.content == '!delete':
        if str(message.author.id) in users:
            users.pop(str(message.author.id))
            save_users()

            await message.channel.send('User deleted')

    elif message.content.startswith('!jobs') and str(message.author.id) in users and users[str(message.author.id)][
        'is_registered'] == 1:
        num_jobs = int(message.content.split("!jobs")[1].split()[0])
        add_filter = None
        if len(message.content.split("!jobs")[1].split()) == 2:
            add_filter = str(message.content.split("!jobs")[1].split()[1])

        key_words = users[message.author.id]['job_key']
        all_posts = []
        await message.channel.send("Getting newest jobs...")
        for key in key_words:
            a = link_api.get_jobs(config['JOBS'], key, num_jobs, add_filter)
            [all_posts.append(b) for b in a if b not in all_posts]

        for ind, post in enumerate(all_posts):
            rand_id = random.randint(1, 9999)
            if rand_id in all_jobs.keys():
                while rand_id in all_jobs.keys():
                    rand_id = random.randint(1, 9999)

            message_post = "Company: {} Job description: {} URL: {}".format(post['company_name'], post['job_post_text'],
                                                                            post['post_url'])
            all_jobs[rand_id] = post
            await send_message(message, message_post, str(rand_id) + " | " + post['post_title'])
            # await message.channel.send(message_post)
    elif message.content.startswith('!alert') and message.author.id in users and users[message.author.id][
        'is_registered'] == 1:
        num_seconds = int(message.content.split("!alert")[1])
        key_words = users[message.author.id]['job_key']
        await trigger_alert(num_seconds, message, key_words)
        await message.channel.send('Alert setup')
        return

    elif message.content.startswith('!questions') and str(message.author.id) in users:
        if message.author.id not in users:
            await message.channel.send('You have to register first, use !register command')
            return

        job_id = int(message.content.split("!questions")[1])
        if job_id not in all_jobs:
            await message.channel.send('Job id wasnt found')
            return

        await message.channel.send('Generating possible questions')
        res = get_possible_questions(all_jobs[job_id]['company_name'], all_jobs[job_id]['job_post_text'])

        message_to_write = """Possible interview questions for job post: 
        {}
        """.format(res)

        await message.channel.send(message_to_write)


# Users
def save_users():
    global users
    json_object = json.dumps(users)

    # Writing to sample.json
    with open("files/users.json", "w") as outfile:
        outfile.write(json_object)


def load_users():
    global users
    try:
        with open('files/users.json', 'r') as openfile:
            users = json.load(openfile)

        print("Loaded! ", len(users.keys()))
    except:
        pass


link_api = LinkApi(config['SECRETS']['linkedin_user'], config['SECRETS']['linkedin_pass'])
set_params(config['SECRETS']['openai_org'], config['SECRETS']['openai_key'])
load_users()
client.run(config['SECRETS']['discord_token'])

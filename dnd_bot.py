import discord
from discord.ext import commands
import aiosqlite
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='d#', intents=intents)

# Races, Classes, and Equipment data
races = {
    "Human": "Versatile and ambitious, humans are known for their adaptability and resilience.",
    "Elf": "Graceful and wise, elves have a deep connection with nature and magic.",
    "Dwarf": "Stout and sturdy, dwarves are known for their toughness and craftsmanship.",
    "Halfling": "Small and nimble, halflings are known for their luck and agility.",
    "Dragonborn": "Proud and powerful, dragonborn possess the heritage of dragons.",
    "Orc": "Strong and fierce, orcs are formidable warriors.",
    "Tiefling": "With infernal heritage, tieflings have a dark charm and magical abilities.",
    "Gnome": "Small and clever, gnomes are known for their intelligence and agility.",
    "Fairy": "Tiny and magical, fairies have an innate connection to nature.",
    "Cyborg": "Enhanced with technology, cyborgs have superior strength and intellect."
}

classes = {
    "Fighter": "Skilled in combat, fighters are versatile warriors.",
    "Wizard": "Masters of arcane magic, wizards can cast powerful spells.",
    "Rogue": "Stealthy and cunning, rogues excel in agility and precision.",
    "Cleric": "Divine spellcasters, clerics are healers and protectors.",
    "Ranger": "Experts in survival and tracking, rangers are at home in the wilderness.",
    "Police Officer": "Modern-day protectors of the peace, skilled in combat and investigation.",
    "Hacker": "Experts in technology and infiltration, hackers can manipulate digital systems.",
    "Engineer": "Skilled in mechanics and invention, engineers can create and repair devices.",
    "Medic": "Healers and caregivers, medics are adept in medicine and first aid.",
    "Explorer": "Adventurers and discoverers, explorers are skilled in navigation and survival."
}

equipment = {
    "Sword": "A basic weapon, effective in close combat. Damage: 1d8, Type: Slashing",
    "Bow": "A ranged weapon, useful for attacking from a distance. Damage: 1d6, Type: Piercing",
    "Staff": "A magical implement, enhances spellcasting abilities. Damage: 1d4, Type: Bludgeoning",
    "Shield": "Provides extra protection in combat. Armor Class: +2",
    "Potion": "A healing potion, restores health when consumed. Healing: 2d4 + 2",
    "Pistol": "A modern firearm, effective at short to medium range. Damage: 1d10, Type: Piercing",
    "Energy Shield": "A high-tech shield, offers superior protection. Armor Class: +3",
    "First Aid Kit": "A modern medical kit, useful for treating injuries. Healing: 3d4 + 3",
    "Grappling Hook": "A tool for climbing and maneuvering. Utility",
    "Laser Sword": "A futuristic weapon, effective in close combat. Damage: 1d12, Type: Energy"
}

adventure_states = {
    "forest_entrance": "You find yourself at the entrance of a dark forest. Do you want to enter? (yes/no)",
    "forest_deep": "You venture deeper into the forest. The trees tower above you, and the path becomes unclear. Make a Perception check (d#check perception).",
    "wolf_encounter": "A wolf appears on the path ahead. Do you want to fight it or try to scare it away? (fight/scare)",
    "fight_wolf": "Roll for attack (d#check strength).",
    "scare_wolf": "Roll for intimidation (d#check charisma).",
    "find_cabin": "You find a small, abandoned cabin. Do you want to enter? (yes/no)",
    "cabin_inside": "Inside the cabin, you find a mysterious chest. Do you want to open it? (yes/no)",
    "cabin_ignore": "You decide not to enter the cabin and continue your journey.",
    "forest_exit": "You have successfully navigated the forest. Your adventure continues...",
    "village": "You arrive at a small village. The villagers seem wary of strangers. Make a Charisma check to gain their trust (d#check charisma).",
    "mountain_path": "The path leads to a steep mountain trail. Do you wish to climb it? (yes/no)",
    "mountain_top": "You reach the mountain top and find a hidden cave. Do you want to explore it? (yes/no)",
    "cave_explore": "The cave is dark and damp. You find a treasure chest. Open it? (yes/no)",
    "mountain_fall": "You slip and fall, sustaining injuries. Roll for Constitution to minimize damage (d#check constitution).",
    "city_entrance": "You arrive at the bustling city gates. Guards stop you. Make a Persuasion check (d#check charisma).",
    "city_allowed": "You are allowed into the city. Where do you want to go? (marketplace/tavern)",
    "marketplace": "The marketplace is full of vendors. You find a mysterious merchant. Do you want to talk to him? (yes/no)",
    "tavern": "The tavern is lively. You overhear a conversation about a hidden treasure. Do you want to investigate? (yes/no)",
    "urban_chase": "You witness a thief stealing a purse. Do you chase after him? (yes/no)",
    "chase_thief": "You chase the thief through the streets. Roll for Dexterity (d#check dexterity).",
    "suburban_park": "You find a peaceful park with a hidden garden. Do you want to explore? (yes/no)",
    "garden_explore": "The garden is beautiful and serene. You find a hidden path. Do you follow it? (yes/no)",
    "abandoned_factory": "An old factory stands before you. Do you enter? (yes/no)",
    "factory_inside": "Inside, you find old machinery and strange noises. Investigate further? (yes/no)",
    "seaside_cliff": "You stand on a cliff overlooking the sea. There's a narrow path down. Climb down? (yes/no)"
}

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    async with aiosqlite.connect('dnd.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            race TEXT,
            class TEXT,
            abilities TEXT,
            background TEXT,
            equipment TEXT,
            adventure_state TEXT
        )''')
        await db.commit()

@bot.command()
async def start(ctx):
    await ctx.send('Welcome to D&D Adventure Bot! Use d#create to create your character.')

@bot.command()
async def create(ctx):
    await ctx.send('Let\'s create your character! First, choose your race. Use d#race <race_name>. Available races are: ' + ', '.join(races.keys()))

@bot.command()
async def race(ctx, *, race_name: str):
    if race_name not in races:
        await ctx.send(f'{race_name} is not a valid race. Available races are: ' + ', '.join(races.keys()))
        return
    async with aiosqlite.connect('dnd.db') as db:
        await db.execute('INSERT OR REPLACE INTO users (user_id, race) VALUES (?, ?)', (ctx.author.id, race_name))
        await db.commit()
    await ctx.send(f'Race set to {race_name}. Now choose your class with d#class <class_name>. Available classes are: ' + ', '.join(classes.keys()))

@bot.command()
async def class_(ctx, *, class_name: str):
    if class_name not in classes:
        await ctx.send(f'{class_name} is not a valid class. Available classes are: ' + ', '.join(classes.keys()))
        return
    async with aiosqlite.connect('dnd.db') as db:
        await db.execute('UPDATE users SET class = ? WHERE user_id = ?', (class_name, ctx.author.id))
        await db.commit()
    await ctx.send(f'Class set to {class_name}. Next, set your abilities with d#abilities <abilities_list>.')

@bot.command()
async def abilities(ctx, *, abilities_list: str):
    async with aiosqlite.connect('dnd.db') as db:
        await db.execute('UPDATE users SET abilities = ? WHERE user_id = ?', (abilities_list, ctx.author.id))
        await db.commit()
    await ctx.send(f'Abilities set to {abilities_list}. Now choose your background with d#background <background_name>.')

@bot.command()
async def background(ctx, *, background_name: str):
    async with aiosqlite.connect('dnd.db') as db:
        await db.execute('UPDATE users SET background = ? WHERE user_id = ?', (background_name, ctx.author.id))
        await db.commit()
    await ctx.send(f'Background set to {background_name}. Finally, set your equipment with d#equipment <equipment_list>. Available equipment: ' + ', '.join(equipment.keys()))

@bot.command()
async def equipment(ctx, *, equipment_list: str):
    async with aiosqlite.connect('dnd.db') as db:
        await db.execute('UPDATE users SET equipment = ? WHERE user_id = ?', (equipment_list, ctx.author.id))
        await db.commit()
    await ctx.send(f'Equipment set to {equipment_list}. Your character creation is complete! Use d#adventure to start your adventure.')

@bot.command()
async def adventure(ctx):
    user_id = ctx.author.id
    async with aiosqlite.connect('dnd.db') as db:
        cursor = await db.execute('SELECT adventure_state FROM users WHERE user_id = ?', (user_id,))
        row = await cursor.fetchone()
        if row and row[0]:
            adventure_state = row[0]
        else:
            adventure_state = 'forest_entrance'
            await db.execute('UPDATE users SET adventure_state = ? WHERE user_id = ?', (adventure_state, user_id))
            await db.commit()

    if adventure_state in adventure_states:
        await ctx.send(adventure_states[adventure_state])
        await update_adventure_state(user_id, 'forest_deep') # Example progression, you can customize this

async def update_adventure_state(user_id: int, new_state: str):
    async with aiosqlite.connect('dnd.db') as db:
        await db.execute('UPDATE users SET adventure_state = ? WHERE user_id = ?', (new_state, user_id))
        await db.commit()

async def skill_check(ability: str, user_id: int):
    async with aiosqlite.connect('dnd.db') as db:
        cursor = await db.execute('SELECT abilities FROM users WHERE user_id = ?', (user_id,))
        row = await cursor.fetchone()
        if row:
            abilities = row[0].split(',')
            ability_score = int([a.split(':')[1] for a in abilities if a.split(':')[0] == ability][0])
            roll = random.randint(1, 20)
            return roll + ability_score
        return None

@bot.command()
async def check(ctx, ability: str):
    user_id = ctx.author.id
    result = await skill_check(ability, user_id)
    if result is not None:
        await ctx.send(f'{ability.capitalize()} check result: {result}')
    else:
        await ctx.send('You need to create a character first using d#create.')

bot.run('YOUR_DISCORD_BOT_TOKEN')

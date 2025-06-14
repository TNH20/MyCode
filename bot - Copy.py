#python bot.py to run

from discord.ext import commands, tasks
import discord
import random 
import asyncio
import yfinance as yf
BOT_TOKEN = "your bot token here"



bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())



@bot.event
async def on_ready():
    print("bot is online")
    for guild in bot.guilds:
        botChannel = discord.utils.get(guild.text_channels, name="bot-channel")
        if botChannel and botChannel .permissions_for(guild.me).send_messages:
            await botChannel.send("I have awoken")
        else:
            print("could not find server name") 
   
    

@bot.command()
async def hello(ctx): #ctx means it doesnt have to search 
    user = ctx.author.name #looks for the users name
    await ctx.send(f"kill yourself {user}!!")


#---------------------server info---------------------
@bot.command(name="serverinfo")
async def server_stats(ctx):
    #giving all the data new names so they are easier to call
    guild = ctx.guild 
    server_name = guild.name
    server_id = guild.id
    member_count = guild.member_count
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    total_channels = len(guild.channels)
    owner = guild.owner
    roles = len(guild.roles)
    created_at = guild.created_at.strftime("%d, %B, %Y")

    embed = discord.Embed(title=f"Server Stats for {server_name}", color=discord.Color.blue()) #how the emebeded text will look 
    embed.add_field(name="Server Name", value=server_name, inline=False) #putting all the data in the embed box 
    embed.add_field(name="Server ID", value=server_id, inline=False)
    embed.add_field(name="Owner", value=owner, inline=False)
    embed.add_field(name="Member Count", value=member_count, inline=False)
    embed.add_field(name="Text Channels", value=text_channels, inline=True)
    embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="Total Channels", value=total_channels, inline=True)
    embed.add_field(name="Roles", value=roles, inline=True)
    embed.add_field(name="Created On", value=created_at, inline=False)

    await ctx.send(embed=embed) #sending the embeded message 

#---------------------reminder------------------------------
@bot.command(name='remind')
async def set_reminder(ctx, time: int, unit: str, *, reminder: str):
    # Convert the time to seconds based on the unit
    user = ctx.author.name
    if unit == 's' or unit == 'seconds':
        wait_time = time
    elif unit == 'm' or unit == 'minutes':
        wait_time = time * 60
    elif unit == 'h' or unit == 'hours':
        wait_time = time * 3600
    else:
        await ctx.send("Invalid time unit. Use 's' for seconds, 'm' for minutes, or 'h' for hours.")
        return

    # Confirm to the user that the reminder is set
    await ctx.send(f"Okay! I will remind you in {time} {unit}.")

    # Wait for the specified time
    await asyncio.sleep(wait_time)

    # Send the reminder message
    await ctx.send(f"{ctx.author.mention}⏰ Reminder: {reminder}")

@bot.event #waits for something to happen
async def on_member_join(member, ctx):
    WelcomeChannel = "welcome"
    channel = discord.utils.get(ctx.guild.text_channels, name=WelcomeChannel)
    welcomeMessage = f"{member.mention} has joined the server, fuck you!"
    if channel:
        await channel.send(welcomeMessage)
    

#--------------------roulette wheel------------
roulette_wheel = { #dictionary listing all the numbers and corresponding colours
    0: "green",
    1: "red", 2: "black", 3: "red", 4: "black", 5: "red", 6: "black",
    7: "red", 8: "black", 9: "red", 10: "black", 11: "black", 12: "red",
    13: "black", 14: "red", 15: "black", 16: "red", 17: "black", 18: "red",
    19: "red", 20: "black", 21: "red", 22: "black", 23: "red", 24: "black",
    25: "red", 26: "black", 27: "red", 28: "black", 29: "black", 30: "red",
    31: "black", 32: "red", 33: "black", 34: "red", 35: "black", 36: "red"
}

# Dictionary to track user's balance
user_balances = {}
slagBalance = {}
# Function gets users balance
def get_balance(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = 1000  # Start each user with a balance of 1000 units
    return user_balances[user_id]

# Function to update the balance of a user
def update_balance(user_id, amount):
    user_balances[user_id] = get_balance(user_id) + amount
    
        

#----------------roulette game---------------------
@bot.command(name='roulette')
async def roulette(ctx, bet_amount: int, *, bet_type: str):
    user_id = ctx.author.id  # Get the user's ID
    balance = get_balance(user_id)  # Get the user's current balance
    
    if bet_amount == 'all':
        bet_amount == user_balances
    # Check if the user has enough balance to place the bet
    if bet_amount > balance:
        await ctx.send(f"Sorry, you are too poor, why dont you get a job. Your current balance is {balance}.")
        return

    # Spin the roulette wheel
    number = random.randint(0, 36)
    color = roulette_wheel[number]  # Get the color corresponding to the spun number

    # Message to display the result of the spin
    result_message = f"The ball landed on {number} {color}!"

    # Determine if the user won or lost and update the balance
    if bet_type.isdigit():  # Bet on a specific number
        bet_number = int(bet_type)
        if bet_number == number:
            winnings = bet_amount * 35  # Payout for a correct number is 35:1
            update_balance(user_id, winnings)
            await ctx.send(f"{result_message} Congratulations, you won {winnings}! Your new balance is {get_balance(user_id)}.")
        else:
            update_balance(user_id, -bet_amount)
            await ctx.send(f"{result_message} Sorry, you lost {bet_amount}. Your new balance is {get_balance(user_id)}.")
    
    elif bet_type.lower() in ["red", "black"]:  # Bet on a color
        if bet_type.lower() == color:
            winnings = bet_amount * 2  # Payout for correct color is 2:1
            update_balance(user_id, winnings)
            await ctx.send(f"{result_message} Congratulations, you won {winnings}! Your new balance is {get_balance(user_id)}.")
        else:
            update_balance(user_id, -bet_amount)
            await ctx.send(f"{result_message} Sorry, you lost {bet_amount}. Your new balance is {get_balance(user_id)}.")

    elif bet_type.lower() in ["even", "odd"]:  # Bet on even or odd
        if (number != 0) and ((number % 2 == 0 and bet_type.lower() == "even") or
                              (number % 2 != 0 and bet_type.lower() == "odd")):
            winnings = bet_amount * 2  # Payout for correct even/odd is 2:1
            update_balance(user_id, winnings)
            await ctx.send(f"{result_message} Congratulations, you won {winnings}! Your new balance is {get_balance(user_id)}.")
        else:
            update_balance(user_id, -bet_amount)
            await ctx.send(f"{result_message} Sorry, you lost {bet_amount}. Your new balance is {get_balance(user_id)}.")
    
    else:
        await ctx.send("Invalid bet type. Please bet on a number (0-36), color (red/black), or even/odd.")

#-----------------balance-----------------------
@bot.command(name='balance')
async def balance(ctx):
    user_id = ctx.author.id  # Get the user's ID
    balance = get_balance(user_id)  # Get the user's balance
    if balance == 0: #this is self explanitory
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name="", value=f"you are broke, you should try getting a job. Your balance is {balance}")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="", value=f"Your current balance is {balance}.")
        await ctx.send(embed=embed)


#-----------------WORK---------------------
@bot.command(name='work')
async def reset_balance(ctx):
    user = ctx.author #looks for the author of the command
    user_id = ctx.author.id 
    balance = get_balance(user_id) 
    amount = random.randint(100, 10000) #random number between 10 and 1000
    update_balance(user_id, amount) #updates user balance with that numberS
    embed = discord.Embed(color=discord.Color.green())
    embed.add_field(name= "", value=f"\n {user} has decided to get a job, +{amount}.")
    embed.add_field(name="", value=f"\n your balance is {get_balance(user_id)}")
    #await ctx.send(f"{user} has decided to get a job, +{amount}.") #prints the amount won   
    #await ctx.send(f"your balance is {get_balance(user_id)}") #prints updated number
    await ctx.send(embed=embed)

@bot.command(name='slut')
async def slut(ctx):
    slagBalance[user_id] = slagBalance + 1
    if slagBalance >= 3:
        role = discord.utils.get(user_id.guild.roles, name="pro slag")
        await user_id.add_roles(role)
    user = ctx.author
    user_id = ctx.author.id
    balance = get_balance(user_id)
    chance = random.randint(0, 1)
    if chance == 0:
        amount = random.randint(1000, 20000)
        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name="", value=f"you got your lil peter out online and got paid {amount}")
        await ctx.send(embed=embed)
        update_balance(user_id, amount)
    if chance == 1:
        amount = random.randint(1000, 20000)
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="", value=f"You got caught jorking in a public park and got fined {amount}")
        await ctx.send(embed=embed)
        update_balance(user_id, -amount)
   

#-----------------roulette scoreboard-------------------
@bot.command(name="scoreBoard")
async def rouletteScoreboard(ctx):
    balanceList = [] #creates array for users balances
    for user_id, balance in user_balances.items(): #for every user find out there balance
        user = await bot.fetch_user(user_id)
        #balance.sort(reverse=True)#sorts the score in descending order DOES NOT WORK!!!!
        balanceList.append(f"{user.name}:{balance}") #put usernames and balances into the array
        if not user_balances: #if there is no balance print "no score"
            balanceList.append(f"{user.name}: no score") #DOESNT WORK IDK WHY 
            return
    embed = discord.Embed(title="current roulette score", description="\n".join(balanceList), color=discord.Color.red()) #embed all the data into a nice looking box 
    await ctx.send(embed=embed) #print the embedded box

#--------------------polling system-------------------
@bot.command(name='poll')
async def create_poll(ctx, question: str, *options: str):
    # Ensure there are at least two options and no more than 10 options
    if len(options) < 2 or len(options) > 10: 
        await ctx.send("You need to provide between 2 and 10 options.")
        return

    # List of emoji numbers for voting 
    emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    # Create the poll embed
    description = []
    for i, option in enumerate(options):
        description.append(f"{emoji_numbers[i]} {option}")
    embed = discord.Embed(title=question, description="\n".join(description), color=discord.Color.pink())
    
    # Sends the emebeded poll message 
    poll_message = await ctx.send(embed=embed)

    #adding the reactions for the amount of options there is 
    for i in range(len(options)):
        await poll_message.add_reaction(emoji_numbers[i])

#-------------------stock market stuff-------------
@bot.command(name='stock')
async def stockmaket(ctx, stock: str, time: str):
    stock = yf.Ticker(stock)
    data = stock.history(period=time)
    embed = discord.Embed(color=discord.Color.green())
    if time == '1d': #for todays data
        info = stock.info
        price = info.get("regularMarketPrice")
        change = info.get("regularMarketChangePercent")
        embed.add_field(name="", value=f"price is:{price}")
        embed.add_field(name="", value=f"change is:{change}")
        sector = stock.info['sector']
        embed.add_field(name="", value=f"sector:{sector}")
        beta = stock.info['beta']
        embed.add_field(name="", value=f"beta:{beta}")
        await ctx.send(embed=embed)

    else:
        embed.add_field(name="", value=data, inline=True)
        await ctx.send(embed=embed)


@tasks.loop(minutes=5)
async def stockCheck():
    tracking = {"AAPL", "TSLA", "GOOG"}
    channel = bot.get_channel(name="stock-market")

    for stock in tracking:
        stock = yf.Ticker(stock)
        price = stock.info.get("regularMarketPrice")
        if price is None:
            continue

        lastPrice = tracking[stock]

        if lastPrice is not None:
            change = ((price - lastPrice) / lastPrice) * 100 #calculating the percentage change

            if abs(change) >= 4:
                up = f"{tracking[stock]} is UP by :{change}%"
                embed = discord.Embed(color=discord.Color.green())
                embed.add_field(name="UP", value= up, inline=True)
                await channel.send(embed=embed)
                if change > 0:
                    down = f"{tracking[stock]} is DOWN by: {change}%"
                    embed = discord.Embed(color=discord.Color.red())
                    embed.add_field(name="DOWN", value=down, inline=True)

    

bot.run(BOT_TOKEN)
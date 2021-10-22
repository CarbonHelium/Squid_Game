#!/usr/bin/env python3
"""
Squid Game: Stepping Stones Game Simulations

Created by Carbon Helium
- YouTube: https://www.youtube.com/c/CarbonHeliumYT
- Twitter: https://twitter.com/CarbonHelium
- Discord: https://discord.gg/wrf8THN

This script was created for a YouTube video and may be unoptimised. I 
am not a computer scientist by any means so don't judge kthx
======================

This code is meant to simulate the stepping stones game featured in 
the show Squid Game. Can specify the amount of simulations, players, 
and stepping stones. Produces a distribution of the number of players 
to survive, and where the deaths occur.

RULES:
- Assume each player knows which stone is correct after another jumps
into that section. Because of this, can just simulate each glass pane
themselves rather than all the players
- Players go in turn order, play fairly so it's all chance
- One broken glass pane = one death
- 50% chance the glass will break on each attempt

This code is in reality just a simulation for a binomial distribution
model where p = 0.5, and you can choose n and the number of trials

"""

import pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import numpy as np

# Specify how many simulations you want, players, and stones
sims = int(10e4)
players = 16
stones = 18

players_survived = np.zeros(players+1)    # Stores the number of players who survive each game
player_wins = np.zeros(players)           # Stores how many times each numbered player survives
death_stones = np.zeros(stones)           # Stores how many deaths occur on each stone
total_deaths = 0                          # Keeps track of the total deaths for the memes

# Creates list of players with their number
player_number = []
for i in range(0, players):
    player_number.append('{}'.format(i+1))

# Player survival count
survived = []
for i in range(0, players+1):
    survived.append('{}'.format(i))
    
# Creates list of stones with their number
stone_number = []
for i in range(0, stones):
    stone_number.append('{}'.format(i+1))

for s in range(0, sims):

    if s % 10000 == 0: print(f'{s} out of {sims} games conducted')

    stone_stability = np.random.randint(2, size=stones)
    game_deaths = 0

    for i in range(0, stones):
        if game_deaths == players:
            break
        if stone_stability[i] == 1:
            death_stones[i] += 1
            game_deaths += 1
            total_deaths += 1
        else:
            continue
    
    players_survived[players - game_deaths] += 1

    for i in range(game_deaths, players):
        player_wins[i] += 1

print('Done!') 
print('============================')
print(f'You killed {total_deaths} people. You monster!')
print('============================')

def main():
    output_dir = pathlib.Path.cwd() / "Squid_Game"
    if not output_dir.is_dir():
        output_dir.mkdir()
    
    # Want win percentage rather than number of wins
    win_perc = (player_wins / sims) * 100
    players_survived_perc = (players_survived / sims) * 100

    # Plots the number of players that survived
    fig1, ax = pyplot.subplots()
    ax.bar(survived, players_survived_perc)
    ax.set_title("Frequency of Surviving Player Counts - Players: {}, Stones: {}".format(players, stones))
    ax.set_xlabel("Number of Surviving Players")
    ax.set_ylabel("% Chance")
    print('% Chance for Number of Players Surviving:')
    print(np.around(players_survived_perc, 1))
    print('============================')

    # Plots the player survivability %
    fig2, ay = pyplot.subplots()
    ay.bar(player_number, win_perc)
    ay.set_title("Player Survivability % - Players: {}, Stones: {}".format(players, stones))
    ay.set_xlabel("Player Number")
    ay.set_ylabel("Win %")
    print('Win Percentage for each player:')
    print(np.around(win_perc, 1))
    print('============================')

    # Save graphs as a png for viewing!
    fig1.savefig("Squid_Game/sg_survival_count_pl={}_st={}.png".format(players, stones))
    fig2.savefig("Squid_Game/sg_win%_pl={}_st={}.png".format(players, stones))

if __name__ == "__main__":
    main()
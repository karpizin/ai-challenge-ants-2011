from tournament_manager import TournamentManager
import os

def register_bots():
    tm = TournamentManager()
    
    bots = {
        "RandomBot": "python3 bots/random_bot/MyBot.py",
        "StatueBot": "python3 bots/statue_bot/MyBot.py",
        "LeftyBot": "python3 bots/lefty_bot/MyBot.py",
        "GreedyFoodBot": "python3 bots/greedy_food_bot/MyBot.py",
        "ExplorerBot": "python3 bots/explorer_bot/MyBot.py",
        "DistanceBot": "python3 bots/distance_bot/MyBot.py",
        "SafetyFirstBot": "python3 bots/safety_first_bot/MyBot.py",
        "AggressiveHillBot": "python3 bots/aggressive_hill_bot/MyBot.py",
        "ScentBot": "python3 bots/scent_bot/MyBot.py",
        "HeatmapBot": "python3 bots/heatmap_bot/MyBot.py"
    }
    
    for name, cmd in bots.items():
        tm.add_player(name, cmd)
        print(f"Registered {name}")

if __name__ == "__main__":
    register_bots()

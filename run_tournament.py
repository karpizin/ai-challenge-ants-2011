import argparse
import os
import random
from tournament_manager import TournamentManager, logger
from register_new_bots import register_bots

def get_map_players(map_path):
    try:
        with open(map_path, 'r') as f:
            for line in f:
                if line.startswith('players '):
                    return int(line.split()[1])
    except:
        pass
    return 2 # Default fallback

def main():
    parser = argparse.ArgumentParser(description="Ants Tournament Runner")
    parser.add_argument("--rounds", type=int, default=100, help="Number of matches to run")
    parser.add_argument("--init", action="store_true", help="Initialize sample bots")
    parser.add_argument("--list", action="store_true", help="Show leaderboard")
    args = parser.parse_args()

    # Always register bots from the bots/ folder
    register_bots()

    tm = TournamentManager()

    if args.init:
        # Add sample bots from the engine dist
        sample_path = "engine/dist/sample_bots/python"
        if os.path.exists(sample_path):
            tm.add_player("RandomBot", f"python3 {sample_path}/RandomBot.py")
            tm.add_player("HunterBot", f"python3 {sample_path}/HunterBot.py")
            tm.add_player("GreedyBot", f"python3 {sample_path}/GreedyBot.py")
            tm.add_player("LeftyBot", f"python3 {sample_path}/LeftyBot.py")
            logger.info("Sample bots added to database.")

    if args.list:
        print("\n🏆 CURRENT LEADERBOARD")
        print("-" * 30)
        for row in tm.get_leaderboard():
            print(f"{row['name']:<20} | {row['rating']:.1f}")
        return

    players = tm.get_active_players()
    if not players:
        logger.error("No players found in database. Run with --init first.")
        return

    # Discover maps
    map_files = []
    for root, _, files in os.walk("engine/maps"):
        for f in files:
            if f.endswith(".map"):
                map_files.append(os.path.join(root, f))

    if not map_files:
        logger.error("No maps found in engine/maps")
        return

    if not os.path.exists("replays"):
        os.makedirs("replays")

    logger.info(f"Starting tournament: {args.rounds} rounds.")

    for r in range(args.rounds):
        logger.info(f"--- Round {r+1}/{args.rounds} ---")
        
        # Pick a map and find compatible bots
        m = random.choice(map_files)
        num_players_needed = get_map_players(m)
        
        if len(players) < num_players_needed:
            logger.warning(f"Map {m} needs {num_players_needed} players, but only {len(players)} available. Skipping.")
            continue
            
        selected_players = random.sample(players, num_players_needed)
        p_ids = [p['id'] for p in selected_players]
        
        tm.run_match(p_ids, m)

    # Print final leaderboard
    print("\n🏆 FINAL LEADERBOARD")
    print("-" * 30)
    for row in tm.get_leaderboard():
        print(f"{row['name']:<20} | {row['rating']:.1f}")

if __name__ == "__main__":
    main()

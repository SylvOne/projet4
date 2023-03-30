def display_players(players):
    if len(players) > 1:
        print(f"---- ( {len(players)} participants) ----")
    else:
        print(f"---- ( {len(players)} participant) ----")
    for player in players:
        print(f"* {player.first_name} {player.last_name} ({player.national_id})")
    print("")
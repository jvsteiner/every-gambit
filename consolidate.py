import chess.pgn


# Function to attach a sequence of moves as variations to a given node
def attach_game_as_variation(root_node, moves, headers):
    current_node = root_node
    board = current_node.board()

    for move in moves:
        # If the move already exists as a variation, traverse it
        existing_node = None
        for variation in current_node.variations:
            if variation.move == move:
                existing_node = variation
                break

        if existing_node:
            current_node = existing_node
        else:
            # Add a new variation
            current_node = current_node.add_variation(move)
            board.push(move)

    current_node.comment = (
        f"vs. {headers.get('Black')} - {headers.get('Result')} - {headers.get('Date')}"
    )


def consolidate_games_to_variations(pgn_filename):
    """
    Consolidates multiple PGN games into a single game with variations.

    Args:
    pgn_filename (str): Path to the PGN file.

    Returns:
    chess.pgn.Game: A single PGN game containing all variations.
    """

    # Read the PGN file
    games = []
    with open(pgn_filename) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            headers = game.headers
            games.append((game, headers))

    if not games:
        return None

    # Initialize the root game with headers from the first game
    root_game = chess.pgn.Game()
    root_game.headers = games[0][1]

    for game in games:
        node = root_game
        moves = list(game[0].mainline_moves())
        attach_game_as_variation(node, moves, game[1])

    return root_game


if __name__ == "__main__":

    # Example usage
    pgn_filename = "spassky-kings-gambit.pgn"
    consolidated_game = consolidate_games_to_variations(pgn_filename)

    # Output the consolidated game to a new PGN file
    output_pgn_filename = "spassky-kg-consolidated.pgn"
    with open(output_pgn_filename, "w") as f:
        f.write(str(consolidated_game))

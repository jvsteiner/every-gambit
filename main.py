import chess.pgn
import io


def process(lines):
    d = []
    for line in lines:
        print(line)
        line = str(line)
        parts = line.split("\\xe2\\x80\\x93")
        name = parts[0].lstrip("b'").strip()
        code = parts[1].strip()
        moves = parts[2].strip().rstrip("\n")
        d.append((f"{name} - {code}", f"{moves}"))
    return d


if __name__ == "__main__":
    with open("gambits.txt", "rb") as f:
        gambits = f.readlines()
    gambits = process(gambits)
    print(gambits)

    main_game = chess.pgn.Game()
    node = main_game

    first_game = chess.pgn.read_game(io.StringIO(gambits[0][1]))
    for move in first_game.mainline_moves():
        node = node.add_variation(move)

    node.comment = gambits[0][0]

    for i in range(1, len(gambits)):
        print(i, gambits[i][0])
        node_parent = main_game
        next_game = chess.pgn.read_game(io.StringIO(gambits[i][1]))
        # next_game_node = node_parent.add_variation(next(next_game.mainline_moves()))

        for move in next_game.mainline_moves():
            node_parent = node_parent.add_variation(move)

        node_parent.comment = gambits[i][0]

    with open("combined_game.pgn", "w") as f:
        exporter = chess.pgn.StringExporter(
            headers=True, variations=True, comments=True
        )
        f.write(main_game.accept(exporter))


# # Read the two PGN games from the files
# with open("game1.pgn") as f:
#     pgn1 = f.read()

# with open("game2.pgn") as f:
#     pgn2 = f.read()

# # Parse the games
# game1 = chess.pgn.read_game(pgn1)
# game2 = chess.pgn.read_game(pgn2)

# # Create a new game that will contain both as variations
# main_game = chess.pgn.Game()

# # Create a node for the root position
# node = main_game

# # Add the first game as the main line
# for move in game1.mainline_moves():
#     node = node.add_variation(move)

# # Add the second game as a variation to the root node
# node_parent = main_game
# second_game_node = node_parent.add_variation(next(game2.mainline_moves()))
# for move in game2.mainline_moves():
#     second_game_node = second_game_node.add_variation(move)

# # Save the combined PGN to a file
# with open("combined_game.pgn", "w") as f:
#     exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
#     f.write(main_game.accept(exporter))

# print("Games combined successfully into combined_game.pgn")

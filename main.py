import chess.pgn
import io


def add_game_to_node(node, game, name):
    node_iter = node
    for move in game.mainline_moves():
        existing_variation = None
        for variation in node_iter.variations:
            if variation.move == move:
                existing_variation = variation
                break
        if existing_variation:
            node_iter = existing_variation
        else:
            node_iter = node_iter.add_variation(move)
    node_iter.comment = node_iter.comment + name


def process(lines):
    d = []
    for line in lines:
        line = str(line)
        parts = line.split("|")
        name = parts[0].lstrip("b'").strip()
        code = parts[1].strip()
        moves = parts[2].strip().rstrip("\n")
        d.append((f"{name} - {code}", f"{moves}"))
    return d


if __name__ == "__main__":
    with open("gambits.txt", "r") as f:
        gambits = f.readlines()
    gambits = process(gambits)

    main_game = chess.pgn.Game()

    for gambit in gambits:
        node = main_game
        next_game = chess.pgn.read_game(io.StringIO(gambit[1]))
        add_game_to_node(node, next_game, gambit[0])

    with open("every_gambit.pgn", "w") as f:
        exporter = chess.pgn.StringExporter(
            headers=True, variations=True, comments=True
        )
        f.write(main_game.accept(exporter))

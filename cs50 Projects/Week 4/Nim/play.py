import sys

from nim import train, play

def main():

    # Check command-line args
    if len(sys.argv) not in [1, 2]:
        sys.exit("Usage: python play.py [training_games=1000]")
    if len(sys.argv) == 2:
        try:
            n = int(sys.argv[1])
        except ValueError:
            sys.exit("Number of Training Games must be an integer")
    else:
        n = 1000

    print(f'Training AI on {n} games')
    ai = train(n)
    print(f'AI Trained on {n} games')
    print(f'Value of {len(ai.q)} actions have been estimated.')
    play(ai)


if __name__ == "__main__":
    main()
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Could be a knight or a knave 
    Or(AKnave,AKnight),
    # but not both 
    Not(And(AKnight,AKnave)),
    # if is a knight then is not a knave and viceversa
    Implication(AKnight,Not(AKnave)),
    Implication(AKnave,Not(AKnight)),
    # if looks for true <--> true Knight and Knight 
    Biconditional(AKnight,And(AKnight,AKnave))

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Could be a knight or a knave
    Or(AKnight, AKnave),
    # if is a knight then is not a knave and viceversa
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)), 
    # Could be a knight or a knave
    Or(BKnight, BKnave),
    # if is a knight then is not a knave and viceversa
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),

    # if aKnight then  both (A + B )are knights or (A +B ) are Knaves
    # if Bknight  then A is a night and b a knave or a is a knave and b is a knight 
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Could be a knight or a knave
    Or(AKnight, AKnave),
    # if is a knight then is not a knave and viceversa
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),

    Or(BKnight, BKnave),

    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    # if aKnight then  both (A + B )are knights or (A +B ) are Knaves
    # if Bknight  then A is a night and b a knave or a is a knave and b is a knight 
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Could be a knight or a knave
    Or(AKnight, AKnave),
    # if is a knight then is not a knave and viceversa
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Or(BKnight, BKnave),

    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),

    Or(CKnight, CKnave),
    Implication(CKnight, Not(CKnave)),
    Implication(CKnave, Not(CKnight)),
    # new information 
    # if A is a knight then A woul be a knight 
    Biconditional(Or(AKnight, AKnight), Or(AKnight, AKnave)),
    #if B is a knight then A is a knight intails A is a knave 
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    # if B is a Knight then C is a knave 
    Biconditional(BKnight, CKnave),
    # if C is a knight then A is a knight too 
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

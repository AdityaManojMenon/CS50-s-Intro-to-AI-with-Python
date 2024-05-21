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
    Or(AKnight, AKnave),

    Biconditional(AKnight, And(AKnight,AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    
    Implication(AKnight,And(AKnave,BKnave)),
    Implication(AKnave,Not(And(AKnave,BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),

    Biconditional(AKnight,And(AKnight,AKnave)),
    Biconditional(BKnight,Not(And(AKnight,AKnave))),
    Biconditional(BKnight,Not(And(BKnight,BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    Or(AKnight,AKnave), # A is either a knight or a knave
    Not(And(AKnight, AKnave)), # A can't be both a knight and a knave
    Or(BKnight,BKnave), # B is either a knight or a knave
    Not(And(BKnight,BKnave)), # B can't be both a knight and a knave
    Or(CKnight,CKnave), # C is either a knight or a knave
    Not(And(CKnight, CKnave)), # C can't be both a knight and a knave

    # B says "A said 'I am a knave'."
    Implication(BKnight, Biconditional(AKnight, Not(AKnight))),  # B says A said "I am a knave"
    Implication(BKnave, Not(Biconditional(AKnight, Not(AKnight)))),  # If B is lying, then A did not say "I am a knave"

    # B say "C is a Knave"
    Implication(BKnight, CKnave),  # If B is a knight, C is a knave
    Implication(BKnave, Not(CKnave)),  # If B is a knave, C is a knight

    # C says "A is a knight."
    Implication(CKnight, AKnight),  # If C is a knight, A is a knight
    Implication(CKnave, Not(AKnight))  # If C is a knave, A is a knave


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

def get_rank(number):
    """A function that returns the rank name as string"""

    rank = ["No Rank", "The Gravekeeper of fifth", "The Quatroguards", "The Third Prayer", "The Second Circle",
            "Choosen ascending", "One of the first", "Sekte Bot"]
    return rank[number]


def get_rank_id(number):
    # -1 and -2 are test values for test server.
    rank = {1: 817941435998535689, 2: 817940839404797982, 3: 815231250843435018, 4: 815230234411532288,
            5: 817935867829682236, 6: 815015673935691816, -1: 1025433481939009630, -2: 1025437474979319879,
            7: 816025727597674496}

    rank_id = rank[number]

    # Get rank (no rank = 0)
    # Rank "The Gravekeeper of the fifth" = 1 817941435998535689
    # Rank "The Quatroguards" = 2 817940839404797982
    # Rank "The third prayer" = 3 815231250843435018
    # Rank "The second circle" = 4 815230234411532288
    # Rank "The choosen ascending" = 5 817935867829682236
    # Rank "One of the first" = 6 815015673935691816
    # Rank Bot = 7 826114593830993933
    # Rank "Trusted Apostle" = 8 816025727597674496

    return rank_id

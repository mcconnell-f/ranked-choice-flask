def instant_runoff(df):
    def irv(df):
        '''
        Finds the winner using an instant runoff voting system

        Parameters
        ----------
        df: pandas data frame of voting results

        Returns
        -------
        votes: tuple list of (votes, candidate) in the
            case of a tie
        sorted(votes)[-1][1]: string of the name of the
            winner
        sorted(first_choice_votes)[-1][1]: string of the
            name of the winner
        '''
        text_to_return = ""

        df = df.fillna('no')
        number_of_voters = len(df)

        # creating a list of candidates
        li = []
        for c in range(1, len(df.columns)+1):
            li += list(df[f'Choice{c}'].values)
        candidates = set(li)
        eliminated_candidates = []
        if 'no' in candidates:
            candidates.remove('no')

        # looping through to redistribute votes
        for round_ in range(1, len(candidates) + 1):
            voter_id = 0

            # dictionary of candidate:votes
            votes_dictionary = {}
            for cand in candidates:
                votes_dictionary[cand] = 0

            # looping through first choice votes
            for vot in list(df[f'Choice1'].values):
                i = 0

                # while the choice candidate is in the eliminated list
                while vot in eliminated_candidates:
                    if i < len(df.columns):

                        # move to next choice candidate
                        vot = df.iloc[voter_id][f'Choice{i + 1}']
                    else:

                        # all choice candidates have been eliminated
                        vot = 'no'
                    i += 1
                if vot != 'no':
                    # adding the vote to the dictionary
                    votes_dictionary[vot] += 1
                voter_id += 1

            # printing vote information
            text_to_return += f"\nRound {round_}:\n"
            for cand in candidates:
                percentage_of_votes = (votes_dictionary[cand]/number_of_voters)*100
                if percentage_of_votes != 0:
                    text_to_return += f"{round(percentage_of_votes, 2)}% {cand} \
    ({votes_dictionary[cand]} votes)\n"

            # creating a tuple list of (votes, candidate)
            # (easier to sort through than a dictionary)
            votes = []
            for cand in candidates:
                if cand not in eliminated_candidates:
                    votes.append((votes_dictionary[cand], cand))

            # check if the most amount of votes > 50%
            if sorted(votes)[-1][0] > (.5*number_of_voters):
                return (sorted(votes)[-1][1], text_to_return)

            # eliminating the candidate with the fewest votes
            elif len(votes) > 1:
                minimum_number_of_votes = sorted(votes)[0][0]
                maximum_number_of_votes = sorted(votes)[-1][0]
                if minimum_number_of_votes == maximum_number_of_votes:
                    first_choice_votes = []
                    for vote_cand in sorted(votes):
                        first_choice_votes.append((df['Choice1'].value_counts()\
                                                   [vote_cand[1]], vote_cand[0]))
                    if sorted(first_choice_votes)[0] == sorted(first_choice_votes)[-1]:
                        return (votes,text_to_return)
                    else:
                        return (sorted(first_choice_votes)[-1][1], text_to_return)
                for vot in votes:
                    if vot[0] == minimum_number_of_votes:
                        eliminated_candidates.append(vot[1])

    w, text = irv(df)
    output_ret = ""
    if isinstance(w, list):
        output_ret += 'TIE between '
        if len(w) == 2:
            output_ret += f"{w[0][1]} and {w[1][1]}"
        else:
            for wi in w:
                if wi != w[-1]:
                    output_ret += f"{wi[1]}, "
                else:
                    output_ret += f"and {wi[1]}"
    else:
        output_ret += f"\n\n{w} is the winner."
    return text + output_ret

def single_transfer(seats,df):
    def stv(seats, df):
        '''
        Finds the winner using a single transferable voting system

        Parameters
        ----------
        seats: integer values of the number of positions to fill
        choices: integer value of the number of choices each
            voter gets to fill in
        df: pandas data frame of voting results

        Returns
        -------
        winners: list of the winners
        '''
        output_ret = ""

        df = df.fillna('no')
        winners = []
        number_of_voters = len(df)

        # creating a list of candidates
        li = []
        for c in range(1, len(df.columns)+1):
            li += list(df[f'Choice{c}'].values)
        candidates = set(li)
        eliminated_candidates = []
        if 'no' in candidates:
            candidates.remove('no')

        # looping through to redistribute votes
        for round_ in range(1, len(candidates) + 1):
            new_winner = False
            voter_id = 0

            # dictionary of candidate:votes
            votes_dictionary = {}
            for cand in candidates:
                votes_dictionary[cand] = 0

            # looping through first choice votes
            for vot in list(df[f'Choice1'].values):
                i = 0

                # while the choice candidate is in the eliminated list
                while vot in eliminated_candidates:
                    if i < len(df.columns):

                        # move to next choice candidate
                        vot = df.iloc[voter_id][f'Choice{i + 1}']
                    else:

                        # all choice candidates have been eliminated
                        vot = 'no'
                    i += 1

                # if a candidate has >= the votes required to win
                # temporarily eliminate them to prevent them from
                # recieving more votes
                if vot in winners:
                    if votes_dictionary[vot] >= ((1/(seats+1))*number_of_voters):
                        eliminated_candidates.append(vot)

                if vot != 'no':

                    # adding the vote to the dictionary
                    if vot in eliminated_candidates:
                        voter_id -= 1
                    else:
                        votes_dictionary[vot] += 1
                voter_id += 1

            # printing vote information
            output_ret += f"\nRound {round_}:"
            for cand in candidates:
                p = (votes_dictionary[cand]/number_of_voters)*100
                if cand in winners:
                    output_ret += f"\n{round(p, 2)}% {cand} ({votes_dictionary[cand]} votes)"
                elif cand not in eliminated_candidates:
                    output_ret += f"\n{round(p, 2)}% {cand} ({votes_dictionary[cand]} votes)"
            output_ret += "\n"

            # removing the winners from the set of eliminated candidates
            votes = []
            eliminated_candidates, winners = list(set(eliminated_candidates)), list(set(winners))
            for winner in winners:
                if winner in eliminated_candidates:
                    eliminated_candidates.remove(winner)

            # creating a tuple list of (votes, candidate)
            # (easier to sort through than a dictionary)
            for cand in candidates:
                if cand not in eliminated_candidates:
                    votes.append((votes_dictionary[cand], cand))
            for i in range(1, seats+1):

                # check if the most amount of votes > the threshold
                if sorted(votes)[-i][0] > ((1/(seats+1))*number_of_voters):
                    if sorted(votes)[-i][1] not in winners:
                        winners.append(sorted(votes)[-i][1])
                        new_winner = True
            if len(winners) == seats:
                return (winners, output_ret)

            # if no one new wins, eliminating the candidate with the fewest votes
            eligible_votes = []
            for tup in votes:
                if tup[1] not in winners:
                    eligible_votes.append(tup)
            if new_winner == False and len(votes) > seats:
                minimum_number_of_votes = sorted(eligible_votes)[0][0]
                maximum_number_of_votes = sorted(eligible_votes)[-1][0]
                if minimum_number_of_votes == maximum_number_of_votes:
                    seats_to_fill = seats-len(winners)
                    first_choice_votes = []
                    for vote_cand in sorted(eligible_votes):
                        first_choice_votes.append((df['Choice1'].value_counts()\
                                                   [vote_cand[1]], vote_cand[0]))
                    top_winners = []
                    max_first_votes = max(eligible_votes)[0]
                    for tup in eligible_votes:
                        if tup[0] == max_first_votes:
                            top_winners.append(tup)
                    winners += top_winners
                    return (winners, output_ret)
                for vot in votes:
                    if vot[0] == minimum_number_of_votes:
                        eliminated_candidates.append(vot[1])
        # returns a list of all winners
        return (winners, output_ret)

    w, text = stv(seats, df)
    text_ret = "\n\n"
    if len(w) == seats:
        if len(w) == 2:
            text_ret += f"{w[0]} and {w[1]}"
        else:
            for wi in w:
                if wi != w[-1]:
                    text_ret += f"{wi}, "
                else:
                    text_ret += f"and {wi}"
        text_ret += f" are the winners."
    else:
        min_c = []
        o_c = []
        min_v = min(w)[0]
        for tup in w:
            if tup[0] == min_v:
                min_c.append(tup)
            else:
                o_c.append(tup)
        if len(min_c) == 1:
            o_c += min_c
            min_c = []
        if len(o_c) == 1:
            text_ret += f"{o_c[0][1]} is a winner."
        elif len(o_c) == 2:
            text_ret += f"{o_c[0][1]} and {o_c[1][1]} are winners."
        elif len(o_c) > 1:
            for t in o_c:
                if t != o_c[-1]:
                    text_ret += f"{t[1]}, "
                else:
                    text_ret += f"and {t[1]} are winners."
        if len(min_c) == 2:
            text_ret += f"RUNOFF between {min_c[0][1]} and {min_c[1][1]}."
        else:
            text_ret += 'RUNOFF between '
            for t in min_c:
                if t != min_c[-1]:
                    text_ret += f"{t[1]}, "
                else:
                    text_ret += f"and {t[1]}."

    return text + text_ret

"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice, make_fair_dice
from ucb import main, trace, log_current_line, interact
import copy
GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times. Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    all_score = 0
    while num_rolls >= 1:
        num_rolls = num_rolls - 1
        one_score = dice()
        if one_score == 1 or all_score == 1:
            all_score = 1
        else:
            all_score = all_score + one_score
    return all_score



def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        turn_score = 1 + int(max(list((str(opponent_score))))) 
    else:
        turn_score = roll_dice(num_rolls, dice)
    return turn_score

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    total_score = score + opponent_score
    if total_score % 7 == 0:
        return four_sided
    else:
        return six_sided

def is_prime(n):
    """Return True if a non-negative number N is prime, otherwise return
    False. 1 is not a prime number!
    """
    assert type(n) == int, 'n must be an integer.'
    assert n >= 0, 'n must be non-negative.'
    k = 2
    if n == 1 or n == 0:
        return False
    judge_prime = True
    while k < n:
        if n % k == 0:
            judge_prime = False
        k = k + 1
    return judge_prime


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    while True:
        current_dice = select_dice(score0, score1)
        if who == 0:
            turn_score = take_turn(strategy0(score0, score1), score1, current_dice)
            score0 += turn_score
            opponent_score = score1
        if who == 1:
            turn_score = take_turn(strategy1(score1, score0), score0, current_dice)
            score1 += turn_score
            opponent_score = score0
        if is_prime(score0 + score1):
            if score0 > score1:
                score0 += turn_score
            if score1 > score0:
                score1 += turn_score
        who = other(who)
        if score0 >= goal or score1 >= goal:
            break
            
    return score0, score1  # You may want to change this line.

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def average_fn(*args):
        total = 0
        i = num_samples
        while i >= 1:
            total = total + fn(*args) # New syntax: *args
            i -= 1
        average = total/num_samples
        return average
    return average_fn

'''dice = make_test_dice(3, 1, 5, 6)
averaged_dice = make_averaged(dice, 1000)
print(averaged_dice())'''

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
    num_dice = 1
    max_average = 0
    max_num = 1
    while num_dice <= 10:
        test = make_averaged(roll_dice, 1000)(num_dice, dice)
        if test > max_average:
            #print(make_averaged(roll_dice, 1000)(num_dice, dice))
            #print(max_average)
            max_average = test
            max_num = num_dice
        num_dice += 1
    return max_num, max_average

#dice = make_test_dice(1,2)
#print(max_scoring_num_rolls(dice))

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test prime_strategy
        print('prime_strategy win rate:', average_win_rate(prime_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))


    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    if  1 + int(max(list(str(opponent_score)))) >= margin:
        rolls = 0
    else:
        rolls = num_rolls
    return rolls # Replace this statement

def prime_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial boost and
    rolls NUM_ROLLS if rolling 0 dice gives the opponent a boost. It also
    rolls 0 dice if that gives at least MARGIN points and rolls NUM_ROLLS
    otherwise.
    """
    "*** YOUR CODE HERE ***"
    #print(margin)
    if is_prime(score + opponent_score + 1+int(max(list(str(opponent_score))))):
        current_score = score + 1+int(max(list(str(opponent_score))))
        #print(current_score)
        if current_score > opponent_score:
            rolls = 0
        if opponent_score > current_score:
            rolls = num_rolls
            
    else:
        if 1+int(max(list(str(opponent_score)))) >= margin:
            rolls = 0
        else:
            rolls = num_rolls
        
    return rolls

#print(prime_strategy(23, 60, 6, 5))
def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    
    """
    "*** YOUR CODE HERE ***"
    def zero_roll(opponent_score):
        return 1+int(max(list(str(opponent_score))))
    zero_current_total_score = score + opponent_score + zero_roll(opponent_score)
    zero_current_score = score + zero_roll(opponent_score)
    
    '''Strategy: Try not to pig out the march'''
    if zero_current_score >= 100:
        return 0

    '''Strategy: Try to leave opponent more four-sided dice'''
    def judge_strategy(score, opponent_score, is_six_sided):
        low_risk_roll_num = 5 #roll number at lower risk
        high_risk_roll_num = 6 #roll number at higher risk
        max_average = 8 #the max expectation when roll (low_risk_roll_num) dices
        if not is_six_sided: 
            low_risk_roll_num = 4
            high_risk_roll_num = 5
            max_average = 4
            
        if opponent_score - score >= 15: # when you fall behind your opponent more than 15 score
            return high_risk_roll_num # take more risks
        else: 
            if (zero_roll(opponent_score) < max_average) & ((zero_current_total_score % 7) != 0):
                return low_risk_roll_num # when you cannot gain advantage by rolling 0 dice, choose low risk number
            else:
                if is_prime(zero_current_total_score) & (zero_current_score < opponent_score):
                    return low_risk_roll_num# when 0 dice give your opponent a boost, you can not roll 0 dice
                else:
                    return 0 # in other condition, roll 0 dice

    if (score + opponent_score) % 7 != 0:
        is_six_sided = 1
    if (score + opponent_score) % 7 == 0:
        is_six_sided = 0
    return judge_strategy(score, opponent_score, is_six_sided)
                        
        

   
        



##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

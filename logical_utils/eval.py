import math
import numpy as np

def calculate_log_odds(probability):
    return math.log(probability / (1 - probability))

def calculate_log_odds_r(probability_0, probability_1):
    return calculate_log_odds(probability_1) - calculate_log_odds(probability_0)

def total_effect(probability_o, probability_i):
    return (calculate_log_odds(probability_i) - calculate_log_odds(probability_o)) / calculate_log_odds(probability_o)

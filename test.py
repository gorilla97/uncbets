def american_moneyline_odds(percentage_likelihood):
    if percentage_likelihood < 1 or percentage_likelihood > 99:
        return "Invalid likelihood percentage"
    
    # Calculate the implied probabilities for Team A and Team B
    implied_prob_a = 100 / (100 - percentage_likelihood)
    implied_prob_b = percentage_likelihood / (-percentage_likelihood + 100)

    # Calculate American moneyline odds for Team A and Team B
    odds_a = round((implied_prob_a - 1) * 100)
    odds_b = round((implied_prob_b - 1) * 100)

    return odds_a, odds_b

# Print American moneyline odds for every percentage likelihood from 1% to 100%
for percentage in range(1, 101):
    odds_a, odds_b = american_moneyline_odds(percentage)
    print(f"Percentage Likelihood: {percentage}% - Team A: +{odds_a}, Team B: +{odds_b}")

american_moneyline_odds(70)
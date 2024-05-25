import numpy as np


class Roulette_Monte_Carlo:
    def __init__(self):
        self.wheel_numbers = [99, 999] + list(range(1, 37))
        self.player_numbers = list(range(1, 37))

    def simulate(self, num_of_simulations, betting_type):
        self.results = np.random.choice(self.wheel_numbers, num_of_simulations)

        betting_options = {
            1: (1, 35),
            2: (2, 17),
            3: (3, 11),
            4: (4, 8),
            5: (5, 6),
            6: (6, 5),
            7: (12, 2),
            8: (18, 1)
        }
        num_choices, self.profit = betting_options.get(betting_type, (1, 1))

        self.user_bets = np.array([np.random.choice(self.player_numbers, num_choices, replace=False) for _ in range(num_of_simulations)])



    def no_strategy_betting(self,num_of_simulations,bet_type):
        self.simulate(num_of_simulations, bet_type)
        results = np.array([np.isin(self.results[i],self.user_bets[i]) for i in range(num_of_simulations)])

        results = np.where(results, self.profit, -1)
        gaining_curve = np.cumsum(results)
        result = np.sum(results)
        max_dropdown=np.min(gaining_curve)
        percent_wins=sum(results)/len(results)

        return result, gaining_curve , max_dropdown,percent_wins


    def _base_martingale(self,num_of_simulations, bet_type, adjust_count_array):
        self.simulate(num_of_simulations, bet_type)
        results = np.array([np.isin(self.results[i],self.user_bets[i]) for i in range(num_of_simulations)])

        profit_indices = np.where(results)[0]

        stakes=np.ones_like(results, dtype=int)
        for i in range(1,len(profit_indices)):
            lenght=len(stakes[profit_indices[i-1]+1:profit_indices[i]+1])
            lenght=profit_indices[i]-profit_indices[i-1]

            if lenght>=1:
                stakes[profit_indices[i-1]+1:profit_indices[i]+1] = 2 ** np.linspace(0, lenght-1,lenght)

        if len(profit_indices):
            lenght=len(stakes[:profit_indices[0]+1])
            stakes[:profit_indices[0]+1] = 2 ** np.linspace(0, lenght-1, lenght)

            lenght_end=len(stakes[profit_indices[-1] + 1:])
            stakes[profit_indices[-1] + 1:] = 2 ** np.linspace(0, lenght_end-1, lenght_end)

        else:
            stakes=2 ** np.linspace(0, len(stakes)-1, len(stakes))



        non_profit_mask = np.ones(len(stakes), dtype=bool)
        non_profit_mask[profit_indices] = False

        stakes[non_profit_mask] *= -1

        gaining_curve = np.cumsum(stakes)

        result = np.sum(stakes)

        percent_wins = sum(results) / len(results)
        max_drawdown = np.min(gaining_curve)

        return result, gaining_curve, max_drawdown, percent_wins



    def martingale_system(self,num_of_simulations, bet_type):
        return self._base_martingale( num_of_simulations, bet_type, False)


    def DAlembert(self, num_of_simulations, bet_type):
        self.simulate(num_of_simulations, bet_type)
        results = np.array([np.isin(self.results[i],self.user_bets[i]) for i in range(num_of_simulations)])

        at_stake = [0 if i == 0 else (-1 if results[i - 1] else 1) for i in range(len(results))]
        at_stake = np.cumsum(at_stake)
        at_stake += 1

        at_stake = at_stake + np.abs(min(at_stake))+1 if min(at_stake) < 0 else at_stake


        profits = np.ones(shape=len(at_stake))

        profits[results] = at_stake[results] * self.profit


        profits[~results] = at_stake[~results] * -1


        result = np.sum(profits)
        gaining_curve = np.cumsum(profits)

        percent_wins = sum(results) / len(results)

        max_drawdown = np.min(gaining_curve)
        return result, gaining_curve, max_drawdown, percent_wins

    def fibonacci(self,n, memo={}):
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = self.fibonacci(n - 1, memo) + self.fibonacci(n - 2, memo)
        return memo[n]

    def get_fibonacci_values(self,indices):
        return np.array([self.fibonacci(index) for index in indices])

    def custom_cumsum(self,numbers):
        cumsum = 0
        result = []
        for number in numbers:
            cumsum += number
            if cumsum < 0:
                cumsum = 0
            result.append(cumsum)
        return result

    def Fibonacci_betting(self, num_of_simulations, bet_type):
        self.simulate(num_of_simulations, bet_type)
        results = np.array([np.isin(self.results[i],self.user_bets[i]) for i in range(num_of_simulations)])

        at_stake = [0 if i == 0 else (-2 if results[i - 1] else 1) for i in range(len(results))]
        fibo_position = self.custom_cumsum(at_stake)

        fibo_position=self.get_fibonacci_values(fibo_position)


        profits = np.ones(shape=len(at_stake))
        profits[results] = fibo_position[results] * self.profit
        profits[~results] = fibo_position[~results] * -1

        result = np.sum(profits)
        gaining_curve = np.cumsum(profits)

        percent_wins = sum(results) / len(results)

        max_drawdown = np.min(gaining_curve)
        return result, gaining_curve, max_drawdown, percent_wins





    def james_bond_strategy(self, num_of_simulations, bet_type):
        self.simulate(num_of_simulations, bet_type)
        bet_1=10
        multiplier_1=35
        results_bet_1 = np.array([self.results[i]==99 for i in range(num_of_simulations)])

        profits_1=np.ones(shape=num_of_simulations)
        profits_1[~results_bet_1]=profits_1[~results_bet_1] *-bet_1
        profits_1[results_bet_1]=profits_1[results_bet_1] *bet_1*multiplier_1


        bet_2=140
        multiplier_2=1
        user_bet_2=range(19,37)
        results_bet_2 = np.array([np.isin(self.results[i], user_bet_2) for i in range(num_of_simulations)])

        profits_2 = np.ones(shape=num_of_simulations)
        profits_2[~results_bet_2] = profits_2[~results_bet_2] * -bet_2
        profits_2[results_bet_2] = profits_2[results_bet_2] * bet_2 * multiplier_2


        bet_3=50
        multiplier_3=5
        user_bet_3 =range(13, 19)
        results_bet_3 = np.array([np.isin(self.results[i], user_bet_3) for i in range(num_of_simulations)])

        profits_3 = np.ones(shape=num_of_simulations)
        profits_3[~results_bet_3] = profits_3[~results_bet_3] * -bet_3
        profits_3[results_bet_3] = profits_3[results_bet_3] * bet_3 * multiplier_3

        profits=profits_3+profits_2+profits_1

        result = np.sum(profits)
        gaining_curve = np.cumsum(profits)


        max_drawdown = np.min(gaining_curve)
        return result, gaining_curve, max_drawdown, 0


    def paroli_strategy(self,num_of_simulations, bet_type):
        self.simulate(num_of_simulations, bet_type)
        results = np.array([np.isin(self.results[i],self.user_bets[i]) for i in range(num_of_simulations)])
        profits = np.array([
            3 if i >= 3 and results[i - 1] and results[i - 2] and not results[i - 3] else
            2 if i >= 2 and results[i - 1] and not results[i - 2] else
            1 if i >= 3 and results[i - 2] and results[i - 1] and results[i - 3] else
            1
            for i in range(num_of_simulations)
        ])

        profits[results] = profits[results] * self.profit
        profits[~results] = profits[~results] * -1
        result = np.sum(profits)
        gaining_curve = np.cumsum(profits)
        percent_wins = sum(results) / len(results)

        max_drawdown = np.min(gaining_curve)
        return result, gaining_curve, max_drawdown, percent_wins

    def simulate_games(self, method, scenario_numbers, betting_type, sequence_length):

        results = np.empty(scenario_numbers)
        curves = np.empty((scenario_numbers,
                           sequence_length))
        max_drawdowns = np.empty(scenario_numbers)
        percent_wins = np.empty(scenario_numbers)


        method_to_call = getattr(self, method, None)
        if method_to_call:
            for i in range(scenario_numbers):

                results[i], curves[i], max_drawdowns[i], percent_wins[i] = method_to_call(sequence_length, betting_type)
            statistics = [np.round(np.min(max_drawdowns), 2), np.round(np.mean(max_drawdowns), 2),
                          np.round(np.max(results), 2), np.round(np.mean(results), 2)]

            return curves,statistics
        else:
            return None,[]
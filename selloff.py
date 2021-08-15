from enum import Enum
# Strategies to sell the tokens
# Strategy terminates when 95% coins are done
class SellStrategy(Enum):
    SELL_THE_TOP = 1       # one sale of the blow off top
    SELL_LINEAR = 2        # chop off by x% (<100%) at @predefined prices linearly to the top
    SELL_EXPONENT = 3      # sell x% (<100%) on each exponential rise until top price

# Class SellOff evaluates the profit total return based on the input strategy.
# It returns the total amount of profit in $$ terms
# More complex strategies like the SELL_LINEAR or SELL_EXPONENT need a stop condition
#   which is enabled by providing a threshold, normally a 95% of all held tokens
#   Can return the remaining tokens value after sell-off is complete, call ->sale_remainder
class SellOff:

    # @sell_strategy - defined by the SellStrategy enum
    # @current - current token price
    # @top - maximum token price prediction
    # @tokens - how many tokens are on sale
    # @rate - sell rate, % by which we sell each round
    # @threshold (opt) - on what percentage of tokens to stop selling
    def __init__(self, sell_strategy, current, top, tokens, rate, sell_exp, threshold):
        self.sell_strategy = sell_strategy
        self.my_price = current
        self.top_price = top
        self.tok_remainder = 0.0
        self.tokens = tokens
        self.rem_tokens = 0
        self.thr = 0
        self.sell_rate = rate       # evaluated both in SELL_LINEAR and SELL_EXPONENT strategies
        self.sell_exp = sell_exp    # evaluated in SELL_EXPONENT strategy
        self.selloffs = 0           # evaluated in SELL_LINEAR strategy
        self.set_sell_thr(threshold)

    # General get/set
    def get_sell_thr(self):
        return self.thr

    def set_sell_thr(self, threshold):
        # Sanitize the optionally provided stop threshold
        if (threshold is None) or (threshold <= 0.0) or (threshold > 1.0):
            self.thr = 0.95     # in %/100
        else:
            self.thr = threshold
        return self.thr

    # Strategy : SELL_THE_TOP
    def sell_top(self):
        v = (self.top_price - self.my_price) * self.tokens * self.thr
        self.tok_remainder = self.tokens * (1.0 - self.thr)
        return v

    # Strategy : SELL_20_PERCENT
    def set_selloffs(self, number_of):
        if (number_of > 1) and (number_of < 21):
            self.selloffs = number_of

    def sell_linear(self):
        sell_rate = self.sell_rate
        if 0 == self.selloffs:
            #print("Sell-Off strategy incomplete, input number of sell-offs (between 2 and 20)")
            return -1
        # generate an array of selloff prices and the number of selloffs
        # possible for the price
        p_top = self.top_price
        p_cur = self.my_price
        p_diff = (p_top - p_cur) / self.selloffs

        # proceed with evaluating sell-offs, first determine sell-off prices
        # for that here we use a linear model implicitly
        tokens = self.tokens
        gain = 0.0
        p = p_cur
        i = 1
        for i in range(self.selloffs):
            gain += (p + p_diff) * sell_rate * tokens
            print("Sale # ", i, " gain = ", gain, " $")
            tokens = (1.0 - sell_rate) * tokens
            print("Tokens left = ", tokens)
            p += p_diff

        self.tok_remainder = tokens
        return gain

    def sell_exponent(self):
        return 0.0

    def get_rem_tokens(self):
        return self.tok_remainder

    # Main sell function
    def sell(self):
        if self.sell_strategy == SellStrategy.SELL_THE_TOP:
            return self.sell_top()
        elif self.sell_strategy == SellStrategy.SELL_LINEAR:
            return self.sell_linear()
        else:
            return self.sell_exponent()

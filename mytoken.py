class Token:
    # @name - token name
    # @api_price - CoinGecko API price
    # @numsel - number of selloff targets
    #           normally passed then as increasing price + percent of stack array
    # @hodl - number of token in the bag
    # @apy - percent earn over 1 year and until sale is complete, 0% = no compounding
    # @ath - last known all-time-high for the token
    # @currency, default=usd
    def __init__(self, price, name, hodl, apy, ath, top, currency):
        self.api_price = price
        self.name = name
        self.hodl_value = price * hodl
        self.apy = apy
        self.ath = ath * hodl
        self.top = top * hodl
        self.apy_per = 1.0 + apy / 100.0
        self.currency = currency
        self.days = 0

    # @days - number of days before selloff
    def apy_gain(self, days):
        self.days = days
        if days > 0:
            return ((self.apy_per * days / 365.0) * self.hodl_value) - self.hodl_value
        else:
            return 0

    # value of holding in currency (default = usd)
    def asset_now(self):
        return self.hodl_value

    def asset_ath(self):
        return self.ath

    def asset_top(self):
        return self.top

    def asset(self, days):
        return self.hodl_value + self.apy_gain(days)


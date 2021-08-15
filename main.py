from mytoken import Token
from pycoingecko import CoinGeckoAPI
from selloff import SellStrategy
from selloff import SellOff

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cg = CoinGeckoAPI()
    if str(cg.ping()).find('Moon') != -1:
        print("API works!")
    else:
        print("API is down!")

    # currency convesion rate (USD to NZD)
    usd_2_nzd = 1.43
    # tax factor for large tax
    tax_factor = 0.7
    # tax factor for ongoing profits
    tax_factor_ongoing = 0.75
    # gross yield on dollars stablecoins
    stc_apy_gross = 10

    # mytokens is a table of ownership structured in the following way
    # TODO: migrate to SQL
    # name / owned_tokens / %apy (0 for none) /
    strategy = SellStrategy.SELL_THE_TOP
    # ############################################################################################################
    # ##### token             hodl             apy          top              strategy               all-time-hi
    # ############################################################################################################
    mytokens = {
        0: {"name": "btc", "id": "bitcoin",        "hold": 0.6418,  "apy": 4.3,  "top": 250000,
            "strategy": strategy,  "ath": 64400},
        1: {"name": "eth", "id": "ethereum",       "hold": 12.00,   "apy": 4.3,  "top": 18000,
            "strategy": strategy,  "ath": 4400},
        2: {"name": "ada", "id": "cardano",        "hold": 38158,   "apy": 5.5,  "top": 13.0,
            "strategy": strategy,  "ath": 2.52},
        3: {"name": "matic", "id": "matic-network",  "hold": 11075,   "apy": 0.0,  "top": 10,
            "strategy": strategy,  "ath": 2.25},
        4: {"name": "link", "id": "chainlink",      "hold": 505.1,   "apy": 6.0,  "top": 200,
            "strategy": strategy,  "ath": 49.95},
        5: {"name": "dot", "id": "polkadot",       "hold": 618.22,  "apy": 13.5, "top": 170,
            "strategy": strategy,  "ath": 50},
        6: {"name": "egld", "id": "elrond-erd-2",   "hold": 90.62,   "apy": 17.0, "top": 900,
            "strategy": strategy,  "ath": 221},
        7: {"name": "vet", "id": "vechain",        "hold": 70709,   "apy": 0.0,  "top": 2,
            "strategy": strategy,  "ath": 0.285},
        8: {"name": "vtho", "id": "vethor-token",   "hold": 15500,   "apy": 1.3,  "top": 0.2,
            "strategy": strategy,  "ath": 0.02},
        9: {"name": "inj", "id": "injective-protocol", "hold": 684.7, "apy": 0.0,  "top": 200,
            "strategy": strategy,  "ath": 25.5},
        10: {"name": "occ", "id": "occamfi",       "hold": 504.88,  "apy": 4.0,  "top": 35,
             "strategy": strategy,  "ath": 17.6},
        11: {"name": "tvk", "id": "terra-virtua-kolect", "hold": 14674, "apy": 0.0, "top": 15,
             "strategy": strategy,  "ath": 1.24},
        12: {"name": "ilv", "id": "illuvium",      "hold": 12.2,    "apy": 100,  "top": 3000,
             "strategy": strategy,  "ath": 330},
        13: {"name": "mana", "id": "decentraland",  "hold": 2896.4,  "apy": 0.0,  "top": 12,
             "strategy": strategy,  "ath": 1.67},
        14: {"name": "ramp", "id": "ramp",          "hold": 9400.8,  "apy": 20,   "top": 10,
             "strategy": strategy,  "ath": 0.92},
        15: {"name": "nim", "id": "nimiq-2",       "hold": 387710,  "apy": 0.0,  "top": 0.05,
             "strategy": strategy,  "ath": 0.014},
        16: {"name": "rsr", "id": "rsr",           "hold": 50945,   "apy": 0.0,  "top": 1,
             "strategy": strategy,  "ath": 0.945},
        17: {"name": "kyl", "id": "kylin-network", "hold": 7530,    "apy": 0.0,  "top": 15,
             "strategy": strategy,  "ath": 2.18},
        18: {"name": "apy", "id": "apy-finance",   "hold": 3654,    "apy": 0.0,  "top": 21,
             "strategy": strategy,  "ath": 6.23},
        19: {"name": "ren", "id": "republic-protocol", "hold": 3425, "apy": 0.0, "top": 6.5,
             "strategy": strategy,  "ath": 1.72},
        20: {"name": "srm", "id": "serum",         "hold": 355.1,   "apy": 0.0,  "top": 67,
             "strategy": strategy,  "ath": 12.3},
        21: {"name": "lina", "id": "linear",        "hold": 46000,   "apy": 67.0, "top": 0.8,
             "strategy": strategy,  "ath": 0.24},
        22: {"name": "epns", "id": "ethereum-push-notification-service", "hold": 825, "apy": 38.6, "top": 14.0,
             "strategy": strategy, "ath": 8.0},
        23: {"name": "atom", "id": "cosmos",        "hold": 62.4,    "apy": 0.0,  "top": 150.0,
             "strategy": strategy, "ath": 28.78},
        24: {"name": "bscs", "id": "bsc-station",   "hold": 5100,    "apy": 17,   "top": 5.0,
             "strategy": strategy, "ath": 1.22},
        25: {"name": "xed", "id": "exeedme",       "hold": 1358,    "apy": 0.0,  "top": 6.0,
             "strategy": strategy, "ath": 1.95},
        26: {"name": "bmi", "id": "bridge-mutual", "hold": 1263,    "apy": 17.8, "top": 20.0,
             "strategy": strategy, "ath": 4.82},
        27: {"name": "nexo", "id": "nexo", "hold": 2233, "apy": 7.5, "top": 20.0,
             "strategy": strategy, "ath": 4.5},
    }

    tok = []
    tok_idx = 0

    my_currency = 'usd'
    number_of_selloffs = 3
    selloff1_days = 30
    mytoken_names = []

    for h in range(len(mytokens)):
        mytoken_names.append(mytokens[h]["id"])

    token_data = cg.get_price(ids=mytoken_names, vs_currencies=my_currency)
    token_ath = cg.get_token_price

    so1 = SellOff(SellStrategy.SELL_LINEAR, 0, 100, 1000, 0.2, 2.0, 1.0)
    so1.set_selloffs(10)
    print("Returned ", so1.sell(), "$ remainder ", so1.get_rem_tokens())

    for tk in token_data:
        token_price = token_data[tk][my_currency]
        # Find the index of the returned token by its str within dict ID property
        tkidx = next(item for item in mytokens if mytokens[item]["id"] == tk)
        # Create object for price evaluation
        tok.append(Token(token_price, tk, mytokens[tkidx]["hold"],
                         mytokens[tkidx]["apy"], mytokens[tkidx]["ath"],
                         mytokens[tkidx]["top"], 'usd'))
        # Get some idea of results
        print(mytokens[tkidx]["name"], "\t:", "{:10.4f}".format(token_price),
              "\tCurrent$:", "{:10.2f}".format(tok[tok_idx].asset_now()),
              "\tin 1yr$:", "{:10.2f}".format(tok[tok_idx].asset(365)),
              "\tATH:", "{:10.2f}".format(tok[tok_idx].asset_ath()),
              "\tTop:", "{:10.2f}".format(tok[tok_idx].asset_top()))
        tok_idx += 1

    print("===========================================================================================================")
    portfolio_now = 0
    portfolio_1yr = 0
    portfolio_ath = 0
    portfolio_top = 0
    # Calculate overall portfolio
    for j in range(len(tok)):
        portfolio_now += tok[j].asset_now()
        portfolio_1yr += tok[j].asset(365)
        portfolio_ath += tok[j].asset_ath()
        portfolio_top += tok[j].asset_top()

    portfolio_now_nzd = portfolio_now * usd_2_nzd
    portfolio_ath_nzd = portfolio_ath * usd_2_nzd
    portfolio_top_nzd = portfolio_top * usd_2_nzd
    dk = 1000.0
    print("Portfolio now: ", "{:10.2f}".format(portfolio_now / dk), "k US$")
    print("               ", "{:10.2f}".format(portfolio_now_nzd / dk), "k NZ$")
    print("Portfolio 1yr: ", "{:10.2f}".format(portfolio_1yr / dk), "k US$")
    print("Portfolio ATH: ", "{:10.2f}".format(portfolio_ath / dk), "k US$")
    print("               ", "{:10.2f}".format(portfolio_ath_nzd / dk), "k NZ$")
    print("Portfolio Top: ", "{:10.2f}".format(portfolio_top / dk), "k US$")
    print("               ", "{:10.2f}".format(portfolio_top_nzd / dk), "k NZ$")
    earn_dollars = portfolio_top_nzd * tax_factor
    print("Top after Tax: ", "{:10.2f}".format(portfolio_top_nzd * tax_factor / dk), "k NZ$")
    # How much do I earn per months
    stc_apy_net = stc_apy_gross * tax_factor_ongoing
    earn_year = earn_dollars * (stc_apy_net / 100.0)
    earn_month = earn_year / 12
    print("===========================================================================================================")
    print("Gross % yield:", "{:2.1f}".format(stc_apy_gross), "%")
    print("Net   % yield:", "{:2.1f}".format(stc_apy_net), "%")
    print("Earn per year:", "{:6.2f}".format(earn_year/dk), "k NZ$")
    print("Earn per month:", "{:6.2f}".format(earn_month), " NZ$")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from lookup import price_lookup

GAME = "Las Navas de Tolosa, 1212"

print("Price Lookup Game: "+GAME)
print("Price Lookup: "+str(price_lookup.game_title(GAME)))


def test_price_lookup_game_title():
    """Look up if the price is an integer"""
    assert isinstance(price_lookup.game_title(GAME),int)

"""Test to see if GameInfo script works as intended"""
from main import GameInfo

#game = GameInfo("288841")
game = GameInfo("116954")
#game = GameInfo("313476")

print("Validating game: ",game.title())
print("Categories: ",game.category())
print("Mechanics: ",game.mechanic())
print("Expansion: ",game.expansion())
print("Year Published: ",game.year_published())
print("Min Players: ",game.minplayers())
print("Max Players: ",game.maxplayers())
print("Playtime: ",game.playtime())
print("Age: ",game.age())


def test_valid():
    """Test to see if a game is stated as valid"""
    assert game.is_valid()

def test_titles():
    """Test to see if a title could be set properly"""
    assert len(game.title()) > 0
    assert isinstance(game.title(), str)

def test_categories():
    """Test to see if a category could be set properly"""
    assert len(game.category()) > 0
    assert isinstance(game.category(), str)

def test_mechanics():
    """Test to see if a mechanic could be set properly"""
    assert len(game.mechanic()) > 0
    assert isinstance(game.mechanic(), str)

def test_bgg_rating():
    """Test to see if a rating could be set properly"""
    assert len(str(game.bgg_rating())) > 0
    assert isinstance(game.bgg_rating(), int)

def test_expansion():
    """Test to see if a expansion could be set properly"""
    assert isinstance(game.expansion(), int)

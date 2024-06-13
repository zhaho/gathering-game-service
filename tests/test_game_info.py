"""Test to see if GameInfo script works as intended"""
import pytest
from main import GameInfo

@pytest.fixture(params=["150376", "116954", "313476"])
def game(request):
    game_id = request.param
    game = GameInfo(game_id)
    print("Validating game: ", game.title())
    print("Categories: ", game.category())
    print("Mechanics: ", game.mechanic())
    print("Expansion: ", game.expansion())
    print("Year Published: ", game.year_published())
    print("Min Players: ", game.minplayers())
    print("Max Players: ", game.maxplayers())
    print("Playtime: ", game.playtime())
    print("Age: ", game.age())
    return game, game_id
    
def test_valid(game):
    """Test to see if a game is stated as valid"""
    game, game_id = game
    assert game.is_valid(), f"Game {game_id} failed validation"

def test_titles(game):
    """Test to see if a title could be set properly"""
    game, game_id = game
    assert len(game.title()) > 0, f"Game {game_id} has an invalid title"
    assert isinstance(game.title(), str), f"Game {game_id} title is not a string"

def test_categories(game):
    """Test to see if a category could be set properly"""
    game, game_id = game
    assert len(game.category()) > 0, f"Game {game_id} has an invalid category"
    assert isinstance(game.category(), str), f"Game {game_id} category is not a string"

def test_mechanics(game):
    """Test to see if a mechanic could be set properly"""
    game, game_id = game
    assert len(game.mechanic()) > 0, f"Game {game_id} has an invalid mechanic"
    assert isinstance(game.mechanic(), str), f"Game {game_id} mechanic is not a string"

def test_bgg_rating(game):
    """Test to see if a rating could be set properly"""
    game, game_id = game
    assert len(str(game.bgg_rating())) > 0, f"Game {game_id} has an invalid BGG rating"
    assert isinstance(game.bgg_rating(), int), f"Game {game_id} BGG rating is not an integer"

def test_expansion(game):
    """Test to see if an expansion could be set properly"""
    game, game_id = game
    assert isinstance(game.expansion(), int), f"Game {game_id} expansion is not an integer"

for game_id in game_ids:
    # Run tests for the current game
    test_valid(game, game_id)
    test_titles(game, game_id)
    test_categories(game, game_id)
    test_mechanics(game, game_id)
    test_bgg_rating(game, game_id)
    test_expansion(game, game_id)

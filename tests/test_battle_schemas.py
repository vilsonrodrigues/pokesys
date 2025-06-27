import pytest
from pydantic import ValidationError
from pokesys.server.schemas.battle import BattleResponse


def test_battle_response_valid():
    response = BattleResponse(reasoning="Pikachu was faster and had type advantage.", winner="Pikachu")
    assert response.reasoning == "Pikachu was faster and had type advantage."
    assert response.winner == "Pikachu"


def test_battle_response_missing_fields():
    with pytest.raises(ValidationError) as exc_info:
        BattleResponse(winner="Pikachu")
    assert "reasoning" in str(exc_info.value)

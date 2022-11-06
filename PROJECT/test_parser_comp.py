import find_comp
import pytest


@pytest.mark.parametrize('drug_1, drug_2, expected_result', [('аспирин', 'анальгин', 'Тяжелые'),
                                                             ('аспирин', 'брал', 'Тяжелые'),
                                                             ('аспирин', 'декарис', ''),
                                                             ('нурофен', 'валсафорс', 'Умеренно выраженные')])
def test_interactions_with_correct_med(drug_1, drug_2, expected_result):
    assert find_comp.find_interaction(drug_1, drug_2) == expected_result

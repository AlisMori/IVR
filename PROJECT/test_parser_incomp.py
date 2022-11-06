import find_incomp
import pytest

@pytest.mark.parametrize('drug_1, drug_2, expected_result', [('djtfk', 'ddyi', ''),
                                                             ('сплр', 'лсл', '')])
def test_interactions_with_incorrect_med(drug_1, drug_2, expected_result):
    assert find_comp.find_interaction(drug_1, drug_2) == expected_result


def test_incomp_with_correct_med():
    assert find_incomp.list_incomp('аспирин') != ''
    assert find_incomp.list_incomp('скинорен') == ''
import find_info
import pytest


def test_url_with_correct_med():
    assert find_info.find_url('аспирин') == 'https://www.rlsnet.ru/drugs/aspirin-346'
    assert find_info.find_url('аспирин 1000') == 'https://www.rlsnet.ru/drugs/aspirin-1000-26569'
    assert find_info.find_url('аспирин кардио') == 'https://www.rlsnet.ru/drugs/aspirin-kardio-7424'
    assert find_info.find_url('амоксиклав') == 'https://www.rlsnet.ru/drugs/amoksiklav-200'


def test_url_with_incorrect_med():
    assert find_info.find_url('аспириннн') == ''
    assert find_info.find_url('fgjfkf') == ''


@pytest.mark.parametrize('name, expected_result', [('аспириннн', None),
                                                   ('fgjfkf', None),
                                                   ('апвраш', None)])
def test_info_indi_contraindi_with_incorrect_med(name, expected_result):
    assert find_info.info(name) is expected_result
    assert find_info.indication(name) is expected_result
    assert find_info.contraindication(name) is expected_result


def test_info_with_correct_med():
    assert find_info.info('аспирин') == 'Информация не найдена'
    assert find_info.info('анальгин') == ' Прозрачный слегка желтоватый раствор. '


def test_indi_and_contraindi_with_correct_med():
    assert find_info.indication('аспирин') == ' болевой синдром различной локализации (суставные, мышечные, ' \
                                              'головная, менструальные, зубная боли); лихорадочные состояния. '
    assert find_info.contraindication('аспирин') == ' Абсолютные: состояния, сопровождающиеся повышенной склонностью' \
                                                    ' к кровотечению; отмеченная ранее повышенная чувствительность ' \
                                                    'к салицилатам и другим НПВС. Относительные: Аспирин 100 мг ' \
                                                    'следует принимать только после консультации врача при следующих ' \
                                                    'состояниях и заболеваниях: одновременная терапия ' \
                                                    'антикоагулянтами (производные кумарина, гепарин); ' \
                                                    'недостаточность глюкозо-6-фосфатдегидрогеназы; ' \
                                                    'бронхиальная астма; ' \
                                                    'хронические заболевания желудка и двенадцатиперстной кишки; ' \
                                                    'нарушение функции почек; подагра; сахарный диабет; ' \
                                                    'беременность; лактация; детский возраст до 12 лет. '

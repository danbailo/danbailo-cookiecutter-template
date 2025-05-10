from collections.abc import Hashable
from copy import deepcopy
from typing import TypeVar

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger import LoggerFactory

KT = TypeVar('KT')
VT = TypeVar('VT')


def update_data_from_objects(data1: dict, data2: dict | list) -> dict:
    """Recebe dois objetos, onde o primeiro obrigatoriamente é um `dict` e o segundo
    podendo ser um `dict` ou um `list`, e retorna um novo `dict` considerando os dados
    do `dict2` mais a esquerda e `dict1` mais a direita.
    """
    logger = LoggerFactory.new()
    to_return = {}
    if isinstance(data2, dict):
        to_return |= data2 | data1
    elif isinstance(data2, list):
        for current_object in data2:
            if not isinstance(current_object, dict):
                continue
            logger.debug(
                'Atualizando objeto de retorno...',
                to_return=to_return,
                current_object=current_object,
            )
            to_return.update(current_object)
        to_return.update(data1)
    logger.debug('Criado novo objeto!', to_return=to_return)
    return to_return


def invert_dict(d: dict[KT, VT]) -> dict[VT, KT]:
    """ "
    Cria um novo dicionário com as chaves e valores invertidos.

    Note que os valores devem ser únicos, pois serão as novas chaves.
    """
    if not d:
        return {}
    return {v: k for k, v in d.items()}


def force_all_keys_exist(data: dict, *keys: Hashable) -> dict:
    """
    Força com que todas as chaves do parâmetro `keys` existam no dicionário `data`.
    Quando a lista de chaves não for um subconjunto das chaves do dicionário, então,
    essas chaves são removidas do dicionário.
    """
    if all(data.get(key) is not None for key in keys):
        return data

    new_dict = deepcopy(data)
    for key in keys:
        new_dict.pop(key, None)
    return new_dict


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Junta dois dicionários, dando preferência para chaves com valores não vazios.
    Dá preferência para o valor mais a direita(dict2) caso ambos sejam vazios.
    """
    merged = {}
    all_keys = set(dict1.keys()).union(dict2.keys())

    for key in all_keys:
        value1 = dict1.get(key)
        value2 = dict2.get(key)
        merged[key] = value1 or value2
    return merged

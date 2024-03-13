import os
import sys

# Добавление пути текущей папки в список путей поиска модулей для импорта
sys.path.append(os.path.dirname(__file__))
# Добавление пути в корень проекта в список путей поиска модулей для импорта
sys.path.append(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0])

from dlms_cosem.cosem.attribute_with_selection import CosemAttributeWithSelection
from dlms_cosem.cosem.base import CosemAttribute, CosemMethod
from dlms_cosem.cosem.obis import Obis

__all__ = ["CosemAttribute", "CosemMethod", "Obis", "CosemAttributeWithSelection"]

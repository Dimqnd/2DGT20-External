import random
from enum import Enum
import json
import os

class AGE_CATEGORIES(Enum):
    CADET_MEN = 0
    CADET_WOMEN = 1
    JUNIOR_MEN = 2
    JUNIOR_WOMEN = 3
    SENIOR_MEN = 4
    SENIOR_WOMEN = 5

class WEIGHT_CATEGORIES(Enum):
    pass

def identify_age_classifications(isMale: bool, age: int) -> list[AGE_CATEGORIES]:
    returnClassifications = []

    womenAgeClassifications = {
        18: AGE_CATEGORIES.CADET_WOMEN,
        21: AGE_CATEGORIES.JUNIOR_WOMEN,
        100: AGE_CATEGORIES.SENIOR_WOMEN
    }

    menAgeClassifications = {
        18: AGE_CATEGORIES.CADET_MEN,
        21: AGE_CATEGORIES.JUNIOR_MEN,
        100: AGE_CATEGORIES.SENIOR_MEN
    }
    
    genderedClassification: dict[int, AGE_CATEGORIES] = womenAgeClassifications if isMale == False else menAgeClassifications
    
    if age < 15:
        raise ValueError('Judoka need to be at least 15 to compete in IJF registered competitions')
    
    for classAge, category in genderedClassification.items():
        if age < classAge:
            returnClassifications.append(category)

    return returnClassifications

def idenfity_weight_classification(ageClass: AGE_CATEGORIES, weight: int):    
    workingDir = os.getcwd()
    filePath = '\cadets_weights.json' if ageClass == AGE_CATEGORIES.CADET_MEN or ageClass == AGE_CATEGORIES.CADET_WOMEN else '\junior_senior_weights.json'
    jsonLocation = workingDir + filePath

    isMale = True if ageClass == AGE_CATEGORIES.SENIOR_MEN or ageClass == AGE_CATEGORIES.CADET_MEN or ageClass == AGE_CATEGORIES.JUNIOR_MEN else False

    with open(jsonLocation, 'r') as f:
        data = json.load(f)

        if isMale == True:
            weightData = data['men']
        else:
            weightData = data['women']

        if weight > weightData[-1]:
            return f'over {weightData[-1]}'
        
        for weightClass in weightData:
            if weight <= weightClass:
                return f'under {weightClass}'
    
    return None

class Judoka:
    def __init__(self, name: str, age: int, weight: float, isMale: bool, isOpens: bool) -> None:
        self._name = name
        self._age = age
        self._weight = weight
        self._isOpens = isOpens # this is important bc people opt in to opens, so it can be a weight added to their category if they wish
        # therefore it is not included in the original 

        self._ageClassifications: list[AGE_CATEGORIES] = identify_age_classifications(isMale, age)
        self._weightCategories: dict[AGE_CATEGORIES, str] = {x: idenfity_weight_classification(x) for x in self._ageClassifications}

        if isOpens:
            if AGE_CATEGORIES.JUNIOR_MEN in self._ageClassifications or AGE_CATEGORIES.JUNIOR_WOMEN in self._ageClassifications \
                or AGE_CATEGORIES.SENIOR_MEN in self._ageClassifications or AGE_CATEGORIES.SENIOR_WOMEN in self._ageClassifications:
                self._ageClassifications.append('Opens')

judoka1 = Judoka('Jane Doe', 24, 66, False, False)
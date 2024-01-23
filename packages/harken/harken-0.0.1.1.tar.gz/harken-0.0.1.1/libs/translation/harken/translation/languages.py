from langcodes import Language, tag_is_valid, standardize_tag
from polyglot.detect import Detector

from lingua import Language, LanguageDetectorBuilder

detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

ISO_639_1 = '639-1'
ISO_639_2 = '639-2'

import warnings
from iso639 import Lang

warnings.filterwarnings("ignore")

def language_detector_polyglot(text, iso=ISO_639_1):
    result = Detector(text + " " + text + " " + text)
    results = []
    for language in result.languages:
        lang = get_language_code(language.code) if iso == ISO_639_1 \
            else get_language_code3(language.code) if iso == ISO_639_2 \
            else language.code
        results.append(
            {'lang': lang, 'score': language.confidence / 100})
    return results


def language_detector_lingua(text, iso=ISO_639_1):
    confidence_values = detector.compute_language_confidence_values(text + " " + text + " " + text)
    results = []
    for lang, score in confidence_values:
        lang = get_language_code(lang) if iso == ISO_639_1 \
            else get_language_code3(lang) if iso == ISO_639_2 \
            else lang
        results.append({'lang': lang, 'score': score})
    return results

def detect_language_full(text, detector="polyglot"):
    try:
        if detector == "polyglot":
            results = language_detector_polyglot(text=text)
        elif detector == "lingua":
            results = language_detector_lingua(text=text)
        elif detector == "fasttext":
            results = language_detector_fasttext(text=text)
        return {'lang': results[0]["lang"], 'score': results[0]["score"]}
    except:
        return {'lang': 'unk', 'score': 0}


def detect_possible_languages(text, iso=ISO_639_1, k=3, detector="polyglot"):
    try:
        if detector == "polyglot":
            results = language_detector_polyglot(text=text, iso=iso)
        elif detector == "lingua":
            results = language_detector_lingua(text=text, iso=iso)
        elif detector == "fasttext":
            results = language_detector_fasttext(text=text, iso=iso)
        return results[0:k]
    except:
        return [{'lang': 'unk', 'score': 0}]


def detect_language(text, iso=ISO_639_1, detector="polyglot"):
    if iso == ISO_639_1:
        return get_language_code(detect_language_full(text, detector=detector)['lang'])
    else:
        return get_language_code3(detect_language_full(text, detector=detector)['lang'])


def detect_language_with_score(text, iso=ISO_639_1, detector="polyglot"):
    result = detect_language_full(text, detector=detector)
    if iso == ISO_639_1:
        return {"lang": get_language_code(result['lang']), "score": result['score']}
    else:
        return {"lang": get_language_code3(result['lang']), "score": result['score']}


def is_a_valid_language(language):
    return tag_is_valid(language)


def get_language_info(language):
    try:
        obj = Lang(language)
        return {'name': obj.name, 'code': obj.pt1, 'display': obj.name, 'code3': obj.pt3}
    except:
        pass
    try:
        obj = Language.get(language)
        return {'name': obj.language_name(), 'code': standardize_tag(obj.to_alpha3()), 'display': obj.display_name(),
                'code3': obj.to_alpha3()}
    except:
        return {'name': 'Unknown', 'code': 'unk', 'display': 'Unknown', 'code3': 'unk'}


def get_language_code(language):
    return get_language_info(language)['code']


def get_language_code3(language):
    return get_language_info(language)['code3']


# FastText Wrapper
import logging
import os
from typing import Dict, Union

import fasttext
import requests

models = {"low_mem": None, "high_mem": None}
FTLANG_CACHE = os.getenv("FTLANG_CACHE", "/tmp/fasttext-langdetect")


def download_model(name: str) -> str:
    target_path = os.path.join(FTLANG_CACHE, name)
    if not os.path.exists(target_path):
        print(f"Downloading {name} model ...")
        url = f"https://dl.fbaipublicfiles.com/fasttext/supervised-models/{name}"  # noqa
        os.makedirs(FTLANG_CACHE, exist_ok=True)
        with open(target_path, "wb") as fp:
            response = requests.get(url)
            fp.write(response.content)
        print(f"Downloaded.")
    return target_path


def get_or_load_model(low_memory=False):
    if low_memory:
        model = models.get("low_mem", None)
        if not model:
            model_path = download_model("lid.176.ftz")
            model = fasttext.load_model(model_path)
            models["low_mem"] = model
        return model
    else:
        model = models.get("high_mem", None)
        if not model:
            model_path = download_model("lid.176.bin")
            model = fasttext.load_model(model_path)
            models["high_mem"] = model
        return model


def detect(text: str, low_memory=False) -> Dict[str, Union[str, float]]:
    model = get_or_load_model(low_memory)
    labels, scores = model.predict(text)
    label = labels[0].replace("__label__", '')
    score = min(float(scores[0]), 1.0)
    return {
        "lang": label,
        "score": score,
    }


def detect_k_languages(text: str, k=3, low_memory=False):
    results = []
    model = get_or_load_model(low_memory)
    labels, scores = model.predict(text, k)
    for i, label in enumerate(labels):
        label = label.replace("__label__", '')
        score = min(float(scores[i]), 1.0)
        results.append({"lang": label, "score": score})
    return results


if __name__ == '__main__':
    print(detect_language_full("my name is "))

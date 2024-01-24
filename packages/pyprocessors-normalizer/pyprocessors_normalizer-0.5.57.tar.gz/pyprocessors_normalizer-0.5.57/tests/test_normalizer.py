import ast
import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_normalizer.normalizers import (
    NormalizeDate,
    CleanDate,
    CleanAmount,
    NormalizeAmount,
    CleanDuration,
    NormalizeDuration,
)
from pyprocessors_normalizer.normalizer import (
    NormalizerProcessor,
    NormalizerParameters,
    compose_functions,
)


def test_durees():
    duree_fun = compose_functions(
        [
            CleanDuration,
            NormalizeDuration,
        ]
    )
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/durees.txt",
    )
    ref = Path(
        testdir,
        "data/durees_norm.txt",
    )
    with source.open("r") as fin:
        with ref.open("r") as fref:
            for lin, lref in zip(fin, fref):
                durees = ast.literal_eval(lin)
                normalized = [duree_fun(date) for date in durees]
                durees_ref = ast.literal_eval(lref)
                assert normalized == durees_ref


def test_dates():
    date_fun = compose_functions(
        [
            CleanDate,
            NormalizeDate,
        ]
    )
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/dates.txt",
    )
    ref = Path(
        testdir,
        "data/dates_norm.txt",
    )
    with source.open("r") as fin:
        with ref.open("r") as fref:
            for lin, lref in zip(fin, fref):
                dates = ast.literal_eval(lin)
                normalized = [date_fun(date) for date in dates]
                dates_ref = ast.literal_eval(lref)
                assert normalized == dates_ref


def test_montants():
    montant_fun = compose_functions(
        [
            CleanAmount,
            NormalizeAmount,
        ]
    )
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/montants.txt",
    )
    ref = Path(
        testdir,
        "data/montants_norm.txt",
    )
    with source.open("r") as fin:
        with ref.open("r") as fref:
            for lin, lref in zip(fin, fref):
                montants = ast.literal_eval(lin)
                normalized = [montant_fun(montant) for montant in montants]
                montants_ref = ast.literal_eval(lref)
                assert normalized == montants_ref


def test_normalize():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/gp_conformitee_test-documents.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]
        formatter = NormalizerProcessor()
        options = NormalizerParameters()
        normalizeds = formatter.process(docs, options)
        norm_file = testdir / "data/gp_conformitee_test-documents-norm.json"
        dl = DocumentList(__root__=normalizeds)
        with norm_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

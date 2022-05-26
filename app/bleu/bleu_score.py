"""
bleu_score.py

Calculate BLEU score information for a pandas dataframe containing language data.
"""

from nltk.translate.bleu_score import (
    corpus_bleu, sentence_bleu, SmoothingFunction)
import pandas as pd
from pathlib import Path
from typing import Tuple

chencherry = SmoothingFunction()


# ====================
def get_ref_and_hyp_column_names(columns: list) -> Tuple[str, list]:

    ref_columns = [c for c in columns if c.lower().startswith('reference')]
    # There should only be one reference column
    # TODO: validate this
    ref_column = ref_columns[0]
    hyp_columns = [c for c in columns if c.lower().startswith('hypothesis')]
    return ref_column, hyp_columns


# ====================
def get_refs_and_hyps(df: pd.DataFrame) -> dict:
    """Generate lists of lists of words in reference and hypothesis texts
    from a pandas dataframe"""

    ref_column, hyp_columns = get_ref_and_hyp_column_names(df.columns)
    output_dict = {key: [] for key in [ref_column] + hyp_columns}

    for _, row in df.iterrows():
        output_dict[ref_column].append([row[ref_column].split()])
        for hyp_column in hyp_columns:
            output_dict[hyp_column].append(row[hyp_column].split())

    return (output_dict)


# ====================
def get_min_max_sents(refs_and_hyps: dict) -> dict:

    ref_column, hyp_columns = get_ref_and_hyp_column_names(refs_and_hyps.keys())
    refs = refs_and_hyps[ref_column]
    output_dict = {}

    for hyp in hyp_columns:
        all_sent_scores = []
        output_dict[hyp] = {}
        for ref_sent, hyp_sent in zip(refs, refs_and_hyps[hyp]):
            all_sent_scores.append({
                'reference': ' '.join(ref_sent[0]),
                'hypothesis': ' '.join(hyp_sent),
                'score': sentence_bleu(
                    ref_sent, hyp_sent, smoothing_function=chencherry.method5),
            })
        output_dict[hyp]['max'] = max(all_sent_scores, key=lambda x: x['score'])
        output_dict[hyp]['min'] = min(all_sent_scores, key=lambda x: x['score'])

    return output_dict


# ====================
def get_corpus_bleu_scores(refs_and_hyps: dict) -> dict:

    ref_column, hyp_columns = get_ref_and_hyp_column_names(refs_and_hyps.keys())
    refs = refs_and_hyps[ref_column]
    output_dict = {}

    for hyp in hyp_columns:
        output_dict[hyp] = corpus_bleu(
            refs, refs_and_hyps[hyp], smoothing_function=chencherry.method5)
            
    return(output_dict)


# ====================
if __name__ == "__main__":

    path = Path(__file__)
    test_xlsx_path = path.parent.parent.absolute() / 'test_files' / 'ja_en_test.xlsx'
    df = pd.read_excel(test_xlsx_path)
    refs_and_hyps = get_refs_and_hyps(df)

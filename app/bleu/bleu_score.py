from nltk.translate.bleu_score import (
    corpus_bleu, sentence_bleu, SmoothingFunction)
import pandas as pd
from pathlib import Path

chencherry = SmoothingFunction()


# ====================
def get_refs_and_hyps(df: pd.DataFrame,
                      ref_column: str = 'reference',
                      hyp_columns: list = ['hypothesis1', 'hypothesis2']
                      ) -> dict:
    """Generate lists of reference and hypothesis sentences
    from a pandas dataframe"""
    
    output_dict = {key: [] for key in [ref_column] + hyp_columns}    

    for _, row in df.iterrows():
        output_dict[ref_column].append([row[ref_column].split()])
        for hyp_column in hyp_columns:
            output_dict[hyp_column].append(row[hyp_column].split())

    print(output_dict)
    return (output_dict)


# ====================
def get_min_max_sents(refs_and_hyps: dict) -> dict:

    all_sent_scores = []
    refs = refs_and_hyps['reference']
    for k, hyps in refs_and_hyps.items():
        if k.startswith('hypothesis'):
            for ref, hyp in zip(refs, hyps):
                all_sent_scores.append({
                    'reference': ' '.join(ref[0]),
                    'hypothesis': ' '.join(hyp),
                    'score': sentence_bleu(
                        ref, hyp, smoothing_function=chencherry.method5),
                    'hypset': k
                })
    
    output_dict = {
        'max': max(all_sent_scores, key=lambda x: x['score']),
        'min': min(all_sent_scores, key=lambda x: x['score']),
    }
    return output_dict


# ====================
def get_corpus_bleu_scores(refs_and_hyps: dict) -> dict:

    output_dict = {}
    refs = refs_and_hyps['reference']
    for k, hyp in refs_and_hyps.items():
        if k.startswith('hypothesis'):
            output_dict[k] = corpus_bleu(
                refs, hyp, smoothing_function=chencherry.method5)
            
    return(output_dict)            


# ====================
if __name__ == "__main__":

    path = Path(__file__)
    test_xlsx_path = path.parent.parent.absolute() / 'test_files' / 'ja_en_test.xlsx'
    df = pd.read_excel(test_xlsx_path)
    refs_and_hyps = get_refs_and_hyps(df)
    print(get_corpus_bleu_scores(refs_and_hyps))
    print(get_min_max_sents(refs_and_hyps))

import sys
import os
import re
from docx import Document


def load_doc(path):
    try:
        return Document(path)
    except Exception as e:
        print(f"FAIL: cannot open report: {e}")
        sys.exit(1)


def doc_text(doc):
    texts = []
    for p in doc.paragraphs:
        texts.append(p.text)
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                texts.append(c.text)
    return "\n".join(texts)


def assert_contains(txt, needle, msg):
    if needle not in txt:
        print(f"FAIL: missing '{needle}' ({msg})")
        sys.exit(1)


def main():
    # Resolve report path (prefer non-timestamped, else latest timestamped)
    report = os.path.join('outputs', 'Final_Report.docx')
    if not os.path.exists(report):
        candidates = [p for p in os.listdir('outputs') if p.startswith('Final_Report_') and p.endswith('.docx')]
        if candidates:
            candidates.sort()
            report = os.path.join('outputs', candidates[-1])
        else:
            print('FAIL: report not found')
            sys.exit(1)

    doc = load_doc(report)
    txt = doc_text(doc)

    # Section headings should appear
    for sec in ['## Executive','## Market','## Regulation','## Competition','## GTM','## Partners','## Risks','## Decision Scorecard']:
        assert_contains(txt, sec, 'section headings')

    # Coverage patterns should appear at least once per case
    cases = [d for d in os.listdir('outputs') if os.path.isdir(os.path.join('outputs', d)) and '_' in d]
    covs = re.findall(r"Coverage: (\d+)%", txt)
    if len(covs) < max(1, len(cases)):
        print('FAIL: coverage occurrences < number of cases')
        sys.exit(1)

    # Each case dir should have required images
    def _check_case_dir(case_dir):
        base = os.path.join('outputs', case_dir)
        try:
            files = os.listdir(base)
        except Exception:
            return False
        ok = any(p.startswith('01_market_summary_') for p in files)
        ok = ok and any(p.startswith('02_customs_flow_') for p in files)
        ok = ok and any(p.startswith('map_') for p in files)
        return ok

    if not all(_check_case_dir(c) for c in cases):
        print('FAIL: required image paths missing in one or more cases')
        sys.exit(1)

    # Segment scores should not all be identical
    seg_scores = re.findall(r"\|\s*(high|mid|low)\s*\|\s*([0-9]+\.[0-9])\s*\|", txt, re.I)
    if seg_scores:
        scores_only = [s for _, s in seg_scores]
        if len(set(scores_only)) == 1:
            print('FAIL: segment scores are identical')
            sys.exit(1)

    # MUST-FAIL implies HOLD
    if 'MUST item FAIL' in txt and 'Decision: RECOMMEND' in txt:
        print('FAIL: MUST-FAIL present but decision is RECOMMEND')
        sys.exit(1)

    print('PASS: report ok')


if __name__ == '__main__':
    main()


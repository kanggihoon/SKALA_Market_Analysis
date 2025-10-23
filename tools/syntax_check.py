import os
import sys
import ast

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, 'src')

def main():
    bad = []
    for dirpath, _, filenames in os.walk(SRC):
        for fn in filenames:
            if not fn.endswith('.py'):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    src = f.read()
                ast.parse(src, filename=path)
            except Exception as e:
                bad.append((path, str(e)))
    if bad:
        print('FAIL: syntax errors found:')
        for p, e in bad:
            print('-', p, '->', e)
        sys.exit(1)
    print('PASS: all Python files parsed successfully')

if __name__ == '__main__':
    main()


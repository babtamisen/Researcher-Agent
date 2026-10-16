#!/usr/bin/env python3
"""Render an answer artifact without rewriting. Not a source/claim validator."""
import json
import sys

def render(obj):
    if not isinstance(obj,dict) or set(obj) != {'blocks'}:
        raise ValueError('expected blocks only')
    blocks=obj['blocks']
    if not isinstance(blocks,list) or not 1 <= len(blocks) <= 100:
        raise ValueError('invalid blocks')
    if any(not isinstance(b,str) or not b.strip() or len(b)>50000 for b in blocks):
        raise ValueError('invalid block')
    return '\n\n'.join(blocks)+'\n'

def main():
    try:
        raw=sys.stdin.buffer.read(262145)
        if len(raw)>262144:raise ValueError('artifact too large')
        text=render(json.loads(raw))
    except (ValueError,TypeError,UnicodeError):
        print('unable_to_render',file=sys.stderr)
        return 2
    sys.stdout.write(text)
    return 0
if __name__=='__main__':sys.exit(main())

#!/usr/bin/env python3
"""Offline structured calculation checker. No network, eval, delivery or file writes."""
import hashlib
import json
import re
import sys
from decimal import Decimal, localcontext, ROUND_HALF_UP

SCALES = {'one': Decimal(1), 'million': Decimal(10)**6, 'billion': Decimal(10)**9}

class Invalid(ValueError):
    pass

def require(ok, code):
    if not ok:
        raise Invalid(code)

def number(value):
    require(isinstance(value, str) and len(value) <= 64 and
            re.fullmatch(r'-?\d+(?:\.\d+)?', value), 'invalid_decimal_string')
    result = Decimal(value)
    require(result.is_finite() and abs(result) <= Decimal('1e24'), 'number_out_of_range')
    return result

def exact(obj, fields):
    require(isinstance(obj, dict) and set(obj) == set(fields), 'invalid_fields')

def validate(record):
    """Verify one allowlisted calculation; withhold all results on failure."""
    try:
        with localcontext() as ctx:
            ctx.prec = 60
            exact(record, ['operation', 'inputs', 'claim'])
            op = record['operation']
            require(isinstance(op, str), 'invalid_operation')
            fields = {'eps': ['income', 'shares'],
                      'net_debt': ['gross', 'restricted', 'pledged', 'available', 'debt'],
                      'deannualize': ['rate'], 'annualize': ['rate']}
            require(op in fields, 'unsupported_operation')
            inputs = record['inputs']
            exact(inputs, fields[op])
            values = {}
            sources = []
            periods = set()
            for key, q in inputs.items():
                exact(q, ['value', 'unit', 'scale', 'period', 'source'])
                require(isinstance(q['source'], str) and 0 < len(q['source'].strip()) <= 2048,
                        'missing_source')
                require(isinstance(q['period'], str) and 0 < len(q['period'].strip()) <= 100,
                        'missing_period')
                require(isinstance(q['scale'], str) and q['scale'] in SCALES, 'invalid_scale')
                expected = 'shares' if key == 'shares' else ('percent' if key == 'rate' else 'USD')
                require(q['unit'] == expected, 'inconsistent_units')
                require(key != 'rate' or q['scale'] == 'one', 'invalid_rate_scale')
                values[key] = number(q['value']) * SCALES[q['scale']]
                sources.append(q['source'])
                periods.add(q['period'])
            require(len(periods) == 1, 'inconsistent_periods')
            exact(record['claim'], ['value', 'places'])
            places = record['claim']['places']
            require(type(places) is int and 0 <= places <= 8, 'invalid_rounding')
            claim = number(record['claim']['value'])
            if op == 'eps':
                require(values['shares'] > 0, 'invalid_share_count')
                result = values['income'] / values['shares']
                unit, formula = 'USD/share', 'income_USD / diluted_shares'
            elif op == 'net_debt':
                require(all(v >= 0 for v in values.values()), 'negative_liquidity_input')
                require(values['gross'] - values['restricted'] - values['pledged'] == values['available'],
                        'unreconciled_liquidity')
                result = values['debt'] - values['available']
                unit, formula = 'USD', 'debt_USD - available_USD'
            else:
                r = values['rate'] / 100
                require(r >= -1, 'invalid_rate_domain')
                result = (((1+r) ** (Decimal(1)/4) - 1) if op == 'deannualize'
                          else ((1+r)**4-1)) * 100
                unit = 'percent'
                formula = ('((1 + rate_percent / 100) ** (1/4) - 1) * 100'
                           if op == 'deannualize' else '((1 + rate_percent / 100) ** 4 - 1) * 100')
            rounded = result.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
            require(claim == rounded, 'claimed_result_mismatch')
            digest = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            return {'status': 'verified', 'scope': 'structured_calculation_only',
                    'record_sha256': digest, 'result': format(rounded, 'f'), 'unit': unit,
                    'formula': formula, 'period': next(iter(periods)),
                    'sources': sorted(set(sources)),
                    'statement': f'{op}: {rounded} {unit}; basis: {next(iter(periods))}.',
                    'publication_authorized': False}
    except (Invalid, ArithmeticError, TypeError, ValueError):
        # Do not echo untrusted values or return partial numerical results.
        code = sys.exc_info()[1]
        return {'status': 'unable_to_verify', 'publication_authorized': False,
                'errors': [{'code': str(code) if isinstance(code, Invalid) else 'invalid_record'}]}

def main():
    try:
        raw = sys.stdin.buffer.read(65537)
        require(len(raw) <= 65536, 'input_too_large')
        def unique(pairs):
            result = {}
            for key, value in pairs:
                require(key not in result, 'duplicate_json_key')
                result[key] = value
            return result
        record = json.loads(raw, object_pairs_hook=unique)
        output = validate(record)
    except (ValueError, UnicodeError):
        output = {'status': 'unable_to_verify', 'publication_authorized': False,
                  'errors': [{'code': 'invalid_json_or_input'}]}
    print(json.dumps(output, sort_keys=True))
    return 0 if output['status'] == 'verified' else 2

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Normalize source-row claims; never infer source definitions."""
import json,sys
from decimal import Decimal,localcontext
from validate import number,require,Invalid,exact,validate,SCALES

def adapt(doc):
    try:
        with localcontext() as ctx:
            ctx.prec=60
            exact(doc,['evidence','mapping','supplied_claim'])
            require(isinstance(doc['evidence'],list) and 1<=len(doc['evidence'])<=100,'invalid_evidence')
            rows={}
            for row in doc['evidence']:
                exact(row,['row_id','locator','original_label','excerpt','value','currency','scale','as_of'])
                for key in ['row_id','locator','original_label','excerpt','as_of']:
                    require(isinstance(row[key],str) and 0<len(row[key].strip())<=4096,'missing_evidence')
                require(row['row_id'] not in rows,'duplicate_row_id')
                require(row['currency']=='USD','inconsistent_units')
                require(isinstance(row['scale'],str) and row['scale'] in SCALES,'invalid_scale')
                number(row['value'])
                rows[row['row_id']]=row
            exact(doc['mapping'],['gross','restricted','pledged','available','debt'])
            exact(doc['supplied_claim'],['row_id','places'])
            ids=list(doc['mapping'].values())+[doc['supplied_claim']['row_id']]
            require(all(isinstance(i,str) and i in rows for i in ids),'missing_row')
            require(len(set(ids))==6,'reused_source_row')
            require(len({rows[i]['as_of'] for i in ids})==1,'inconsistent_periods')
            def quantity(i):
                r=rows[i]
                return dict(value=r['value'],unit='USD',scale=r['scale'],period=r['as_of'],source=r['locator'])
            claim=rows[ids[-1]]
            base=number(claim['value'])*SCALES[claim['scale']]
            record=dict(operation='net_debt',inputs={k:quantity(v) for k,v in doc['mapping'].items()},claim=dict(value=format(base,'f'),places=doc['supplied_claim']['places']))
            result=validate(record)
            return dict(status='adapted',record=record,validation=result,evidence=doc['evidence'],mapping=doc['mapping'],claim_source=claim['locator'],publication_authorized=False)
    except (ValueError,TypeError,ArithmeticError):
        return dict(status='unable_to_adapt',publication_authorized=False,errors=[{'code':'invalid_source_record'}])

def main():
    try:
        raw=sys.stdin.buffer.read(65537)
        require(len(raw)<=65536,'input_too_large')
        def unique(pairs):
            d={}
            for k,v in pairs:
                require(k not in d,'duplicate_key');d[k]=v
            return d
        out=adapt(json.loads(raw,object_pairs_hook=unique))
    except (ValueError,UnicodeError):out={'status':'unable_to_adapt','publication_authorized':False}
    # Record may include rejected claim for private audit, never publication.
    print(json.dumps(out,sort_keys=True))
    return 0 if out.get('validation',{}).get('status')=='verified' else 2
if __name__=='__main__':sys.exit(main())

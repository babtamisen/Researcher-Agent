# Researcher calculation prototype 0.1

Offline, Python 3.12 standard library only. No credentials, network access, packages, elevation, Gateway plugins, or delivery integration required. Run from an ordinary user account.

Supported operations: diluted EPS (USD income divided by shares), reconciled net debt (USD), annualized-to-quarterly and quarterly-to-annualized rates (four quarters/year). USD only in this prototype. Net debt excludes leases unless included in the supplied debt definition; choose inputs consistently.

Run:

    python3 -m unittest discover -s tests -v
    python3 validate.py < examples/eps-valid.json

Input is ONE JSON record on stdin, maximum 64 KiB. Exit 0 means the structured calculation and supplied claim match. Exit 2 means unable_to_verify. Output is one JSON object. Caller must also check process exit, bound execution time, and validate output. No output files are written.

Each quantity has decimal-string value, unit (USD/shares/percent), scale (one/million/billion), period, and a nonempty source locator. For rates use scale one and percentage POINTS: "5.8", never "5.8%" or "0.058" for a 5.8% input. For EPS income/shares must cover the same period; supply diluted weighted-average shares. For net debt all inputs must refer to the same date. period is an exact-match label, not a semantic date parser.

claim.value is the expected result in BASE output units: USD/share, USD, or percent. places is 0..8 decimal places; ROUND_HALF_UP applies. Net debt of 202 million USD must be claimed as "202000000". The calculator normalizes input scales before calculating. Negative net debt means net cash.

Liquidity reconciliation is deliberately strict: gross - restricted - pledged must equal available EXACTLY; no inferred rounding tolerance or invented exclusion is accepted. Rounded source statements can therefore be rejected. A later version may support explicit justified tolerances. Restricted and pledged amounts must be disjoint exclusions; this program cannot prove that from a document.

Unknown fields/operations, missing citations/periods, cross-unit inputs, invalid decimals, duplicate JSON keys, nonpositive share counts, rate inputs below -100%, inconsistent periods and mismatched results are rejected. No arbitrary expressions/code are evaluated.

Success returns a canonical formula, result, unit, period, source list, deterministic statement, and SHA256 of the normalized JSON record. Reuse that statement directly for numerical presentation. A hash is an audit fingerprint, NOT a signature, permission or publication gate. All responses explicitly set publication_authorized=false.

LIMITS
This validates supplied structured records, not source truth, extraction accuracy, free-form drafts, formula text in prose, investment conclusions or all report claims. If both extracted values and supplied claim are wrong consistently, it can pass. Citation presence does not prove a citation supports the value. Exact period labels do not establish comparability. A model can ignore the script. No Gateway publication blocking is implemented. Do not describe this as an enforced final-answer validator.

No existing researcher files should be replaced. Rollback: delete the disposable extracted directory; no configuration change is needed for offline tests. See OPENCLAW-INSTRUCTIONS.txt for the controlled runtime canary.

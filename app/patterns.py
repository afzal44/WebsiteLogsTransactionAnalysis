import re
patterns = {"transaction":[
    re.compile(
        r"\{\s*"
    r"transaction:\s*\{\s*"
    r"id:\s*'(?P<id>[^']+)'\s*,\s*"
    r"type:\s*'(?P<type>[^']+)'\s*,\s*"
    r"source:\s*'(?P<source>[^']+)'\s*,\s*"
    r"action:\s*'(?P<action>[^']+)'\s*,\s*"
    r"userId:\s*'(?P<userId>[^']+)'\s*,\s*"
    r"paymentBalance:\s*(?P<paymentBalance>[0-9\.]+)\s*,\s*"
    r"updatePaymentBalance:\s*(?P<updatePaymentBalance>true|false)\s*,\s*"
    r"metadata:\s*[`'](?P<metadata>\{.*?\})[`']\s*,\s*"
    r"currency:\s*'(?P<currency>[^']+)'\s*,\s*"
    r"amount:\s*(?P<amount>[0-9\.]+)\s*,\s*"
    r"vat:\s*(?P<vat>[0-9\.]+)\s*,\s*"
    r"oldBalance:\s*(?P<oldBalance>[0-9\.]+)\s*,\s*"
    r"newBalance:\s*(?P<newBalance>[0-9\.]+)\s*"
    r"\}\s*\}"
    ),
    re.compile(
    r"\{\s*"
    r"transaction:\s*\{\s*"
    r"id:\s*'(?P<id>[^']+)'\s*,\s*"
    r"type:\s*'(?P<type>[^']+)'\s*,\s*"
    r"source:\s*'(?P<source>[^']+)'\s*,\s*"
    r"action:\s*'(?P<action>[^']+)'\s*,\s*"
    r"userId:\s*'(?P<userId>[^']+)'\s*,\s*"
    r"paymentBalance:\s*(?P<paymentBalance>[0-9\.]+)\s*,\s*"
    r"updatePaymentBalance:\s*(?P<updatePaymentBalance>true|false)\s*,\s*"
    r"metadata:\s*'(?P<metadata>\{.*?\})'\s*,\s*"
    r"currency:\s*'(?P<currency>[^']+)'\s*,\s*"
    r"amount:\s*(?P<amount>[0-9\.]+)\s*,\s*"
    r"vat:\s*(?P<vat>[0-9\.]+)\s*,\s*"
    r"oldBalance:\s*(?P<oldBalance>[0-9\.]+)\s*,\s*"
    r"newBalance:\s*(?P<newBalance>[0-9\.]+)\s*"
    r"\}\s*\}"
),
re.compile(r"\{\s+transaction:\s+\{\s+id:\s+'[A-Z0-9]+',\s+type:\s+'[A-Z]+',\s+source:\s+'[A-Z_]+',\s+action:\s+'[A-Z_]+',\s+userId:\s+'[a-f0-9-]+',\s+paymentBalance:\s+\d+,\s+updatePaymentBalance:\s+(true|false),\s+metadata:\s+'[^']*',\s+currency:\s+'[A-Z]+',\s+amount:\s+\d+,\s+vat:\s+\d+,\s+oldBalance:\s+\d+,\s+newBalance:\s+\d+\s+\}\s+\}"),
re.compile(
    r"{transaction: (\{(.*?)\})}"
),
re.compile(
    r"{transaction: ({(.*?)})}"
),
 re.compile(r"sync {{([^:]+): (.*?)}"),
re.compile(r"\{\s*transaction\s*:\s*\{\s*.*?\s*\}\s*\}"
),
re.compile(r"^\{ transaction: \{(?P<data>.*?)\}\}$")
],
"error":[
    re.compile(r'\{[^{}]*\}'),
    re.compile(r"\{\s+userId:\s+'[a-f0-9-]+',\s+subscriptionBalance:\s+\d+(\.\d+)?,\s+paymentBalance:\s+\d+(\.\d+)?\s+\}"),
    re.compile(r"ERROR  Subscription balance and payment balance are not in sync {.*?}"),
    
]
}
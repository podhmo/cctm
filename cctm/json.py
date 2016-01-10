# -*- coding:utf-8 -*-
import json
from functools import partial

load = json.load
loads = json.loads
dump = partial(json.dump, indent=2, ensure_ascii=False)
dumps = partial(json.dumps, indent=2, ensure_ascii=False)

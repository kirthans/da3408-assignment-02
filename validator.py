import os
import re
from pathlib import Path

import pandas as pd

SHARD_DIR = Path("signup_shards")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REQUIRED_FIELDS = ["user_id", "email", "full_name"]

completion_index = int(os.environ["JOB_COMPLETION_INDEX"])
node_name = os.environ.get("NODE_NAME", "unknown")
shard_path = SHARD_DIR / f"signups_shard_{completion_index}.csv"

df = pd.read_csv(shard_path)
invalid_rows = 0

for _, row in df.iterrows():
    has_missing_required_field = any(
        pd.isna(row[field]) or not str(row[field]).strip()
        for field in REQUIRED_FIELDS
    )
    has_malformed_email = not EMAIL_PATTERN.fullmatch(str(row["email"]).strip())

    if has_missing_required_field or has_malformed_email:
        invalid_rows += 1

print(
    "VALIDATION_RESULT "
    f"shard_index={completion_index} "
    f"node_name={node_name} "
    f"invalid_rows={invalid_rows}"
)
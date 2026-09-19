import random
from pathlib import Path

import pandas as pd

random.seed(42)

OUTPUT_DIR = Path("signup_shards")
EXPECTED_INVALID_COUNTS = [2, 3, 1, 4, 2, 5, 3, 2]
COUNTRIES = ["India", "Japan", "Canada", "Germany"]

def valid_row(shard_index: int, row_index: int) -> dict:
    return {
        "user_id": f"user-{shard_index}-{row_index}",
        "email": f"user{shard_index}_{row_index}@example.com",
        "full_name": f"User {shard_index} {row_index}",
        "country": random.choice(COUNTRIES),
    }

def invalid_row(shard_index: int, row_index: int, invalid_index: int) -> dict:
    row = valid_row(shard_index, row_index)

    if invalid_index % 2 == 0:
        row["email"] = f"invalid-email-{shard_index}-{invalid_index}"
    else:
        row["full_name"] = ""

    return row

OUTPUT_DIR.mkdir(exist_ok=True)

for shard_index, invalid_count in enumerate(EXPECTED_INVALID_COUNTS):
    rows = [valid_row(shard_index, row_index) for row_index in range(20)]

    for invalid_index in range(invalid_count):
        rows.append(
            invalid_row(
                shard_index,
                100 + invalid_index,
                invalid_index,
            )
        )

    random.shuffle(rows)


    output_path = OUTPUT_DIR / f"signups_shard_{shard_index}.csv"
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"{output_path}: expected invalid rows = {invalid_count}")
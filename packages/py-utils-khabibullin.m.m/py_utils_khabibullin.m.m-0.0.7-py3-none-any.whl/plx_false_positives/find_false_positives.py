import json


def print_false_positives(file: str):
    with open(file) as f:
        data = json.load(f)
        mismatches = data["mismatches"]
        for item in mismatches:
            if item["deal_value"] is not None:
                print(item)

    print(f"Count of items: {len(data)}")

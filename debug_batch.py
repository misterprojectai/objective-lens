#!/usr/bin/env python3
"""
Debug: inspect what Haiku actually returned for a batch
Usage: python3 debug_batch.py msgbatch_015yoZhUiTt1gJewPGtME59J
"""

import sys
import anthropic

client = anthropic.Anthropic()
batch_id = sys.argv[1]

print(f"Inspecting batch: {batch_id}")
print()

count = 0
for result in client.messages.batches.results(batch_id):
    if count >= 3:  # show first 3 results only
        break
    print(f"=== {result.custom_id} ===")
    print(f"Result type: {result.result.type}")
    if result.result.type == "succeeded":
        raw = result.result.message.content[0].text
        print(f"Response length: {len(raw)} chars")
        print(f"First 500 chars:")
        print(repr(raw[:500]))
    print()
    count += 1

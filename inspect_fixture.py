from pathlib import Path
import json

p = Path("backup_ids_utf8_nobom.json")
raw = p.read_bytes()

print("=== FIRST 32 BYTES ===")
print(raw[:32])
print("HEX:", raw[:32].hex(" "))

# decodificar
text = raw.decode("utf-8", errors="replace")

print("\n=== FIRST 5 LINES ===")
lines = text.splitlines()
for i in range(min(5, len(lines))):
    print(f"{i+1}:", repr(lines[i]))

print("\n=== FIRST 200 CHARS ===")
print(repr(text[:200]))

print("\n=== JSON LOAD TEST ===")
try:
    json.loads(text)
    print("JSON OK ✅")
except json.JSONDecodeError as e:
    print("JSON ERROR ❌")
    print("Line:", e.lineno)
    print("Column:", e.colno)
    print("Position:", e.pos)
    print("Message:", e.msg)

    start = max(e.pos - 60, 0)
    end = min(e.pos + 60, len(text))
    snippet = text[start:end]

    print("\n=== CONTEXT ===")
    print(repr(snippet))
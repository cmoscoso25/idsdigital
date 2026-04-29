from pathlib import Path

src = Path("backup_ids_utf8.json")
dst = Path("backup_ids_utf8_nobom.json")

raw = src.read_bytes()

# UTF-8 BOM bytes: EF BB BF
if raw.startswith(b"\xef\xbb\xbf"):
    raw = raw[3:]
    print("✅ BOM removido")
else:
    print("ℹ️ El archivo no tiene BOM (nada que hacer)")

dst.write_bytes(raw)
print(f"✅ Archivo generado: {dst}")
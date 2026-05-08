import os
import pathlib
import nbformat
from nbconvert import MarkdownExporter

print("--- INICIANDO CONVERSIÓN NATIVA (SIN TRAMPOLINES) ---", flush=True)

# 1. Instanciamos el exportador de Markdown
exporter = MarkdownExporter()
base_path = pathlib.Path('.').absolute()

# 2. Localizamos los archivos
files = list(base_path.rglob('*.ipynb'))
print(f"Archivos encontrados: {len(files)}", flush=True)

for ipynb_path in files:
    try:
        # Definimos el nombre del archivo de salida (.md)
        target_path = ipynb_path.with_suffix('.md')
        print(f"📖 Leyendo: {ipynb_path.name}...", end=" ", flush=True)

        # LEER el notebook (formato JSON interno)
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            nb_content = nbformat.read(f, as_version=4)

        # EXPORTAR a Markdown
        (body, resources) = exporter.from_notebook_node(nb_content)

        # GUARDAR el resultado
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(body)
            
        print("✅ ¡Hecho!", flush=True)

    except Exception as e:
        print(f"❌ Error en {ipynb_path.name}: {e}", flush=True)

print("\n--- PROCESO FINALIZADO ---", flush=True)
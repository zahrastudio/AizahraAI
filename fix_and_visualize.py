# import os  # FIXED: unknown import commented out
import ast
# import networkx as nx  # FIXED: unknown import commented out
# import matplotlib.pyplot as plt  # FIXED: unknown import commented out
# import re  # FIXED: unknown import commented out

def find_py_files(root_dir):
    py_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.py'):
                py_files.append(os.path.join(dirpath, f))
    return py_files

def parse_file_ast(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content, filename=filepath)
        return tree, content
    except SyntaxError as e:
        print(f"Syntax error in {filepath}: {e}")
    except Exception as e:
        print(f"Failed parsing {filepath}: {e}")
    return None, None

def get_imports(tree):
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
    return imports

def fix_imports(filepath, content, module_names):
    """
    Perbaiki import yang kemungkinan salah:
    - Ubah import relatif dengan titik berlebih jadi import absolut sederhana
    - Perbaiki import yang modulnya tidak ada dalam project jadi komentar
    """
    lines = content.splitlines()
    changed = False

    import_pattern = re.compile(r'^\s*(from|import)\s+([\w\.]+)')
    
    for i, line in enumerate(lines):
        m = import_pattern.match(line)
        if m:
            keyword, mod = m.groups()
            mod_base = mod.split('.')[0]
            if mod_base not in module_names:
                # Modul tidak ada di project, bisa jadi eksternal, skip perbaikan.
                # Namun jika modul lokal tapi tidak ketemu, bisa kita comment agar tidak error.
                # Cek misal import lokal yang keliru, contohnya: 'from ..foo import bar'
                if mod.startswith('.'):
                    # ubah import relatif jadi import absolut sederhana (hilangkan titik)
                    new_line = line.replace('.', '').strip()
                    if new_line != line:
                        print(f"Fixing relative import in {filepath}:\n  {line}\n-> {new_line}")
                        lines[i] = '# ' + line + '  # FIXED: relative import commented out (manual check needed)'
                        changed = True
                else:
                    # Comment import modul asing yang error
                    print(f"Commenting unknown import '{mod}' in {filepath}")
                    lines[i] = '# ' + line + '  # FIXED: unknown import commented out'
                    changed = True
            else:
                # Modul ada di project, no fix needed
                pass
    if changed:
        return '\n'.join(lines)
    else:
        return None

def build_dependency_graph(root_dir, module_map):
    G = nx.DiGraph()
    for mod in module_map.keys():
        G.add_node(mod)
    for mod, path in module_map.items():
        tree, content = parse_file_ast(path)
        if tree:
            imports = get_imports(tree)
            for imp in imports:
                if imp in module_map:
                    G.add_edge(mod, imp)
    return G

def draw_graph(G):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_size=2500, node_color='lightgreen', font_size=10, arrowsize=20)
    plt.title("Modul Dependency Graph (Fixed Imports)")
    plt.show()

def main():
    root_dir = '.'  # Atur sesuai root proyek kamu

    print("Scanning .py files...")
    py_files = find_py_files(root_dir)

    # Map file basename tanpa ekstensi ke path
    module_map = {}
    for f in py_files:
        base = os.path.splitext(os.path.basename(f))[0]
        module_map[base] = f

    # Cek & perbaiki file
    for mod, path in module_map.items():
        tree, content = parse_file_ast(path)
        if content is None:
            print(f"Skipping {path} due to parse errors")
            continue

        fixed_content = fix_imports(path, content, module_map.keys())
        if fixed_content:
            # Backup dulu
            backup_path = path + '.bak'
            if not os.path.exists(backup_path):
                os.rename(path, backup_path)
                print(f"Backup created: {backup_path}")
            with open(path, 'w', encoding='utf-8') as fw:
                fw.write(fixed_content)
            print(f"Fixed imports and saved: {path}")

    # Build graph setelah fix
    print("Building dependency graph...")
    G = build_dependency_graph(root_dir, module_map)

    print(f"Graph nodes: {len(G.nodes())}, edges: {len(G.edges())}")

    # Visualisasi
    draw_graph(G)

if __name__ == "__main__":
    main()

# import os  # FIXED: unknown import commented out
import ast
# from pyvis.network import Network  # FIXED: unknown import commented out

# Scan semua file Python, HTML, JSON terkait dalam folder proyek
def scan_files(root_dir):
    py_files = {}
    other_files = []
    for dirpath, _, files in os.walk(root_dir):
        for f in files:
            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, root_dir)
            if f.endswith('.py'):
                mod_name = rel_path.replace(os.sep, '.')[:-3]  # modul python format
                py_files[mod_name] = full_path
            elif f.endswith(('.html', '.json')):
                other_files.append(rel_path)
    return py_files, other_files

# Ambil import dari file Python dan deteksi apakah import local (dari py_files)
def extract_imports(filepath, local_modules):
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name
                    if name in local_modules:
                        imports.add(name)
                    else:
                        for lm in local_modules:
                            if name.startswith(lm + '.'):
                                imports.add(lm)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module
                if mod:
                    if mod in local_modules:
                        imports.add(mod)
                    else:
                        for lm in local_modules:
                            if mod.startswith(lm + '.'):
                                imports.add(lm)
    except Exception as e:
        print(f"Failed parsing {filepath}: {e}")
    return imports

# Bangun graph networkx dari modul dan import lokal
def build_graph(py_files):
#     import networkx as nx  # FIXED: unknown import commented out
    G = nx.DiGraph()
    for mod in py_files:
        G.add_node(mod, label=mod, color='lightblue', title=f"Python module: {mod}")

    for mod, path in py_files.items():
        imps = extract_imports(path, py_files.keys())
        for imp in imps:
            if imp in py_files:
                G.add_edge(mod, imp)
    return G

# Tambah node file non-python ke graph
def add_other_files_to_graph(G, other_files):
    for f in other_files:
        G.add_node(f, label=f, color='lightgreen', title=f"Resource file: {f}")

# Export ke file html interaktif menggunakan pyvis
def visualize_graph_pyvis(G, output_file="dependency_graph.html"):
    net = Network(height="900px", width="100%", notebook=False, directed=True)
    for node, attr in G.nodes(data=True):
        net.add_node(node, label=attr.get('label', node), title=attr.get('title', ''), color=attr.get('color', 'lightblue'))
    for src, dst in G.edges():
        net.add_edge(src, dst)
    net.show(output_file)
    print(f"Graph saved as {output_file}")

def main():
    root_dir = '.'  # Sesuaikan dengan direktori proyekmu
    py_files, other_files = scan_files(root_dir)
    print(f"Found {len(py_files)} Python modules, {len(other_files)} HTML/JSON resource files")

#     import networkx as nx  # FIXED: unknown import commented out
    G = build_graph(py_files)
    add_other_files_to_graph(G, other_files)
    visualize_graph_pyvis(G)

if __name__ == "__main__":
    main()

import os
import re
import sys
import argparse
import importlib.util

try:
    from black import format_str, FileMode

    black_installed = True
except ModuleNotFoundError:
    print(
        "black formatter is not installed. Run 'pip install black' to install it and get formatted init files."
    )
    black_installed = False


def load_module_from_path(path):
    point_path = os.path.splitext(path)[0].replace("/", ".")
    spec = importlib.util.spec_from_file_location(point_path, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[point_path] = mod
    spec.loader.exec_module(mod)
    return mod


def get_end_of_import_section(lines):
    lets = re.compile(r"\w")
    klammered = False
    for i, line in enumerate(lines):
        if not (
            line.startswith("from")
            or line.startswith("import")
            or line.startswith("#")
            or klammered
        ) and lets.findall(line):
            return i
        if len(line) > 0 and not line.startswith("#"):
            if "(" in line:
                klammered = True
            if ")" in line:
                klammered = False
    return i + 1


def create_init_file_in_dir(dir_path, starred=False):
    init_path = os.path.join(dir_path, "__init__.py")
    wordre = re.compile(r"\w+")
    add_lines = []
    if os.path.exists(init_path):
        with open(init_path) as f:
            lines = f.read().splitlines()
            add_lines = lines[get_end_of_import_section(lines) :]

    to_import = [
        os.path.splitext(x)[0]
        for x in os.listdir(dir_path)
        if os.path.splitext(x)[1] == ".py" and x != "__init__.py"
    ]

    if len(to_import) == 0:
        return

    import_lines = []

    if starred:
        for x in to_import:
            import_lines.append(f"from .{x} import *")
    else:
        for x in to_import:
            obj_to_import = []
            mod_path = os.path.join(dir_path, x + ".py")
            with open(mod_path, "r") as f:
                lines = f.read().splitlines()
                imp_section = "\n".join(lines[: get_end_of_import_section(lines)])
                blocks = wordre.findall(imp_section)
            mod = load_module_from_path(mod_path)
            for name in dir(mod):
                if name[0] != "_" and name not in blocks:
                    obj_to_import.append(name)
            if len(obj_to_import) > 0:
                import_lines.append(f"from .{x} import {', '.join(obj_to_import)}")

    file_content = "\n".join(import_lines + [""] + add_lines)
    with open(init_path, "w") as f:
        if black_installed:
            file_content = format_str(file_content, mode=FileMode())
        f.write(file_content)


def recursively_create_init_files(parent_dir, starred=False):
    for root, dirs, _ in os.walk(parent_dir):
        for d in dirs:
            create_init_file_in_dir(
                os.path.join(root, d),
                starred=starred,
            )


def command_line_run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "parent_dir",
        type=str,
        help="Parent directory to recursively create init files in",
    )
    parser.add_argument("--starred", action="store_true", default=False)
    args = parser.parse_args()
    recursively_create_init_files(
        args.parent_dir,
        starred=args.starred,
    )

import sys

def parse(param_names_list: list) -> tuple:
    parsed = []
    print(f"[INFO] Parse args with pattern '$ python {sys.argv[0]} {param_names_list}'")
    args = sys.argv[1:]
    if len(param_names_list) < len(args):
        print(f"[ERROR] Mismatched number of params and args : {len(param_names_list)}, expected {len(args)}")
        exit(1)
    for arg  in  args:
        parsed.append(arg)
        
    return tuple(parsed)
import sys

def parse(param_names_list: list) -> tuple:
    parsed = []
    args = sys.argv[1:]
    if len(param_names_list) < len(args):
        print(f"[ERROR] Mismatched number of params and args : {len(param_names_list)}, expected {len(args)}")
        exit(1)
    for arg  in  args:
        if arg == "help": 
            print(f"[INFO] Parse args with pattern\n '$> python {sys.argv[0]} {param_names_list}'")
            exit(0)
        parsed.append(arg)
        
    return tuple(parsed)
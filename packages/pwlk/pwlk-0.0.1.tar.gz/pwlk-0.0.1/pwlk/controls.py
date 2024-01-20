from rich.table import Table
from rich.console import Console
from rich.rule import Rule
from rich import print, inspect

import platform
import sys
import argparse

def GetArgs(parser: argparse.ArgumentParser, argtable: bool=True, console: Console = Console()):
    '''GetArgs Init function to be used on a configured parser object. Argtable allows to display 
    user values as well as help on defineded args. If not given as argument, a console object is 
    created internally.

    Args:
        parser (argparse.ArgumentParser): argparse.ArgumentParser object, required with anticipated configuration
        argtable (bool, optional): Displays and returns argtable. Defaults to True.
        console (Console, optional): Console instance for rich printing. Defaults to Console().

    Returns:
        args, parser(, argtable): parsing result, input ArgumentParser, Table object
    '''
    # > Parsing the object to store user args
    args = parser.parse_args()
    if argtable:
        # > Defining an argtable to display argname, associated flag, default and arg dtype
        argtable = Table(title = 'Parsed arguments ref. table', title_justify = 'left', padding = (0,2))
        argtable.add_column(header = 'Argument', style = 'italic', justify='center')
        argtable.add_column(header = 'Flag', style = 'bold', justify='center')
        argtable.add_column(header = 'Value', style = 'yellow', justify='left')
        argtable.add_column(header = 'Dtype', style = 'blue', justify='center')
        for arg in vars(args): 
            # Adding a row for each args (Namespace parsing result) item(s)
            argtable.add_row(f'--{arg}' , f'-{arg[:1]}' , f'{getattr(args, arg)}' , f'{getattr(args, arg).__class__.__name__}')
        console.print(argtable)
        return args, parser, argtable
    else:
        return args, parser

def header(console: Console = Console()) -> Table:
    
    console.print(Rule(style = 'white'))
    header = Table(title="> Python script execution init ...", title_justify = "left", border_style="white", min_width = 60, expand=True)
    header.add_column("Variable", style="yellow", header_style="bold yellow")
    header.add_column("Variable states", style="italic yellow", header_style="bold yellow")
    header.add_row("node.os",   f'{platform.uname().system}')
    header.add_row("node.name", f'{platform.uname().node}')
    header.add_row("sys.argv",  f'{repr(sys.argv)}')
    header.add_row("sys.path",  f'{sys.path[0]}')
    console.print(header)
    return header


if __name__ == '__main__':
    
    # inspect(argparse.ArgumentParser, methods=1)
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, 
        description = 'Program & parsing options description', epilog = f'Author : Pawlicki Loïc\n{'─'*30}\n')
    
    parser.add_argument('-f', '--flag_attr', default = 0,   type = int, metavar = '', action= 'store',  help = 'help_text')
    
    console = Console()
    header = header(console)
    args, argtable, parser = GetArgs(parser, console)
print([arg for arg in vars(args)])
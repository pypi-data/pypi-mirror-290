# Imports
import importlib
from customized_table import *
from termcolor import colored


#
# Lists all non-internal functions in a HTML table
#
def generate(package_name, filename): # INTERNAL
    t = CustomizedTable(["",""])
    # Module path
    try:
        path = importlib.util.find_spec(package_name).submodule_search_locations[0]
    except:
        print(colored("Error:", "red", attrs=["bold"]) + " package " + colored(package_name, "blue") + " not found. Make sure it is installed.")
        return
    # Source file
    if not filename.endswith(".py"):
        filename += ".py"
    try:   
        lines = open(path+"/"+filename, "rt").readlines()
    except:
        print(colored("Error:", "red", attrs=["bold"]) + " source file " + colored(filename, "blue") + " not found in package.")
        return
    desc = []
    pars = []
    rets = []
    idx = 0
    for r in lines:
        r = r.strip()
        if r.startswith("#"):
            if "# PARAMS" in r:
                idx = 1
            elif "# RETURNS" in r:
                idx = 2
            elif r != "#":
                if idx == 0:
                    desc.append(r.replace("#","").strip())
                if idx == 1:
                    p = r.replace("# ","").strip()
                    p = "&nbsp;&nbsp;&nbsp;&nbsp;<em>" + p.replace(":","</em>:")
                    pars.append(p)
                if idx == 2:
                    p = r.replace("# ","").strip()
                    rets.append(p)
        elif r.startswith("def ") and "# INTERNAL" not in r:
            d = ""
            if len(desc) > 0:
                d = "<br>".join(desc)
            r = r.replace("(","<font color='#888'> (")
            t.add_row([r.replace("def ","").replace(":",""),"<font color='blue'>" + d + "</font>"])
            pr = ""
            re = ""
            if len(pars) > 0:
                pr = "<br>".join(pars)
            if len(rets) > 0:
                re = "Returns:<br>" + "<br>".join(rets)
            if pr != "" or re != "":
                t.add_row(["<font color='green'>" + pr + "</font>","<font color='#fc9e03'>" + re + "</font>"])
        else:
            desc = []
            pars = []
            rets = []
            idx = 0
    print()
    try:
        lines = open(path+"/__init__.py", "rt").readlines()
        ver = None
        for r in lines:
            r = r.strip()
            if r.startswith("__version__"):
                ver = r[r.find("\"")+1:r.rfind("\"")]
        if ver is not None:
            t.add_row([f"Version: <font color='#9e0504'>{ver}</font>",""], style={"border": "top bottom"})
    except:
        pass
    t.display()
    print()


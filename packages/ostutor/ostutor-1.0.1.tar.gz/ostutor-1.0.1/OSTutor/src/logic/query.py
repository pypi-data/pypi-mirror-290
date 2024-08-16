from ..dao import InstDao, OptDao, InstExtraDao
from ..view.display import display
import curses
from ..data import Parse

def Query(admin, instruction):
    instDao = InstDao()
    optDao = OptDao()
    instExtraDao = InstExtraDao()
    parse = Parse()
    type = "admin" if admin else "user"
    inst = instDao.SelectByNameAndType(instruction, type)
    if inst is None:
        return 
    opts = optDao.SelectById(inst.id)
    extras = instExtraDao.SelectById(inst.id)
    description = [f"    {i}" for i in parse.splitContent(inst.description)]

    lines = [
        "RPM", f"    {inst.rpm}", 
        "BRIEF", f"    {inst.brief}",
        "SYNOPSIS", f"    {inst.synopsis}", '\n',
        "DESCRIPTION", *description,
        "EXAMPLES", f"    {inst.example}",
        "OPTIONS", *[f'    {i.content}' for i in opts],
    ]
    for i in extras:
        lines.append(i.title.upper())
        lines= lines + [f"    {e}" for e in parse.splitContent(i.text)]
    try:
        curses.wrapper(display, lines)
    except:
        return


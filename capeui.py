# -*- coding: utf-8 -*-
"""CapeUI - a Tkinter GUI toolkit for Kadis programs, distributed via Cape."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


def _parent_widget(parent):
    if "_widget" in parent:
        return parent["_widget"]
    if "_root" in parent:
        return parent["_root"]
    raise ValueError("capeui: parent must have _widget or _root")


# ============================================================
# App / window
# ============================================================

def app(title, w=800, h=600, icon=None):
    root = tk.Tk()
    root.title(str(title))
    root.geometry(str(int(w)) + "x" + str(int(h)))
    root.minsize(320, 200)
    if icon:
        try:
            if str(icon).lower().endswith(".ico"):
                root.iconbitmap(str(icon))
            else:
                img = tk.PhotoImage(file=str(icon))
                root.iconphoto(True, img)
                root._icon_img = img  # keep reference
        except Exception as e:
            print("icon error:", e)
    return {"_root": root, "_w": int(w), "_h": int(h)}


def set_icon(a, path):
    try:
        if str(path).lower().endswith(".ico"):
            a["_root"].iconbitmap(str(path))
        else:
            img = tk.PhotoImage(file=str(path))
            a["_root"].iconphoto(True, img)
            a["_root"]._icon_img = img
    except Exception as e:
        print("icon error:", e)


def run(a):
    a["_root"].mainloop()


def close(a):
    try:
        a["_root"].destroy()
    except Exception:
        pass


def title(a, s):
    a["_root"].title(str(s))


def resize(a, w, h):
    a["_root"].geometry(str(int(w)) + "x" + str(int(h)))


def on_close(a, handler):
    a["_root"].protocol("WM_DELETE_WINDOW", handler)


# ============================================================
# Menu bar
# ============================================================

def menubar(a):
    """Create a menu bar. Call menu() on the result to add menus."""
    m = tk.Menu(a["_root"])
    a["_root"].config(menu=m)
    return {"_widget": m, "_kind": "menubar", "_app": a}


def menu(bar, label):
    """Add a menu (File, Edit, ...) to the menu bar. Returns the menu dict
    that menu_item() should be called on."""
    m = tk.Menu(bar["_widget"], tearoff=0)
    bar["_widget"].add_cascade(label=str(label), menu=m)
    return {"_widget": m, "_kind": "menu"}


def menu_item(m, label, handler, accelerator=""):
    """Add a clickable item to a menu. `accelerator` is just the displayed
    shortcut text — actual key bindings still go through bind_key()."""
    def cb():
        try:
            handler()
        except Exception as e:
            print("menu item error:", e)
    if accelerator:
        m["_widget"].add_command(label=str(label), command=cb,
                                  accelerator=str(accelerator))
    else:
        m["_widget"].add_command(label=str(label), command=cb)


def menu_separator(m):
    m["_widget"].add_separator()


def menu_check(m, label, var_holder, handler):
    """Checkbox menu item. var_holder is a dict {"v": bool}."""
    if "v" not in var_holder:
        var_holder["v"] = tk.BooleanVar(value=False)
    def cb():
        try:
            handler(bool(var_holder["v"].get()))
        except Exception as e:
            print("menu check error:", e)
    m["_widget"].add_checkbutton(label=str(label),
                                  variable=var_holder["v"], command=cb)


def menu_radio(m, label, value, var_holder, handler):
    """Radio menu item. Multiple radio items in the same menu share a
    var_holder dict."""
    if "v" not in var_holder:
        var_holder["v"] = tk.StringVar(value=str(value))
    def cb():
        try:
            handler(str(var_holder["v"].get()))
        except Exception as e:
            print("menu radio error:", e)
    m["_widget"].add_radiobutton(label=str(label), value=str(value),
                                  variable=var_holder["v"], command=cb)


# ============================================================
# Layout containers
# ============================================================

def row(parent, padx=8, pady=4, fill="x"):
    frame = tk.Frame(_parent_widget(parent))
    frame.pack(fill=fill, padx=int(padx), pady=int(pady))
    return {"_widget": frame, "_kind": "row"}


def col(parent, padx=8, pady=4, expand=True):
    frame = tk.Frame(_parent_widget(parent))
    frame.pack(fill="both" if expand else "x", expand=bool(expand),
               padx=int(padx), pady=int(pady))
    return {"_widget": frame, "_kind": "col"}


def pane(parent, orient="horizontal"):
    """Split pane. orient is "horizontal" (side by side) or
    "vertical" (top/bottom). Add children with pane_add()."""
    paned = tk.PanedWindow(_parent_widget(parent),
                            orient=str(orient),
                            sashwidth=6, sashrelief="flat", bd=0)
    paned.pack(fill="both", expand=True, padx=4, pady=4)
    return {"_widget": paned, "_kind": "pane", "_orient": str(orient)}


def pane_add(pane, container, weight=1):
    """Add a container (row, col, text_area, ...) to a pane."""
    pane["_widget"].add(container["_widget"], stretch="always",
                          minsize=60)


def sidebar(parent, width=220):
    """Fixed-width container for a sidebar. Place it with pack(side='left')
    from the caller's perspective — or use it as a child of a horizontal
    pane."""
    frame = tk.Frame(_parent_widget(parent), width=int(width))
    frame.pack(side="left", fill="y", padx=4, pady=4)
    frame.pack_propagate(False)
    return {"_widget": frame, "_kind": "sidebar", "_width": int(width)}


def spacer(parent, px=8):
    f = tk.Frame(_parent_widget(parent), height=int(px))
    f.pack(fill="x")
    return {"_widget": f, "_kind": "spacer"}


def separator(parent):
    f = ttk.Separator(_parent_widget(parent), orient="horizontal")
    f.pack(fill="x", padx=8, pady=8)
    return {"_widget": f, "_kind": "separator"}


# ============================================================
# Widgets
# ============================================================

def label(parent, text="", anchor="w", fill="x", padx=8, pady=2):
    w = tk.Label(_parent_widget(parent), text=str(text), anchor=str(anchor))
    w.pack(fill=str(fill), padx=int(padx), pady=int(pady))
    return {"_widget": w, "_kind": "label"}


def button(parent, text, on_click=None, side=None, padx=2, pady=2):
    def cb():
        try:
            if on_click is not None:
                on_click()
        except Exception as e:
            print("button error:", e)
    w = tk.Button(_parent_widget(parent), text=str(text), command=cb)
    if side:
        w.pack(side=str(side), padx=int(padx), pady=int(pady))
    else:
        w.pack(fill="x", padx=int(padx), pady=int(pady))
    return {"_widget": w, "_kind": "button"}


def entry(parent, placeholder=""):
    w = tk.Entry(_parent_widget(parent))
    if placeholder:
        w.insert(0, str(placeholder))
    w.pack(fill="x", padx=8, pady=2)
    return {"_widget": w, "_kind": "entry"}


def text_area(parent, height=10):
    w = tk.Text(_parent_widget(parent), height=int(height))
    w.pack(fill="both", expand=True, padx=8, pady=2)
    return {"_widget": w, "_kind": "text"}


def text_area_scrolled(parent):
    """Text area with a vertical scrollbar."""
    frame = tk.Frame(_parent_widget(parent))
    frame.pack(fill="both", expand=True, padx=8, pady=2)
    w = tk.Text(frame)
    sb = ttk.Scrollbar(frame, orient="vertical", command=w.yview)
    w.configure(yscrollcommand=sb.set)
    w.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return {"_widget": w, "_kind": "text", "_frame": frame, "_scroll": sb}


def checkbox(parent, text, on_change=None):
    var = tk.BooleanVar()
    def cb():
        try:
            if on_change is not None:
                on_change(bool(var.get()))
        except Exception as e:
            print("checkbox error:", e)
    w = tk.Checkbutton(_parent_widget(parent), text=str(text),
                        variable=var, command=cb)
    w.pack(anchor="w", padx=8, pady=2)
    return {"_widget": w, "_var": var, "_kind": "checkbox"}


def radio_group(parent, options, on_change=None):
    var = tk.StringVar()
    if options:
        var.set(str(options[0]))
    frame = tk.Frame(_parent_widget(parent))
    frame.pack(fill="x", padx=8, pady=2)
    widgets = []
    for opt in options:
        def cb(v=opt):
            try:
                if on_change is not None:
                    on_change(str(v))
            except Exception as e:
                print("radio error:", e)
        r = tk.Radiobutton(frame, text=str(opt), value=str(opt),
                            variable=var, command=cb)
        r.pack(side="left", padx=4)
        widgets.append(r)
    return {"_widget": frame, "_var": var, "_kind": "radio", "_items": widgets}


def dropdown(parent, options, on_change=None):
    var = tk.StringVar()
    if options:
        var.set(str(options[0]))
    def cb(*_):
        try:
            if on_change is not None:
                on_change(str(var.get()))
        except Exception as e:
            print("dropdown error:", e)
    w = ttk.Combobox(_parent_widget(parent), textvariable=var,
                      values=[str(o) for o in options], state="readonly")
    w.bind("<<ComboboxSelected>>", cb)
    w.pack(fill="x", padx=8, pady=2)
    return {"_widget": w, "_var": var, "_kind": "dropdown"}


def slider(parent, lo=0, hi=100, init=50, on_change=None):
    var = tk.DoubleVar(value=float(init))
    def cb(*_):
        try:
            if on_change is not None:
                on_change(float(var.get()))
        except Exception as e:
            print("slider error:", e)
    w = tk.Scale(_parent_widget(parent), from_=float(lo), to=float(hi),
                  orient="horizontal", variable=var, command=cb)
    w.pack(fill="x", padx=8, pady=2)
    return {"_widget": w, "_var": var, "_kind": "slider"}


def progress(parent):
    w = ttk.Progressbar(_parent_widget(parent), mode="determinate", maximum=100)
    w.pack(fill="x", padx=8, pady=2)
    return {"_widget": w, "_kind": "progress"}


def listbox(parent, items=None, on_select=None, height=8):
    frame = tk.Frame(_parent_widget(parent))
    frame.pack(fill="both", expand=True, padx=8, pady=2)
    w = tk.Listbox(frame, height=int(height))
    if items:
        for i in items:
            w.insert("end", str(i))
    if on_select is not None:
        def cb(*_):
            sel = w.curselection()
            if sel:
                try:
                    on_select(int(sel[0]), str(w.get(sel[0])))
                except Exception as e:
                    print("listbox select error:", e)
        w.bind("<<ListboxSelect>>", cb)
    sb = ttk.Scrollbar(frame, orient="vertical", command=w.yview)
    w.configure(yscrollcommand=sb.set)
    w.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return {"_widget": w, "_kind": "listbox"}


def table(parent, columns, rows=None):
    frame = tk.Frame(_parent_widget(parent))
    frame.pack(fill="both", expand=True, padx=8, pady=2)
    tree = ttk.Treeview(frame, columns=[str(c) for c in columns],
                          show="headings", height=12)
    for c in columns:
        tree.heading(str(c), text=str(c))
        tree.column(str(c), width=120, anchor="w")
    if rows:
        for r in rows:
            tree.insert("", "end", values=[str(x) for x in r])
    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return {"_widget": tree, "_kind": "table"}


# ============================================================
# Reads / writes
# ============================================================

def get_text(widget):
    k = widget.get("_kind")
    w = widget["_widget"]
    if k == "entry":
        return w.get()
    if k == "text":
        return w.get("1.0", "end-1c")
    if k in ("label", "button"):
        return w.cget("text")
    return ""


def set_text(widget, s):
    k = widget.get("_kind")
    w = widget["_widget"]
    t = str(s)
    if k in ("label", "button"):
        w.config(text=t)
    elif k == "entry":
        w.delete(0, "end")
        w.insert(0, t)
    elif k == "text":
        w.delete("1.0", "end")
        w.insert("1.0", t)


def is_checked(widget):
    return bool(widget["_var"].get()) if widget.get("_kind") == "checkbox" else False


def set_checked(widget, v):
    if widget.get("_kind") == "checkbox":
        widget["_var"].set(bool(v))


def radio_value(widget):
    return str(widget["_var"].get()) if widget.get("_kind") == "radio" else ""


def dropdown_value(widget):
    return str(widget["_var"].get()) if widget.get("_kind") == "dropdown" else ""


def set_dropdown(widget, v):
    if widget.get("_kind") == "dropdown":
        widget["_var"].set(str(v))


def slider_value(widget):
    return float(widget["_var"].get()) if widget.get("_kind") == "slider" else 0.0


def set_slider(widget, v):
    if widget.get("_kind") == "slider":
        widget["_var"].set(float(v))


def progress_set(widget, pct):
    if widget.get("_kind") == "progress":
        widget["_widget"]["value"] = float(pct)


def listbox_add(widget, s):
    if widget.get("_kind") == "listbox":
        widget["_widget"].insert("end", str(s))


def listbox_clear(widget):
    if widget.get("_kind") == "listbox":
        widget["_widget"].delete(0, "end")


def listbox_items(widget):
    if widget.get("_kind") != "listbox":
        return []
    lb = widget["_widget"]
    return [lb.get(i) for i in range(lb.size())]


def listbox_selected(widget):
    if widget.get("_kind") != "listbox":
        return None
    lb = widget["_widget"]
    sel = lb.curselection()
    return lb.get(sel[0]) if sel else None


def table_add(widget, r):
    if widget.get("_kind") == "table":
        widget["_widget"].insert("", "end", values=[str(x) for x in r])


def table_clear(widget):
    if widget.get("_kind") == "table":
        w = widget["_widget"]
        for item in w.get_children():
            w.delete(item)


def table_rows(widget):
    if widget.get("_kind") != "table":
        return []
    w = widget["_widget"]
    return [list(w.item(i, "values")) for i in w.get_children()]


# ============================================================
# Dialogs
# ============================================================

def alert(parent, text, title="Info"):
    messagebox.showinfo(str(title), str(text))


def confirm(parent, text, title="Confirm"):
    return bool(messagebox.askyesno(str(title), str(text)))


def error(parent, text, title="Error"):
    messagebox.showerror(str(title), str(text))


def prompt(parent, text, title="Input"):
    return messagebox.askstring(str(title), str(text))


def open_file(parent, title="Open", filters=None):
    return filedialog.askopenfilename(
        title=str(title),
        filetypes=filters or [("All files", "*.*")]) or None


def save_file(parent, title="Save", filters=None, default_ext=""):
    return filedialog.asksaveasfilename(
        title=str(title),
        filetypes=filters or [("All files", "*.*")],
        defaultextension=str(default_ext)) or None


def open_folder(parent, title="Open folder"):
    return filedialog.askdirectory(title=str(title)) or None


# ============================================================
# Events
# ============================================================

def bind_key(a, key, handler):
    a["_root"].bind(str(key), lambda e: handler())


def after(a, ms, handler):
    def cb():
        try:
            handler()
        except Exception as e:
            print("after error:", e)
    a["_root"].after(int(ms), cb)


def focus(widget):
    try:
        widget["_widget"].focus_set()
    except Exception:
        pass


def destroy(widget):
    try:
        widget["_widget"].destroy()
    except Exception:
        pass

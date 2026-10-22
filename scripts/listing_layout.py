"""Reflow printed Markdown listings without changing their word sequence.

The paper's 9 pt monospace face fits about 72 characters per line. Keep a
small safety margin and balance short paragraph tails before TeX wraps them.
"""
import re
import textwrap


def wrap_paragraph(text, width=70):
    indent = re.match(r" *", text)[0]
    words = text.split()
    if not words:
        return ""
    continuation = indent + ("  " if words[0] in {"*", "-"} else "")
    lines = textwrap.wrap(" ".join(words), width=width,
                          initial_indent=indent, subsequent_indent=continuation,
                          break_long_words=False, break_on_hyphens=False)
    # Do not leave one or two words dangling after a full line of prose.
    if len(lines) > 1:
        tail = lines[-1].split()
        previous = lines[-2].split()
        while (len(tail) < 3 or len(" ".join(tail)) < 18) and len(previous) > 3:
            tail.insert(0, previous.pop())
        lines[-2] = (indent if len(lines) == 2 else continuation) + " ".join(previous)
        lines[-1] = continuation + " ".join(tail)
    return "\n".join(lines)


def reflow_listing(body, width=70):
    result, pending = [], []

    def flush():
        if pending:
            result.append(wrap_paragraph(" ".join(pending), width))
            pending.clear()

    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
            result.append("")
        elif stripped.startswith(("#", "|", "steward ")):
            flush()
            if stripped.startswith("steward ") and "   #" in line:
                command, comment = line.split("   #", 1)
                result.extend([command.rstrip(), "    #" + comment])
            else:
                result.append(wrap_paragraph(line, width))
        elif stripped.startswith(("* ", "- ", "[reply", "[refusal", "[50-row",
                                  "[no network", "steps[]:", '"method_id',
                                  "Hard constraints:", "The provision ceiling")):
            flush()
            pending.append(line)
        else:
            pending.append(line if not pending else stripped)
    flush()
    output = "\n".join(result).strip("\n") + "\n"
    assert body.split() == output.split(), "Listing content changed"
    assert all(len(line) <= width for line in output.splitlines()), "Overlong listing line"
    return output


def reflow_latex_listings(source):
    return re.sub(r"(\\begin\{lstlisting\}[^\n]*\n)(.*?)(\\end\{lstlisting\})",
                  lambda m: m[1] + reflow_listing(m[2]) + m[3], source, flags=re.S)

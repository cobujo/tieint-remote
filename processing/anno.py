import re
# from sql import session_scope, engine_named, safe_check_dot_db
# from sql.models import AcDbMTextBase

# def test_mtext():
#     db_name = safe_check_dot_db('SNX406.db')
#     with session_scope(engine_named(db_name)) as ss:
#         texts = []
#         res = ss.query(AcDbMTextBase).all()
#
#         for r in res:
#             texts.append(r.text_string)
#
#     new_texts = [make_mtext_readable(t) for t in texts]
#
#     return [texts, new_texts]


def make_mtext_readable(string: str, add_newlines=True) -> str:
    newline_sub = r'\n' if add_newlines else r' '
    patterns_and_subs = [
        (r'(\\p\w.+?;)', ''),  # ?? not sure if this is a style or whitespace, but structure roughly is: \pxx-#,l#;CONTENT IS HERE
        (r'({\\.+?;|})', ''),  # styles(?), structure is: {\CONTENT IS HERE;}
        (r'({\\L)', ''),  # underline style (start of string/style only), structure is: {\LCONTENT HERE}
        (r'(\\.+?;)', ''),  # title styles, structure is: \A#; CONTENT HERE
        (r'(\\P)', newline_sub),  # newlines, structure is: \P
        (r'(%%C)', '⌀')  # diameter symbol
    ]

    for pattern, sub in patterns_and_subs:
        string = re.sub(pattern, sub, string)

    return string

"""Claim under audit, not a verified fact: the caller says the session is already authenticated.

Three read paths over documents from two tenants. The contract exposes `text` only.
"""
DOCS = {'a1': {'tenant': 'A', 'text': 'A synthetic', 'internal_note': 'A synthetic note'},
        'b1': {'tenant': 'B', 'text': 'B synthetic', 'internal_note': 'B synthetic note'}}

def unsafe_get(session, doc_id):
    if not session:
        raise PermissionError()
    return DOCS[doc_id]

def leaky_get(session, doc_id):
    """Compares tenants, yet distinguishes absent from forbidden and hands back shared state."""
    if not session:
        raise PermissionError()
    doc = DOCS[doc_id]
    if doc['tenant'] != session['tenant']:
        raise PermissionError()
    return doc

def safe_get(session, doc_id):
    if not session:
        raise PermissionError()
    doc = DOCS.get(doc_id)
    if doc is None or doc['tenant'] != session['tenant']:
        raise PermissionError()
    return {'text': doc['text']}

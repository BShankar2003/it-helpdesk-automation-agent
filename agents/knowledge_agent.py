# agents/knowledge_agent.py
import json, os

KB_PATH = "data/kb.json"

def search_kb(query, top_k=3):
    """
    Very simple KB search: substring match on title or steps.
    """
    try:
        with open(KB_PATH,"r") as f:
            kb = json.load(f)
    except Exception:
        return []
    q = query.lower()
    hits = []
    for item in kb:
        text = (item.get("title","") + " " + " ".join(item.get("steps",[]))).lower()
        if q in text or any(word in text for word in q.split()):
            hits.append(item)
    # return top_k results
    return hits[:top_k]

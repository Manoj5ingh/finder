import threading

from .gmail_search import GmailSearch
# from .slack_search import SlackSearch
import asyncio

SEARCH_CLASSES = {
    'gmail': GmailSearch,
    # 'slack': SlackSearch,
}


def perform_search(method_class, user_id, search_text, results):
    instance = SEARCH_CLASSES.get(method_class)()
    method = getattr(instance, "search", None)
    results.append({method_class: method(user_id, search_text)})


# def perform_parallel_searches(user_id, search_text, methods):
#     tasks = []
#     for method in methods:
#         search_method = SEARCH_METHODS.get(method)
#         if search_method:
#             searcher = search_method()
#             task = perform_search(searcher, user_id, search_text)
#             tasks.append(task)
#
#     results = await asyncio.gather(*tasks)
#     return results

def search_text(user_id, search_text, methods):
    threads = []
    results = []
    for method in methods:
        threads.append(threading.Thread(target=perform_search, args=(method, user_id, search_text, results)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results

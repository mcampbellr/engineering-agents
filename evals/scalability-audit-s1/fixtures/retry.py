"""Three attempts total at each of three layers; no real network requests."""
def leaf(counter):
    counter[0] += 1
    raise TimeoutError('synthetic dependency unavailable')

def retry(call, attempts=3):
    for _ in range(attempts):
        try:
            return call()
        except TimeoutError:
            pass
    raise TimeoutError('attempt budget exhausted')

def layered(counter):
    return retry(lambda: retry(lambda: retry(lambda: leaf(counter))))

def single_owner(counter):
    return retry(lambda: leaf(counter))

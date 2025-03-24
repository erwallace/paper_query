import random
import string


def random_string(n=6):
    """Generate a random string of fixed length, n."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for i in range(n))

def pytoken():
    import random, string
    generate_random_string = lambda length: ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
    if __name__ == "__main__": print(generate_random_string(3920))

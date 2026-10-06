"""Display the canonical data without overwriting it."""
from data import load_data

if __name__ == "__main__":
    print(load_data().to_string(index=False))

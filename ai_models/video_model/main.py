# main.py

import sys

from sympy import im
from ai_models.video_model import train
from ai_models.video_model import test_video
def show_menu():
    print("\n========== AI Face Detection System ==========")
    print("1. Train Model")
    print("2. Test Video / Run Detection")
    print("3. Exit")
    print("==============================================")

def train_model():
    try:
        print("\n[INFO] Starting training...")
        from ai_models.video_model import train
        train.main()
    except Exception as e:
        print(f"[ERROR] Training failed: {e}")

def test_model():
    try:
        print("\n[INFO] Running face detection...")
        from ai_models.video_model import test_video
        test_video.main()
    except Exception as e:
        print(f"[ERROR] Testing failed: {e}")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            train_model()
        elif choice == "2":
            test_model()
        elif choice == "3":
            print("\n[INFO] Exiting program. Goodbye!")
            sys.exit()
        else:
            print("[WARNING] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
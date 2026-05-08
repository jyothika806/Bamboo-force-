import os
import torch
import numpy as np
from dataset import load_video_fast
from model import VideoModel
def main():
    device = torch.device("cpu")

    X = []
    y = []

    base_path =  os.path.join(os.path.dirname(__file__), "dataset")

    print("[INFO] Loading dataset...")

    for label, folder in [(1, "real"), (0, "spoof")]:
        path = os.path.join(base_path, folder)

        for file in os.listdir(path):
            if file.endswith(".mp4"):
                video = load_video_fast(os.path.join(path, file))
                X.append(video)
                y.append(label)

    print("[INFO] Dataset loaded")

    X = torch.tensor(np.array(X)).float().permute(0,1,4,2,3)
    y = torch.tensor(y)

    print(f"[INFO] Data shape: {X.shape}")

    # Initialize model
    model = VideoModel().to(device)

    # Example loss & optimizer
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    print("[INFO] Starting training...")

    # Simple training loop
    for epoch in range(5):
        optimizer.zero_grad()

        outputs = model(X)
        loss = criterion(outputs, y)

        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

    # Save model
    torch.save(model.state_dict(), "video_liveness_model.pth")
    print("[INFO] Model saved!")


if __name__ == "__main__":
    main()

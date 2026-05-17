import torch
import torch.nn as nn


class RideRiskAutoEncoder(nn.Module):

    def __init__(self, input_dim):

        super().__init__()

        # ============================================
        # ENCODER
        # ============================================

        self.encoder = nn.Sequential(

            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),

            nn.Linear(64, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 8)
        )

        # ============================================
        # DECODER
        # ============================================

        self.decoder = nn.Sequential(

            nn.Linear(8, 16),
            nn.ReLU(),

            nn.Linear(16, 32),
            nn.ReLU(),

            nn.Linear(32, 64),
            nn.ReLU(),

            nn.Linear(64, input_dim)
        )

    # ============================================
    # FORWARD PASS
    # ============================================

    def forward(self, x):

        encoded = self.encoder(x)

        decoded = self.decoder(encoded)

        return decoded
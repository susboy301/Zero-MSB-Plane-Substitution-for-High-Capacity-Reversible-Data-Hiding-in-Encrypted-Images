class ResidualBlock:
    def __init__(self, bid, residuals):
        self.id = bid
        self.residuals = residuals
        self.class_id = None

        # --- BPZS metadata ---
        self.zero_planes = 0   # implicit mode

        # --- storage ---
        self.slack = 0
        self.compressed = {
            "plane_bits": [],
            "residual_bits": []
        }

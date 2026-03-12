# Reversible Data Hiding (RDH) Project

This project implements a Reversible Data Hiding (RDH) algorithm in Encrypted Images (RDH-EI). It allows embedding a payload into an encrypted image and perfectly recovering the original image upon decryption, while also extracting the payload error-free.

## 📂 Project Structure

- **`main.py`**: The entry point of the application. Orchestrates the entire pipeline: reading images, computing residuals, encryption, embedding, extraction, and recovery.
- **`core/`**: Contains core algorithms for image processing.
  - `residuals.py`: Implementation of the LOCO-I (JPEG-LS) predictor for computing and recovering residuals.
  - `block.py`: Definition of the `ResidualBlock` class to manage block-level data.
  - `classify.py`: Logic to classify blocks based on entropy/complexity.
  - `compress.py`: Hybrid compression logic using Bit-Plane Zero-Run (BPZS) for smooth blocks and simplified coding for textured blocks.
- **`embed/`**: Functions for embedding data.
  - `embed_aux.py`: Embeds auxiliary information (compressed residuals) into the encrypted image.
  - `embed_payload.py`: Embeds user payload into the remaining capacity of the image.
- **`recover/`**: Functions for data extraction.
  - `extract_aux.py`: Extracts auxiliary information.
  - `extract_payload.py`: Extracts the embedded user payload.
- **`utils/`**: Utility functions.
  - `EncryptionImg.py`: Simulates image encryption using XOR with a stream cipher.
  - `psnr.py`: Calculates Peak Signal-to-Noise Ratio (PSNR) to measure image quality.
  - `dec_to_bin.py` / `bin_to_dec.py`: Helpers for binary conversion.
- **`analysis/`**: Security and quality analysis metrics.
  - `psnr.py` / `mae.py`: Visual quality metrics (Peak Signal-to-Noise Ratio, Mean Absolute Error).
  - `entropy.py`: Shannon entropy calculation.
  - `correlation.py`: Analysis of adjacent pixel correlation (Diagonal/Horizontal/Vertical).
  - `npcr_uaci.py`: Differential attack resistance metrics (NPCR, UACI).
  - `chi_square.py`: Statistical attack analysis.

## 🗺️ Roadmap & Algorithm Flow

The process consists of several distinct phases designed to ensure reversibility and high payload capacity.

### Phase 1: Residual Analysis (Pre-processing)
Before encryption, the image is analyzed to create a "map" that allows for later recovery.
1.  **Prediction (LOCO-I)**: For every pixel, a prediction is made using its neighbors (Left, Up, Up-Left).
2.  **Residual Calculation**: The difference (`Residual = Image - Prediction`) is computed. This decorrelates the image data, making it easier to compress.

### Phase 1.1: Block Compression
The residuals are compressed to create space for the payload.
1.  **Block Division**: The residual image is divided into non-overlapping blocks (e.g., 4x4).
2.  **Classification**: Blocks are analyzed (e.g., using entropy) to determine if they are "smooth" or "textured".
3.  **Hybrid Compression**:
    -   **Smooth Blocks**: Compressed using Bit-Plane Zero-Substitution (BPZS). Leading zero bit-planes are identified and skipped.
    -   **Textured Blocks**: Compressed using a fallback method (e.g., fixed-length coding of sign and magnitude).
4.  **Auxiliary Data Generation**: The compressed bitstream of the residuals is collected. This data is *Self-Embedded* later to enable reversibility.

### Phase 2: Image Encryption
The original image (not the residuals) is encrypted to protect privacy.
-   **Stream Cipher**: Properties of the image are masked by XORing with a pseudorandom key (stream cipher). This produces a noise-like encrypted image.

### Phase 2.1: Auxiliary Data Embedding
The compressed residuals (Auxiliary Data) need to be stored inside the encrypted image itself so the receiver can reconstruct the original image.
-   **Multi-Bitplane Embedding**: The auxiliary bits are embedded into the LSBs (Least Significant Bits) of the encrypted pixels.
-   The algorithm calculates the minimum number of bit-planes ($k$) required to store all auxiliary data.

### Phase 3: Payload Embedding
Once the auxiliary data is safely tucked away, the remaining space is used for the actual user payload.
-   **Capacity Calculation**: The system identifies pixels that were *not* fully utilized by the auxiliary data.
-   **Embedding**: The user's message (payload) is embedded into the LSBs of these spare pixels.
-   **Security**: A payload encryption key governs the random permutation of pixel locations used for embedding, adding an extra layer of security.

### Phase 4: Extraction & Recovery
The receiver performs these steps to retrieve data and restore the image.
1.  **Payload Extraction**: Using the payload key, the receiver extracts the user's message from the spare LSBs.
2.  **Auxiliary Extraction**: The auxiliary data (compressed residuals) is extracted from the reserved bit-planes.
3.  **Image Recovery**:
    -   The auxiliary data is decompressed to restore the Residuals.
    -   The LOCO-I predictor is re-run (using the same causal logic) to generate predictions.
    -   `Original = Prediction + Residual` is computed to perfectly reconstruct the original image.

## 🚀 Usage

1.  **Setup**: Ensure you have Python installed along with `numpy` and `opencv-python`.
    ```bash
    pip install numpy opencv-python
    ```
2.  **Configuration**: Open `main.py` and adjust parameters if needed:
    -   `DATASET_DIR`: Path to your image dataset.
    -   `MAX_PAYLOAD`: Maximum bits to embed.
3.  **Run**:
    ```bash
    python main.py
    ```
    The script will process images in the directory, reporting:
    -   Embedding Capacity (bpp)
    -   Payload Extraction success
    -   Perfect Reversibility check (Image == Recovered)

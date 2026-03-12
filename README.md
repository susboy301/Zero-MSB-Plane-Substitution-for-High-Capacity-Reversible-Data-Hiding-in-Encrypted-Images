# Zero MSB-Plane Substitution for High-Capacity RDHEI

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the official Python implementation of the paper **"Zero MSB-Plane Substitution for High-Capacity Reversible Data Hiding in Encrypted Images: A Block-Wise RRBE Scheme Without Rearrangement."** This project presents a novel Reversible Data Hiding in Encrypted Images (RDHEI) framework designed for secure cloud-based image storage. By exploiting the natural bit-plane sparsity of LOCO-I prediction residuals at the block level, this scheme achieves state-of-the-art embedding capacities without relying on computationally expensive block rearrangement, Huffman coding, or complex Map/Inf structures.

## 🚀 Key Features

* **High Capacity:** Achieves an average embedding rate of **4.67 bpp** on BOSSbase and **4.07 bpp** on BOWS-2, representing a 23.2% and 9.9% improvement over the nearest state-of-the-art comparator.
* **Lossless Reversibility:** Guarantees exact pixel-level image recovery ($\text{PSNR} = \infty$) upon decryption.
* **Lean Auxiliary Overhead:** Replaces complex metadata structures with a single, fixed 3-bit $z_k$ header per $4\times4$ tile.
* **Hybrid Block Encoding:** Intelligently switches between *plane-mode* for smooth tiles (vacating zero MSB-planes for payload) and *sign-magnitude mode* for textured tiles (ensuring exact recovery for high-energy content).
* **Strict Separability:** Implements a true three-party pipeline (Content Owner, Data Hider, Receiver) where payload extraction and image recovery operate under completely independent cryptographic keys ($K_d$ and $K_e$).

## ⚙️ System Architecture

The pipeline is divided into four strictly separable phases:
1. **Phase I (Content Owner):** Plaintext-domain LOCO-I residual computation, $4\times4$ block partitioning, zero MSB-plane analysis, and space reservation.
2. **Phase II (Encryption):** Image encryption via XOR with a CSPRNG keystream, followed by the secure embedding of the auxiliary bitstream into the LSBs.
3. **Phase III (Data Hider):** Ciphertext-domain payload embedding via pseudo-random LSB substitution using the data-hiding key ($K_d$).
4. **Phase IV (Receiver):** Independent payload extraction and lossless image reconstruction. 

## 📊 Experimental Results

Extensive evaluations were conducted across 20,000 benchmark images (10,000 BOSSbase, 10,000 BOWS-2).

| Dataset | Image Size | Mean Capacity (bpp) | Max Capacity (bpp) | PSNR | Extraction Success |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BOSSbase v1.01** | $512 \times 512$ | 4.673 | 7.890 | $\infty$ | 100.00% |
| **BOWS-2** | $256 \times 256$ | 4.068 | 7.289 | $\infty$ | 99.97% |

**Security Metrics:** The XOR-encrypted ciphertext demonstrates ideal statistical security, achieving a Shannon entropy of $\geq 7.997$ bits/pixel, adjacent-pixel correlation of $|r| < 0.015$, and NPCR $\approx 99.6\%$.

## 🛠️ Requirements & Setup

This project requires **Python 3.10+**. To set up the environment, clone the repository and install the required dependencies:

```bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
cd YOUR-REPO-NAME
pip install -r requirements.txt

# SECURITY UPGRADES — README
# ===========================
# 5 files upgraded.  Drop these into your project replacing the originals.
# ZERO capacity change.  All 10,000-image results remain valid.

FILES CHANGED
─────────────
1. EncryptionImg.py     (utils/)
2. embed_aux.py         (embed/)
3. extract_aux.py       (recover/)
4. embed_payload.py     (embed/)
5. extract_payload.py   (recover/)
6. main.py              (root)


WHAT EACH FILE CHANGED AND WHY
───────────────────────────────

1. EncryptionImg.py
   BEFORE: np.random.default_rng(123)  — small integer seed, NOT cryptographically secure
   AFTER:  SHA-256 normalises any int/bytes key to 32 bytes.
           If pycryptodome is installed → ChaCha20 stream cipher (IETF RFC 8439).
           If not installed → NumPy PCG64 fallback with warning.
   WHY:    Upgrades from "statistically secure" to "cryptographically secure".
           Reviewers cannot argue the keystream is recoverable with known-plaintext.
   INSTALL: pip install pycryptodome

2. embed_aux.py
   BEFORE: Writes aux bits in sequential raster order (pixel 0, 1, 2, ...).
           Aux bitstream is in plaintext.
   AFTER:  TWO upgrades:
     A) ENCRYPT aux bitstream: XOR each bit with a PRNG stream derived from key_aux.
        Aux content in the image is now random-looking, not readable.
     B) SCATTER aux pixel positions: use PRNG permutation to spread aux
        across the ENTIRE image, not concentrated at the front.
   RETURNS: (marked_enc, aux_k, aux_positions)  ← aux_positions is NEW
   WHY:    Closes both "unencrypted auxiliary" and "patch-removal" vulnerabilities.

3. extract_aux.py
   BEFORE: extract_aux(img, num_bits) — reads sequential pixels, no key needed.
   AFTER:  extract_aux(img, num_bits, key, k) — must provide key and k.
           Regenerates same scattered positions, reads them, XOR-decrypts.
   WHY:    Must mirror exactly what embed_aux now does.

4. embed_payload.py
   BEFORE: embed_payload(img, bits, start_pixel, key) — skips pixels < start_pixel.
   AFTER:  embed_payload(img, bits, start_pixel=None, key=999, aux_positions=None)
           When aux_positions is provided (recommended), excludes exactly those pixels.
           Falls back to start_pixel if aux_positions is None (backward compatible).
   WHY:    Since aux pixels are now scattered (not at the front), start_pixel
           no longer correctly identifies which pixels to skip.

5. extract_payload.py
   BEFORE: extract_payload(img, len, start_pixel, key) — skips pixels < start_pixel.
   AFTER:  Same signature upgrade as embed_payload. Accepts aux_positions.
   WHY:    Must mirror embed_payload exactly.

6. main.py
   CHANGES:
     a) key_img = 0xA3F1... (256-bit constant) instead of key_img = 123
     b) embed_aux(...) now returns 3 values — unpack aux_positions
     c) embed_payload/extract_payload now receive aux_positions=aux_positions
     d) extract_aux now called with key=key_aux, k=aux_k


HOW TO RUN
──────────
Optional (for ChaCha20 cipher):
    pip install pycryptodome

Then run as before:
    python main.py

Output format is identical — same CSV columns, same image outputs.


VERIFICATION
────────────
After running, verify:
  1. extraction_success column should still be True for all images
  2. capacity_bpp should be IDENTICAL to before (no capacity change)
  3. entropy_enc should still be ~7.999 (histogram is still uniform)
  4. psnr should still be inf (perfect recovery unchanged)


SECURITY PROPERTIES AFTER UPGRADE
───────────────────────────────────
  ✓ Brute-force resistance:     256-bit key space (up from 32-bit int)
  ✓ Statistical indistinguish:  Histogram still uniform (XOR of uniform)
  ✓ Auxiliary encrypted:        z_k headers and compressed bits are ciphertext
  ✓ Patch-removal resistance:   Aux scattered across full image (like payload)
  ✓ Separability:               image recovery and payload extraction still independent
  ✓ Perfect reversibility:      PSNR = ∞ unchanged


BACKWARD COMPATIBILITY
──────────────────────
  extract_aux_legacy(img, num_bits) is available if you have old code
  that calls the 2-argument form. It prints a DeprecationWarning.

  embed_payload and extract_payload still accept start_pixel as a
  fallback if aux_positions is None.

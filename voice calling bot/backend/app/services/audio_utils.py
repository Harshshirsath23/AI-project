import math
import struct
import base64
from typing import Tuple

# Pre-computed G.711 mu-law lookup tables for 8-bit mu-law to 16-bit PCM conversion
MULAW_TO_PCM16 = []
for i in range(256):
    mu = ~i & 0xFF
    sign = (mu & 0x80)
    exponent = (mu >> 4) & 0x07
    mantissa = mu & 0x0F
    sample = ((mantissa << 3) + 0x84) << exponent
    sample -= 0x84
    if sign:
        sample = -sample
    MULAW_TO_PCM16.append(max(-32768, min(32767, sample)))

def mulaw_to_pcm16(mulaw_bytes: bytes) -> bytes:
    """Decodes 8kHz 8-bit mu-law audio to 16-bit signed PCM LE audio bytes."""
    samples = [MULAW_TO_PCM16[b] for b in mulaw_bytes]
    return struct.pack(f"<{len(samples)}h", *samples)

def pcm16_to_mulaw(pcm_bytes: bytes) -> bytes:
    """Encodes 16-bit signed PCM LE audio bytes to 8kHz 8-bit mu-law bytes."""
    samples = struct.unpack(f"<{len(pcm_bytes) // 2}h", pcm_bytes[:(len(pcm_bytes) // 2) * 2])
    mulaw = bytearray()
    for s in samples:
        sign = 0x80 if s < 0 else 0x00
        s = abs(s)
        s = min(32767, s + 0x84)
        exponent = 7
        for exp in range(7):
            if s < (2 ** (exp + 5)):
                exponent = exp
                break
        mantissa = (s >> (exponent + 3)) & 0x0F
        byte = ~(sign | (exponent << 4) | mantissa) & 0xFF
        mulaw.append(byte)
    return bytes(mulaw)

def calculate_audio_energy(mulaw_bytes: bytes) -> float:
    """
    Calculates Root-Mean-Square (RMS) audio energy level from mu-law audio bytes.
    Used for Voice Activity Detection (VAD) and barge-in detection.
    """
    if not mulaw_bytes:
        return 0.0
    pcm_samples = [MULAW_TO_PCM16[b] for b in mulaw_bytes]
    sum_squares = sum(sample * sample for sample in pcm_samples)
    rms = math.sqrt(sum_squares / len(pcm_samples))
    return rms

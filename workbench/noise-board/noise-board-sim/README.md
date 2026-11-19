# Noise Board Simulator

A standalone **classical pseudorandom** noise board simulation, written in
Python standard library only. Self-contained in `/tmp/noise-board-sim`.

## Important — what this is and is not

- **IS** a pseudorandom software simulation using Python's `random.Random`
  (Mersenne Twister).
- **IS NOT** a hardware noise generator.
- **IS NOT** a source of quantum entropy.
- **IS NOT** cryptographically secure.
- **IS NOT** calibrated against any physical device.
- **IS NOT** connected to 004c, Time Loom, CUP, GitHub, or any other
  repository or experiment. No results produced here are experimental,
  quantum-hardware, or 004c results.

## Files

| File | Purpose |
|---|---|
| `DESIGN_NOTE.md` | Short design note, sources, two-channel scheme, limitations. |
| `noise_board.py` | Runnable simulator (CLI). |
| `test_noise_board.py` | Automated tests (criteria stated up-front in the module docstring). |
| `README.md` | This file. |

## Requirements

- Python 3.9+ (uses `statistics.fmean`, available since 3.8).
- No third-party packages.
- No network access required.

## Quick start

```sh
cd /tmp/noise-board-sim

# 1. Single-channel white noise, seed=42, 10 samples
python3 noise_board.py --seed 42 --source white --samples 10 \
    --mu 0 --sigma 1

# 2. Two-channel white noise with target correlation 0.5
python3 noise_board.py --seed 42 --source white --samples 1000 \
    --two-channel --correlation 0.5 \
    --mu 0 --sigma 1

# 3. Telegraph noise
python3 noise_board.py --seed 7 --source telegraph --samples 20 \
    --amplitude 1.0 --switch-prob 0.2

# 4. Burst noise
python3 noise_board.py --seed 7 --source burst --samples 200 \
    --p-burst 0.05 --burst-len 10 --burst-sigma 2.0
```

## Running the tests

```sh
cd /tmp/noise-board-sim
python3 -m unittest test_noise_board -v
```

Or directly:

```sh
python3 test_noise_board.py
```

The test module docstring states every criterion before any test runs.

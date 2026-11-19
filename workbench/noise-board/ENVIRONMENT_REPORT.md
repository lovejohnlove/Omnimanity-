# Environment Report — Noise Board Workbench

## Status

This report documents the execution environment that hosted the noise board
workbench work. It is a **classical synthetic software model** environment
report — **not physical validation**, **not quantum**, **not 004c**.

Tests were run and commits were made in prior turns within this same
environment. This specific report was produced as a read-only snapshot; no
tests were run and no commits were made during the snapshot turn itself.

## Measured facts

All values measured with read-only commands. No secrets inspected.
Host-specific identifiers, private machine paths, and infrastructure
fingerprints have been removed.

| Item | Value |
|---|---|
| OS family | Debian GNU/Linux 13 (trixie) |
| Kernel major version | Linux 5.10.x x86_64 SMP |
| Architecture | x86_64 |
| CPU model | Intel Xeon (family 6, model 173) |
| vCPU count | 2 (2 cores, 1 thread/core, 1 socket) |
| Virtualization | KVM, full virtualization |
| RAM total | 3.9 GiB |
| RAM available | 3.4 GiB |
| Swap | 0 B (none) |
| Disk total | 9.9 GiB |
| Disk available | 8.0 GiB (15% used) |
| Python | 3.12.16 |
| Git | 2.47.3 |

## Workspace classification

Linux container inside a KVM-hosted VM. Not a local machine. Not a bare VM.

The container shares the host kernel. The hypervisor is KVM with full
virtualization.

## Persistence of the working directory

**Partially measured, not guaranteed.**

- Measured: the persistent working directory survived across at least one
  inter-message recycling event with identical SHA-256 hashes.
- Counter-evidence: in an earlier turn, a user-created `scripts/`
  subdirectory under the persistent working directory was found missing
  after a recycling event. The specific recycling event that removed it
  is not further identified; the location is established (a `scripts/`
  subdirectory under the persistent working directory), but the timing
  and cause of its removal are unresolved.
- The environment note says the working directory is kept, but at least
  one recycling event in this conversation removed a user-created
  subdirectory.

## Untested / not measured

- CPU governor (cpufreq not exposed in container).
- Cloud provider / instance type.
- Whether the underlying KVM VM is dedicated.
- Network egress policy.
- Git push credentials (confirmed absent: no SSH keys, no credential
  helper, no GitHub CLI, no browser session, no `.netrc`).

## What was not done (in the snapshot turn only)

- No secrets inspected.
- No credentials stored or transmitted.
- No files changed.
- No tests run.
- No commits made.

(Prior turns in this same environment did run tests and make commits; those
results are recorded in the per-project REPORT.md files and in
WORKBENCH_REPORT.md.)

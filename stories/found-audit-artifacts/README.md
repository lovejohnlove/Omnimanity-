# Recovered V5 Audit Snapshots

This folder preserves two raw Google Drive “PLAIN” files labeled V5. They are useful for comparing revisions and trying local consistency checks, but they are not a sealed test package, canonical specification, or empirical result. The V5 labels identify the source snapshots; they do not prove original provenance or canonical status.

The raw bytes of both scripts were independently SHA-256 hashed and match the values in the Drive V5 expected-hash record. A matching hash confirms byte identity to that recorded value, not who authored the code, whether it is the intended canonical version, or whether an empirical claim is true. See [`FILES.md`](FILES.md) for exact source titles, purposes, sizes, and full hashes.

The audit helper compares two supplied numeric series within a tolerance and can compare their ranges. Its built-in example passes identical synthetic lists, so its `VERIFIED` output applies only to those inputs. The preregistration helper applies a three-boolean decision rule and demonstrates it with generated regression data; it is not the original 7,895-byte preregistration harness.

The original 11,127-byte Session A harness, the original 7,895-byte preregistration harness, and the paired alpha series were not recovered as raw files in this search. No empirical dual-anchor result is claimed here. Other found files with disputed version status are intentionally left out of this first bundle.

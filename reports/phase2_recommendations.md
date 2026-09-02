# Phase 2 Recommendations

## Data Cleaning
- Standardize all timestamps to UTC/ISO format.
- Handle any NULL values identified in the profiling step.

## Feature Engineering
- Convert categorical identifiers (like user, pc) into categorical integer codes.
- Extract hour of day and day of week from timestamps.

## Graph Generation
- `user` and `pc` are strong node candidates.
- Edges should be generated based on event co-occurrences.

# MovieRatingSystem-PythonDSA
An algorithmic tracking system that catalogs titles by numerical rating thresholds using a self-balancing AVL Tree structure.

This implementation pairs structural height-balanced tree nodes with a fast direct-lookup index map. This architectural choice ensuresthat record evictions can be initiated by a text-based item name while strictly maintaining a logarithmic O(log n) time boundary for balance restorations.

## Core Features
### Strict Balance Management
- Dynamically enforces tree balancing protocols via systematic rotations (left, right, left-right, right-left) to keep maximum structural lookup depths confined strictly to \(O(\log n)\) boundaries.

### Deterministic Tie-Breaking
- Avoids tree node overwrite collisions by implementing composite tree keys. If multiple films carry identical integer ratings, alphabetical naming logic safely sorts the corresponding branches.

### O(1) Direct-Name Dereferencing
- Features a separate memory map that associates strings directly with their rating slots, letting you pinpoint and evict elements instantly without triggering an O(n) structural scan across the tree.

### Sub-Tree Range Isolation
- Performs highly efficient, bounded in-order traversals that retrieve matching entries within defined upper and lower target boundaries without reading irrelevant branches.

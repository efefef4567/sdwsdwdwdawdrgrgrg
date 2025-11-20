"""
# DISABLED: Enhanced History Management for BSEE

# DISABLED: Provides comprehensive history tracking for transformation replay functionality.
# DISABLED: Stores complete state snapshots for each operation with timing information
# DISABLED: and metrics evolution for advanced visualization.
"""

# DISABLED: import json
# DISABLED: import time
# DISABLED: import threading
# DISABLED: from dataclasses import dataclass, asdict
# DISABLED: from datetime import datetime
# DISABLED: from pathlib import Path
# DISABLED: from typing import Callable, Dict, List, Optional, Any, Tuple


# DISABLED: @dataclass
# DISABLED: class OperationSnapshot:
    """Enhanced snapshot of operation state for advanced replay."""
# DISABLED:     operation_name: str
# DISABLED:     operation_params: Dict[str, Any]
# DISABLED:     before_data: bytes
# DISABLED:     after_data: bytes
# DISABLED:     before_hex: str
# DISABLED:     after_hex: str
# DISABLED:     metrics_before: Dict[str, float]
# DISABLED:     metrics_after: Dict[str, float]
# DISABLED:     timing_info: Dict[str, float]
# DISABLED:     byte_changes: List[Tuple[int, int, int]]  # (index, old_value, new_value)
# DISABLED:     metadata: Dict[str, Any]
# DISABLED:     timestamp: float


# DISABLED: @dataclass
# DISABLED: class AnalysisSession:
    """Complete analysis session with all operations."""
# DISABLED:     session_id: str
# DISABLED:     start_time: float
# DISABLED:     end_time: float
# DISABLED:     initial_data: bytes
# DISABLED:     final_data: bytes
# DISABLED:     operations: List[OperationSnapshot]
# DISABLED:     session_metadata: Dict[str, Any]
# DISABLED:     total_execution_time: float


# DISABLED: @dataclass
# DISABLED: class OperationEntry:
    """Represents a single operation in the history."""
# DISABLED:     step_number: int                 # Sequential step number
# DISABLED:     operation_name: str             # Name of operation applied
# DISABLED:     parameters: Dict[str, any]      # Parameters used
# DISABLED:     inverse_function: Callable      # Function to reverse operation
# DISABLED:     cost: float                     # Cost of operation
# DISABLED:     timestamp: datetime             # When operation was applied
# DISABLED:     parent_state_id: str            # State before operation
# DISABLED:     resulting_state_id: str         # State after operation
# DISABLED:     effectiveness_score: float      # Score improvement achieved
# DISABLED:     snapshot: Optional[OperationSnapshot] = None  # Enhanced replay data

# DISABLED:     def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
# DISABLED:         return {
# DISABLED:             'step_number': self.step_number,
# DISABLED:             'operation_name': self.operation_name,
# DISABLED:             'parameters': self.parameters,
# DISABLED:             'cost': self.cost,
# DISABLED:             'timestamp': self.timestamp.isoformat(),
# DISABLED:             'parent_state_id': self.parent_state_id,
# DISABLED:             'resulting_state_id': self.resulting_state_id,
# DISABLED:             'effectiveness_score': self.effectiveness_score
# DISABLED:         }


# DISABLED: class HistoryManager:
    """Enhanced history manager for replay and advanced visualization."""

# DISABLED:     def __init__(self, max_history_size: int = 1000, auto_save: bool = True):
        """
# DISABLED:         Initialize enhanced history manager.

# DISABLED:         Args:
# DISABLED:             max_history_size: Maximum number of operations to keep in memory
# DISABLED:             auto_save: Whether to automatically save history to disk
        """
# DISABLED:         self.max_history_size = max_history_size
# DISABLED:         self.auto_save = auto_save

        # Current session
# DISABLED:         self.current_session: Optional[AnalysisSession] = None
# DISABLED:         self.session_start_time: Optional[float] = None

        # Original entries for backward compatibility
# DISABLED:         self.entries: List[OperationEntry] = []
# DISABLED:         self.state_index: Dict[str, int] = {}  # state_id -> step_number
# DISABLED:         self.operation_counts: Dict[str, int] = {}  # operation_name -> count

        # Enhanced operation snapshots
# DISABLED:         self.operation_snapshots: List[OperationSnapshot] = []

        # Session history storage
# DISABLED:         self.session_history: List[AnalysisSession] = []
# DISABLED:         self.storage_directory = Path("history")
# DISABLED:         self.storage_directory.mkdir(exist_ok=True)

        # Threading lock for thread safety
# DISABLED:         self._lock = threading.Lock()

        # Callbacks for events
# DISABLED:         self.on_operation_added: Optional[callable] = None
# DISABLED:         self.on_session_completed: Optional[callable] = None

# DISABLED:     def add_entry(self, entry: OperationEntry) -> None:
        """Add a new operation entry to the history."""
# DISABLED:         self.entries.append(entry)
# DISABLED:         self.state_index[entry.resulting_state_id] = entry.step_number

        # Update operation counts
# DISABLED:         self.operation_counts[entry.operation_name] = \
# DISABLED:             self.operation_counts.get(entry.operation_name, 0) + 1

# DISABLED:     def get_chain_to_state(self, state_id: str) -> List[OperationEntry]:
        """Get the complete operation chain from root to specified state."""
# DISABLED:         if state_id not in self.state_index:
# DISABLED:             return []

# DISABLED:         target_step = self.state_index[state_id]
# DISABLED:         return self.entries[:target_step]

# DISABLED:     def generate_inverse_chain(self, state_id: str) -> List[Callable]:
        """Generate the chain of inverse functions to reverse to original state."""
# DISABLED:         chain = self.get_chain_to_state(state_id)
# DISABLED:         return [entry.inverse_function for entry in reversed(chain)]

# DISABLED:     def export_to_json(self, state_id: str, original_file: str) -> Dict:
        """Export operation history to JSON format for external analysis."""
# DISABLED:         chain = self.get_chain_to_state(state_id)

        # Extract inverse operations (functions can't be serialized, so we save names)
# DISABLED:         inverse_operations = []
# DISABLED:         for entry in reversed(chain):
# DISABLED:             inverse_op = {
# DISABLED:                 'step': entry.step_number,
# DISABLED:                 'operation': self._get_inverse_operation_name(entry.operation_name),
# DISABLED:                 'params': entry.parameters
# DISABLED:             }
# DISABLED:             inverse_operations.append(inverse_op)

# DISABLED:         return {
# DISABLED:             'original_file': original_file,
# DISABLED:             'final_state_id': state_id,
# DISABLED:             'total_operations': len(chain),
# DISABLED:             'total_cost': sum(entry.cost for entry in chain),
# DISABLED:             'operations': [entry.to_dict() for entry in chain],
# DISABLED:             'inverse_operations': inverse_operations,
# DISABLED:             'operation_statistics': self._get_operation_statistics()
# DISABLED:         }

# DISABLED:     def validate_reversibility(self, final_state_id: str, original_binary: bytes) -> bool:
        """Validate that the inverse chain correctly reproduces the original binary."""
# DISABLED:         try:
# DISABLED:             inverse_chain = self.generate_inverse_chain(final_state_id)

            # Start with current state (we would need the current binary data)
            # For now, this is a placeholder that validates the chain structure
# DISABLED:             if not inverse_chain:
# DISABLED:                 return len(self.entries) == 0

            # Validate that we have the right number of inverse functions
# DISABLED:             chain_length = len(self.get_chain_to_state(final_state_id))
# DISABLED:             return len(inverse_chain) == chain_length

# DISABLED:         except Exception:
# DISABLED:             return False

# DISABLED:     def get_operation_count(self, operation_name: str) -> int:
        """Get the total count of a specific operation."""
# DISABLED:         return self.operation_counts.get(operation_name, 0)

# DISABLED:     def get_total_cost(self) -> float:
        """Get total cost of all operations."""
# DISABLED:         return sum(entry.cost for entry in self.entries)

# DISABLED:     def get_operation_effectiveness(self, operation_name: str) -> float:
        """Get average effectiveness score for an operation."""
# DISABLED:         operation_entries = [e for e in self.entries if e.operation_name == operation_name]
# DISABLED:         if not operation_entries:
# DISABLED:             return 0.0

# DISABLED:         total_effectiveness = sum(e.effectiveness_score for e in operation_entries)
# DISABLED:         return total_effectiveness / len(operation_entries)

# DISABLED:     def get_most_effective_operations(self, top_n: int = 10) -> List[Dict]:
        """Get the most effective operations by score/cost ratio."""
# DISABLED:         operation_stats = {}

# DISABLED:         for entry in self.entries:
# DISABLED:             if entry.operation_name not in operation_stats:
# DISABLED:                 operation_stats[entry.operation_name] = {
# DISABLED:                     'total_cost': 0.0,
# DISABLED:                     'total_effectiveness': 0.0,
# DISABLED:                     'count': 0
# DISABLED:                 }

# DISABLED:             stats = operation_stats[entry.operation_name]
# DISABLED:             stats['total_cost'] += entry.cost
# DISABLED:             stats['total_effectiveness'] += entry.effectiveness_score
# DISABLED:             stats['count'] += 1

        # Calculate score/cost ratio
# DISABLED:         results = []
# DISABLED:         for op_name, stats in operation_stats.items():
# DISABLED:             if stats['total_cost'] > 0:
# DISABLED:                 ratio = stats['total_effectiveness'] / stats['total_cost']
# DISABLED:                 results.append({
# DISABLED:                     'operation': op_name,
# DISABLED:                     'score_per_cost': ratio,
# DISABLED:                     'total_cost': stats['total_cost'],
# DISABLED:                     'total_effectiveness': stats['total_effectiveness'],
# DISABLED:                     'count': stats['count']
# DISABLED:                 })

        # Sort by ratio and return top N
# DISABLED:         results.sort(key=lambda x: x['score_per_cost'], reverse=True)
# DISABLED:         return results[:top_n]

# DISABLED:     def clear(self) -> None:
        """Clear all history."""
# DISABLED:         self.entries.clear()
# DISABLED:         self.state_index.clear()
# DISABLED:         self.operation_counts.clear()

# DISABLED:     def get_summary(self) -> Dict:
        """Get a summary of the operation history."""
# DISABLED:         if not self.entries:
# DISABLED:             return {
# DISABLED:                 'total_operations': 0,
# DISABLED:                 'total_cost': 0.0,
# DISABLED:                 'unique_operations': 0,
# DISABLED:                 'most_used_operation': None
# DISABLED:             }

# DISABLED:         return {
# DISABLED:             'total_operations': len(self.entries),
# DISABLED:             'total_cost': self.get_total_cost(),
# DISABLED:             'unique_operations': len(self.operation_counts),
# DISABLED:             'most_used_operation': max(self.operation_counts.items(), key=lambda x: x[1])[0] if self.operation_counts else None,
# DISABLED:             'operation_counts': self.operation_counts.copy()
# DISABLED:         }

# DISABLED:     def _get_inverse_operation_name(self, operation_name: str) -> str:
        """Get the name of the inverse operation."""
        # This would be expanded based on the operations registry
# DISABLED:         inverse_map = {
# DISABLED:             'xor_constant': 'xor_constant',
# DISABLED:             'xor_range': 'xor_range',
# DISABLED:             'rotate_left': 'rotate_right',
# DISABLED:             'rotate_right': 'rotate_left',
# DISABLED:             'bitplane_extract': 'bitplane_insert',
# DISABLED:             'bitplane_insert': 'bitplane_extract',
            # Add more mappings as needed
# DISABLED:         }
# DISABLED:         return inverse_map.get(operation_name, f'inverse_{operation_name}')

# DISABLED:     def _get_operation_statistics(self) -> Dict:
        """Get detailed statistics about operations used."""
# DISABLED:         stats = {}
# DISABLED:         for op_name, count in self.operation_counts.items():
# DISABLED:             operation_entries = [e for e in self.entries if e.operation_name == op_name]
# DISABLED:             total_cost = sum(e.cost for e in operation_entries)
# DISABLED:             avg_cost = total_cost / len(operation_entries) if operation_entries else 0
# DISABLED:             avg_effectiveness = sum(e.effectiveness_score for e in operation_entries) / len(operation_entries) if operation_entries else 0

# DISABLED:             stats[op_name] = {
# DISABLED:                 'count': count,
# DISABLED:                 'total_cost': total_cost,
# DISABLED:                 'average_cost': avg_cost,
# DISABLED:                 'average_effectiveness': avg_effectiveness
# DISABLED:             }

# DISABLED:         return stats

    # Enhanced methods for transformation viewer
# DISABLED:     def start_session(self, session_id: str = None, initial_data: bytes = b"",
# DISABLED:                      metadata: Dict[str, Any] = None) -> str:
        """
# DISABLED:         Start a new analysis session.

# DISABLED:         Args:
# DISABLED:             session_id: Optional session ID (auto-generated if not provided)
# DISABLED:             initial_data: Initial binary data
# DISABLED:             metadata: Session metadata

# DISABLED:         Returns:
# DISABLED:             Session ID
        """
# DISABLED:         with self._lock:
# DISABLED:             if session_id is None:
# DISABLED:                 session_id = f"session_{int(time.time())}_{len(self.session_history)}"

# DISABLED:             self.session_start_time = time.time()

# DISABLED:             self.current_session = AnalysisSession(
# DISABLED:                 session_id=session_id,
# DISABLED:                 start_time=self.session_start_time,
# DISABLED:                 end_time=0.0,
# DISABLED:                 initial_data=initial_data,
# DISABLED:                 final_data=initial_data,
# DISABLED:                 operations=[],
# DISABLED:                 session_metadata=metadata or {},
# DISABLED:                 total_execution_time=0.0
# DISABLED:             )

            # Clear operation snapshots for new session
# DISABLED:             self.operation_snapshots.clear()

# DISABLED:             return session_id

# DISABLED:     def add_operation_snapshot(self, operation_name: str, operation_params: Dict[str, Any],
# DISABLED:                              before_data: bytes, after_data: bytes,
# DISABLED:                              metrics_before: Dict[str, float] = None,
# DISABLED:                              metrics_after: Dict[str, float] = None,
# DISABLED:                              timing_info: Dict[str, float] = None,
# DISABLED:                              metadata: Dict[str, Any] = None) -> OperationSnapshot:
        """
# DISABLED:         Add enhanced operation snapshot for replay.

# DISABLED:         Args:
# DISABLED:             operation_name: Name of the operation
# DISABLED:             operation_params: Parameters used for the operation
# DISABLED:             before_data: Data before operation
# DISABLED:             after_data: Data after operation
# DISABLED:             metrics_before: Metrics calculated before operation
# DISABLED:             metrics_after: Metrics calculated after operation
# DISABLED:             timing_info: Timing information for the operation
# DISABLED:             metadata: Additional operation metadata

# DISABLED:         Returns:
# DISABLED:             Created operation snapshot
        """
# DISABLED:         with self._lock:
# DISABLED:             if self.current_session is None:
# DISABLED:                 raise ValueError("No active session. Call start_session() first.")

            # Create snapshot
# DISABLED:             snapshot = OperationSnapshot(
# DISABLED:                 operation_name=operation_name,
# DISABLED:                 operation_params=operation_params or {},
# DISABLED:                 before_data=before_data,
# DISABLED:                 after_data=after_data,
# DISABLED:                 before_hex=before_data.hex(),
# DISABLED:                 after_hex=after_data.hex(),
# DISABLED:                 metrics_before=metrics_before or {},
# DISABLED:                 metrics_after=metrics_after or {},
# DISABLED:                 timing_info=timing_info or {},
# DISABLED:                 byte_changes=self._analyze_byte_changes(before_data, after_data),
# DISABLED:                 metadata=metadata or {},
# DISABLED:                 timestamp=time.time()
# DISABLED:             )

            # Add to current session
# DISABLED:             self.current_session.operations.append(snapshot)
# DISABLED:             self.current_session.final_data = after_data

            # Update session execution time
# DISABLED:             if timing_info and 'execution_time' in timing_info:
# DISABLED:                 self.current_session.total_execution_time += timing_info['execution_time']

            # Add to snapshots list
# DISABLED:             self.operation_snapshots.append(snapshot)

            # Limit history size
# DISABLED:             if len(self.operation_snapshots) > self.max_history_size:
# DISABLED:                 self.operation_snapshots.pop(0)

            # Auto-save if enabled
# DISABLED:             if self.auto_save:
# DISABLED:                 self._save_session_snapshot(snapshot)

            # Notify callback
# DISABLED:             if self.on_operation_added:
# DISABLED:                 self.on_operation_added(snapshot)

# DISABLED:             return snapshot

# DISABLED:     def end_session(self, final_metadata: Dict[str, Any] = None) -> AnalysisSession:
        """
# DISABLED:         End current session and add to history.

# DISABLED:         Args:
# DISABLED:             final_metadata: Additional metadata for session completion

# DISABLED:         Returns:
# DISABLED:             Completed session
        """
# DISABLED:         with self._lock:
# DISABLED:             if self.current_session is None:
# DISABLED:                 raise ValueError("No active session to end.")

# DISABLED:             self.current_session.end_time = time.time()
# DISABLED:             self.current_session.session_metadata.update(final_metadata or {})

            # Add to history
# DISABLED:             self.session_history.append(self.current_session)

            # Auto-save complete session
# DISABLED:             if self.auto_save:
# DISABLED:                 self._save_complete_session(self.current_session)

            # Notify callback
# DISABLED:             if self.on_session_completed:
# DISABLED:                 self.on_session_completed(self.current_session)

# DISABLED:             completed_session = self.current_session
# DISABLED:             self.current_session = None
# DISABLED:             self.session_start_time = None

# DISABLED:             return completed_session

# DISABLED:     def get_current_session(self) -> Optional[AnalysisSession]:
        """Get currently active session."""
# DISABLED:         return self.current_session

# DISABLED:     def get_session_history(self, limit: int = None) -> List[AnalysisSession]:
        """
# DISABLED:         Get session history.

# DISABLED:         Args:
# DISABLED:             limit: Maximum number of sessions to return

# DISABLED:         Returns:
# DISABLED:             List of analysis sessions
        """
# DISABLED:         with self._lock:
# DISABLED:             history = self.session_history.copy()
# DISABLED:             if limit:
# DISABLED:                 return history[-limit:]
# DISABLED:             return history

# DISABLED:     def get_session_by_id(self, session_id: str) -> Optional[AnalysisSession]:
        """Get session by ID."""
# DISABLED:         with self._lock:
# DISABLED:             for session in self.session_history:
# DISABLED:                 if session.session_id == session_id:
# DISABLED:                     return session
# DISABLED:             return None

# DISABLED:     def get_operation_snapshots(self, session_id: str = None) -> List[OperationSnapshot]:
        """
# DISABLED:         Get operation snapshots.

# DISABLED:         Args:
# DISABLED:             session_id: Optional session ID (uses current session if not provided)

# DISABLED:         Returns:
# DISABLED:             List of operation snapshots
        """
# DISABLED:         with self._lock:
# DISABLED:             if session_id:
# DISABLED:                 session = self.get_session_by_id(session_id)
# DISABLED:                 return session.operations if session else []
# DISABLED:             elif self.current_session:
# DISABLED:                 return self.current_session.operations.copy()
# DISABLED:             else:
# DISABLED:                 return self.operation_snapshots.copy()

# DISABLED:     def export_session_for_replay(self, session_id: str = None) -> Dict[str, Any]:
        """
# DISABLED:         Export session data in format suitable for transformation viewer.

# DISABLED:         Args:
# DISABLED:             session_id: Optional session ID (uses current session if not provided)

# DISABLED:         Returns:
# DISABLED:             Export data dictionary
        """
# DISABLED:         with self._lock:
# DISABLED:             if session_id:
# DISABLED:                 session = self.get_session_by_id(session_id)
# DISABLED:             else:
# DISABLED:                 session = self.current_session

# DISABLED:             if not session:
# DISABLED:                 return {}

            # Convert operations to replay format
# DISABLED:             operations = []
# DISABLED:             for op in session.operations:
# DISABLED:                 operation_data = {
# DISABLED:                     'name': op.operation_name,
# DISABLED:                     'params': op.operation_params,
# DISABLED:                     'before_hex': op.before_hex,
# DISABLED:                     'after_hex': op.after_hex,
# DISABLED:                     'metrics_before': op.metrics_before,
# DISABLED:                     'metrics_after': op.metrics_after,
# DISABLED:                     'timing': op.timing_info,
# DISABLED:                     'byte_changes': op.byte_changes,
# DISABLED:                     'metadata': op.metadata,
# DISABLED:                     'timestamp': op.timestamp
# DISABLED:                 }
# DISABLED:                 operations.append(operation_data)

# DISABLED:             return {
# DISABLED:                 'session_id': session.session_id,
# DISABLED:                 'start_time': session.start_time,
# DISABLED:                 'end_time': session.end_time,
# DISABLED:                 'initial_data': session.initial_data.hex(),
# DISABLED:                 'final_data': session.final_data.hex(),
# DISABLED:                 'operations': operations,
# DISABLED:                 'session_metadata': session.session_metadata,
# DISABLED:                 'total_execution_time': session.total_execution_time
# DISABLED:             }

# DISABLED:     def _analyze_byte_changes(self, before: bytes, after: bytes) -> List[Tuple[int, int, int]]:
        """Analyze byte changes between before and after data."""
# DISABLED:         changes = []
# DISABLED:         min_len = min(len(before), len(after))

        # Find changed bytes
# DISABLED:         for i in range(min_len):
# DISABLED:             if before[i] != after[i]:
# DISABLED:                 changes.append((i, before[i], after[i]))

        # Handle insertions/deletions
# DISABLED:         if len(before) < len(after):
            # Insertions
# DISABLED:             for i in range(len(before), len(after)):
# DISABLED:                 changes.append((i, -1, after[i]))  # -1 indicates insertion
# DISABLED:         elif len(before) > len(after):
            # Deletions
# DISABLED:             for i in range(len(after), len(before)):
# DISABLED:                 changes.append((i, before[i], -1))  # -1 indicates deletion

# DISABLED:         return changes

# DISABLED:     def _save_session_snapshot(self, snapshot: OperationSnapshot):
        """Save individual operation snapshot."""
# DISABLED:         try:
# DISABLED:             snapshot_file = self.storage_directory / f"snapshot_{int(snapshot.timestamp)}.json"
# DISABLED:             with open(snapshot_file, 'w') as f:
# DISABLED:                 json.dump(asdict(snapshot), f, indent=2, default=str)
# DISABLED:         except Exception as e:
            # Log error but don't crash
# DISABLED:             print(f"Error saving snapshot: {e}")

# DISABLED:     def _save_complete_session(self, session: AnalysisSession):
        """Save complete session to disk."""
# DISABLED:         try:
# DISABLED:             session_file = self.storage_directory / f"session_{session.session_id}.json"
# DISABLED:             session_data = {
# DISABLED:                 'session': asdict(session),
# DISABLED:                 'export_timestamp': datetime.now().isoformat()
# DISABLED:             }
# DISABLED:             with open(session_file, 'w') as f:
# DISABLED:                 json.dump(session_data, f, indent=2, default=str)
# DISABLED:         except Exception as e:
# DISABLED:             print(f"Error saving session: {e}")

# DISABLED:     def analyze_session(self, session_id: str = None) -> Dict[str, Any]:
        """
# DISABLED:         Analyze a session and return comprehensive statistics.

# DISABLED:         Args:
# DISABLED:             session_id: Optional session ID (uses current session if not provided)

# DISABLED:         Returns:
# DISABLED:             Session analysis data
        """
# DISABLED:         with self._lock:
# DISABLED:             if session_id:
# DISABLED:                 session = self.get_session_by_id(session_id)
# DISABLED:             else:
# DISABLED:                 session = self.current_session

# DISABLED:             if not session:
# DISABLED:                 return {}

            # Calculate statistics
# DISABLED:             total_operations = len(session.operations)
# DISABLED:             total_byte_changes = 0
# DISABLED:             data_size_change = len(session.final_data) - len(session.initial_data)

# DISABLED:             for op in session.operations:
# DISABLED:                 total_byte_changes += len(op.byte_changes)

# DISABLED:             return {
# DISABLED:                 'total_operations': total_operations,
# DISABLED:                 'total_byte_changes': total_byte_changes,
# DISABLED:                 'data_size_change': data_size_change,
# DISABLED:                 'total_execution_time': session.total_execution_time,
# DISABLED:                 'session_duration': session.end_time - session.start_time if session.end_time > 0 else 0,
# DISABLED:                 'operations_by_type': self._count_operations_by_type(session.operations),
# DISABLED:                 'average_operation_time': session.total_execution_time / total_operations if total_operations > 0 else 0
# DISABLED:             }

# DISABLED:     def _count_operations_by_type(self, operations: List[OperationSnapshot]) -> Dict[str, int]:
        """Count operations by type."""
# DISABLED:         counts = {}
# DISABLED:         for op in operations:
# DISABLED:             counts[op.operation_name] = counts.get(op.operation_name, 0) + 1
# DISABLED:         return counts

# DISABLED:     def set_callbacks(self, on_operation_added: callable = None,
# DISABLED:                      on_session_completed: callable = None):
        """Set callback functions for events."""
# DISABLED:         if on_operation_added:
# DISABLED:             self.on_operation_added = on_operation_added
# DISABLED:         if on_session_completed:
# DISABLED:             self.on_session_completed = on_session_completed
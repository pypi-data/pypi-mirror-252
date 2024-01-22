from voltaire_bundler.user_operation.user_operation import UserOperation


class UserOperationsWithEntryPoint:
    entry_point_contract: str
    verified_at_block_hash: int
    chain_id: int
    user_operations: UserOperation
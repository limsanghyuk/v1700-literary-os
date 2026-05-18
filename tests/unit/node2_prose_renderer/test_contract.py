import pytest
from v1700.nodes.node2_prose_renderer.contract import SurfaceOnlyContract

def test_surface_only_contract_passes():
    SurfaceOnlyContract().assert_valid()

def test_surface_only_contract_blocks_structural_permission():
    with pytest.raises(AssertionError):
        SurfaceOnlyContract(allow_reveal_change=True).assert_valid()

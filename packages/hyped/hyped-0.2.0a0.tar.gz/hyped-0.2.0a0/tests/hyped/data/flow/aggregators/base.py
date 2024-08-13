import pickle
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from datasets import Features, Sequence

from hyped.common.feature_checks import (
    check_feature_equals,
    check_object_matches_feature,
)
from hyped.data.flow.core.nodes.aggregator import (
    BaseDataAggregator,
    BaseDataAggregatorConfig,
    Batch,
    DataAggregationManager,
)
from hyped.data.flow.core.nodes.base import IOContext
from hyped.data.flow.core.refs.inputs import InputRefs
from hyped.data.flow.core.refs.outputs import OutputRefs
from hyped.data.flow.core.refs.ref import FeatureRef

UNSET = object()


# TODO: This base class has a high overlap with the base test for processors,
#       we should refactor that to share the same class to some extend
class BaseDataAggregatorTest:
    # aggregator to test
    aggregator_type: type[BaseDataAggregator]
    aggregator_config: BaseDataAggregatorConfig
    # input values
    input_features: Features
    input_data: Batch
    input_index: None | list[int] = None

    expected_value_feature: None | Features = None
    # expected initial state
    expected_initial_value: None | Any = UNSET
    expected_initial_state: None | Any = UNSET
    # expected output
    expected_output_value: None | Any = UNSET
    expected_output_state: None | Any = UNSET
    # others
    rank: int = 0

    node_id: str = "node_id"

    @pytest.fixture
    def aggregator(self):
        cls = type(self)
        return cls.aggregator_type.from_config(cls.aggregator_config)

    @pytest.fixture
    def flow(self):
        cls = type(self)
        mock_flow = MagicMock()
        mock_flow.add_processor_node = MagicMock(return_value=cls.node_id)
        return mock_flow

    @pytest.fixture
    def input_refs(self, aggregator, flow) -> InputRefs:
        cls = type(self)
        input_refs = {
            k: FeatureRef(key_=k, feature_=v, node_id_=cls.node_id, flow_=flow)
            for k, v in cls.input_features.items()
        }
        return aggregator._in_refs_validator.validate(**input_refs)

    @pytest.fixture
    def output_refs(self, aggregator, input_refs, flow) -> OutputRefs:
        return aggregator._out_refs_type(
            flow,
            "out",
            aggregator._out_refs_type.build_features(
                aggregator.config, input_refs
            ),
        )

    @pytest.fixture
    def io_context(self, output_refs):
        cls = type(self)
        return IOContext(
            node_id=cls.node_id,
            inputs=cls.input_features,
            outputs=output_refs.build_features(
                cls.aggregator_config, cls.input_features
            ),
        )

    @pytest.fixture
    @patch("hyped.data.flow.core.nodes.aggregator._manager")
    def manager(
        self, mock_manager, aggregator, io_context
    ) -> DataAggregationManager:
        cls = type(self)
        # Mock the multiprocessing manager object
        mock_manager.dict = MagicMock(side_effect=lambda x: dict(x))
        mock_manager.Lock = MagicMock(return_value=MagicMock())
        # create aggregation manager
        cls = type(self)
        return DataAggregationManager(
            aggregators=[aggregator], io_contexts=[io_context]
        )

    def test_call(self, aggregator, input_refs):
        cls = type(self)

        if input_refs is not None:
            # call the processor
            out = aggregator.call(**input_refs.named_refs)
            # check the output features
            if cls.expected_value_feature is not None:
                assert out.feature_ == cls.expected_value_feature

    @pytest.mark.asyncio
    async def test_pickle(
        self, manager, aggregator, input_refs, output_refs, io_context
    ):
        # pickle and unpickle processor
        serialized = pickle.dumps(aggregator)
        reconstructed = pickle.loads(serialized)
        # run the test case on the reconstructed processor
        # make sure the underlying feature model is the same
        await self.test_case(
            manager, reconstructed, input_refs, output_refs, io_context
        )

    @pytest.mark.asyncio
    async def test_case(
        self, manager, aggregator, input_refs, output_refs, io_context
    ):
        cls = type(self)
        # check input data
        input_keys = set(cls.input_data.keys())
        assert aggregator.required_input_keys.issubset(input_keys)
        assert check_object_matches_feature(
            cls.input_data,
            {k: Sequence(v) for k, v in cls.input_features.items()},
        )

        # build default index if not specifically given
        input_index = (
            cls.input_index
            if cls.input_index is not None
            else list(range(len(next(iter(cls.input_data.values())))))
        )
        assert len(input_index) == len(next(iter(cls.input_data.values())))

        # check initial aggregation state
        if cls.expected_initial_value != UNSET:
            assert (
                manager._value_buffer[cls.node_id]
                == cls.expected_initial_value
            ), (
                f"Expected {manager._value_buffer[cls.node_id]}, "
                f"got {cls.expected_initial_value}"
            )
        if cls.expected_initial_state != UNSET:
            assert (
                manager._state_buffer[cls.node_id]
                == cls.expected_initial_state
            ), (
                f"Expected {manager._state_buffer[cls.node_id]}, "
                f"got {cls.expected_initial_state}"
            )

            if cls.expected_value_feature is not None:
                assert check_feature_equals(
                    output_refs.feature_, cls.expected_value_feature
                )
                assert check_object_matches_feature(
                    manager._value_buffer[cls.node_id],
                    cls.expected_value_feature,
                )

        # run aggregation
        await manager.aggregate(
            aggregator, cls.input_data, input_index, cls.rank, io_context
        )

        # check aggregation value matches output features
        assert check_object_matches_feature(
            manager._value_buffer[cls.node_id], output_refs.feature_
        )

        # check aggregation state after execution
        if cls.expected_output_value != UNSET:
            assert (
                manager._value_buffer[cls.node_id] == cls.expected_output_value
            ), (
                f"Expected {manager._value_buffer[cls.node_id]}, "
                f"got {cls.expected_output_value}"
            )
        if cls.expected_output_state != UNSET:
            assert (
                manager._state_buffer[cls.node_id] == cls.expected_output_state
            ), (
                f"Expected {manager._state_buffer[cls.node_id]}, "
                f"got {cls.expected_output_ctx}"
            )

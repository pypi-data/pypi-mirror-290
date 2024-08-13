from unittest.mock import MagicMock, call

import pytest
from datasets import Features, Sequence, Value
from pydantic import ValidationError

from hyped.data.flow.core.refs.inputs import InputRefs, InputRefsContainer
from hyped.data.flow.core.refs.outputs import OutputRefs
from hyped.data.flow.core.refs.ref import FeatureRef
from hyped.data.flow.processors.ops.collect import (
    CollectFeatures,
    CollectFeaturesConfig,
    CollectFeaturesOutputRefs,
    NestedContainer,
    _path_to_str,
)
from tests.hyped.data.flow.processors.base import BaseDataProcessorTest


class TestNestedContainer:
    def test_basics(self):
        # test parse sequence
        container = NestedContainer[int](data=[1, 1])
        assert isinstance(container.data[0], NestedContainer)
        assert isinstance(container.data[1], NestedContainer)
        assert isinstance(container.data[0].data, int)
        assert isinstance(container.data[1].data, int)
        # test parse dict
        container = NestedContainer[int](data={"a": 1, "b": 1})
        assert isinstance(container.data["a"], NestedContainer)
        assert isinstance(container.data["b"], NestedContainer)
        assert isinstance(container.data["a"].data, int)
        assert isinstance(container.data["b"].data, int)
        # test parse nested
        container = NestedContainer[int](data={"a": [1, 1], "b": 1})
        assert isinstance(container.data["a"], NestedContainer)
        assert isinstance(container.data["b"], NestedContainer)
        assert isinstance(container.data["a"].data[0], NestedContainer)
        assert isinstance(container.data["a"].data[1], NestedContainer)
        assert isinstance(container.data["a"].data[0].data, int)
        assert isinstance(container.data["a"].data[1].data, int)
        assert isinstance(container.data["b"].data, int)
        # invalid type
        with pytest.raises(ValidationError):
            NestedContainer[int](data=[1, "a"])

    def test_map(self):
        container = NestedContainer[int](data={"a": [1, 2], "b": 3})
        # create mock mapping function and apply it to the container
        f = MagicMock(return_value="x")
        mapped_container = container.map(f, str)
        # make sure the function was applied to all values
        f.assert_has_calls(
            [
                call(("a", 0), 1),
                call(("a", 1), 2),
                call(("b",), 3),
            ]
        )
        # check output
        assert mapped_container == NestedContainer[str](
            data={"a": ["x", "x"], "b": "x"}
        )

    def test_flatten(self):
        container = NestedContainer[int](data={"a": [1, 2], "b": 3})
        assert container.flatten() == {("a", 0): 1, ("a", 1): 2, ("b",): 3}

    def test_unpack(self):
        container = NestedContainer[int](data={"a": [1, 2], "b": 3})
        assert container.unpack() == {"a": [1, 2], "b": 3}


mock_flow = MagicMock()
mock_flow.add_processor_node = MagicMock(return_value="node_id")

int_ref = FeatureRef(
    key_="int", feature_=Value("int32"), node_id_="0", flow_=mock_flow
)
str_ref = FeatureRef(
    key_="str", feature_=Value("string"), node_id_="1", flow_=mock_flow
)
dct_ref = FeatureRef(
    key_="dct",
    feature_=Features({"val": Value("int32")}),
    node_id_="2",
    flow_=mock_flow,
)
lst_ref = FeatureRef(
    key_="lst",
    feature_=Sequence(Value("int32")),
    node_id_="3",
    flow_=mock_flow,
)


def test_invalid_sequence():
    with pytest.raises(TypeError):
        CollectFeatures().call(
            collection=NestedContainer[FeatureRef](data=[int_ref, str_ref])
        )


class BaseCollectFeaturesTest(BaseDataProcessorTest):
    # processor
    processor_type = CollectFeatures
    processor_config = CollectFeaturesConfig()
    # collection
    collection: dict | list

    @pytest.fixture
    def nested_collection(self) -> NestedContainer[FeatureRef]:
        cls = type(self)
        return NestedContainer[FeatureRef](data=cls.collection)

    @pytest.fixture
    def input_refs(self, nested_collection, flow) -> InputRefs:
        named_refs = {
            _path_to_str(key): ref
            for key, ref in nested_collection.flatten().items()
        }
        return InputRefsContainer(named_refs=named_refs, flow=flow)

    @pytest.fixture
    def output_refs(self, processor, nested_collection, flow) -> OutputRefs:
        # build output feature references
        return processor._out_refs_type(
            flow,
            "out",
            processor._out_refs_type.build_features(
                processor.config, {"collection": nested_collection}
            ),
        )

    def test_call(self, processor, nested_collection):
        cls = type(self)
        out = processor.call(collection=nested_collection)
        if cls.expected_output_features is not None:
            assert out.feature_ == cls.expected_output_features


class TestCollectFeatures_mapping(BaseCollectFeaturesTest):
    collection = {"a": int_ref, "b": str_ref}
    # inputs
    input_features = {"a": int_ref.feature_, "b": str_ref.feature_}
    input_data = {
        "a": [i for i in range(100)],
        "b": [str(i) for i in range(100, 200)],
    }
    input_index = list(range(100))
    # expected outputs
    expected_output_features = {
        "collected": {"a": int_ref.feature_, "b": str_ref.feature_}
    }
    expected_output_data = {
        "collected": [{"a": i, "b": str(100 + i)} for i in range(100)]
    }


class TestCollectFeatures_sequence(BaseCollectFeaturesTest):
    collection = [int_ref, int_ref, int_ref]
    # inputs
    input_features = {
        "0": int_ref.feature_,
        "1": int_ref.feature_,
        "2": int_ref.feature_,
    }
    input_data = {
        "0": list(range(100)),
        "1": list(range(100)),
        "2": list(range(100)),
    }
    input_index = list(range(100))
    # expected outputs
    expected_output_features = {
        "collected": Sequence(int_ref.feature_, length=3)
    }
    expected_output_data = {"collected": [[i, i, i] for i in range(100)]}


class TestCollectFeatures_nested(BaseCollectFeaturesTest):
    # collection
    collection = {
        "a": {
            "b": int_ref,
            "c": [
                {"x": str_ref, "y": str_ref},
                {"x": str_ref, "y": str_ref},
            ],
        }
    }
    # inputs
    input_features = {
        "a.b": int_ref.feature_,
        "a.c.0.x": str_ref.feature_,
        "a.c.0.y": str_ref.feature_,
        "a.c.1.x": str_ref.feature_,
        "a.c.1.y": str_ref.feature_,
    }
    input_data = {
        "a.b": [i for i in range(100)],
        "a.c.0.x": [str(i) for i in range(100)],
        "a.c.0.y": [str(i) for i in range(100)],
        "a.c.1.x": [str(i) for i in range(100)],
        "a.c.1.y": [str(i) for i in range(100)],
    }
    input_index = list(range(100))
    # expected output
    expected_output_data = {
        "collected": [
            {
                "a": {
                    "b": i,
                    "c": [
                        {"x": str(i), "y": str(i)},
                        {"x": str(i), "y": str(i)},
                    ],
                }
            }
            for i in range(100)
        ]
    }


class TestCollectFeatures_nested_dict(BaseCollectFeaturesTest):
    collection = {"a": dct_ref, "b": str_ref}
    # inputs
    input_features = {"a": dct_ref.feature_, "b": str_ref.feature_}
    input_data = {
        "a": [{"val": i} for i in range(100)],
        "b": [str(i) for i in range(100, 200)],
    }
    input_index = list(range(100))
    # expected outputs
    expected_output_features = {
        "collected": {"a": dct_ref.feature_, "b": str_ref.feature_}
    }
    expected_output_data = {
        "collected": [{"a": {"val": i}, "b": str(100 + i)} for i in range(100)]
    }


class TestCollectFeatures_nested_list(BaseCollectFeaturesTest):
    collection = {"a": lst_ref, "b": str_ref}
    # inputs
    input_features = {"a": lst_ref.feature_, "b": str_ref.feature_}
    input_data = {
        "a": [[i] for i in range(100)],
        "b": [str(i) for i in range(100, 200)],
    }
    input_index = list(range(100))
    # expected outputs
    expected_output_features = {
        "collected": {"a": lst_ref.feature_, "b": str_ref.feature_}
    }
    expected_output_data = {
        "collected": [{"a": [i], "b": str(100 + i)} for i in range(100)]
    }

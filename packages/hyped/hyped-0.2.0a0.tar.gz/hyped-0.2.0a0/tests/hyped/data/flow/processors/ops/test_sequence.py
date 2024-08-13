import pytest
from datasets import Features, Sequence, Value

from hyped.data.flow.processors.ops import sequence
from tests.hyped.data.flow.processors.base import BaseDataProcessorTest


class TestSequenceLength(BaseDataProcessorTest):
    processor_type = sequence.SequenceLength
    processor_config = sequence.SequenceLengthConfig()

    input_features = Features({"a": Sequence(Value("int32"))})
    input_data = {"a": [[1, 2, 3], [1, 2], [1]]}
    input_index = [0, 1, 2]

    expected_output_features = Features({"result": Value("int64")})
    expected_output_data = {"result": [3, 2, 1]}


class TestSequenceGetItem(BaseDataProcessorTest):
    processor_type = sequence.SequenceGetItem
    processor_config = sequence.SequenceGetItemConfig()

    input_features = Features(
        {"sequence": Sequence(Value("int32")), "index": Value("int32")}
    )
    input_data = {
        "sequence": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "index": [0, 1, 2],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"gathered": Value("int32")})
    expected_output_data = {"gathered": [1, 5, 9]}


class TestSequenceGetItem_MultiIndex(BaseDataProcessorTest):
    processor_type = sequence.SequenceGetItem
    processor_config = sequence.SequenceGetItemConfig()

    input_features = Features(
        {
            "sequence": Sequence(Value("int32")),
            "index": Sequence(Value("int32")),
        }
    )
    input_data = {
        "sequence": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "index": [[0], [0, 1], [0, 1, 2]],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"gathered": Sequence(Value("int32"))})
    expected_output_data = {"gathered": [[1], [4, 5], [7, 8, 9]]}


class TestSequenceGetItem_MultiIndex_FixedLength(BaseDataProcessorTest):
    processor_type = sequence.SequenceGetItem
    processor_config = sequence.SequenceGetItemConfig()

    input_features = Features(
        {
            "sequence": Sequence(Value("int32")),
            "index": Sequence(Value("int32"), length=2),
        }
    )
    input_data = {
        "sequence": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "index": [[0, 1], [1, 2], [0, 2]],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features(
        {"gathered": Sequence(Value("int32"), length=2)}
    )
    expected_output_data = {"gathered": [[1, 2], [5, 6], [7, 9]]}


class TestSequenceSetItem(BaseDataProcessorTest):
    processor_type = sequence.SequenceSetItem
    processor_config = sequence.SequenceSetItemConfig()

    input_features = Features(
        {
            "sequence": Sequence(Value("int32")),
            "index": Value("int32"),
            "value": Value("int32"),
        }
    )
    input_data = {
        "sequence": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "index": [0, 1, 2],
        "value": [-1, -2, -3],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"result": Sequence(Value("int32"))})
    expected_output_data = {"result": [[-1, 2, 3], [4, -2, 6], [7, 8, -3]]}


class TestSequenceSetItem_MultiIndex(BaseDataProcessorTest):
    processor_type = sequence.SequenceSetItem
    processor_config = sequence.SequenceSetItemConfig()

    input_features = Features(
        {
            "sequence": Sequence(Value("int32")),
            "index": Sequence(Value("int32")),
            "value": Sequence(Value("int32")),
        }
    )
    input_data = {
        "sequence": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "index": [[0], [0, 1], [0, 1, 2]],
        "value": [[-1], [-1, -2], [-1, -2, -3]],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"result": Sequence(Value("int32"))})
    expected_output_data = {"result": [[-1, 2, 3], [-1, -2, 6], [-1, -2, -3]]}


class TestSequenceSetItem_MultiIndex_FixedLength(BaseDataProcessorTest):
    processor_type = sequence.SequenceSetItem
    processor_config = sequence.SequenceSetItemConfig()

    input_features = Features(
        {
            "sequence": Sequence(Value("int32")),
            "index": Sequence(Value("int32"), length=2),
            "value": Sequence(Value("int32"), length=2),
        }
    )
    input_data = {
        "sequence": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "index": [[0, 1], [1, 2], [0, 2]],
        "value": [[-1, -2], [-1, -2], [-1, -2]],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"result": Sequence(Value("int32"))})
    expected_output_data = {"result": [[-1, -2, 3], [4, -1, -2], [-1, 8, -2]]}


class TestSequenceContains(BaseDataProcessorTest):
    processor_type = sequence.SequenceContains
    processor_config = sequence.SequenceContainsConfig()

    input_features = Features(
        {"sequence": Sequence(Value("int32")), "value": Value("int32")}
    )
    input_data = {
        "sequence": [[0, 1, 2], [0, 0, 1], [0, 0, 0]],
        "value": [0, 1, 2],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"contains": Value("bool")})
    expected_output_data = {"contains": [True, True, False]}


class TestSequenceCountOf(BaseDataProcessorTest):
    processor_type = sequence.SequenceCountOf
    processor_config = sequence.SequenceCountOfConfig()

    input_features = Features(
        {"sequence": Sequence(Value("int32")), "value": Value("int32")}
    )
    input_data = {
        "sequence": [[0, 1, 2], [0, 0, 1], [0, 0, 0]],
        "value": [0, 0, 0],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"count": Value("int64")})
    expected_output_data = {"count": [1, 2, 3]}


class TestSequenceIndexOf(BaseDataProcessorTest):
    processor_type = sequence.SequenceIndexOf
    processor_config = sequence.SequenceIndexOfConfig()

    input_features = Features(
        {"sequence": Sequence(Value("int32")), "value": Value("int32")}
    )
    input_data = {
        "sequence": [[0, 1, 2], [0, 0, 1], [1, 0, 0]],
        "value": [0, 0, 0],
    }
    input_index = [0, 1, 2]

    expected_output_features = Features({"index": Value("int64")})
    expected_output_data = {"index": [0, 0, 1]}


class TestSequenceChainInvalidTypes(BaseDataProcessorTest):
    processor_type = sequence.SequenceChain
    processor_config = sequence.SequenceChainConfig()
    input_features = Features(
        {
            "sequences": {
                "0": Sequence(Value("string")),
                "1": Sequence(Value("int32")),
            }
        }
    )
    expected_input_verification_error = RuntimeError


class TestSequenceChainNonConsecutiveIntegerIndex(BaseDataProcessorTest):
    processor_type = sequence.SequenceChain
    processor_config = sequence.SequenceChainConfig()
    input_features = Features(
        {
            "sequences": {
                "1": Sequence(Value("string")),
                "3": Sequence(Value("string")),
            }
        }
    )
    expected_input_verification_error = RuntimeError


class TestSequenceChainNonIntegerIndex(BaseDataProcessorTest):
    processor_type = sequence.SequenceChain
    processor_config = sequence.SequenceChainConfig()
    input_features = Features(
        {
            "sequences": {
                "a": Sequence(Value("string")),
                "b": Sequence(Value("string")),
            }
        }
    )
    expected_input_verification_error = RuntimeError


class TestSequenceChain(BaseDataProcessorTest):
    processor_type = sequence.SequenceChain
    processor_config = sequence.SequenceChainConfig()

    input_features = Features(
        {
            "sequences": {
                "0": Sequence(Value("int32")),
                "1": Sequence(Value("int32")),
            }
        }
    )
    input_data = {
        "sequences": [
            {
                "0": [1, 2, 3],
                "1": [4, 5, 6],
            }
        ]
    }
    input_index = [0]

    expected_output_features = Features({"result": Sequence(Value("int32"))})
    expected_output_data = {"result": [[1, 2, 3, 4, 5, 6]]}


class TestSequenceChain_FixedLength(BaseDataProcessorTest):
    processor_type = sequence.SequenceChain
    processor_config = sequence.SequenceChainConfig()

    input_features = Features(
        {
            "sequences": {
                "0": Sequence(Value("int32"), length=3),
                "1": Sequence(Value("int32"), length=3),
            }
        }
    )
    input_data = {
        "sequences": [
            {
                "0": [1, 2, 3],
                "1": [4, 5, 6],
            }
        ]
    }
    input_index = [0]

    expected_output_features = Features(
        {"result": Sequence(Value("int32"), length=6)}
    )
    expected_output_data = {"result": [[1, 2, 3, 4, 5, 6]]}


class TestSequenceZip(BaseDataProcessorTest):
    processor_type = sequence.SequenceZip
    processor_config = sequence.SequenceZipConfig()

    input_features = Features(
        {
            "sequences": {
                "0": Sequence(Value("int32"), length=4),
                "1": Sequence(Value("int32"), length=4),
            }
        }
    )
    input_data = {
        "sequences": [
            {
                "0": [0, 1, 2, 3],
                "1": [4, 5, 6, 7],
            }
        ]
    }
    input_index = [0]

    expected_output_features = Features(
        {"result": Sequence(Sequence(Value("int32"), length=2), length=4)}
    )
    expected_output_data = {"result": [[(0, 4), (1, 5), (2, 6), (3, 7)]]}

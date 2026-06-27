from app.pipeline.label_encoder import CategoricalEncoder
from app.pipeline.scaler import MinMaxStaticScaler

def test_label_encoding_maps_correctly():
    encoder = CategoricalEncoder()
    assert encoder.encode('gender', 'male') == 0
    assert encoder.encode('gender', 'female') == 1
    assert encoder.encode('cholesterol_level', 'high') == 2

def test_unknown_category_raises_error():
    encoder = CategoricalEncoder()
    try:
        encoder.encode('gender', 'unknown')
        assert False, "Should raise ValueError"
    except ValueError:
        assert True

def test_minmax_scaling_produces_0_to_1():
    scaler = MinMaxStaticScaler()
    # Age 18 -> min, Age 100 -> max
    assert scaler.scale('age', 18) == 0.0
    assert scaler.scale('age', 100) == 1.0
    
    # Value in between
    val = scaler.scale('age', 59)
    assert 0.0 < val < 1.0

def test_static_values_match_training_set():
    scaler = MinMaxStaticScaler()
    # Check some constraints
    assert scaler.params['systolic_bp']['min'] == 70
    assert scaler.params['systolic_bp']['max'] == 250

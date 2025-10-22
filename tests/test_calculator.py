def test_placeholder_calculator_imports():
    from app.calculator import Calculator
    assert hasattr(Calculator, "__doc__")

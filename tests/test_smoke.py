def test_packages_importable():
    import src.clean
    import src.collect

    assert src.clean and src.collect

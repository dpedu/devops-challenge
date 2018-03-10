from doctorapp.app import get_args


def test_get_args():
    """
    Simply test that we accept all the desired args
    """
    result = get_args(["-l", "127.0.0.1", "-p", "40000", "--debug"])
    assert result.listen == "127.0.0.1"
    assert result.port == 40000
    assert result.debug is True

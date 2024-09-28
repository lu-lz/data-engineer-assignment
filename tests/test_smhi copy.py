from smhi.smhi import SmhiParser


def test_check_connection():
    parser = SmhiParser()
    assert 200 == parser.check_connection()

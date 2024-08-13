"""Some general tests to ensure we're correclty setting up mocks and other supports for testing."""

from configparser import ConfigParser


# testing /mock/MockFileManager
def test_monkeypatch_open_read(mock_file_io, simpleconfig):
    filename = "somefile.txt"
    mock_file_io.write(filename, simpleconfig)

    parser = ConfigParser()
    parser.read(filename)
    assert parser.sections() == ["section"]


def test_monkeypatch_open_write(mock_file_io, simpleconfig):
    parser = ConfigParser()
    parser.add_section("section")
    parser.set("section", "key", "value")

    filename = "somefile.txt"
    parser.write(open(filename, "wb"))
    assert mock_file_io.read(filename) == simpleconfig

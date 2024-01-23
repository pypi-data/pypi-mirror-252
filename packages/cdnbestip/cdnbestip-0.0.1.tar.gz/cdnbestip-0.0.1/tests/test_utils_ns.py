from cdnbestip.utils.ns import extract_host_and_domain


def test_extract_host_and_domain():
    host, domain = extract_host_and_domain('www.example.com')
    assert host == 'www'
    assert domain == 'example.com'

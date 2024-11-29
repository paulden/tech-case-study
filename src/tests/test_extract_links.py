import unittest
from unittest.mock import patch, MagicMock

from src.url_extractor.extract_links import extract_links


class TestExtractLinks(unittest.TestCase):
    @patch("src.url_extractor.extract_links.requests")
    def test_extraction_should_fail_if_status_code_is_above_299(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests.get.return_value = mock_response

        self.assertRaises(ConnectionError, extract_links, "https://example.com")

    @patch("src.url_extractor.extract_links.requests")
    def test_extraction_should_return_links_from_html(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<!DOCTYPE html><html><body><h2>HTML Links</h2><p>HTML links are defined with the a tag:</p><a href="https://example.com/1">This is a link</a><a href="https://example.com/2">This is another link</a></body></html>'
        mock_requests.get.return_value = mock_response

        links = extract_links("https://example.com")

        self.assertEqual(links, ["https://example.com/1", "https://example.com/2"])

    @patch("src.url_extractor.extract_links.requests")
    def test_extraction_should_filter_out_links_unrelated_to_url(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<!DOCTYPE html><html><body><h2>HTML Links</h2><p>HTML links are defined with the a tag:</p><a href="https://example.com/1">This is a link</a><a href="https://external.com/1">This is an external link</a><a href="mailto:contact@example.com">Contact</a></body></html>'
        mock_requests.get.return_value = mock_response

        links = extract_links("https://example.com")

        self.assertEqual(links, ["https://example.com/1"])

    @patch("src.url_extractor.extract_links.requests")
    def test_extraction_should_keep_relative_links(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<!DOCTYPE html><html><body><h2>HTML Links</h2><p>HTML links are defined with the a tag:</p><a href="https://example.com/1">This is a link</a><a href="home">This is a relative link</a></body></html>'
        mock_requests.get.return_value = mock_response

        links = extract_links("https://example.com")

        self.assertEqual(links, ["https://example.com/1", "https://example.com/home"])

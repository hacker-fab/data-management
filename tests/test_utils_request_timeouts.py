"""Offline regression checks for bounded job queue API requests."""

import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


FAKE_REQUESTS = types.ModuleType("requests")
FAKE_REQUESTS.post = Mock()
FAKE_REQUESTS.put = Mock()
with patch.dict(sys.modules, {"requests": FAKE_REQUESTS}):
    spec = importlib.util.spec_from_file_location(
        "hackerfab_utils_under_test",
        Path(__file__).resolve().parents[1] / "data_management" / "utils.py",
    )
    utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils)


class TestRequestTimeouts(unittest.TestCase):
    def setUp(self):
        FAKE_REQUESTS.post.reset_mock()
        FAKE_REQUESTS.put.reset_mock()

    def test_generate_upload_url_has_timeout(self):
        response = Mock(status_code=200)
        response.json.return_value = {"upload_url": "https://example.test/upload", "s3_key": "sample"}
        FAKE_REQUESTS.post.return_value = response
        self.assertEqual(
            utils.get_file_upload_url_and_key("job-1"),
            ("https://example.test/upload", "sample"),
        )
        FAKE_REQUESTS.post.assert_called_once_with(
            f"{utils.JOB_QUEUE_BASE_URL}/generate_upload_url",
            json={"job_id": "job-1"}, timeout=utils.REQUEST_TIMEOUT,
        )

    def test_file_upload_has_timeout(self):
        FAKE_REQUESTS.put.return_value = Mock(status_code=200)
        payload = b"image-bytes"
        utils.upload_file(payload, "https://example.test/upload")
        FAKE_REQUESTS.put.assert_called_once_with(
            "https://example.test/upload", data=payload,
            timeout=utils.REQUEST_TIMEOUT,
        )

    def test_enqueue_has_timeout(self):
        response = Mock(status_code=200)
        response.json.return_value = {"job_id": "job-2"}
        FAKE_REQUESTS.post.return_value = response
        self.assertEqual(
            utils.enqueue_job("spincoater", {"rpm": 100}, 1),
            (response, "job-2"),
        )
        FAKE_REQUESTS.post.assert_called_once_with(
            f"{utils.JOB_QUEUE_BASE_URL}/jobs",
            json={"machine": "spincoater", "input_parameters": {"rpm": 100}, "priority": 1},
            timeout=utils.REQUEST_TIMEOUT,
        )


if __name__ == "__main__":
    unittest.main()

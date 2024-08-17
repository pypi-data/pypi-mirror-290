import unittest
from unittest.mock import patch, MagicMock
from resk.openai_protector import OpenAIProtector

class TestOpenAIProtector(unittest.TestCase):

    def setUp(self):
        self.protector = OpenAIProtector(model="gpt-4o", preserved_prompts=2)

    def test_sanitize_input(self):
        input_text = "<script>alert('XSS')</script>Hello<endoftext>"
        sanitized = self.protector.sanitize_input(input_text)
        self.assertEqual(sanitized, "&lt;script&gt;alert('XSS')&lt;/script&gt;Hello")

    def test_close_html_tags(self):
        input_text = "<p>Unclosed paragraph<div>Nested <b>bold"
        closed = self.protector._close_html_tags(input_text)
        self.assertEqual(closed, "<p>Unclosed paragraph<div>Nested <b>bold</b></div></p>")

    def test_truncate_text(self):
        long_text = "a" * (self.protector.max_context_length * 5)
        truncated = self.protector._truncate_text(long_text)
        self.assertEqual(len(truncated), self.protector.max_context_length * 4)

    def test_manage_sliding_context(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
        ]
        managed = self.protector.manage_sliding_context(messages)
        self.assertEqual(len(managed), 4)  # 2 preserved + 2 most recent
        self.assertEqual(managed[0], messages[0])
        self.assertEqual(managed[1], messages[1])
        self.assertEqual(managed[-2], messages[-2])
        self.assertEqual(managed[-1], messages[-1])

    @patch('openai.ChatCompletion.create')
    def test_protect_openai_call(self, mock_create):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message={"content": "Test response"})]
        mock_create.return_value = mock_response

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello<endoftext>"},
        ]

        response = self.protector.protect_openai_call(
            mock_create,
            model="gpt-4o",
            messages=messages
        )

        self.assertEqual(response.choices[0].message["content"], "Test response")
        mock_create.assert_called_once()
        called_args = mock_create.call_args[1]
        self.assertEqual(called_args['model'], "gpt-4o")
        self.assertEqual(len(called_args['messages']), 2)
        self.assertNotIn("<endoftext>", called_args['messages'][1]['content'])

if __name__ == '__main__':
    unittest.main()
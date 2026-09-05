import importlib.util
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "presentations" / "gpt-image2-ppt" / "scripts"


def load_module(name):
    specification = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(specification)
    with patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
        specification.loader.exec_module(module)
    return module


class PptSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_module("generate_ppt")
        cls.renderer = load_module("render_template")

    def test_explicit_environment_wins(self):
        environment = {
            "OPENAI_BASE_URL": "https://explicit.example.invalid/v1",
            "OPENAI_API_KEY": "fixture-explicit",
            "JULING_GPT_IMAGE2_BASE_URL": "https://fallback.example.invalid/v1",
            "JULING_GPT_IMAGE2_API_KEY": "fixture-fallback",
        }
        with patch.dict(os.environ, environment, clear=True), patch.object(self.generator, "_load_scoped_env_files"):
            self.generator.load_skill_env()
            self.assertEqual(os.environ["OPENAI_API_KEY"], "fixture-explicit")
            self.assertEqual(os.environ["OPENAI_BASE_URL"], environment["OPENAI_BASE_URL"])

    def test_alias_fills_missing_configuration(self):
        with patch.dict(os.environ, {"JULING_GPT_IMAGE2_API_KEY": "fixture-fallback"}, clear=True), patch.object(self.generator, "_load_scoped_env_files"):
            self.generator.load_skill_env()
            self.assertEqual(os.environ["OPENAI_API_KEY"], "fixture-fallback")

    def test_platform_configuration_precedes_alias(self):
        environment = {
            "gpt-image2-ppt_OPENAI_API_KEY": "fixture-platform",
            "JULING_GPT_IMAGE2_API_KEY": "fixture-fallback",
        }
        with patch.dict(os.environ, environment, clear=True), patch.object(self.generator, "_load_scoped_env_files"):
            self.generator.load_skill_env()
            self.assertEqual(os.environ["OPENAI_API_KEY"], "fixture-platform")

    def check_renderer(self, conversion_error=None):
        presentation = Mock()
        presentation.slide_layouts = [None] * 7
        pptx = types.SimpleNamespace(Presentation=Mock(return_value=presentation))
        with patch.dict(sys.modules, {"pptx": pptx}), patch.object(sys, "platform", "linux"), patch.object(self.renderer, "_find_libreoffice", return_value="fixture-soffice"), patch.object(self.renderer, "_convert_pptx_to_pdf", side_effect=conversion_error) as convert:
            result = self.renderer.check_render_backend()
            convert.assert_called_once()
            presentation.save.assert_called_once()
        return result

    def test_renderer_requires_conversion(self):
        valid, messages = self.check_renderer()
        self.assertTrue(valid)
        self.assertTrue(any("real conversion" in message for message in messages))

    def test_broken_renderer_is_not_ready(self):
        valid, messages = self.check_renderer(RuntimeError("fixture conversion failure"))
        self.assertFalse(valid)
        self.assertTrue(any("fixture conversion failure" in message for message in messages))


if __name__ == "__main__":
    unittest.main()

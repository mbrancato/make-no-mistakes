import tempfile
import unittest
from pathlib import Path

from scripts import generate_agents as generator


class GenerateAgentsTests(unittest.TestCase):
    def write_guide(self, root, identifier, category, requires=""):
        language = "\nlanguage: go" if category == "language" else ""
        required = f"\nrequires: [{requires}]" if requires else ""
        (root / f"AGENTS.{identifier}.md").write_text(
            f"---\nid: {identifier}\ntitle: {identifier.title()}\nsummary: {identifier} guide\n"
            f"category: {category}{language}{required}\n---\n\n# {identifier.title()}\n\nBody.\n",
            encoding="utf-8",
        )

    def test_resolves_dependencies_and_renders_category_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "go", "language", "testing")
            self.write_guide(root, "testing", "testing", "process")
            self.write_guide(root, "process", "process")
            guides = generator.discover_guides(root, root / "AGENTS.md")
            selected = generator.resolve_selection(guides, ["go"])
            self.assertEqual([guide.id for guide in selected], ["process", "testing", "go"])
            rendered = generator.render(selected, False)
            self.assertNotIn("generator-version", rendered)
            self.assertLess(rendered.index("## Process"), rendered.index("## Testing"))
            self.assertIn("## Go", rendered)

    def test_includes_a_header_automatically(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "all", "header")
            self.write_guide(root, "process", "process")
            guides = generator.discover_guides(root, root / "AGENTS.md")
            selected = generator.resolve_selection(guides, ["process"])
            self.assertEqual([guide.id for guide in selected], ["all", "process"])
            self.assertTrue(generator.render(selected, False).startswith("# All\n\nBody."))

    def test_async_python_includes_general_python_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "python", "language")
            self.write_guide(root, "py-async", "language", "python")
            self.write_guide(root, "py-pytest", "language")
            guides = generator.discover_guides(root, root / "AGENTS.md")
            selected = generator.resolve_selection(guides, ["py-async", "py-pytest"])
            self.assertEqual(
                [guide.id for guide in selected],
                ["py-async", "py-pytest", "python"],
            )

    def test_rejects_duplicate_ids_and_missing_language(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "one", "process")
            self.write_guide(root, "two", "process")
            (root / "AGENTS.two.md").write_text((root / "AGENTS.one.md").read_text(), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate guide id"):
                generator.discover_guides(root, root / "AGENTS.md")
            (root / "AGENTS.two.md").write_text(
                "---\nid: two\ntitle: Two\nsummary: Two guide\ncategory: language\n---\n\n# Two\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "require language"):
                generator.discover_guides(root, root / "AGENTS.md")

import tempfile
import unittest
from pathlib import Path

from scripts import generate_agents as generator


class GenerateAgentsTests(unittest.TestCase):
    def write_guide(
        self, root, identifier, category, requires="", title=None, body=None, language_value="go"
    ):
        language = f"\nlanguage: {language_value}" if category == "language" else ""
        required = f"\nrequires: [{requires}]" if requires else ""
        guide_title = title or identifier.title()
        guide_body = body or f"# {guide_title}\n\nBody.\n"
        (root / f"AGENTS.{identifier}.md").write_text(
            f"---\nid: {identifier}\ntitle: {guide_title}\nsummary: {identifier} guide\n"
            f"category: {category}{language}{required}\n---\n\n{guide_body}",
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
                ["python", "py-async", "py-pytest"],
            )

    def test_groups_language_guides_by_base_language(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "py-unittest", "language", language_value="python-unittest")
            self.write_guide(root, "go", "language", language_value="go")
            self.write_guide(root, "py-async", "language", language_value="python-async")
            self.write_guide(root, "python", "language", language_value="python")
            self.write_guide(root, "py-pytest", "language", language_value="python-pytest")
            guides = generator.discover_guides(root, root / "AGENTS.md")

            selected = generator.resolve_selection(
                guides, ["py-unittest", "go", "py-async", "python", "py-pytest"]
            )

            self.assertEqual(
                [guide.id for guide in selected],
                ["go", "python", "py-async", "py-pytest", "py-unittest"],
            )

    def test_renders_category_owned_headings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(
                root,
                "architecture",
                "structure",
                title="Clean Architecture",
                body="# Layout\n\n## Dependencies\n",
            )
            self.write_guide(
                root,
                "test-design",
                "testing",
                title="Test Design",
                body="# Test Design\n\n## Assertions\n",
            )
            self.write_guide(
                root,
                "logging",
                "observability",
                title="Structured Logging",
                body="# Structured Logging\n\n## Fields\n",
            )
            guides = generator.discover_guides(root, root / "AGENTS.md")
            rendered = generator.render(
                generator.resolve_selection(guides, ["architecture", "test-design", "logging"]),
                False,
            )
            self.assertIn("## Code Structure\n\n### Layout\n\n#### Dependencies", rendered)
            self.assertIn("## Testing\n\n### Test Design\n\n#### Assertions", rendered)
            self.assertIn(
                "## Observability and Operations\n\n### Structured Logging\n\n#### Fields",
                rendered,
            )
            self.assertNotIn("section_title", rendered)

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

    def test_rejects_cyclic_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "one", "process", "two")
            self.write_guide(root, "two", "testing", "one")

            with self.assertRaisesRegex(ValueError, "cyclic guide dependency: one -> two -> one"):
                generator.discover_guides(root, root / "AGENTS.md")

    def test_renders_dependencies_before_selected_guides(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "base", "process")
            self.write_guide(root, "feature", "process", "base")
            guides = generator.discover_guides(root, root / "AGENTS.md")

            selected = generator.resolve_selection(guides, ["feature"])

            self.assertEqual([guide.id for guide in selected], ["base", "feature"])

    def test_allows_multiple_process_guides(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "first", "process")
            self.write_guide(root, "second", "process")
            guides = generator.discover_guides(root, root / "AGENTS.md")

            selected = generator.resolve_selection(guides, ["first", "second"])

            self.assertEqual({guide.id for guide in selected}, {"first", "second"})

    def test_allows_multiple_cross_cutting_guides(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "resilience", "guidance")
            self.write_guide(root, "security", "guidance")
            guides = generator.discover_guides(root, root / "AGENTS.md")

            selected = generator.resolve_selection(guides, ["resilience", "security"])

            self.assertEqual({guide.id for guide in selected}, {"resilience", "security"})

    def test_uses_parentheses_for_one_of_categories(self):
        self.assertEqual(generator.selection_marker("structure", True), "(x)")
        self.assertEqual(generator.selection_marker("structure", False), "( )")

    def test_uses_brackets_for_multi_select_categories(self):
        self.assertEqual(generator.selection_marker("guidance", True), "[x]")
        self.assertEqual(generator.selection_marker("guidance", False), "[ ]")

    def test_rejects_multiple_structure_guides(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "first", "structure")
            self.write_guide(root, "second", "structure")
            guides = generator.discover_guides(root, root / "AGENTS.md")

            with self.assertRaisesRegex(ValueError, "allows only one selected guide"):
                generator.resolve_selection(guides, ["first", "second"])

    def test_selects_vertical_slice_as_the_structure_guide(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "clean-layered", "structure")
            self.write_guide(
                root,
                "vertical-slice",
                "structure",
                title="Vertical Slice Architecture",
                body="# Feature-Oriented Organization\n\n- Keep features cohesive.\n",
            )
            guides = generator.discover_guides(root, root / "AGENTS.md")

            selected = generator.resolve_selection(guides, ["vertical-slice"])
            rendered = generator.render(selected, False)

            self.assertEqual([guide.id for guide in selected], ["vertical-slice"])
            self.assertIn("### Feature-Oriented Organization", rendered)

    def test_validates_required_categories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "process", "process")
            guides = generator.discover_guides(root, root / "AGENTS.md")

            with self.assertRaisesRegex(ValueError, "requires a guide from: structure"):
                generator.validate_required_selection(guides, ["process"])

    def test_supports_explicit_body_rendering_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(root, "body", "process")
            guide_path = root / "AGENTS.body.md"
            guide_path.write_text(
                guide_path.read_text(encoding="utf-8").replace(
                    "category: process", "category: process\nrender: body"
                ),
                encoding="utf-8",
            )
            guides = generator.discover_guides(root, root / "AGENTS.md")

            rendered = generator.render(generator.resolve_selection(guides, ["body"]), False)

            self.assertEqual(rendered.count("Body"), 2)
            self.assertIn("### Body", rendered)

    def test_preserves_bulleted_directives_in_generated_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_guide(
                root,
                "rules",
                "process",
                body="# Rules\n\n- First directive.\n- Second directive.\n",
            )
            guides = generator.discover_guides(root, root / "AGENTS.md")

            rendered = generator.render(generator.resolve_selection(guides, ["rules"]), False)

            self.assertIn("- First directive.\n- Second directive.", rendered)

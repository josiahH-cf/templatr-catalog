# Contributing to the Templatr Catalog

Thank you for sharing your prompts with the community!

## Before You Start

- Read the [README](README.md) for the catalog format and template file format.
- Test your template locally using `/import` in Templatr before submitting.
- Check existing templates so you are not duplicating something already present.

## Submission Process

1. **Fork** `josiahH-cf/templatr-catalog`.
2. Create a branch: `git checkout -b add/your-template-name`.
3. Add your template file to `templates/` using lowercase snake_case naming (`my_template.json`).
4. Add an entry to `catalog.json` — all required fields must be present (see README).
5. Run the generation script locally to verify the catalog is valid:
   ```
   python scripts/generate_catalog.py
   ```
6. Commit and push your branch, then open a Pull Request against `main`.

## PR Guidelines

- **One template per PR** whenever possible. Multiple closely related templates in a single PR are fine with explanation.
- Write a brief PR description: what the template does, what model/use-case it targets, and what you tested.
- The PR title should be: `Add: <Template Name>` (e.g. `Add: Code Review Checklist`).

## Quality Standards

Templates must:

- Produce useful, non-trivial output (not a simple echo or hello-world prompt).
- Work correctly with at least one open-weight model (e.g. Llama 3, Mistral, Phi).
- Not contain personal data, secrets, offensive content, or copyrighted material.
- Use `{{variable_name}}` syntax for any dynamic input — do not hardcode placeholder text as static content.

## Versioning

Bump the `version` field in your `catalog.json` entry (semver) whenever you update a template after initial submission. This helps users know when a template has changed.

## Review

Maintainers will review your PR for quality, format compliance, and uniqueness. We may request changes before merging. Reviews are done on a best-effort basis.

## Reporting Issues

If a catalog template is broken, outdated, or inappropriate, please open a GitHub issue with:
- Template name
- Description of the problem
- Steps to reproduce (if relevant)

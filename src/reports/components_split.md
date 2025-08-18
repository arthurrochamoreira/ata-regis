# Component Split Report

## Import Mapping
- `ui.tokens.primary_button` → `components.PrimaryButton`
- `ui.tokens.secondary_button` → `components.SecondaryButton`
- `ft.IconButton` in tables → `components.IconAction`
- `ft.TextField` in forms and search → `components.TextInput`

## Removed Local Styles
- Icon button hover styles moved to `components.button.style`.
- Text field borders and focus styles centralized in `components.input.style`.

## New Tokens
- None added; existing tokens from `theme` reused throughout.

Pending: table and badge components are available but not yet adopted across all screens.

# Garden tracker design checklist

This project uses [Checklist Design](https://www.checklist.design/browse) as a
review framework and shadcn-vue as its UI component foundation. Apply only the
items relevant to the screen or flow being changed.

## Every screen

- Give the page one clear title and one obvious primary action.
- Keep navigation position, labels, and active state consistent.
- Make the layout usable at narrow mobile widths without horizontal scrolling.
- Preserve visible keyboard focus and logical tab order.
- Use meaningful headings, landmarks, labels, and button text.
- Avoid icon-only actions unless they have an accessible name.

## Data and content

- Show a skeleton or progress state while initial data loads.
- Provide an intentional empty state that explains what is missing.
- Offer a useful next action from empty states.
- Keep partial data usable instead of hiding an entire screen.
- Use readable dates, units, status labels, and garden terminology.

## Forms

- Pair every control with a persistent label.
- Mark required information and use sensible initial values.
- Match control types to the data: dates, numbers, selects, and text areas.
- Disable submission while a request is in progress.
- Keep entered values when a recoverable submission fails.
- Put specific validation or API errors near the form.
- Confirm successful saves without forcing the user to infer them.

## Buttons and actions

- Use one primary button per local task area.
- Use secondary, outline, ghost, and destructive variants consistently.
- Start labels with clear verbs such as “Add”, “Save”, “Complete”, or “Record”.
- Disable unavailable actions and explain the prerequisite nearby.
- Give destructive or irreversible actions an explicit confirmation.

## Dialogs

- Use shadcn-vue `Dialog` for focused desktop tasks.
- Give every dialog a title and short description.
- Move focus into the dialog and return it to the trigger on close.
- Allow Escape and the close control to dismiss non-destructive dialogs.
- Keep forms short; use a page when the task becomes multi-step.

## Feedback

- Show errors in plain language and state how to recover.
- Give immediate success feedback after create, update, complete, and harvest
  actions.
- Do not use color as the only indication of status or failure.
- Keep loading, empty, error, success, and disabled states visually distinct.

## Feature review

Before considering a UI feature complete:

1. Walk its happy path with realistic garden data.
2. Check loading, empty, error, success, and disabled states.
3. Test keyboard-only operation.
4. Test a narrow mobile viewport and a desktop viewport.
5. Run `npm run typecheck` and `npm run build`.


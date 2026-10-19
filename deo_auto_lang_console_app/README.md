# DEO AutoLang Console

Operations console for catalog curators and reviewers. This folder is reserved for the first console UI.

The API intentionally has no review, publish, or admin endpoints yet. Before creating those actions, implement sign-in, role-based authorization, audit history, and the two-person review rule required by the product specification. Do not expose the local MVP request store on a public network.

Planned first workflow: view submitted configuration requests, create a draft catalog entry, request technical review, and publish only after a different reviewer approves it.

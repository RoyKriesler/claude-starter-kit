---
name: feedback-verify-before-claiming-fixed
description: Never say a UI or visual bug is fixed without a screenshot of the live rendered output
metadata:
  type: feedback
---
Reading source code is not proof a visual bug is gone. CSS, 3D scenes and runtime composition produce artefacts invisible in source.

**Why:** a "fixed, just redeploy" claim based on code inspection is often wrong; the screenshot afterwards shows the bug still there.

**How to apply:** after any UI fix or deploy, take a Playwright or browser screenshot of the live URL and look at it before reporting. Repeat until it matches. If verification is impossible, say so. Related: [[feedback-test-before-delivery]].

# Iteration

## What went wrong

The Crossyroad checker marked right-facing as MET even though its screenshot didn't show the character. When I asked for evidence, it admitted, “The right-facing pose was never visible, so the left/right requirement should have been UNVERIFIED.”

## Why it happened

The checker used the game's internal direction values to assume the character looked correct. The skill didn't clearly require visible evidence for appearance or a separate check for every direction.

## What I changed

I updated the skill to require clear screenshots for visual requirements, retry unclear captures, and mark anything it still couldn't judge as UNVERIFIED. I also required every case to pass before marking a whole requirement MET.

## Rerun

I reran the check in a fresh chat. It captured all eight keys and retook shots where the character was cut off. It marked all requirements MET with screenshot references. I checked the screenshots and agreed with the revised results.

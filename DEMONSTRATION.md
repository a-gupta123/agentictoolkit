# Demonstration

## Task
I used the MCP tool to find requirements for Movie Recommender and Crossyroad, then ran the checker on each live site in a fresh chat.

## Run 1 — Movie Recommender

The MCP searches included `movie filters`, `Find Movies`, and `no movies`. The reply found this requirement in `/Users/gupta/Movie Recommender/README.md`: “The form asks for genre, mood, rating, and year; only one of those is required.” The checker tested the blank form, Comedy with Funny, rating 7+, and years 2015–2024, then Documentary with rating 8+ and year 1902. It marked all three MET. Its report included “Please choose at least one filter,” “Showing 8 popular titles with at least 50 ratings,” and “No movies matched those filters.” I checked the screenshots and agreed with the results.

## Run 2 — Crossyroad

The MCP searches included `WASD`, `direction it jumps`, and `opposite direction`. The reply found this in `/Users/gupta/crossyroad/prompt_log.md`: “I want a chicken that can jump forward, sideways, and backwards using the arrows or WASD keys.” The checker pressed ArrowUp, ArrowLeft, ArrowRight, ArrowDown, W, A, D, and S and initially marked movement and facing as MET. When I asked for its evidence, it admitted, “The right-facing pose was never visible, so the left/right requirement should have been UNVERIFIED.” I updated the skill to require clear visual evidence and reran it in a fresh chat. The checker reported, “Reframed ArrowDown and S when the first crop cut off the body, then judged the full character.” It marked all requirements MET and cited captures for every key, including `03-arrow-right.png` and `07-d-right.png`. I checked the screenshots and agreed with the revised results.

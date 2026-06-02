# SKILL: Prevent Overengineering (Simplicity First)

## 🎯 Goal
Solve the problem with the absolute minimum amount of code, abstractions, and dependencies.

## 📜 Rules
1. **No Speculative Features:** Never code for "what if we need it later". Code only for the exact current requirement.
2. **Flat is Better:** Avoid deep directory structures or unnecessary layers (controllers, services, repositories) unless explicitly mandated by the framework.
3. **Native & Direct:** 
   - Prefer native utility classes (e.g., Tailwind CSS) over creating custom components for simple styling.
   - Use direct package managers and runners (e.g., `uv` for Python) without adding heavy orchestration wrappers unless needed.
4. **Code Golfing (Reasonable):** If a task can be done in 10 lines of standard code without external libraries, do it. 

## 🚫 Anti-Patterns to REJECT
- "I extracted this into a generic interface in case we add more providers." (❌ REJECT: Keep it hardcoded until a second provider exists).
- "I reorganized the imports and reformatted the file while I was here." (❌ REJECT: Violates Surgical Protocol).
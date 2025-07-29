# Strict Test-Driven Development (TDD) Pattern

## Overview
This document defines the MANDATORY Test-Driven Development methodology for ALL projects in this repository. TDD is not optional - it is a fundamental requirement that ensures code quality, maintainability, and correctness.

## Core TDD Cycle: Red-Green-Refactor

### The Sacred Three Steps
1. **RED**: Write a failing test FIRST
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve the code while keeping tests green

**CRITICAL**: You MUST follow this cycle for EVERY piece of functionality. No exceptions.

## Detailed TDD Process

### Step 1: Think and Plan (Before Writing Any Test)
Before writing any test, you MUST:
1. **Understand the requirement completely**
   - What is the expected behavior?
   - What are the edge cases?
   - What are the error conditions?
   - What are the performance requirements?

2. **Design the interface first**
   - How will this code be used?
   - What is the most intuitive API?
   - What makes sense from the caller's perspective?

3. **Plan your test cases**
   - Happy path scenarios
   - Edge cases
   - Error conditions
   - Boundary conditions

### Step 2: Write the Test (RED Phase)
```
REMEMBER: The test MUST fail initially. If it passes without implementation, your test is wrong.
```

1. **Start with the test file**
   - Create test file BEFORE implementation file
   - Name it according to project conventions (e.g., `test_*.py`, `*.test.js`, `*_test.go`)

2. **Write descriptive test names**
   - Test names should describe WHAT is being tested and EXPECTED behavior
   - Examples:
     - `test_user_creation_with_valid_email_succeeds()`
     - `test_divide_by_zero_raises_exception()`
     - `test_cache_returns_none_for_expired_entries()`

3. **Follow the AAA pattern**
   - **Arrange**: Set up test data and conditions
   - **Act**: Execute the functionality being tested
   - **Assert**: Verify the expected outcome

4. **Run the test and ensure it FAILS**
   - If it passes, your test is incorrect
   - The failure message should be meaningful

### Step 3: Write Implementation (GREEN Phase)
```
CRITICAL: Write ONLY enough code to make the test pass. Do not add extra functionality.
```

1. **Create the minimal implementation**
   - Resist the urge to add features not required by current test
   - It's OK if the code is ugly at this stage
   - Focus ONLY on making the test pass

2. **Run the test**
   - Must see it go from RED to GREEN
   - If still failing, fix the implementation (not the test!)

3. **Commit immediately**
   - As soon as test passes, commit your work
   - Use meaningful commit messages like "Add: user email validation"

### Step 4: Refactor (REFACTOR Phase)
```
Only refactor when tests are GREEN. Never refactor with failing tests.
```

1. **Improve code quality**
   - Remove duplication
   - Improve naming
   - Simplify logic
   - Extract methods/functions
   - Apply design patterns if needed

2. **Run tests after EVERY change**
   - Even the smallest refactoring can break functionality
   - Tests are your safety net

3. **Keep refactoring atomic**
   - One improvement at a time
   - Commit after each successful refactoring

## Coverage Requirements

### Minimum Coverage Standards
- **Overall Coverage**: Minimum 80%
- **Critical Path Coverage**: 100% (authentication, payments, data integrity)
- **New Code Coverage**: 90% minimum for all new features
- **Branch Coverage**: Minimum 75%

### What to Test
1. **All public interfaces**
2. **Edge cases and boundaries**
3. **Error conditions and exceptions**
4. **Integration points**
5. **State changes**
6. **Async operations**

### What NOT to Test
1. **Third-party libraries** (unless wrapping them)
2. **Language features** (e.g., getters/setters)
3. **Configuration files**
4. **Pure UI styling**

## Language-Agnostic Testing Principles

### Test Structure Guidelines
Regardless of language, maintain:
1. **Isolation**: Tests should not depend on each other
2. **Repeatability**: Tests must produce same results every time
3. **Speed**: Unit tests should be fast (< 100ms per test)
4. **Clarity**: Test intent should be obvious

### Mocking and Stubbing
1. **Mock external dependencies**
   - Databases
   - File systems
   - Network calls
   - Third-party services

2. **Use test doubles appropriately**
   - Dummy: Passed around but never used
   - Stub: Provides canned responses
   - Spy: Records how it was called
   - Mock: Pre-programmed with expectations
   - Fake: Working implementation for testing

## Common TDD Mistakes to Avoid

### Fatal Mistakes
1. **Writing implementation before tests** - This defeats the entire purpose
2. **Writing multiple tests before implementation** - Work in small cycles
3. **Not running tests to see them fail** - You can't trust a test you haven't seen fail
4. **Changing tests to make them pass** - Fix the implementation, not the test
5. **Skipping the refactor phase** - Technical debt accumulates quickly

### Quality Mistakes
1. **Testing implementation details** - Test behavior, not internals
2. **Creating overly complex tests** - If test is hard to write, design is probably wrong
3. **Inadequate test naming** - Names should document expected behavior
4. **Ignoring test maintenance** - Tests need refactoring too
5. **Not testing edge cases** - This is where bugs hide

## Enforcing TDD in Projects

### Pre-commit Hooks
Every project MUST include:
```yaml
- repo: local
  hooks:
    - id: test-coverage
      name: Check test coverage
      entry: <language-specific-coverage-command>
      language: system
      pass_filenames: false
      always_run: true
```

### CI/CD Pipeline Requirements
1. **Run all tests on every commit**
2. **Block merging if tests fail**
3. **Block merging if coverage drops below threshold**
4. **Generate coverage reports**
5. **Track coverage trends over time**

## TDD Workflow Integration

### With Version Control
1. **Commit after each RED-GREEN-REFACTOR cycle**
2. **Use conventional commits**:
   - `test: add test for user validation`
   - `feat: implement user validation`
   - `refactor: extract validation logic`

### With Code Review
1. **Tests are reviewed as rigorously as implementation**
2. **Reviewers should verify**:
   - Test completeness
   - Test clarity
   - Edge case coverage
   - No testing of implementation details

## Practical TDD Example

### Step-by-step TDD Demonstration
```
Requirement: Create a function that calculates the factorial of a number
```

1. **First Test (Simplest Case)**:
   ```
   Test: factorial(0) should return 1
   - Write test
   - Run test (FAILS - function doesn't exist)
   - Implement: def factorial(n): return 1
   - Run test (PASSES)
   - Commit
   ```

2. **Second Test (Next Simplest)**:
   ```
   Test: factorial(1) should return 1
   - Write test
   - Run test (PASSES - already works!)
   - No implementation needed
   ```

3. **Third Test (Force Generalization)**:
   ```
   Test: factorial(5) should return 120
   - Write test
   - Run test (FAILS - returns 1)
   - Implement: proper factorial logic
   - Run test (PASSES)
   - Refactor: improve algorithm
   - Run all tests (ALL PASS)
   - Commit
   ```

4. **Edge Cases**:
   ```
   Test: factorial(-1) should raise ValueError
   Test: factorial(1.5) should raise TypeError
   Test: factorial(None) should raise TypeError
   ```

## Remember: TDD is a Discipline

**Think Long and Hard**: Before writing any code, think through the problem systematically.

**Step by Step**: One test, one implementation, one refactoring at a time.

**Ask Questions**: If requirements are unclear, ASK before writing tests.

**Update Understanding**: As you learn more about the problem, update your tests.

**Use Subagents**: For complex test scenarios, use subagents to explore edge cases.

---

## Final Reminder
TDD is not about testing. TDD is about DESIGN. The tests are a beneficial side effect. The real value is in thinking through your design before implementing it.

**If you're not doing TDD, you're not following the project standards.**
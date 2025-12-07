# Stock Portfolio Kanban Tracker - Production Refactor Plan

## Phase 1: Code Architecture Refactoring ⚙️
- [ ] Create modular component structure in `app/components/`
  - [ ] `app/components/stock_card.py` - Draggable stock card component
  - [ ] `app/components/stage_column.py` - Droppable stage column component
  - [ ] `app/components/modals.py` - All modal components (confirmation, force, add, detail, ocean)
  - [ ] `app/components/header.py` - Application header with search and filters
- [ ] Split state logic into separate files
  - [ ] `app/states/base_state.py` - Base application state (app config, user settings)
  - [ ] Keep `app/states/kanban_state.py` - Board-specific logic
- [ ] Create page layouts in `app/pages/`
  - [ ] `app/pages/dashboard.py` - Main Kanban board page
- [ ] Add comprehensive type hints and docstrings to all functions
- [ ] Update `app/app.py` to import from new modular structure

---

## Phase 2: Mobile-First Responsive Design 📱
- [ ] Implement responsive header with hamburger menu on mobile
- [ ] Create mobile column switcher (tabs or vertical accordion)
- [ ] Desktop: Horizontal scrolling Kanban columns (current behavior)
- [ ] Mobile (<768px): Tab-based column view OR vertical stack
- [ ] Ensure all touch targets are minimum 44x44px
- [ ] Move action buttons to bottom "thumb zone" on mobile
- [ ] Add responsive breakpoints using Tailwind classes
- [ ] Test drag-and-drop works on touch devices

---

## Phase 3: CSV Export Feature 📊
- [ ] Add "Export CSV" button to header
- [ ] Create `export_to_csv()` event handler in KanbanState
- [ ] Generate CSV with columns: Stock ID, Ticker, Company Name, Current Stage, Days in Stage, Last Updated
- [ ] Implement download functionality using rx.download()
- [ ] Add loading state during export generation

---

## Phase 4: Automated Testing Suite 🧪
- [ ] Create `tests/` directory structure
- [ ] Create `tests/test_logic.py` with pytest tests
- [ ] Test 1: Valid transition validation (forward progress)
- [ ] Test 2: Invalid transition validation (Ocean -> Live Deal blocked unless forced)
- [ ] Test 3: Tracker accuracy (TransitionLog creation on move)
- [ ] Test 4: days_in_stage calculation with timezone handling
- [ ] Create `tests/test_state.py` for state management tests
- [ ] Add pytest configuration and dependencies

---

## Phase 5: Documentation & Configuration 📚
- [ ] Create comprehensive `README.md` with:
  - [ ] Installation instructions
  - [ ] Architecture overview (folder structure)
  - [ ] Audit Trail logic explanation (StateTransitionLog/TransitionLog)
  - [ ] Mobile design decisions and responsive behavior
  - [ ] Usage guide with screenshots
  - [ ] Development and testing instructions
- [ ] Add environment variable support (DATABASE_URL placeholder for future)
- [ ] Create `.env.example` file with required variables
- [ ] Add inline code comments for complex logic

---

## Phase 6: UI Verification - Production Readiness ✅
- [ ] Test desktop layout (horizontal Kanban board)
- [ ] Test mobile layout (responsive columns/tabs)
- [ ] Test CSV export generates correct data
- [ ] Test touch interactions on mobile viewport
- [ ] Verify all modals work on mobile screens
- [ ] Test hamburger menu navigation
- [ ] Run pytest suite and verify all tests pass
- [ ] Verify documentation accuracy
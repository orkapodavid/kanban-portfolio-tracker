# Stock Portfolio Kanban Tracker - Production Refactor Plan

## Phase 1: Code Architecture Refactoring ✅
- [x] Create modular component structure in `app/components/`
  - [x] `app/components/stock_card.py` - Draggable stock card component
  - [x] `app/components/stage_column.py` - Droppable stage column component
  - [x] `app/components/modals.py` - All modal components (confirmation, force, add, detail, ocean)
  - [x] `app/components/header.py` - Application header with search and filters
- [x] Split state logic into separate files
  - [x] `app/states/base_state.py` - Base application state (app config, user settings)
  - [x] Keep `app/states/kanban_state.py` - Board-specific logic
- [x] Create page layouts in `app/pages/`
  - [x] `app/pages/dashboard.py` - Main Kanban board page
- [x] Add comprehensive type hints and docstrings to all functions
- [x] Update `app/app.py` to import from new modular structure

---

## Phase 2: Mobile-First Responsive Design ✅
- [x] Implement responsive header with hamburger menu on mobile
- [x] Create mobile column switcher (tabs or vertical accordion)
- [x] Desktop: Horizontal scrolling Kanban columns (current behavior)
- [x] Mobile (<768px): Tab-based column view OR vertical stack
- [x] Ensure all touch targets are minimum 44x44px
- [x] Move action buttons to bottom "thumb zone" on mobile
- [x] Add responsive breakpoints using Tailwind classes
- [x] Test drag-and-drop works on touch devices

---

## Phase 3: CSV Export Feature ✅
- [x] Add "Export CSV" button to header
- [x] Create `export_to_csv()` event handler in KanbanState
- [x] Generate CSV with columns: Stock ID, Ticker, Company Name, Current Stage, Days in Stage, Last Updated
- [x] Implement download functionality using rx.download()
- [x] Add loading state during export generation

---

## Phase 4: Automated Testing Suite 🧪
- [ ] Create `tests/` directory structure
- [ ] Create `tests/test_logic.py` with pytest tests
  - [ ] Test 1: Valid transition validation (forward progress)
  - [ ] Test 2: Invalid transition validation (Ocean -> Live Deal blocked unless forced)
  - [ ] Test 3: Tracker accuracy (TransitionLog creation on move)
  - [ ] Test 4: days_in_stage calculation with timezone handling
- [ ] Create `tests/test_state.py` for state management tests
- [ ] Add pytest configuration to requirements.txt

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
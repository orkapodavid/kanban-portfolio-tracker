# Stock Portfolio Kanban Tracker - Implementation Plan

## Phase 1: Database Models and State Management ✅
- [x] Create Stock model (ticker PK, company_name, status, last_updated)
- [x] Create TransitionLog model (id PK, ticker FK, previous_stage, new_stage, timestamp, user_comment, updated_by)
- [x] Initialize SQLite database with schema and sample data
- [x] Create main application state class with stock loading and filtering by status
- [x] Implement data access methods for reading stocks and writing transition logs

---

## Phase 2: Kanban Board UI and Layout ✅
- [x] Design header with app title, search functionality, and "Add New Stock" button
- [x] Implement 8 Kanban columns (Universe, Prospects, Outreach, Discovery, Live Deal, Execute, Tracker, Ocean)
- [x] Create stock card component displaying ticker and company_name
- [x] Add horizontal scroll layout for board columns
- [x] Style cards with hover states and visual feedback
- [x] Implement search/filter functionality to find stocks by ticker

---

## Phase 3: Drag-and-Drop with Transaction Handling ✅
- [x] Install reflex-enterprise for drag-and-drop components
- [x] Wrap stock cards with draggable component (rxe.dnd.draggable)
- [x] Wrap stage columns with drop target component (rxe.dnd.drop_target)
- [x] Create confirmation modal with user input (updated_by field and comment textarea)
- [x] Implement drop event handler to capture move and trigger modal
- [x] Create backend transaction: update Stock status + insert TransitionLog entry
- [x] Add error handling for database operations
- [x] Implement optimistic UI updates with rollback on failure

---

## Phase 4: Additional Features and Polish ✅
- [x] Add "Add New Stock" modal with form (ticker, company_name, initial stage)
- [x] Implement stock creation with validation
- [x] Add empty state messaging for columns with no stocks
- [x] Create transition history view/modal to display TransitionLog entries for a stock
- [x] Add timestamp formatting and last_updated display
- [x] Implement responsive design for different screen sizes
- [x] Add loading states and error toasts for user feedback
- [x] Add stock count badges to column headers
- [x] Implement delete stock functionality
- [x] Add visual polish and hover effects

---

## Phase 5: State Machine Logic Implementation ✅
- [x] Define strict StageDef enum with display names and associated colors
- [x] Implement stage color mapping: Universe (Gray), Prospects (Blue), Outreach (Indigo), Discovery (Purple), Live Deal (Orange), Execute (Green), Tracker (Teal), Ocean (Slate/Dark Gray)
- [x] Create validate_transition() function with business rules
- [x] Implement forward progress validation (linear stage movement)
- [x] Implement Ocean rule (can move to Ocean from ANY stage)
- [x] Implementation restoration rule (Ocean → Prospects only)
- [x] Add skip validation (warn if skipping >2 stages, but allow it)
- [x] Enhance move_stock() to use validation logic
- [x] Display validation warnings in confirmation modal UI
- [x] Log validation warnings in transition comments

---

## Phase 6: UI Verification and Testing ✅
- [x] Test drag-and-drop functionality across all 8 stages
- [x] Verify confirmation modal appears with correct stock and stage information
- [x] Test "Add New Stock" modal with validation (duplicate tickers, empty fields)
- [x] Verify search functionality filters stocks correctly
- [x] Test transition history modal displays all stock movements
- [x] Verify delete stock functionality with toast notifications
- [x] Test responsive layout and horizontal scrolling
- [x] Verify empty state messaging appears in columns without stocks
- [x] Test state machine validation rules (forward progress, Ocean rule, restoration, skip warnings)
- [x] Verify validation warnings display correctly in modal
- [x] Test stage color coding across all 8 stages

---

## Phase 7: Deal Velocity & Staleness Tracking ✅
- [x] Update Stock model to add `current_stage_entered_at` DateTime field
- [x] Add computed property `days_in_stage` that calculates (now - current_stage_entered_at)
- [x] Update move_stock() to set `current_stage_entered_at` when stage changes
- [x] Update submit_new_stock() to initialize `current_stage_entered_at` for new records
- [x] Initialize `current_stage_entered_at` for existing sample data in initialize_sample_data()
- [x] Update stock card UI to display staleness indicator
- [x] Implement conditional badge formatting: Green (<7 days), Default (7-30 days), Red (>30 days)
- [x] Add visual "Days in Stage" badge to each stock card
- [x] Add "Show Stale Only" filter button in header
- [x] Implement filter toggle to show only stocks with >30 days in stage

---

## Phase 8: UI Verification - Staleness Indicators
- [ ] Verify staleness badges display correctly on all cards with proper icons
- [ ] Test conditional color formatting (Green Fresh badge, Red Stale badge, Gray default)
- [ ] Verify "Show Stale Only" filter button works and displays only stale stocks
- [ ] Test that days_in_stage updates correctly when stocks are moved
- [ ] Verify empty state messaging when stale filter shows no results

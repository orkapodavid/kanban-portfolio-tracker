# 🎯 Kanban Portfolio Tracker

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Reflex](https://img.shields.io/badge/reflex-0.6+-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-20%20passing-brightgreen.svg)

A **production-ready, mobile-first Kanban board** for tracking and managing financial instrument portfolios (stocks, deals, prospects). Built with [Reflex](https://reflex.dev/) for seamless full-stack Python development.

🚀 **[Live Demo](#)** (Coming Soon)

---

## ✨ Features

- 🎨 **Drag-and-Drop Kanban Board** - Intuitive card movement across stages
- 📱 **Mobile-First Responsive Design** - Perfect UX on all screen sizes
- 📊 **Audit Trail Tracker** - Immutable history of all state transitions
- 📁 **CSV Export** - Download portfolio data with staleness metrics
- ⚠️ **Force Transition Validation** - Business rule enforcement with override capability
- 🔄 **Real-Time State Updates** - Instant UI reflection of all changes
- 🎯 **Staleness Detection** - Automatic flagging of deals stuck in stages
- 🌙 **Clean, Modern UI** - Tailwind CSS with smooth animations

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository:**
   bash
   git clone https://github.com/orkapodavid/kanban-portfolio-tracker.git
   cd kanban-portfolio-tracker
   

2. **Create a virtual environment:**
   bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   

3. **Install dependencies:**
   bash
   pip install -r requirements.txt
   

4. **Run the application:**
   bash
   reflex run
   

5. **Open your browser:**
   Navigate to `http://localhost:3000`

---

## 🏗️ Architecture Overview


kanban-portfolio-tracker/
├── app/
│   ├── models.py              # Data models (Stock, StateTransitionLog, StageDef)
│   ├── app.py                 # Main application entry point
│   ├── states/
│   │   ├── base_state.py      # Global app state (users, theme)
│   │   └── kanban_state.py    # Board logic and event handlers
│   ├── components/
│   │   ├── stock_card.py      # Draggable stock card component
│   │   ├── stage_column.py    # Droppable stage column component
│   │   ├── modals.py          # All modal dialogs
│   │   └── header.py          # App header with search/filters
│   └── pages/
│       └── dashboard.py       # Main Kanban board page
├── tests/
│   ├── conftest.py            # Pytest fixtures
│   └── test_logic.py          # Comprehensive business logic tests
├── assets/                    # Static assets (icons, images)
├── requirements.txt           # Python dependencies
├── rxconfig.py                # Reflex configuration
└── README.md                  # This file


---

## 🔍 Core Features Deep Dive

### 📋 Audit Trail Logic

Every stock movement creates an **immutable record** in the `StateTransitionLog` table:


class StateTransitionLog(rx.Base):
    id: int
    stock_id: int
    ticker: str
    previous_stage: str        # Where it moved FROM
    new_stage: str             # Where it moved TO
    timestamp: datetime        # Exact time of transition (UTC)
    user_comment: str          # Mandatory user explanation
    updated_by: str            # User who performed the action
    days_in_previous_stage: int  # Duration before moving
    is_forced_transition: bool   # Was this a forced/invalid move?
    forced_rationale: str        # Reason for forcing


**Benefits:**
- Complete history of every deal's journey
- Accountability for all state changes
- Audit compliance for financial tracking
- Staleness metrics (`days_in_stage` calculation)
- Forced transition detection and flagging

### 📱 Mobile Design Decisions

The application adapts seamlessly between desktop and mobile:

| Screen Size | Layout Strategy |
|-------------|----------------|
| **Desktop (≥768px)** | Horizontal scrolling columns with drag-and-drop |
| **Mobile (<768px)** | Tab-based column switcher with vertical scrolling |

**Mobile Optimizations:**
- ✅ Hamburger menu for navigation
- ✅ 44x44px minimum touch targets (accessibility)
- ✅ Action buttons in "thumb zone" (bottom of screen)
- ✅ Responsive grid system (Tailwind breakpoints)
- ✅ Touch-optimized drag-and-drop

**Responsive Breakpoint:**

/* Tailwind CSS md: prefix = 768px */
<div class="hidden md:flex">  /* Desktop only */
<div class="flex md:hidden">  /* Mobile only */


---

## 🎮 Usage Guide

### Adding Stocks

1. Click **"Add New Stock"** button in header
2. Enter ticker symbol (e.g., `AAPL`)
3. Enter company name (e.g., `Apple Inc.`)
4. Select initial stage (default: `Universe`)
5. Click **"Create Stock"**

### Moving Stocks Between Stages

1. **Drag** a stock card from its current column
2. **Drop** it onto a target stage column
3. Enter a **mandatory comment** explaining the move
4. Click **"Save & Move"**

**Invalid Moves:**
- If you attempt an invalid transition (e.g., backward or skip stages), the system will:
  - Show a warning modal
  - Request a **rationale** for forcing the move
  - Flag the transition with a yellow indicator

### Viewing Deal Details & History

1. Click on any stock card
2. **Overview Tab:** View current stage, days in stage, internal ID
3. **Activity Log Tab:** See complete transition history with timestamps

### Filtering & Search

- **Search Bar:** Filter by ticker or company name
- **Show Stale Only:** Display only stocks with >30 days in current stage
- **Clear Filters:** Reset all active filters

### Exporting Data

1. Click **"Export CSV"** button in header
2. CSV includes: Stock ID, Ticker, Company, Stage, Days in Stage, Last Updated
3. File downloads automatically as `kanban_export_YYYYMMDD_HHMMSS.csv`

---

## 🧪 Testing

The project includes a comprehensive test suite with **20 tests** covering all business logic.

### Run All Tests

bash
pytest tests/ -v


### Run Specific Test Class

bash
pytest tests/test_logic.py::TestTransitionValidation -v


### Test Coverage Areas

| Test Class | Coverage |
|------------|----------|
| `TestTransitionValidation` | Business rules for stage transitions |
| `TestTrackerAccuracy` | Audit trail logging integrity |
| `TestDaysInStageCalculation` | Time tracking and timezone handling |
| `TestStateManagement` | State updates and data consistency |

**Example Output:**

======================== test session starts =========================
tests/test_logic.py::TestTransitionValidation::test_valid_forward_progression PASSED
tests/test_logic.py::TestTrackerAccuracy::test_move_creates_log_entry PASSED
...
======================== 20 passed in 0.14s ==========================


---

## 🔐 Environment Variables

Create a `.env` file in the project root for configuration:

bash
# Database URL (optional - for future DB integration)
DATABASE_URL=postgresql://user:pass@localhost:5432/kanban

# Application Settings
APP_ENV=development
DEBUG=true


See `.env.example` for a template.

---

## 🛠️ Development

### Running in Development Mode

bash
reflex run


This starts the development server with:
- Hot reload enabled
- Automatic browser refresh on code changes
- Debug mode active

### Building for Production

bash
reflex export


### Project Structure Best Practices

- **Models (`app/models.py`):** Data structures only, no business logic
- **States (`app/states/`):** Event handlers and state management
- **Components (`app/components/`):** Reusable UI elements
- **Pages (`app/pages/`):** Route-level layouts composing components

---

## 📊 Kanban Stages

The system uses 8 fixed stages representing the investment pipeline:

1. **Universe** - Initial screening pool
2. **Prospects** - Potential investments identified
3. **Outreach** - Contact initiated
4. **Discovery** - Due diligence phase
5. **Live Deal** - Active negotiation
6. **Execute** - Transaction execution
7. **Tracker** - Post-investment monitoring
8. **Ocean** - Archive (closed/rejected deals)

**Transition Rules:**
- Standard flow: Sequential progression (Universe → Prospects → Outreach → ...)
- Any stage → Ocean (archive anytime)
- Ocean → Prospects only (standard restoration)
- Backward/skipping moves require forced transition with rationale

---

## 🗺️ Roadmap

- [ ] **Database Integration** - PostgreSQL persistence layer
- [ ] **User Authentication** - Role-based access control
- [ ] **Real-Time Collaboration** - Multi-user synchronization
- [ ] **Advanced Analytics** - Funnel metrics and conversion rates
- [ ] **Email Notifications** - Alerts for stale deals
- [ ] **Custom Stage Configuration** - User-defined pipelines
- [ ] **API Endpoints** - REST API for external integrations

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development Guidelines:**
- Write tests for new features
- Follow PEP 8 style guide
- Add type hints to all functions
- Update documentation for API changes

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Reflex](https://reflex.dev/) - Full-stack Python framework
- UI components styled with [Tailwind CSS](https://tailwindcss.com/)
- Drag-and-drop powered by `reflex-enterprise` DnD library
- Icons from [Lucide Icons](https://lucide.dev/)

---

## 📧 Contact

**Project Maintainer:** David OR  
**Repository:** [github.com/orkapodavid/kanban-portfolio-tracker](https://github.com/orkapodavid/kanban-portfolio-tracker)

For questions or support, please [open an issue](https://github.com/orkapodavid/kanban-portfolio-tracker/issues).

---

<div align="center">
  Made with ❤️ using Reflex
</div>

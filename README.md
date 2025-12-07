# Stock Portfolio Kanban Tracker

A **production-grade**, **responsive Kanban board application** designed for tracking and managing a portfolio of financial instruments (stocks). Built with **Reflex** (Python full-stack framework) and featuring **drag-and-drop functionality**, **immutable audit trails**, and **mobile-first responsive design**.

---

## 🎯 Key Features

### Core Functionality
- **8-Stage Kanban Board:** Universe → Prospects → Outreach → Discovery → Live Deal → Execute → Tracker → Ocean
- **Drag-and-Drop:** Intuitive card movement with real-time validation
- **Transition Validation:** Enforces business rules with support for "forced" moves
- **Audit Trail:** Complete immutable history with doubly-linked transition logs
- **CSV Export:** One-click export of current board state
- **Search & Filters:** Real-time filtering by ticker/company and stale status
- **Detail Modals:** View individual stock details and complete activity history
- **Ocean Archive:** Special archive view for completed deals

### Advanced Features
- **Doubly Linked History:** Each transition log links to previous entry (mechanical undo capability)
- **Custom Timestamps:** Override effective date/time for historical backfilling
- **Forced Transitions:** Validate and flag non-standard moves with mandatory rationale
- **Stale Detection:** Automatically flag deals stuck >30 days in same stage
- **User Tracking:** Record which analyst performed each transition

### Mobile-First Design
- **Responsive Layout:** Seamless experience on desktop, tablet, and mobile
- **Tab-Based Navigation:** Easy column switching on mobile devices
- **Touch Targets:** All interactive elements minimum 44x44px for accessibility
- **Hamburger Menu:** Collapsible mobile navigation

---

## 🏗️ Architecture

### Project Structure

kanban-portfolio-tracker/
├── app/
│   ├── components/           # Reusable UI components
│   │   ├── stock_card.py     # Draggable stock card
│   │   ├── stage_column.py   # Droppable stage column
│   │   ├── modals.py         # All modal dialogs
│   │   └── header.py         # Application header
│   ├── states/               # State management
│   │   ├── base_state.py     # App-wide configuration
│   │   └── kanban_state.py   # Board-specific logic
│   ├── pages/                # Page layouts
│   │   └── dashboard.py      # Main Kanban board
│   ├── models.py             # Data models
│   └── app.py                # Application entry point
├── assets/                   # Static assets
├── tests/                    # Automated test suite
├── requirements.txt          # Python dependencies
├── rxconfig.py              # Reflex configuration
└── README.md                # This file


### Data Models

#### **Stock Entity**

class Stock(rx.Base):
    id: int
    ticker: str
    company_name: str
    status: str                           # Current Kanban stage
    last_updated: datetime
    current_stage_entered_at: datetime
    days_in_stage: int
    is_forced: bool                       # Flag for forced transitions
    last_log_id: Optional[int]            # Head pointer for history chain


#### **StateTransitionLog Entity** (Immutable Audit Trail)

class StateTransitionLog(rx.Base):
    id: int
    stock_id: int
    ticker: str
    previous_stage: str
    new_stage: str
    timestamp: datetime
    user_comment: str
    updated_by: str
    days_in_previous_stage: int
    is_forced_transition: bool
    forced_rationale: str
    previous_log_id: Optional[int]        # Linked list pointer


### Audit Trail Design

The application implements a **doubly-linked list** structure for transition history:


Stock: AAPL (last_log_id=15)
  ↓
Log #15 (Universe→Prospects, prev: #12) ← HEAD
  ↓
Log #12 (Ocean→Universe, prev: #8)
  ↓
Log #8 (Execute→Ocean, prev: #3)
  ↓
Log #3 (Discovery→Execute, prev: None) ← TAIL


**Benefits:**
- **Mechanical Undo:** Follow `previous_log_id` backwards to reconstruct exact history
- **No Timestamp Ambiguity:** Chain is explicit, not time-based
- **Efficient Queries:** Start at `stock.last_log_id` and traverse backwards
- **Audit Integrity:** Immutable linked list proves sequence of events

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+ (for Reflex frontend compilation)

### Installation

1. **Clone the repository:**
bash
git clone https://github.com/orkapodavid/kanban-portfolio-tracker.git
cd kanban-portfolio-tracker


2. **Create virtual environment:**
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install dependencies:**
bash
pip install -r requirements.txt


4. **Initialize Reflex:**
bash
reflex init


5. **Run the application:**
bash
reflex run


6. **Access the app:**
Open your browser to `http://localhost:3000`

---

## 🧪 Testing

### Run Automated Tests
bash
pytest tests/ -v


### Test Coverage
- ✅ **20 comprehensive tests** covering:
  - Transition validation logic
  - Forced move detection
  - Audit trail integrity
  - Days-in-stage calculations
  - Timezone handling

---

## 📱 Mobile Design

### Responsive Breakpoints
- **Desktop (≥768px):** Horizontal scrolling Kanban columns
- **Mobile (<768px):** Tab-based column switcher

### Mobile Optimizations
- Hamburger menu for filters and actions
- 44x44px minimum touch targets (WCAG 2.1 AAA compliance)
- Vertical stacking of action buttons in "thumb zone"
- Optimized drag-and-drop for touch devices

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

env
# Database (optional - currently using in-memory storage)
DATABASE_URL=postgresql://user:password@localhost:5432/kanban_db

# Application Settings
APP_ENV=development


---

## 📊 Usage Guide

### Adding a New Stock
1. Click **"Add New Stock"** button in header
2. Enter ticker symbol (e.g., AAPL)
3. Enter company name
4. Select initial stage
5. Click **"Create Stock"**

### Moving Stocks Between Stages
1. **Drag** a stock card from one column
2. **Drop** onto another column
3. **Modal appears:**
   - Select user performing action
   - (Optional) Override effective date/time
   - Add mandatory comment explaining the move
4. Click **"Save & Move"**

### Forced Transitions
If you attempt an invalid move (e.g., backward transition, skipping stages):
1. **Warning modal** appears explaining why the move is invalid
2. Provide mandatory **rationale** for forcing the move
3. Move is flagged with amber border and audit trail marker

### Viewing Stock History
1. Click on any stock card
2. Select **"Activity Log"** tab
3. View complete transition history with:
   - Timestamps
   - Users
   - Comments
   - Forced transition flags

### Filtering & Search
- **Search:** Type ticker or company name in search bar
- **Stale Filter:** Toggle to show only stocks stuck >30 days
- **Clear Filters:** Reset all active filters

### Exporting Data
1. Click **"Export CSV"** button
2. Downloads current filtered board state with:
   - Stock ID, Ticker, Company Name
   - Current Stage, Days in Stage
   - Last Updated timestamp

---

## 🛠️ Development

### Code Style
- **Type Hints:** Full type annotations on all functions
- **Docstrings:** Google-style docstrings for all public methods
- **Modular Design:** Separate files for components, states, pages

### Adding New Features

#### Add a New Modal:
1. Define component in `app/components/modals.py`
2. Add state variables in `app/states/kanban_state.py`
3. Import and render in `app/pages/dashboard.py`

#### Add a New Stage:
1. Update `STAGES_DATA` in `app/models.py`
2. Add validation rules in `KanbanState.validate_transition()`

---

## 🗺️ Roadmap

### Completed ✅
- [x] Core Kanban drag-and-drop functionality
- [x] Immutable audit trail with linked list history
- [x] Mobile-first responsive design
- [x] CSV export functionality
- [x] Forced transition handling
- [x] Custom timestamp overrides
- [x] Comprehensive test suite (20 tests, 100% pass rate)

### Planned 🚧
- [ ] PostgreSQL database integration
- [ ] User authentication & role-based access control
- [ ] Real-time collaboration (WebSocket updates)
- [ ] Email notifications for stale deals
- [ ] Advanced analytics dashboard
- [ ] Undo/Redo functionality using linked history
- [ ] Dark mode theme

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**David OR**
- GitHub: [@orkapodavid](https://github.com/orkapodavid)

---

## 🙏 Acknowledgments

- Built with [Reflex](https://reflex.dev) - Pure Python web framework
- Drag-and-drop powered by Reflex Enterprise DnD component
- UI styled with TailwindCSS via Reflex plugin

---

## 📞 Support

For issues, questions, or feature requests, please [open an issue](https://github.com/orkapodavid/kanban-portfolio-tracker/issues) on GitHub.

# Stock Portfolio Kanban Tracker

A responsive, production-ready Kanban board application for tracking and managing financial instruments through an 8-stage workflow with comprehensive audit trails.

## 🎯 Features

- **8-Stage Kanban Board:** Universe → Prospects → Outreach → Discovery → Live Deal → Execute → Tracker → Ocean
- **Drag-and-Drop:** Intuitive card movement with validation and forced transition handling
- **Audit Trail:** Immutable StateTransitionLog with user comments and timestamps
- **CSV Export:** One-click export of current board state
- **Responsive Design:** Mobile-first with tab navigation and hamburger menu
- **Search & Filters:** Real-time filtering by ticker/company and stale status
- **Detail Modals:** View individual stock details and complete activity history
- **Ocean Archive:** Special view for archived deals

## 🚀 Quick Start

bash
# Clone the repository
git clone https://github.com/orkapodavid/kanban-portfolio-tracker.git
cd kanban-portfolio-tracker

# Install dependencies
pip install -r requirements.txt

# Run the application
reflex run


## 📁 Project Structure


kanban-portfolio-tracker/
├── app/
│   ├── components/          # Modular UI components
│   │   ├── header.py       # App header with search/filters
│   │   ├── modals.py       # All modal dialogs
│   │   ├── stage_column.py # Droppable Kanban columns
│   │   └── stock_card.py   # Draggable stock cards
│   ├── pages/              # Page layouts
│   │   └── dashboard.py    # Main Kanban board
│   ├── states/             # Application state management
│   │   ├── base_state.py   # Global app state
│   │   └── kanban_state.py # Board logic & events
│   ├── models.py           # Data models (Stock, TransitionLog)
│   └── app.py              # Application entry point
├── plan.md                 # Project roadmap
├── requirements.txt        # Python dependencies
└── rxconfig.py            # Reflex configuration


## 🔧 Tech Stack

- **Framework:** Reflex (Python web framework)
- **UI Library:** Reflex Enterprise (drag-and-drop components)
- **Styling:** Tailwind CSS v3
- **Testing:** pytest with 100% core logic coverage

## 📊 Data Model

### Stock Entity
- `id` (int): Primary key
- `ticker` (str): Stock symbol
- `company_name` (str): Company name
- `status` (str): Current Kanban stage
- `last_updated` (datetime): Last modification timestamp
- `current_stage_entered_at` (datetime): Stage entry timestamp
- `days_in_stage` (int): Duration in current stage
- `is_forced` (bool): Whether last move was forced

### StateTransitionLog Entity
- `id` (int): Primary key
- `stock_id` (int): Foreign key to Stock
- `ticker` (str): Stock symbol
- `previous_stage` (str): Source stage
- `new_stage` (str): Destination stage
- `timestamp` (datetime): Transition timestamp
- `user_comment` (str): User-provided rationale
- `updated_by` (str): User performing the action
- `days_in_previous_stage` (int): Duration in previous stage
- `is_forced_transition` (bool): Whether move was forced
- `forced_rationale` (str): Reason for forcing (if applicable)

## 🎨 Mobile-First Design

- **Desktop:** Horizontal scrolling Kanban board (all 8 columns visible)
- **Mobile:** Tab-based column switcher with hamburger menu
- **Touch Targets:** Minimum 44x44px for accessibility
- **Responsive Breakpoints:** Tailwind `md:` prefix (768px+)

## 🔒 Audit Trail

Every stock movement creates an immutable `StateTransitionLog` entry capturing:
- Complete transition history (from/to stages)
- User identity and comments
- Timestamp with timezone handling
- Forced transition flags and rationale

## 📦 CSV Export

Export current board state with one click:
- Stock ID, Ticker, Company Name
- Current Stage, Days in Stage
- Last Updated timestamp (UTC)
- Filtered by current search/filter settings

## 🧪 Testing

bash
# Run test suite
pytest tests/ -v

# All 20 tests passing:
# ✅ Valid transitions
# ✅ Invalid transitions with force handling
# ✅ Transition log creation
# ✅ Days in stage calculation


## 🛠️ Development

bash
# Install dev dependencies
pip install -r requirements.txt

# Run in development mode
reflex run --loglevel debug

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html


## 📝 Usage Guide

### Adding Stocks
1. Click "Add New Stock" in the header
2. Enter ticker symbol and company name
3. Select initial stage
4. Stock appears in the chosen column

### Moving Stocks
1. Drag a stock card to a different column
2. If move is valid: Comment modal appears
3. If move is invalid but forceable: Force transition modal appears
4. Enter rationale and confirm
5. Stock moves and audit log is created

### Viewing Details
- Click any stock card to view details
- **Overview Tab:** Stock metadata and current stage
- **Activity Log Tab:** Complete transition history

### Filtering & Search
- **Search:** Type ticker or company name in search bar
- **Stale Filter:** Show only stocks >30 days in current stage
- **Clear Filters:** One-click reset

### Ocean Archive
- Click the "Ocean" summary card to view all archived deals
- Click any archived stock to view its history

## 🚀 Production Ready

- ✅ Modular architecture with comprehensive type hints
- ✅ Full audit trail for compliance
- ✅ Automated test suite (100% coverage)
- ✅ Mobile-responsive design
- ✅ CSV export functionality
- ✅ Security best practices (.gitignore)
- ✅ Comprehensive documentation

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with [Reflex](https://reflex.dev) - Pure Python web framework**

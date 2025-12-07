# Stock Portfolio Kanban Tracker

A production-ready, mobile-responsive Kanban board application for tracking financial portfolio stages with comprehensive audit trails, drag-and-drop functionality, and real-time validation.

## 🚀 Features

### Core Functionality
- **8-Stage Kanban Board**: Universe → Prospects → Outreach → Discovery → Live Deal → Execute → Tracker → Ocean
- **Drag-and-Drop**: Intuitive card movement with validation and forced transition handling
- **Audit Trail**: Immutable StateTransitionLog with user comments and timestamps
- **CSV Export**: One-click export of current board state
- **Search & Filters**: Real-time filtering by ticker/company and stale status
- **Detail Modals**: View individual stock details and complete activity history
- **Ocean Archive**: Special view for archived deals

### Business Logic
- **Transition Validation**: Enforces sequential stage progression
- **Forced Transitions**: Flagged moves with mandatory rationale
- **Staleness Tracking**: Automatic calculation of days in current stage
- **User Attribution**: All changes tracked with user identity

### Mobile-First Design
- **Responsive Layout**: Tab-based navigation on mobile, horizontal scrolling on desktop
- **Touch Targets**: Minimum 44x44px buttons for accessibility
- **Hamburger Menu**: Collapsible navigation on small screens

## 📁 Project Structure


kanban-portfolio-tracker/
├── app/
│   ├── __init__.py
│   ├── app.py                 # Main application entry point
│   ├── models.py              # Data models (Stock, StateTransitionLog, StageDef)
│   ├── components/            # Reusable UI components
│   │   ├── __init__.py
│   │   ├── header.py          # Application header with search/filters
│   │   ├── stock_card.py      # Draggable stock card component
│   │   ├── stage_column.py    # Droppable stage column component
│   │   └── modals.py          # All modal dialogs
│   ├── states/                # Application state management
│   │   ├── __init__.py
│   │   ├── base_state.py      # Base configuration state
│   │   └── kanban_state.py    # Kanban board logic
│   └── pages/                 # Page layouts
│       ├── __init__.py
│       └── dashboard.py       # Main dashboard page
├── assets/                    # Static assets
├── tests/                     # Automated test suite
│   ├── conftest.py            # pytest fixtures
│   └── test_logic.py          # Business logic tests
├── requirements.txt
├── rxconfig.py
└── README.md


## 🛠️ Installation

### Prerequisites
- Python 3.11+
- pip
- Git

### Setup

1. Clone the repository:
bash
git clone https://github.com/orkapodavid/kanban-portfolio-tracker.git
cd kanban-portfolio-tracker


2. Create a virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install dependencies:
bash
pip install -r requirements.txt


4. (Optional) Configure environment variables:
bash
cp .env.example .env
# Edit .env with your settings (DATABASE_URL for future use)


5. Initialize the Reflex app:
bash
reflex init


6. Run the development server:
bash
reflex run


7. Open your browser to `http://localhost:3000`

## 🧪 Running Tests

bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_logic.py -v


## 📊 Data Model

### Stock Entity
- `id`: Unique identifier
- `ticker`: Stock ticker symbol (e.g., AAPL)
- `company_name`: Full company name
- `status`: Current Kanban stage
- `last_updated`: Timestamp of last modification
- `current_stage_entered_at`: When stock entered current stage
- `days_in_stage`: Calculated staleness metric
- `is_forced`: Flag for forced transitions

### StateTransitionLog Entity
- `id`: Unique identifier
- `stock_id`: Reference to Stock
- `ticker`: Cached ticker for historical reference
- `previous_stage`: Stage before transition
- `new_stage`: Stage after transition
- `timestamp`: When transition occurred
- `user_comment`: User-provided rationale
- `updated_by`: User who made the change
- `days_in_previous_stage`: Duration in previous stage
- `is_forced_transition`: Whether this was a forced move
- `forced_rationale`: Explanation for forced moves

## 🎯 Usage Guide

### Moving Stocks
1. **Drag and Drop**: Click and drag a stock card to a new stage column
2. **Confirmation Modal**: Enter a comment explaining the move
3. **Select User**: Choose who is making the change
4. **Submit**: Click "Save & Move"

### Forced Transitions
- If you try to move a stock backward or skip stages, you'll see a warning modal
- Provide a rationale for the exception
- These moves are flagged with 🏴 icon and highlighted in audit logs

### Filtering and Search
- **Search Bar**: Type ticker or company name to filter
- **Stale Filter**: Toggle "Show Stale Only" to see stocks >30 days in stage
- **Clear**: Reset all filters

### Exporting Data
- Click "Export CSV" in the header
- Downloads current filtered view with all stock details
- Filename includes timestamp for versioning

### Viewing Details
- **Click any stock card** to open detail modal
- **Overview Tab**: See basic info and current stage duration
- **Activity Log Tab**: View complete transition history with user comments

### Ocean Archive
- Click the Ocean summary card to view archived deals
- Shows complete list with last updated timestamps
- Click any archived deal to view its history

## 🏗️ Architecture Decisions

### State Management
- **In-Memory Lists**: Current implementation uses Python lists for simplicity
- **Future Database**: Prepared for PostgreSQL/SQLite integration (see DATABASE_URL in .env.example)
- **Audit Trail**: Immutable log ensures compliance and historical accuracy

### Responsive Design
- **Mobile (<768px)**: Tab-based column switching, vertical layout
- **Desktop (≥768px)**: Horizontal scrolling Kanban board
- **Touch Targets**: All interactive elements meet WCAG 2.1 guidelines (44x44px minimum)

### Validation Logic
- **Sequential Progression**: Universe → Prospects → Outreach → Discovery → Live Deal → Execute → Tracker
- **Ocean Exception**: Can be accessed from any stage (archive)
- **Restoration**: Ocean can only return to Prospects (standard) or any stage (forced)

## 🔒 Security

- No hardcoded secrets in codebase
- `.gitignore` prevents accidental secret commits
- Environment variables for sensitive configuration
- All forced transitions logged for audit compliance

## 🗺️ Roadmap

### Completed ✅
- [x] Core Kanban functionality with drag-and-drop
- [x] Audit trail and state transition logging
- [x] Mobile-responsive design
- [x] CSV export
- [x] Automated testing suite (20 tests, 100% pass rate)
- [x] Comprehensive documentation
- [x] GitHub publication

### Future Enhancements
- [ ] PostgreSQL database integration
- [ ] User authentication and role-based access control
- [ ] Real-time collaboration (WebSocket updates)
- [ ] Advanced analytics dashboard
- [ ] Email notifications for stale deals
- [ ] Bulk operations (multi-select and move)
- [ ] Custom stage definitions (user-configurable workflow)
- [ ] API endpoints for external integrations

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for public methods
- Include tests for new features
- Update documentation as needed

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Reflex](https://reflex.dev/) - Pure Python web framework
- Drag-and-drop powered by [Reflex Enterprise](https://reflex.dev/docs/enterprise/)
- UI components styled with [Tailwind CSS](https://tailwindcss.com/)

## 📧 Contact

**David OR** - [@orkapodavid](https://github.com/orkapodavid)

**Project Link**: [https://github.com/orkapodavid/kanban-portfolio-tracker](https://github.com/orkapodavid/kanban-portfolio-tracker)

---

**Note**: This is a production-ready starter application. For deployment, consider adding:
- Database persistence layer
- User authentication
- Environment-specific configuration
- Monitoring and logging infrastructure
- CI/CD pipeline

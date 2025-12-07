import reflex as rx
from app.states.kanban_state import KanbanState


def header() -> rx.Component:
    """
    Application header with search, filters, and actions.

    Returns:
        rx.Component: The header component.
    """
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("bookmark", class_name="h-6 w-6 text-blue-600"),
                rx.el.h1(
                    "Stock State Tracker",
                    class_name="text-xl font-bold text-gray-900 tracking-tight",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search by Ticker...",
                        on_change=KanbanState.set_search_query,
                        class_name="pl-9 pr-4 py-2 bg-gray-100 border-transparent focus:bg-white focus:border-blue-500 focus:ring-0 rounded-lg text-sm w-64 transition-all",
                        default_value=KanbanState.search_query,
                    ),
                    class_name="relative",
                ),
                rx.cond(
                    (KanbanState.search_query != "") | KanbanState.show_stale_only,
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4 mr-1"),
                        "Clear",
                        on_click=KanbanState.clear_filters,
                        class_name="flex items-center px-3 py-2 text-gray-500 hover:text-gray-700 text-sm font-medium hover:bg-gray-100 rounded-lg transition-colors",
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        KanbanState.show_stale_only,
                        rx.icon("filter_x", class_name="h-4 w-4 mr-2"),
                        rx.icon("filter", class_name="h-4 w-4 mr-2"),
                    ),
                    rx.cond(KanbanState.show_stale_only, "Show All", "Show Stale Only"),
                    on_click=KanbanState.toggle_stale_filter,
                    class_name=rx.cond(
                        KanbanState.show_stale_only,
                        "flex items-center px-4 py-2 bg-red-100 text-red-700 border border-red-200 text-sm font-medium rounded-lg hover:bg-red-200 transition-colors",
                        "flex items-center px-4 py-2 bg-white text-gray-700 border border-gray-300 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-4 w-4 mr-2"),
                    "Add New Stock",
                    on_click=KanbanState.open_add_modal,
                    class_name="flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-center max-w-[1800px] mx-auto w-full",
        ),
        class_name="bg-white border-b border-gray-200 px-6 py-4 z-20 relative",
    )
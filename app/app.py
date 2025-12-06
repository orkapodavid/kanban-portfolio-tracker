import reflex as rx
import reflex_enterprise as rxe
from app.states.kanban_state import KanbanState
from app.models import Stock, StageDef


@rx.memo
def draggable_stock_card(stock: Stock) -> rx.Component:
    """
    Renders a draggable stock card with actions and timestamps.
    Includes clickable overlay (z-20) for details modal and context menu (z-30).
    """
    return rxe.dnd.draggable(
        rx.el.div(
            rx.el.div(
                class_name="absolute inset-0 z-20 cursor-pointer rounded-lg",
                on_click=lambda: KanbanState.open_detail_modal(stock.id),
            ),
            rx.el.div(
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon(
                            "send_horizontal",
                            class_name="text-gray-400 h-5 w-5 hover:text-blue-600 cursor-pointer",
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "View Details",
                            on_click=lambda: KanbanState.open_detail_modal(
                                stock.id, "overview"
                            ),
                            class_name="cursor-pointer",
                        ),
                        rx.menu.item(
                            "View History",
                            on_click=lambda: KanbanState.open_detail_modal(
                                stock.id, "activity"
                            ),
                            class_name="cursor-pointer",
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Delete Stock",
                            on_click=lambda: KanbanState.delete_stock(stock.id),
                            class_name="text-red-600 cursor-pointer hover:bg-red-50",
                        ),
                    ),
                ),
                class_name="absolute top-3 right-3 z-30",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        stock.ticker, class_name="font-bold text-gray-900 text-base"
                    ),
                    rx.el.div(
                        stock.company_name,
                        class_name="text-xs text-gray-500 truncate max-w-[160px] mt-0.5",
                    ),
                    class_name="flex flex-col pr-6",
                ),
                class_name="mb-3 relative z-10",
            ),
            rx.el.div(
                rx.cond(
                    stock.days_in_stage < 7,
                    rx.el.div(
                        rx.icon("square_check", class_name="h-3.5 w-3.5 mr-1.5"),
                        rx.el.span("Fresh", class_name="font-bold mr-1.5"),
                        rx.el.span(f"{stock.days_in_stage}d"),
                        class_name="flex items-center text-[11px] text-green-700 bg-green-50 px-2 py-1 rounded-full border border-green-200 w-fit shadow-sm",
                    ),
                    rx.cond(
                        stock.days_in_stage > 30,
                        rx.el.div(
                            rx.icon("triangle_alert", class_name="h-3.5 w-3.5 mr-1.5"),
                            rx.el.span("Stale", class_name="font-bold mr-1.5"),
                            rx.el.span(f"{stock.days_in_stage}d"),
                            class_name="flex items-center text-[11px] text-red-700 bg-red-50 px-2 py-1 rounded-full border border-red-200 w-fit shadow-sm",
                        ),
                        rx.el.div(
                            rx.icon("hourglass", class_name="h-3.5 w-3.5 mr-1.5"),
                            rx.el.span(f"{stock.days_in_stage} days"),
                            class_name="flex items-center text-[11px] text-gray-600 bg-gray-50 px-2 py-1 rounded-full border border-gray-200 w-fit",
                        ),
                    ),
                ),
                class_name="flex items-center mt-3 relative z-10",
            ),
            rx.el.div(
                rx.icon("clock", class_name="h-3 w-3 text-gray-300 mr-1"),
                rx.el.span(
                    "Updated ",
                    rx.moment(stock.last_updated, from_now=True),
                    class_name="text-[10px] text-gray-400",
                ),
                class_name="flex items-center mt-3 pt-2 border-t border-gray-50 relative z-10",
            ),
            rx.cond(
                stock.is_forced,
                rx.el.div(
                    rx.icon("flag", class_name="h-3 w-3 text-white"),
                    class_name="absolute -top-1 -left-1 bg-amber-500 rounded-full p-1 shadow-sm z-30",
                    title="Forced Transition",
                ),
            ),
            class_name=rx.cond(
                stock.is_forced,
                "bg-white p-4 rounded-lg shadow-sm border-l-4 border-l-amber-400 border-y border-r border-gray-200 hover:shadow-md transition-all cursor-grab active:cursor-grabbing select-none group relative",
                "bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md hover:border-blue-300 transition-all cursor-grab active:cursor-grabbing select-none group relative",
            ),
        ),
        type="stock",
        item={"stock_id": stock.id, "ticker": stock.ticker},
        key=stock.id,
    )


@rx.memo
def droppable_stage_column(stage: StageDef) -> rx.Component:
    """
    Renders a droppable column for a specific stage.
    Includes special handling for 'Ocean' stage (summary view) vs standard list.
    """
    drop_params = rxe.dnd.DropTarget.collected_params
    stocks_in_stage = KanbanState.stocks_by_stage[stage.name]
    base_style = f"flex-shrink-0 w-80 {stage.bg_color} rounded-xl p-4 h-full overflow-y-auto border {stage.border_color} transition-colors"
    active_style = f"flex-shrink-0 w-80 {stage.bg_color} rounded-xl p-4 h-full overflow-y-auto border-2 border-blue-400 transition-colors"
    return rxe.dnd.drop_target(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(stage.name, class_name=f"font-semibold {stage.color}"),
                    rx.el.span(
                        stocks_in_stage.length(),
                        class_name="ml-2 px-2 py-0.5 text-xs font-medium bg-white/50 text-gray-600 rounded-full border border-gray-100",
                    ),
                    class_name="flex items-center",
                ),
                class_name=f"flex items-center justify-between mb-4 sticky top-0 {stage.bg_color} backdrop-blur py-2 z-10",
            ),
            rx.el.div(
                rx.cond(
                    stage.name == "Ocean",
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "🌊", class_name="text-4xl mb-2 block text-center"
                            ),
                            rx.el.span(
                                f"{stocks_in_stage.length()} Deals in Ocean",
                                class_name="font-bold text-slate-700 block text-center",
                            ),
                            rx.el.span(
                                "Click to view archive",
                                class_name="text-xs text-slate-500 block text-center mt-1",
                            ),
                            class_name="bg-white/80 p-6 rounded-lg shadow-sm border border-slate-300 cursor-pointer hover:bg-white transition-colors hover:shadow-md group",
                            on_click=KanbanState.open_ocean_modal,
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.cond(
                        stocks_in_stage.length() > 0,
                        rx.foreach(
                            stocks_in_stage,
                            lambda stock: draggable_stock_card(
                                key=stock.id, stock=stock
                            ),
                        ),
                        rx.el.div(
                            rx.el.span(
                                "No stocks",
                                class_name="text-sm font-medium text-gray-400 mb-1",
                            ),
                            rx.el.span(
                                "Drop items here", class_name="text-xs text-gray-300"
                            ),
                            class_name=f"flex flex-col items-center justify-center h-32 border-2 border-dashed {stage.border_color} rounded-lg opacity-60",
                        ),
                    ),
                ),
                class_name="flex flex-col gap-3 min-h-[150px]",
            ),
            class_name=rx.cond(drop_params.is_over, active_style, base_style),
        ),
        accept=["stock"],
        on_drop=lambda item: KanbanState.handle_drop(item, stage.name),
    )


def confirmation_modal() -> rx.Component:
    """
    Modal for confirming stock movement and adding comments.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirm Stage Change"),
            rx.dialog.description(
                "Please verify the details of this transition and add a required comment.",
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Moving: ",
                        rx.el.span(
                            KanbanState.pending_move_ticker,
                            class_name="font-bold text-gray-900",
                        ),
                        class_name="text-sm text-gray-500 block mb-1",
                    ),
                    rx.el.label(
                        "To Stage: ",
                        rx.el.span(
                            KanbanState.pending_move_stage,
                            class_name="font-bold text-blue-600",
                        ),
                        class_name="text-sm text-gray-500 block mb-4",
                    ),
                ),
                rx.el.label(
                    "Updated By",
                    class_name="text-sm font-medium text-gray-700 block mb-2",
                ),
                rx.el.select(
                    rx.foreach(
                        KanbanState.available_users,
                        lambda user: rx.el.option(user, value=user),
                    ),
                    value=KanbanState.modal_user,
                    on_change=KanbanState.set_modal_user,
                    class_name="w-full rounded-md border border-gray-300 p-2 text-sm mb-4 focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
                ),
                rx.el.label(
                    "Transition Comment",
                    class_name="text-sm font-medium text-gray-700 block mb-2",
                ),
                rx.el.textarea(
                    placeholder="Add a comment explaining this move...",
                    on_change=KanbanState.set_modal_comment,
                    class_name="w-full rounded-md border border-gray-300 p-2 text-sm h-24 mb-6 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none",
                    default_value=KanbanState.modal_comment,
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=KanbanState.cancel_move,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
                    )
                ),
                rx.el.button(
                    "Save & Move",
                    on_click=KanbanState.confirm_move,
                    disabled=KanbanState.modal_comment == "",
                    class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="flex justify-end gap-3",
            ),
        ),
        open=KanbanState.is_modal_open,
        on_open_change=lambda open: rx.cond(open, rx.noop(), KanbanState.cancel_move),
    )


def force_transition_modal() -> rx.Component:
    """
    Modal for handling invalid/forced transitions.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.icon("triangle_alert", class_name="h-6 w-6 text-amber-600"),
                rx.dialog.title("⚠ Invalid Transition Warning"),
                class_name="flex items-center gap-2 mb-2",
            ),
            rx.dialog.description(
                "You are moving this deal outside the standard process. This action will be flagged in the system.",
                class_name="mb-4 text-gray-600",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"Reason: {KanbanState.transition_warning}",
                        class_name="text-sm font-medium text-amber-700",
                    ),
                    class_name="bg-amber-50 border border-amber-200 rounded-md p-3 mb-4",
                ),
                rx.el.label(
                    "Please provide a reason for this exception",
                    class_name="text-sm font-medium text-gray-700 block mb-2",
                ),
                rx.el.textarea(
                    placeholder="Rationale for forcing this move...",
                    on_change=KanbanState.set_force_rationale,
                    class_name="w-full rounded-md border border-gray-300 p-2 text-sm h-24 mb-6 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 resize-none",
                    default_value=KanbanState.force_rationale,
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=KanbanState.close_force_modal,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
                    )
                ),
                rx.el.button(
                    "Confirm Force Move",
                    on_click=KanbanState.confirm_force_move,
                    disabled=KanbanState.force_rationale == "",
                    class_name="px-4 py-2 text-sm font-medium text-white bg-amber-600 rounded-md hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="flex justify-end gap-3",
            ),
        ),
        open=KanbanState.is_force_modal_open,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), KanbanState.close_force_modal
        ),
    )


def header() -> rx.Component:
    """
    Application header with search and actions.
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


def add_stock_modal() -> rx.Component:
    """
    Modal for adding a new stock.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Add New Stock"),
            rx.dialog.description(
                "Enter the details for the new stock record.", class_name="mb-4"
            ),
            rx.el.div(
                rx.el.label(
                    "Ticker Symbol",
                    class_name="text-sm font-medium text-gray-700 block mb-1",
                ),
                rx.el.input(
                    placeholder="e.g. AAPL",
                    on_change=KanbanState.set_new_stock_ticker,
                    class_name="w-full rounded-md border border-gray-300 p-2 text-sm mb-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 uppercase",
                    default_value=KanbanState.new_stock_ticker,
                ),
                rx.el.label(
                    "Company Name",
                    class_name="text-sm font-medium text-gray-700 block mb-1",
                ),
                rx.el.input(
                    placeholder="e.g. Apple Inc.",
                    on_change=KanbanState.set_new_stock_company,
                    class_name="w-full rounded-md border border-gray-300 p-2 text-sm mb-3 focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
                    default_value=KanbanState.new_stock_company,
                ),
                rx.el.label(
                    "Initial Stage",
                    class_name="text-sm font-medium text-gray-700 block mb-1",
                ),
                rx.el.select(
                    rx.foreach(KanbanState.stages, lambda s: rx.el.option(s, value=s)),
                    value=KanbanState.new_stock_stage,
                    on_change=KanbanState.set_new_stock_stage,
                    class_name="w-full rounded-md border border-gray-300 p-2 text-sm mb-6 focus:border-blue-500 focus:ring-1 focus:ring-blue-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=KanbanState.close_add_modal,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
                    )
                ),
                rx.el.button(
                    "Create Stock",
                    on_click=KanbanState.submit_new_stock,
                    class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700",
                ),
                class_name="flex justify-end gap-3",
            ),
        ),
        open=KanbanState.is_add_modal_open,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), KanbanState.close_add_modal
        ),
    )


def deal_detail_modal() -> rx.Component:
    """
    Modal for viewing and editing deal details.
    Includes Overview tab (edit ticker) and Activity Log tab (history table).
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                f"Deal Details: {KanbanState.current_detail_stock.company_name}",
                class_name="mb-1",
            ),
            rx.dialog.description(
                "Manage deal information and view activity history.",
                class_name="text-sm text-gray-500 mb-4",
            ),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Overview", value="overview"),
                    rx.tabs.trigger("Activity Log", value="activity"),
                ),
                rx.tabs.content(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Internal ID",
                                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1",
                            ),
                            rx.el.div(
                                KanbanState.current_detail_stock.id,
                                class_name="text-sm font-mono bg-gray-100 px-3 py-2 rounded border border-gray-200 w-fit",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Ticker Symbol",
                                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    on_change=KanbanState.set_edit_ticker_value,
                                    class_name="uppercase text-sm font-bold border border-gray-300 rounded-l px-3 py-2 focus:ring-blue-500 focus:border-blue-500",
                                    default_value=KanbanState.edit_ticker_value,
                                ),
                                rx.el.button(
                                    "Rename",
                                    on_click=KanbanState.save_ticker_edit,
                                    class_name="bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded-r hover:bg-blue-700 transition-colors",
                                ),
                                class_name="flex items-center",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Current Stage",
                                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1",
                            ),
                            rx.el.div(
                                KanbanState.current_detail_stock.status,
                                class_name="text-base font-medium text-gray-900",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Time in Stage",
                                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "clock", class_name="h-4 w-4 text-gray-400 mr-2"
                                ),
                                rx.el.span(
                                    f"{KanbanState.current_detail_stock.days_in_stage} Days",
                                    class_name="font-medium",
                                ),
                                class_name="flex items-center text-gray-700 bg-gray-50 border border-gray-200 px-3 py-2 rounded w-fit",
                            ),
                            class_name="mb-4",
                        ),
                        class_name="py-4 space-y-4",
                    ),
                    value="overview",
                ),
                rx.tabs.content(
                    rx.scroll_area(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Date",
                                        class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider py-2 px-2",
                                    ),
                                    rx.el.th(
                                        "From",
                                        class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider py-2 px-2",
                                    ),
                                    rx.el.th(
                                        "To",
                                        class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider py-2 px-2",
                                    ),
                                    rx.el.th(
                                        "User",
                                        class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider py-2 px-2",
                                    ),
                                    rx.el.th(
                                        "Comment",
                                        class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider py-2 px-2",
                                    ),
                                    rx.el.th(
                                        "Type",
                                        class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider py-2 px-2",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    KanbanState.current_detail_logs,
                                    lambda log: rx.el.tr(
                                        rx.el.td(
                                            rx.moment(
                                                log.timestamp, format="MMM D, HH:mm"
                                            ),
                                            class_name="text-xs text-gray-600 py-3 border-b border-gray-100 px-2",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                log.previous_stage,
                                                class_name="text-gray-500 text-xs",
                                            ),
                                            class_name="py-3 border-b border-gray-100 px-2",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                log.new_stage,
                                                class_name="font-medium text-blue-600 text-xs",
                                            ),
                                            class_name="py-3 border-b border-gray-100 px-2",
                                        ),
                                        rx.el.td(
                                            log.updated_by,
                                            class_name="text-xs text-gray-600 py-3 border-b border-gray-100 px-2",
                                        ),
                                        rx.el.td(
                                            rx.el.div(
                                                rx.el.span(
                                                    log.user_comment,
                                                    class_name="block text-xs text-gray-800",
                                                ),
                                                rx.cond(
                                                    log.is_forced_transition,
                                                    rx.el.div(
                                                        rx.el.span(
                                                            "REASON: ",
                                                            class_name="font-bold text-[10px]",
                                                        ),
                                                        log.forced_rationale,
                                                        class_name="mt-1 text-[10px] text-amber-800 bg-amber-50 p-1 rounded border border-amber-100",
                                                    ),
                                                ),
                                            ),
                                            class_name="py-3 border-b border-gray-100 max-w-[200px] px-2",
                                        ),
                                        rx.el.td(
                                            rx.cond(
                                                log.is_forced_transition,
                                                rx.el.span(
                                                    "FORCED",
                                                    class_name="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-700",
                                                ),
                                                rx.el.span(
                                                    "Standard",
                                                    class_name="px-1.5 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-500",
                                                ),
                                            ),
                                            class_name="py-3 border-b border-gray-100 px-2",
                                        ),
                                        class_name=rx.cond(
                                            log.is_forced_transition,
                                            "bg-amber-50/50 hover:bg-amber-50 transition-colors",
                                            "hover:bg-gray-50 transition-colors",
                                        ),
                                        key=log.id,
                                    ),
                                )
                            ),
                            class_name="w-full",
                        ),
                        type="always",
                        scrollbars="vertical",
                        class_name="max-h-[400px] h-full",
                    ),
                    value="activity",
                ),
                value=KanbanState.active_detail_tab,
                on_change=KanbanState.set_active_detail_tab,
                class_name="w-full",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Close",
                        on_click=KanbanState.close_detail_modal,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 mt-4",
                    )
                ),
                class_name="flex justify-end",
            ),
            max_width="700px",
        ),
        open=KanbanState.is_detail_modal_open,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), KanbanState.close_detail_modal
        ),
    )


def ocean_archive_modal() -> rx.Component:
    """
    Modal for viewing the Ocean archive list.
    Triggered by clicking the Ocean summary card.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Ocean Archive"),
            rx.dialog.description(
                f"Archived deals ({KanbanState.ocean_stocks.length()} total)",
                class_name="mb-4",
            ),
            rx.scroll_area(
                rx.el.div(
                    rx.foreach(
                        KanbanState.ocean_stocks,
                        lambda stock: rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    stock.ticker, class_name="font-bold text-gray-900"
                                ),
                                rx.el.span(
                                    stock.company_name,
                                    class_name="text-sm text-gray-500 ml-2",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "clock", class_name="h-3 w-3 text-gray-400 mr-1"
                                ),
                                rx.moment(stock.last_updated, from_now=True),
                                class_name="flex items-center text-xs text-gray-400",
                            ),
                            class_name="flex items-center justify-between p-3 bg-gray-50 border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-200 cursor-pointer transition-all",
                            on_click=lambda: KanbanState.open_detail_modal(stock.id),
                            key=stock.id,
                        ),
                    ),
                    class_name="flex flex-col gap-2",
                ),
                class_name="max-h-[500px] pr-2",
                type="always",
                scrollbars="vertical",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Close Archive",
                        on_click=KanbanState.close_ocean_modal,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 mt-4",
                    )
                ),
                class_name="flex justify-end",
            ),
        ),
        open=KanbanState.is_ocean_modal_open,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), KanbanState.close_ocean_modal
        ),
    )


def index() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.scroll_area(
                rx.el.div(
                    rx.foreach(
                        KanbanState.stage_defs,
                        lambda stage: droppable_stage_column(
                            stage=stage, key=stage.name
                        ),
                    ),
                    class_name="flex gap-6 px-6 pb-6 min-w-max",
                ),
                scrollbars="horizontal",
                type="always",
                class_name="w-full h-full",
            ),
            class_name="flex-1 overflow-hidden py-6 bg-gray-100",
        ),
        confirmation_modal(),
        force_transition_modal(),
        add_stock_modal(),
        deal_detail_modal(),
        ocean_archive_modal(),
        class_name="flex flex-col h-screen font-['Inter'] bg-gray-50",
        on_mount=KanbanState.on_load,
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        )
    ],
)
app.add_page(index, route="/")
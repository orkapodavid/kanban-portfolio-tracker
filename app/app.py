import reflex as rx
import reflex_enterprise as rxe
from app.states.kanban_state import KanbanState
from app.models import Stock


@rx.memo
def draggable_stock_card(stock: Stock) -> rx.Component:
    """
    Renders a draggable stock card with actions and timestamps.
    """
    return rxe.dnd.draggable(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(stock.ticker, class_name="font-bold text-gray-900"),
                    rx.el.div(
                        stock.company_name,
                        class_name="text-xs text-gray-500 truncate max-w-[150px]",
                    ),
                    class_name="flex flex-col",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon(
                            "send_horizontal",
                            class_name="text-gray-400 h-4 w-4 hover:text-blue-600 cursor-pointer",
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "View History",
                            on_click=lambda: KanbanState.view_history(stock.ticker),
                            class_name="cursor-pointer",
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Delete Stock",
                            on_click=lambda: KanbanState.delete_stock(stock.ticker),
                            class_name="text-red-600 cursor-pointer hover:bg-red-50",
                        ),
                    ),
                ),
                class_name="flex justify-between items-start mb-2",
            ),
            rx.el.div(
                rx.icon("clock", class_name="h-3 w-3 text-gray-400 mr-1"),
                rx.el.span(
                    "Updated ",
                    rx.moment(stock.last_updated, from_now=True),
                    class_name="text-xs text-gray-400",
                ),
                class_name="flex items-center mt-2 border-t border-gray-100 pt-2",
            ),
            class_name="bg-white p-3 rounded-lg shadow-sm border border-gray-200 hover:shadow-md hover:border-blue-300 transition-all cursor-grab active:cursor-grabbing select-none group relative",
        ),
        type="stock",
        item={"ticker": stock.ticker},
    )


@rx.memo
def droppable_stage_column(stage_name: str) -> rx.Component:
    """
    Renders a droppable column for a specific stage with counts and empty states.
    """
    drop_params = rxe.dnd.DropTarget.collected_params
    stocks_in_stage = KanbanState.stocks_by_stage[stage_name]
    return rxe.dnd.drop_target(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(stage_name, class_name="font-semibold text-gray-700"),
                    rx.el.span(
                        stocks_in_stage.length(),
                        class_name="ml-2 px-2 py-0.5 text-xs font-medium bg-gray-200 text-gray-600 rounded-full",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between mb-4 sticky top-0 bg-gray-50/95 backdrop-blur py-2 z-10",
            ),
            rx.el.div(
                rx.cond(
                    stocks_in_stage.length() > 0,
                    rx.foreach(
                        stocks_in_stage,
                        lambda stock: draggable_stock_card(
                            key=stock.ticker, stock=stock
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
                        class_name="flex flex-col items-center justify-center h-32 border-2 border-dashed border-gray-200 rounded-lg",
                    ),
                ),
                class_name="flex flex-col gap-3 min-h-[150px]",
            ),
            class_name=rx.cond(
                drop_params.is_over,
                "flex-shrink-0 w-80 bg-blue-50 rounded-xl p-4 h-full overflow-y-auto border-2 border-blue-400 transition-colors",
                "flex-shrink-0 w-80 bg-gray-50 rounded-xl p-4 h-full overflow-y-auto border border-gray-200 transition-colors",
            ),
        ),
        accept=["stock"],
        on_drop=lambda item: KanbanState.handle_drop(item, stage_name),
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


def history_modal() -> rx.Component:
    """
    Modal for viewing transition history.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(f"History: {KanbanState.history_stock_ticker}"),
            rx.dialog.description(
                "Record of stage transitions for this stock.", class_name="mb-4"
            ),
            rx.scroll_area(
                rx.el.div(
                    rx.foreach(
                        KanbanState.history_logs,
                        lambda log: rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    rx.moment(
                                        log.timestamp, format="MMM D, YYYY HH:mm"
                                    ),
                                    class_name="text-xs text-gray-400 min-w-[120px]",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            log.previous_stage,
                                            class_name="text-gray-500 line-through mr-2",
                                        ),
                                        rx.icon(
                                            "arrow-right",
                                            class_name="h-3 w-3 text-gray-400 mx-1 inline",
                                        ),
                                        rx.el.span(
                                            log.new_stage,
                                            class_name="font-medium text-blue-600 ml-2",
                                        ),
                                        class_name="text-sm",
                                    ),
                                    rx.el.p(
                                        log.user_comment,
                                        class_name="text-xs text-gray-600 mt-1 italic",
                                    ),
                                    rx.el.p(
                                        f"Updated by {log.updated_by}",
                                        class_name="text-[10px] text-gray-400 mt-1",
                                    ),
                                    class_name="flex-1",
                                ),
                                class_name="flex gap-4 items-start",
                            ),
                            class_name="border-b border-gray-100 last:border-0 pb-3 last:pb-0",
                        ),
                    ),
                    class_name="flex flex-col gap-3",
                ),
                class_name="max-h-[400px] pr-4",
                type="always",
                scrollbars="vertical",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Close",
                        on_click=KanbanState.close_history,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
                    )
                ),
                class_name="flex justify-end mt-6",
            ),
            max_width="600px",
        ),
        open=KanbanState.is_history_open,
        on_open_change=lambda open: rx.cond(open, rx.noop(), KanbanState.close_history),
    )


def index() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.scroll_area(
                rx.el.div(
                    rx.foreach(
                        KanbanState.stages,
                        lambda stage: droppable_stage_column(
                            stage_name=stage, key=stage
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
        add_stock_modal(),
        history_modal(),
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
import reflex as rx
from app.states.kanban_state import KanbanState


def confirmation_modal() -> rx.Component:
    """
    Modal for confirming stock movement and adding comments.

    Returns:
        rx.Component: The confirmation dialog component.
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

    Returns:
        rx.Component: The force transition dialog component.
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


def add_stock_modal() -> rx.Component:
    """
    Modal for adding a new stock.

    Returns:
        rx.Component: The add stock dialog component.
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
    Includes Overview tab and Activity Log tab (history table).

    Returns:
        rx.Component: The detail dialog component.
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
                                KanbanState.current_detail_stock.ticker,
                                class_name="text-base font-bold text-gray-900 border border-gray-200 rounded px-3 py-2 bg-gray-50",
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

    Returns:
        rx.Component: The ocean archive dialog component.
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
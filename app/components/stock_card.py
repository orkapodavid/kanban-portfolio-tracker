import reflex as rx
import reflex_enterprise as rxe
from app.states.kanban_state import KanbanState
from app.models import Stock


@rx.memo
def draggable_stock_card(stock: Stock) -> rx.Component:
    """
    Renders a draggable stock card with actions and timestamps.
    Includes clickable overlay for details modal and context menu.

    Args:
        stock (Stock): The stock data object to render.

    Returns:
        rx.Component: The draggable card component.
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
                        rx.el.button(
                            rx.icon(
                                "send_horizontal",
                                class_name="text-gray-400 h-5 w-5 hover:text-blue-600",
                            ),
                            class_name="h-8 w-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors min-h-[44px] min-w-[44px] md:min-h-0 md:min-w-0",
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
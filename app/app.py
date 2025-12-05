import reflex as rx
from app.states.kanban_state import KanbanState, STAGES
from app.models import Stock


def stock_item(stock: Stock) -> rx.Component:
    """
    Renders a simple debug view of a stock item.
    """
    return rx.el.div(
        rx.el.div(
            rx.el.span(stock.ticker, class_name="font-bold text-gray-900 mr-2"),
            rx.el.span(stock.company_name, class_name="text-sm text-gray-500"),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.span("Last Updated: ", class_name="text-xs text-gray-400"),
            rx.el.span(
                stock.last_updated.to_string(), class_name="text-xs text-gray-600"
            ),
            class_name="mt-1",
        ),
        rx.el.div(
            rx.el.button(
                "Move Next ->",
                on_click=lambda: KanbanState.move_stock(
                    stock.ticker, "Ocean", "Debug Move", "Tester"
                ),
                class_name="text-xs text-blue-600 hover:text-blue-800 mt-2 font-medium",
            ),
            class_name="flex gap-2",
        ),
        class_name="bg-white p-3 rounded border border-gray-200 shadow-sm mb-2",
    )


def stage_column(stage_name: str) -> rx.Component:
    """
    Renders a column for a specific stage.
    """
    return rx.el.div(
        rx.el.h3(
            stage_name,
            class_name="font-semibold text-gray-700 mb-3 sticky top-0 bg-gray-50 py-2 border-b",
        ),
        rx.el.div(
            rx.foreach(
                KanbanState.stocks,
                lambda stock: rx.cond(
                    stock.status == stage_name, stock_item(stock), rx.fragment()
                ),
            ),
            class_name="flex flex-col gap-2 min-h-[200px]",
        ),
        class_name="flex-shrink-0 w-72 bg-gray-50 rounded-lg p-4 mr-4 h-full overflow-y-auto border border-gray-200",
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    "Stock Portfolio Tracker (Backend Phase)",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.div(
                    rx.el.span(
                        "Database Status: ",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    rx.cond(
                        KanbanState.last_error != "",
                        rx.el.span(
                            KanbanState.last_error,
                            class_name="text-sm text-red-600 font-bold",
                        ),
                        rx.el.span(
                            "Connected & Syncing",
                            class_name="text-sm text-green-600 font-bold",
                        ),
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex justify-between items-center max-w-[1600px] mx-auto",
            ),
            class_name="bg-white border-b border-gray-200 px-6 py-4",
        ),
        rx.el.main(
            rx.el.div(
                rx.foreach(KanbanState.stages, stage_column),
                class_name="flex h-full overflow-x-auto pb-4 px-6",
            ),
            class_name="flex-1 overflow-hidden py-6 bg-gray-100",
        ),
        class_name="flex flex-col h-screen font-['Inter']",
        on_mount=KanbanState.on_load,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        )
    ],
)
app.add_page(index, route="/")
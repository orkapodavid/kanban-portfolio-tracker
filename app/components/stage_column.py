import reflex as rx
import reflex_enterprise as rxe
from app.states.kanban_state import KanbanState
from app.models import StageDef
from app.components.stock_card import draggable_stock_card


@rx.memo
def droppable_stage_column(stage: StageDef) -> rx.Component:
    """
    Renders a droppable column for a specific stage.
    Includes special handling for 'Ocean' stage (summary view) vs standard list.

    Args:
        stage (StageDef): The definition of the stage to render.

    Returns:
        rx.Component: The droppable column component.
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
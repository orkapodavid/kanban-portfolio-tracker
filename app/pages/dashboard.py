import reflex as rx
from app.states.kanban_state import KanbanState
from app.components import (
    header,
    droppable_stage_column,
    confirmation_modal,
    force_transition_modal,
    add_stock_modal,
    deal_detail_modal,
    ocean_archive_modal,
)


def dashboard_page() -> rx.Component:
    """
    Main dashboard page for the Kanban board.
    Composes the header, board columns, and global modals.

    Returns:
        rx.Component: The dashboard page component.
    """
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        KanbanState.stages,
                        lambda stage_name: rx.el.button(
                            stage_name,
                            on_click=lambda: KanbanState.set_mobile_active_stage(
                                stage_name
                            ),
                            class_name=rx.cond(
                                KanbanState.mobile_active_stage == stage_name,
                                "px-4 py-2 text-sm font-semibold text-blue-600 border-b-2 border-blue-600 whitespace-nowrap min-h-[44px]",
                                "px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 whitespace-nowrap min-h-[44px]",
                            ),
                        ),
                    ),
                    class_name="flex overflow-x-auto no-scrollbar gap-2 px-4 border-b border-gray-200 bg-white",
                ),
                class_name="md:hidden sticky top-0 z-10",
            ),
            rx.scroll_area(
                rx.el.div(
                    rx.foreach(
                        KanbanState.stage_defs,
                        lambda stage: rx.el.div(
                            droppable_stage_column(stage=stage),
                            class_name=rx.cond(
                                KanbanState.mobile_active_stage == stage.name,
                                "block w-full h-full flex-shrink-0",
                                "hidden md:block h-full flex-shrink-0",
                            ),
                            key=stage.name,
                        ),
                    ),
                    class_name="flex flex-col md:flex-row gap-6 px-4 md:px-6 pb-6 min-w-full md:min-w-max h-full",
                ),
                scrollbars="horizontal",
                type="always",
                class_name="w-full h-full",
            ),
            class_name="flex-1 overflow-hidden py-0 md:py-6 bg-gray-100 flex flex-col",
        ),
        confirmation_modal(),
        force_transition_modal(),
        add_stock_modal(),
        deal_detail_modal(),
        ocean_archive_modal(),
        class_name="flex flex-col h-screen font-['Inter'] bg-gray-50",
        on_mount=KanbanState.on_load,
    )
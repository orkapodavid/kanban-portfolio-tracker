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
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

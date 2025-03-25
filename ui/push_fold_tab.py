"""
Onglet des paramètres Push/Fold pour l'application OpenHoldem Profile Generator
"""
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from ui.components import (create_scroll_area, create_push_fold_position_frame,
                        create_push_fold_call_frame)

def create_push_fold_tab(main_window):
    """
    Crée l'onglet des paramètres Push/Fold
    
    Args:
        main_window (OpenHoldemProfileGenerator): Instance de la fenêtre principale
    
    Returns:
        QScrollArea: Zone de défilement contenant l'onglet Push/Fold
    """
    push_fold_scroll, push_fold_widget, push_fold_layout = create_scroll_area()
    
    # Use a notebook for organization
    pf_notebook = QTabWidget()
    push_fold_layout.addWidget(pf_notebook)
    
    # Create tabs for different stack sizes
    tab_1bb, widget_1bb, layout_1bb = create_scroll_area()
    tab_2_5bb, widget_2_5bb, layout_2_5bb = create_scroll_area()
    tab_6_10bb, widget_6_10bb, layout_6_10bb = create_scroll_area()
    tab_10_25bb, widget_10_25bb, layout_10_25bb = create_scroll_area()
    call_ranges, widget_call, layout_call = create_scroll_area()
    
    pf_notebook.addTab(tab_1bb, "1BB")
    pf_notebook.addTab(tab_2_5bb, "2-5BB")
    pf_notebook.addTab(tab_6_10bb, "6-10BB")
    pf_notebook.addTab(tab_10_25bb, "10-25BB")
    pf_notebook.addTab(call_ranges, "Call Ranges")
    
    # 1BB Tab
    frame_1bb = create_push_fold_position_frame("1BB Stack Push Ranges", {
        "EP": (main_window.push_1bb_ep, lambda v: setattr(main_window, 'push_1bb_ep', v)),
        "MP": (main_window.push_1bb_mp, lambda v: setattr(main_window, 'push_1bb_mp', v)),
        "CO": (main_window.push_1bb_co, lambda v: setattr(main_window, 'push_1bb_co', v)),
        "BTN": (main_window.push_1bb_btn, lambda v: setattr(main_window, 'push_1bb_btn', v)),
        "SB": (main_window.push_1bb_sb, lambda v: setattr(main_window, 'push_1bb_sb', v)),
        "BB": (main_window.push_1bb_bb, lambda v: setattr(main_window, 'push_1bb_bb', v))
    })
    layout_1bb.addWidget(frame_1bb)
    
    # 2BB range function
    frame_2bb = create_push_fold_position_frame("2BB Stack Push Ranges", {
        "EP": (main_window.push_2bb_ep, lambda v: setattr(main_window, 'push_2bb_ep', v)),
        "MP": (main_window.push_2bb_mp, lambda v: setattr(main_window, 'push_2bb_mp', v)),
        "CO": (main_window.push_2bb_co, lambda v: setattr(main_window, 'push_2bb_co', v)),
        "BTN": (main_window.push_2bb_btn, lambda v: setattr(main_window, 'push_2bb_btn', v)),
        "SB": (main_window.push_2bb_sb, lambda v: setattr(main_window, 'push_2bb_sb', v)),
        "BB": (main_window.push_2bb_bb, lambda v: setattr(main_window, 'push_2bb_bb', v))
    })
    layout_2_5bb.addWidget(frame_2bb)
    
    frame_3bb = create_push_fold_position_frame("3BB Stack Push Ranges", {
        "EP": (main_window.push_3bb_ep, lambda v: setattr(main_window, 'push_3bb_ep', v)),
        "MP": (main_window.push_3bb_mp, lambda v: setattr(main_window, 'push_3bb_mp', v)),
        "CO": (main_window.push_3bb_co, lambda v: setattr(main_window, 'push_3bb_co', v)),
        "BTN": (main_window.push_3bb_btn, lambda v: setattr(main_window, 'push_3bb_btn', v)),
        "SB": (main_window.push_3bb_sb, lambda v: setattr(main_window, 'push_3bb_sb', v)),
        "BB": (main_window.push_3bb_bb, lambda v: setattr(main_window, 'push_3bb_bb', v))
    })
    layout_2_5bb.addWidget(frame_3bb)
    
    frame_4bb = create_push_fold_position_frame("4BB Stack Push Ranges", {
        "EP": (main_window.push_4bb_ep, lambda v: setattr(main_window, 'push_4bb_ep', v)),
        "MP": (main_window.push_4bb_mp, lambda v: setattr(main_window, 'push_4bb_mp', v)),
        "CO": (main_window.push_4bb_co, lambda v: setattr(main_window, 'push_4bb_co', v)),
        "BTN": (main_window.push_4bb_btn, lambda v: setattr(main_window, 'push_4bb_btn', v)),
        "SB": (main_window.push_4bb_sb, lambda v: setattr(main_window, 'push_4bb_sb', v)),
        "BB": (main_window.push_4bb_bb, lambda v: setattr(main_window, 'push_4bb_bb', v))
    })
    layout_2_5bb.addWidget(frame_4bb)
    
    frame_5bb = create_push_fold_position_frame("5BB Stack Push Ranges", {
        "EP": (main_window.push_5bb_ep, lambda v: setattr(main_window, 'push_5bb_ep', v)),
        "MP": (main_window.push_5bb_mp, lambda v: setattr(main_window, 'push_5bb_mp', v)),
        "CO": (main_window.push_5bb_co, lambda v: setattr(main_window, 'push_5bb_co', v)),
        "BTN": (main_window.push_5bb_btn, lambda v: setattr(main_window, 'push_5bb_btn', v)),
        "SB": (main_window.push_5bb_sb, lambda v: setattr(main_window, 'push_5bb_sb', v)),
        "BB": (main_window.push_5bb_bb, lambda v: setattr(main_window, 'push_5bb_bb', v))
    })
    layout_2_5bb.addWidget(frame_5bb)
    
    # 6-10BB Tab
    frame_6bb = create_push_fold_position_frame("6BB Stack Push Ranges", {
        "EP": (main_window.push_6bb_ep, lambda v: setattr(main_window, 'push_6bb_ep', v)),
        "MP": (main_window.push_6bb_mp, lambda v: setattr(main_window, 'push_6bb_mp', v)),
        "CO": (main_window.push_6bb_co, lambda v: setattr(main_window, 'push_6bb_co', v)),
        "BTN": (main_window.push_6bb_btn, lambda v: setattr(main_window, 'push_6bb_btn', v)),
        "SB": (main_window.push_6bb_sb, lambda v: setattr(main_window, 'push_6bb_sb', v)),
        "BB": (main_window.push_6bb_bb, lambda v: setattr(main_window, 'push_6bb_bb', v))
    })
    layout_6_10bb.addWidget(frame_6bb)
    
    frame_7bb = create_push_fold_position_frame("7BB Stack Push Ranges", {
        "EP": (main_window.push_7bb_ep, lambda v: setattr(main_window, 'push_7bb_ep', v)),
        "MP": (main_window.push_7bb_mp, lambda v: setattr(main_window, 'push_7bb_mp', v)),
        "CO": (main_window.push_7bb_co, lambda v: setattr(main_window, 'push_7bb_co', v)),
        "BTN": (main_window.push_7bb_btn, lambda v: setattr(main_window, 'push_7bb_btn', v)),
        "SB": (main_window.push_7bb_sb, lambda v: setattr(main_window, 'push_7bb_sb', v)),
        "BB": (main_window.push_7bb_bb, lambda v: setattr(main_window, 'push_7bb_bb', v))
    })
    layout_6_10bb.addWidget(frame_7bb)
    
    frame_8bb = create_push_fold_position_frame("8BB Stack Push Ranges", {
        "EP": (main_window.push_8bb_ep, lambda v: setattr(main_window, 'push_8bb_ep', v)),
        "MP": (main_window.push_8bb_mp, lambda v: setattr(main_window, 'push_8bb_mp', v)),
        "CO": (main_window.push_8bb_co, lambda v: setattr(main_window, 'push_8bb_co', v)),
        "BTN": (main_window.push_8bb_btn, lambda v: setattr(main_window, 'push_8bb_btn', v)),
        "SB": (main_window.push_8bb_sb, lambda v: setattr(main_window, 'push_8bb_sb', v)),
        "BB": (main_window.push_8bb_bb, lambda v: setattr(main_window, 'push_8bb_bb', v))
    })
    layout_6_10bb.addWidget(frame_8bb)
    
    frame_9bb = create_push_fold_position_frame("9BB Stack Push Ranges", {
        "EP": (main_window.push_9bb_ep, lambda v: setattr(main_window, 'push_9bb_ep', v)),
        "MP": (main_window.push_9bb_mp, lambda v: setattr(main_window, 'push_9bb_mp', v)),
        "CO": (main_window.push_9bb_co, lambda v: setattr(main_window, 'push_9bb_co', v)),
        "BTN": (main_window.push_9bb_btn, lambda v: setattr(main_window, 'push_9bb_btn', v)),
        "SB": (main_window.push_9bb_sb, lambda v: setattr(main_window, 'push_9bb_sb', v)),
        "BB": (main_window.push_9bb_bb, lambda v: setattr(main_window, 'push_9bb_bb', v))
    })
    layout_6_10bb.addWidget(frame_9bb)
    
    frame_10bb = create_push_fold_position_frame("10BB Stack Push Ranges", {
        "EP": (main_window.push_10bb_ep, lambda v: setattr(main_window, 'push_10bb_ep', v)),
        "MP": (main_window.push_10bb_mp, lambda v: setattr(main_window, 'push_10bb_mp', v)),
        "CO": (main_window.push_10bb_co, lambda v: setattr(main_window, 'push_10bb_co', v)),
        "BTN": (main_window.push_10bb_btn, lambda v: setattr(main_window, 'push_10bb_btn', v)),
        "SB": (main_window.push_10bb_sb, lambda v: setattr(main_window, 'push_10bb_sb', v)),
        "BB": (main_window.push_10bb_bb, lambda v: setattr(main_window, 'push_10bb_bb', v))
    })
    layout_6_10bb.addWidget(frame_10bb)
    
    # 10-25BB Tab
    frame_10_15bb = create_push_fold_position_frame("10-15BB Stack Push Ranges", {
        "EP": (main_window.push_10_15bb_ep, lambda v: setattr(main_window, 'push_10_15bb_ep', v)),
        "MP": (main_window.push_10_15bb_mp, lambda v: setattr(main_window, 'push_10_15bb_mp', v)),
        "CO": (main_window.push_10_15bb_co, lambda v: setattr(main_window, 'push_10_15bb_co', v)),
        "BTN": (main_window.push_10_15bb_btn, lambda v: setattr(main_window, 'push_10_15bb_btn', v)),
        "SB": (main_window.push_10_15bb_sb, lambda v: setattr(main_window, 'push_10_15bb_sb', v)),
        "BB": (main_window.push_10_15bb_bb, lambda v: setattr(main_window, 'push_10_15bb_bb', v))
    })
    layout_10_25bb.addWidget(frame_10_15bb)
    
    frame_15_20bb = create_push_fold_position_frame("15-20BB Stack Push Ranges", {
        "EP": (main_window.push_15_20bb_ep, lambda v: setattr(main_window, 'push_15_20bb_ep', v)),
        "MP": (main_window.push_15_20bb_mp, lambda v: setattr(main_window, 'push_15_20bb_mp', v)),
        "CO": (main_window.push_15_20bb_co, lambda v: setattr(main_window, 'push_15_20bb_co', v)),
        "BTN": (main_window.push_15_20bb_btn, lambda v: setattr(main_window, 'push_15_20bb_btn', v)),
        "SB": (main_window.push_15_20bb_sb, lambda v: setattr(main_window, 'push_15_20bb_sb', v)),
        "BB": (main_window.push_15_20bb_bb, lambda v: setattr(main_window, 'push_15_20bb_bb', v))
    })
    layout_10_25bb.addWidget(frame_15_20bb)
    
    frame_20_25bb = create_push_fold_position_frame("20-25BB Stack Push Ranges", {
        "EP": (main_window.push_20_25bb_ep, lambda v: setattr(main_window, 'push_20_25bb_ep', v)),
        "MP": (main_window.push_20_25bb_mp, lambda v: setattr(main_window, 'push_20_25bb_mp', v)),
        "CO": (main_window.push_20_25bb_co, lambda v: setattr(main_window, 'push_20_25bb_co', v)),
        "BTN": (main_window.push_20_25bb_btn, lambda v: setattr(main_window, 'push_20_25bb_btn', v)),
        "SB": (main_window.push_20_25bb_sb, lambda v: setattr(main_window, 'push_20_25bb_sb', v)),
        "BB": (main_window.push_20_25bb_bb, lambda v: setattr(main_window, 'push_20_25bb_bb', v))
    })
    layout_10_25bb.addWidget(frame_20_25bb)
    
    # Call Ranges Tab
    frame_call_1bb = create_push_fold_call_frame("1BB Stack Call Ranges", {
        "vs_EP": (main_window.call_1bb_vs_ep, lambda v: setattr(main_window, 'call_1bb_vs_ep', v)),
        "vs_MP": (main_window.call_1bb_vs_mp, lambda v: setattr(main_window, 'call_1bb_vs_mp', v)),
        "vs_CO": (main_window.call_1bb_vs_co, lambda v: setattr(main_window, 'call_1bb_vs_co', v)),
        "vs_BTN": (main_window.call_1bb_vs_btn, lambda v: setattr(main_window, 'call_1bb_vs_btn', v)),
        "vs_SB": (main_window.call_1bb_vs_sb, lambda v: setattr(main_window, 'call_1bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_1bb)
    
    frame_call_2bb = create_push_fold_call_frame("2BB Stack Call Ranges", {
        "vs_EP": (main_window.call_2bb_vs_ep, lambda v: setattr(main_window, 'call_2bb_vs_ep', v)),
        "vs_MP": (main_window.call_2bb_vs_mp, lambda v: setattr(main_window, 'call_2bb_vs_mp', v)),
        "vs_CO": (main_window.call_2bb_vs_co, lambda v: setattr(main_window, 'call_2bb_vs_co', v)),
        "vs_BTN": (main_window.call_2bb_vs_btn, lambda v: setattr(main_window, 'call_2bb_vs_btn', v)),
        "vs_SB": (main_window.call_2bb_vs_sb, lambda v: setattr(main_window, 'call_2bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_2bb)
    
    frame_call_3bb = create_push_fold_call_frame("3BB Stack Call Ranges", {
        "vs_EP": (main_window.call_3bb_vs_ep, lambda v: setattr(main_window, 'call_3bb_vs_ep', v)),
        "vs_MP": (main_window.call_3bb_vs_mp, lambda v: setattr(main_window, 'call_3bb_vs_mp', v)),
        "vs_CO": (main_window.call_3bb_vs_co, lambda v: setattr(main_window, 'call_3bb_vs_co', v)),
        "vs_BTN": (main_window.call_3bb_vs_btn, lambda v: setattr(main_window, 'call_3bb_vs_btn', v)),
        "vs_SB": (main_window.call_3bb_vs_sb, lambda v: setattr(main_window, 'call_3bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_3bb)
    
    frame_call_4bb = create_push_fold_call_frame("4BB Stack Call Ranges", {
        "vs_EP": (main_window.call_4bb_vs_ep, lambda v: setattr(main_window, 'call_4bb_vs_ep', v)),
        "vs_MP": (main_window.call_4bb_vs_mp, lambda v: setattr(main_window, 'call_4bb_vs_mp', v)),
        "vs_CO": (main_window.call_4bb_vs_co, lambda v: setattr(main_window, 'call_4bb_vs_co', v)),
        "vs_BTN": (main_window.call_4bb_vs_btn, lambda v: setattr(main_window, 'call_4bb_vs_btn', v)),
        "vs_SB": (main_window.call_4bb_vs_sb, lambda v: setattr(main_window, 'call_4bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_4bb)
    
    frame_call_5bb = create_push_fold_call_frame("5BB Stack Call Ranges", {
        "vs_EP": (main_window.call_5bb_vs_ep, lambda v: setattr(main_window, 'call_5bb_vs_ep', v)),
        "vs_MP": (main_window.call_5bb_vs_mp, lambda v: setattr(main_window, 'call_5bb_vs_mp', v)),
        "vs_CO": (main_window.call_5bb_vs_co, lambda v: setattr(main_window, 'call_5bb_vs_co', v)),
        "vs_BTN": (main_window.call_5bb_vs_btn, lambda v: setattr(main_window, 'call_5bb_vs_btn', v)),
        "vs_SB": (main_window.call_5bb_vs_sb, lambda v: setattr(main_window, 'call_5bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_5bb)
    
    frame_call_6_10bb = create_push_fold_call_frame("6-10BB Stack Call Ranges", {
        "vs_EP": (main_window.call_6_10bb_vs_ep, lambda v: setattr(main_window, 'call_6_10bb_vs_ep', v)),
        "vs_MP": (main_window.call_6_10bb_vs_mp, lambda v: setattr(main_window, 'call_6_10bb_vs_mp', v)),
        "vs_CO": (main_window.call_6_10bb_vs_co, lambda v: setattr(main_window, 'call_6_10bb_vs_co', v)),
        "vs_BTN": (main_window.call_6_10bb_vs_btn, lambda v: setattr(main_window, 'call_6_10bb_vs_btn', v)),
        "vs_SB": (main_window.call_6_10bb_vs_sb, lambda v: setattr(main_window, 'call_6_10bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_6_10bb)
    
    frame_call_10_15bb = create_push_fold_call_frame("10-15BB Stack Call Ranges", {
        "vs_EP": (main_window.call_10_15bb_vs_ep, lambda v: setattr(main_window, 'call_10_15bb_vs_ep', v)),
        "vs_MP": (main_window.call_10_15bb_vs_mp, lambda v: setattr(main_window, 'call_10_15bb_vs_mp', v)),
        "vs_CO": (main_window.call_10_15bb_vs_co, lambda v: setattr(main_window, 'call_10_15bb_vs_co', v)),
        "vs_BTN": (main_window.call_10_15bb_vs_btn, lambda v: setattr(main_window, 'call_10_15bb_vs_btn', v)),
        "vs_SB": (main_window.call_10_15bb_vs_sb, lambda v: setattr(main_window, 'call_10_15bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_10_15bb)
    
    frame_call_15_25bb = create_push_fold_call_frame("15-25BB Stack Call Ranges", {
        "vs_EP": (main_window.call_15_25bb_vs_ep, lambda v: setattr(main_window, 'call_15_25bb_vs_ep', v)),
        "vs_MP": (main_window.call_15_25bb_vs_mp, lambda v: setattr(main_window, 'call_15_25bb_vs_mp', v)),
        "vs_CO": (main_window.call_15_25bb_vs_co, lambda v: setattr(main_window, 'call_15_25bb_vs_co', v)),
        "vs_BTN": (main_window.call_15_25bb_vs_btn, lambda v: setattr(main_window, 'call_15_25bb_vs_btn', v)),
        "vs_SB": (main_window.call_15_25bb_vs_sb, lambda v: setattr(main_window, 'call_15_25bb_vs_sb', v))
    })
    layout_call.addWidget(frame_call_15_25bb)
    
    return push_fold_scroll

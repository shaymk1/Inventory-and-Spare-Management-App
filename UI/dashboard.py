"""
Main dashboard with navigation
"""

import tkinter
import customtkinter as ctk
from logic.db import db
from UI.spare_form import SpareManagement
from UI.borrow_form import BorrowForm
from UI.return_form import ReturnForm

#  imports for image handling
try:
    from PIL import Image, UnidentifiedImageError

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL not installed. Using text logos.")
import os


class ScrollableFrame(ctk.CTkScrollableFrame):
    """Custom scrollable frame with better styling"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(border_width=0, fg_color="transparent")


class Dashboard(ctk.CTkToplevel):
    def __init__(self, user_info, parent_app):
        super().__init__()
        self.user_info = user_info
        self.parent_app = parent_app

        # Window setup
        self.title(f"Spare Manager - {user_info['full_name']}")
        self.state("zoomed")

        # Set protocol for window close
        self.protocol("WM_DELETE_WINDOW", self._cleanup_and_exit)

        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_frame()

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self._logout)

        # Load initial dashboard view
        self._launch_dashboard()

    def _create_sidebar(self):
        """Create navigation sidebar with scrollbar"""
        # Main sidebar container
        self.sidebar = ctk.CTkFrame(
            self, width=240, corner_radius=0, fg_color="#2b2b2b"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Configure sidebar grid for proper scrolling
        self.sidebar.grid_rowconfigure(1, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        # Fixed top section (won't scroll)
        top_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        # Welcome user
        welcome_label = ctk.CTkLabel(
            top_frame,
            text=f"👋 {self.user_info['full_name']}",
            font=("Arial", 16, "bold"),
            wraplength=200,
        )
        welcome_label.pack(pady=(10, 5))

        role_text = (
            "👨‍💻 Developer" if self.user_info.get("is_developer") else "👷 Manager"
        )
        role_label = ctk.CTkLabel(
            top_frame, text=role_text, font=("Arial", 12), text_color="gray"
        )
        role_label.pack(pady=(0, 10))

        # Separator
        ctk.CTkLabel(top_frame, text="━" * 25, text_color="gray").pack(pady=5)

        # Scrollable area for navigation buttons
        scrollable_frame = ScrollableFrame(
            self.sidebar,
            width=220,
            # height=400,  # Fixed height to enable scrolling
            fg_color="transparent",
        )
        scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        # ===== LOGO IN SIDEBAR =====
        logo_container = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        logo_container.pack(pady=(0, 15))

        # Logo icon with circle background
        icon_frame = ctk.CTkFrame(
            logo_container,
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#2E8B57",  # Green background
        )
        icon_frame.pack()
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(icon_frame, text="🔧", font=("Arial", 24)).pack(expand=True)

        # App name
        ctk.CTkLabel(
            logo_container,
            text="SPARE MANAGER",
            font=("Arial", 12, "bold"),
            text_color="#4FC3F7",
        ).pack(pady=(5, 0))

        # Tagline
        ctk.CTkLabel(
            logo_container,
            text="Inventory System",
            font=("Arial", 10),
            text_color="gray",
        ).pack()
        # Navigation buttons in scrollable area
        nav_buttons = [
            ("📊 Dashboard", self._launch_dashboard),
            ("📦 Manage Spares", self._show_spares),
            ("⬇️ Borrow Items", self._show_borrow),
            ("⬆️ Return Items", self._show_return),
            ("📜 View History", self._show_history),
            ("📈 Reports", self._show_reports),
            ("🔔 Alerts", self._show_alerts),
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                scrollable_frame,
                text=text,
                command=command,
                anchor="w",
                height=42,
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#3a3a3a",
                text_color=("gray10", "#DCE4EE"),
                corner_radius=8,
            )
            btn.pack(pady=2, fill="x", padx=5)

        # Admin only section
        if self.user_info.get("is_developer"):
            # Separator
            sep = ctk.CTkFrame(scrollable_frame, height=2, fg_color="gray")
            sep.pack(pady=10, fill="x")

            admin_label = ctk.CTkLabel(
                scrollable_frame,
                text="Admin Tools",
                font=("Arial", 12, "bold"),
                text_color="orange",
            )
            admin_label.pack(pady=5)

            admin_buttons = [
                ("👥 User Management", self.show_users),
                ("💾 Backup System", self.show_backup),
                ("⚙️ System Settings", self.show_settings),
                ("📋 Audit Log", self.show_audit_log),
                ("🔄 Sync Tools", self.show_sync_tools),
                ("🔧 Maintenance", self.show_maintenance),
            ]

            for text, command in admin_buttons:
                btn = ctk.CTkButton(
                    scrollable_frame,
                    text=text,
                    command=command,
                    anchor="w",
                    height=38,
                    font=("Arial", 13),
                    fg_color="transparent",
                    hover_color="#3a3a3a",
                    text_color="orange",
                    corner_radius=6,
                )
                btn.pack(pady=1, fill="x", padx=5)

        # Fixed bottom section (won't scroll)
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, sticky="sew", padx=10, pady=(0, 10))

        # Separator
        ctk.CTkLabel(bottom_frame, text="━" * 25, text_color="gray").pack(pady=5)

        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            bottom_frame,
            text="🚪 Logout",
            command=self._logout,
            fg_color="#F44336",
            hover_color="#D32F2F",
            height=42,
            font=("Arial", 14, "bold"),
            corner_radius=8,
        )
        logout_btn.pack(pady=5, fill="x")

    def _create_main_frame(self):
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Title bar for current view
        self.title_frame = ctk.CTkFrame(
            self.main_frame, height=50, fg_color="transparent"
        )
        self.title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.title_frame.grid_columnconfigure(0, weight=1)

        self.view_title = ctk.CTkLabel(
            self.title_frame, text="", font=("Arial", 22, "bold")
        )
        self.view_title.grid(row=0, column=0, sticky="w")

        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    def _clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _launch_dashboard(self):
        """
        Shows the dashboard CONTENT (stats, overview).
        Called when user clicks "Dashboard" in sidebar.
        """
        self.view_title.configure(text="📊 Dashboard")
        self._clear_content()

        # Dashboard content
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== LOGO IN MAIN DASHBOARD =====
        row_start = 0

        # Logo container
        logo_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        logo_container.grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Logo icon with background circle
        icon_frame = ctk.CTkFrame(
            logo_container,
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#2E8B57",  # Green circle
            bg_color="transparent",
        )
        icon_frame.pack()
        icon_frame.pack_propagate(False)

        ctk.CTkLabel(icon_frame, text="🔧", font=("Arial", 32)).pack(expand=True)

        # App name
        ctk.CTkLabel(
            logo_container,
            text="Dashboard Overview",
            font=("Arial", 18, "bold"),
            text_color="#4FC3F7",
        ).pack(pady=(10, 5))

        # Tagline
        ctk.CTkLabel(
            logo_container,
            text="Inventory Management System",
            font=("Arial", 12),
            text_color="gray",
        ).pack()

        row_start = 1  # Stats start below logo
        # Get stats from database
        try:
            # from logic.db import db

            # Query 1: Count active spares
            spares_result = db.execute(
                "SELECT COUNT(*) as count FROM spares WHERE is_active = 1", fetch=True
            )
            spares_count = spares_result[0]["count"] if spares_result else 0

            # Query 2: Total quantity of all spares
            total_result = db.execute(
                "SELECT SUM(quantity) as total FROM spares WHERE is_active = 1",
                fetch=True,
            )
            total_items = (
                total_result[0]["total"]
                if total_result and total_result[0]["total"]
                else 0
            )

            # Query 3: Low stock items (using low_stock_threshold)
            low_stock_result = db.execute(
                "SELECT COUNT(*) as count FROM spares WHERE quantity <= low_stock_threshold AND is_active = 1",
                fetch=True,
            )
            low_stock_count = low_stock_result[0]["count"] if low_stock_result else 0

            # Query 4: Today's movements (using movement_date)
            movements_result = db.execute(
                "SELECT COUNT(*) as count FROM movements WHERE date(movement_date) = date('now')",
                fetch=True,
            )
            movements_count = movements_result[0]["count"] if movements_result else 0

        except Exception as e:
            print(f"Database error: {e}")
            # Use default values if queries fail
            spares_count = 0
            total_items = 0
            low_stock_count = 0
            movements_count = 0

        # Display stats
        stats = [
            ("📦", "Active Spares", str(spares_count)),
            ("🔢", "Total Items", str(total_items)),
            ("⚠️", "Low Stock Items", str(low_stock_count)),
            ("📝", "Today's Movements", str(movements_count)),
        ]

        # Create stat cards
        for i, (icon, label, value) in enumerate(stats):
            card = ctk.CTkFrame(
                stats_frame,
                width=200,
                height=120,
                corner_radius=15,
                border_width=2,
                border_color="#3a3a3a",
            )
            card.grid(
                row=row_start + (i // 2), column=i % 2, padx=15, pady=15, sticky="nsew"
            )

            # Icon
            ctk.CTkLabel(card, text=icon, font=("Arial", 24)).pack(pady=(20, 10))
            # Label
            ctk.CTkLabel(card, text=label, font=("Arial", 12), text_color="gray").pack()
            # Value
            ctk.CTkLabel(card, text=value, font=("Arial", 20, "bold")).pack(pady=5)

        # Configure grid
        for i in range(2):
            stats_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            stats_frame.grid_rowconfigure(i, weight=1)

    def _show_spares(self):
        """Show spare management interface"""
        self.view_title.configure(text="📦 Manage Spares")
        self._clear_content()

        # Create spare management interface
        self.spare_management = SpareManagement(self.content_frame, self.user_info)

    def _show_borrow(self):
        """Show borrow interface"""
        self.view_title.configure(text="⬇️ Borrow Items")
        self._clear_content()

        # Create borrow interface
        self.borrow_form = BorrowForm(self.content_frame, self.user_info)

    def _show_return(self):
        """Show return interface"""
        self.view_title.configure(text="⬆️ Return Items")
        self._clear_content()

        # Create return interface
        self.return_form = ReturnForm(self.content_frame, self.user_info)

    def _show_history(self):
        """Show comprehensive movement history with filters and borrower info"""
        self.view_title.configure(text="📜 Complete History")
        self._clear_content()

        try:
            # Import and use the comprehensive MovementHistory class
            from UI.history import MovementHistory

            self.history_interface = MovementHistory(self.content_frame, self.user_info)

        except ImportError as e:
            # Fallback if history module isn't available yet
            print(f"Comprehensive history module not found: {e}")
            self._show_fallback_history()

        except Exception as e:
            # Handle any other errors gracefully
            print(f"Error loading history: {e}")
            self._show_error_history(str(e))

    def _show_fallback_history(self):
        """Show fallback history view when comprehensive module isn't available"""
        fallback_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        fallback_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            fallback_frame, text="📜 Movement History", font=("Arial", 22, "bold")
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            fallback_frame,
            text="Comprehensive history module is being installed...",
            font=("Arial", 14),
            text_color="gray",
        ).pack(pady=(0, 20))

        # Show current simple history
        self._show_current_history_data(fallback_frame)

        # Instructions
        info_frame = ctk.CTkFrame(fallback_frame, corner_radius=10)
        info_frame.pack(fill="x", pady=20, padx=10)

        ctk.CTkLabel(
            info_frame,
            text="ℹ️ What to expect in the comprehensive history:",
            font=("Arial", 14, "bold"),
        ).pack(pady=(10, 5), padx=10, anchor="w")

        features = [
            "✅ All borrow and return activities",
            "✅ Borrower name tracking",
            "✅ Filter by date range, type, status, and borrower",
            "✅ Export to CSV functionality",
            "✅ Real-time statistics",
            "✅ Status indicators (Pending/Partial/Complete)",
        ]

        for feature in features:
            ctk.CTkLabel(info_frame, text=feature, font=("Arial", 12)).pack(
                pady=2, padx=20, anchor="w"
            )

        # Quick action buttons
        button_frame = ctk.CTkFrame(fallback_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        # View Borrow History button (from borrow form)
        ctk.CTkButton(
            button_frame,
            text="📋 View Simple Borrow History",
            width=250,
            height=40,
            font=("Arial", 14),
            fg_color="#2196F3",
            command=self._show_borrow_history_dialog,
        ).pack(pady=5)

        # Refresh button
        ctk.CTkButton(
            button_frame,
            text="🔄 Refresh View",
            width=200,
            height=35,
            font=("Arial", 13),
            command=self.show_history,  # Recursive refresh
        ).pack(pady=5)

    def _show_error_history(self, error_msg):
        """Show error state for history"""
        error_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        error_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            error_frame,
            text="⚠️ Error Loading History",
            font=("Arial", 24, "bold"),
            text_color="orange",
        ).pack(pady=20)

        ctk.CTkLabel(
            error_frame,
            text=f"Error: {error_msg}",
            font=("Arial", 12),
            text_color="red",
            wraplength=600,
        ).pack(pady=10)

        # Debug info
        debug_frame = ctk.CTkFrame(error_frame, corner_radius=10)
        debug_frame.pack(fill="x", pady=20, padx=50)

        ctk.CTkLabel(
            debug_frame, text="Troubleshooting:", font=("Arial", 14, "bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")

        steps = [
            "1. Make sure UI/history.py exists",
            "2. Check that logic/db.py is working",
            "3. Verify database has movements table",
            "4. Restart the application",
        ]

        for step in steps:
            ctk.CTkLabel(debug_frame, text=step, font=("Arial", 11)).pack(
                pady=2, padx=20, anchor="w"
            )

    def _show_current_history_data(self, parent_frame):
        """Show current actual history data from database"""
        try:
            from logic.db import db

            # Get actual history data
            movements = db.execute(
                """
                SELECT 
                    m.movement_date,
                    m.movement_type,
                    m.quantity,
                    m.notes,
                    m.returned_quantity,
                    s.name as spare_name,
                    s.code as spare_code,
                    u.full_name as user_name
                FROM movements m
                JOIN spares s ON m.spare_id = s.id
                JOIN users u ON m.user_id = u.id
                ORDER BY m.movement_date DESC
                LIMIT 20
                """,
                fetch=True,
            )

            if not movements:
                ctk.CTkLabel(
                    parent_frame,
                    text="No movement history found in database",
                    font=("Arial", 14),
                    text_color="gray",
                ).pack(pady=20)
                return

            # Create a simple table
            table_frame = ctk.CTkFrame(parent_frame)
            table_frame.pack(fill="both", expand=True, pady=10)

            # Create scrollable frame
            scroll_frame = ctk.CTkScrollableFrame(table_frame, height=300)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Table headers
            headers = ["Date", "Type", "Spare", "Qty", "User", "Notes"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(
                    scroll_frame, text=header, font=("Arial", 11, "bold"), width=100
                )
                label.grid(row=0, column=col, padx=5, pady=10, sticky="w")

            # Add data rows
            for row, movement in enumerate(movements, start=1):
                # Format date
                date_str = movement["movement_date"]
                if date_str:
                    try:
                        from datetime import datetime

                        if "T" in date_str:
                            date_obj = datetime.fromisoformat(
                                date_str.replace("T", " ")
                            )
                        else:
                            date_obj = datetime.strptime(
                                date_str.split(".")[0], "%Y-%m-%d %H:%M:%S"
                            )
                        display_date = date_obj.strftime("%b %d\n%H:%M")
                    except:
                        display_date = date_str
                else:
                    display_date = "N/A"

                # Truncate spare name
                spare_name = movement["spare_name"]
                if len(spare_name) > 15:
                    spare_display = spare_name[:13] + "..."
                else:
                    spare_display = spare_name

                spare_text = f"{spare_display}\n({movement['spare_code']})"

                # Determine status
                status_color = "white"
                if movement["movement_type"] == "borrow":
                    returned = movement["returned_quantity"] or 0
                    if returned == 0:
                        status_color = "#FF9800"  # Orange
                    elif returned < movement["quantity"]:
                        status_color = "#FFC107"  # Amber
                    else:
                        status_color = "#4CAF50"  # Green

                data = [
                    display_date,
                    movement["movement_type"].title(),
                    spare_text,
                    str(movement["quantity"]),
                    movement["user_name"],
                    (movement["notes"] or "")[:30]
                    + ("..." if len(movement["notes"] or "") > 30 else ""),
                ]

                for col, value in enumerate(data):
                    label = ctk.CTkLabel(
                        scroll_frame,
                        text=value,
                        font=("Arial", 10),
                        width=100,
                        text_color=status_color if col == 1 else "white",
                    )
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

            # Show record count
            ctk.CTkLabel(
                parent_frame,
                text=f"Showing {len(movements)} most recent records",
                font=("Arial", 11),
                text_color="gray",
            ).pack(pady=(10, 0))

        except Exception as e:
            print(f"Error loading current history: {e}")
            ctk.CTkLabel(
                parent_frame,
                text=f"Could not load history data: {str(e)}",
                font=("Arial", 12),
                text_color="orange",
            ).pack(pady=10)

    def _show_borrow_history_dialog(self):
        """Show the simple borrow history dialog"""
        try:
            # This creates a temporary borrow form just to show its history
            temp_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            temp_frame.pack_forget()  # Hide it

            from UI.borrow_form import BorrowForm

            borrow_form = BorrowForm(temp_frame, self.user_info)
            borrow_form.show_borrow_history()

        except Exception as e:
            from UI.components.message_dialog import MessageDialog

            MessageDialog.show_error(
                self.content_frame, "Error", f"Cannot show borrow history:\n{str(e)}"
            )

    def _show_reports(self):
        """Show reports"""
        self.view_title.configure(text="📈 Reports")
        self._clear_content()

        # Reports interface
        reports_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        reports_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            reports_frame, text="Available Reports", font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Report cards
        report_cards = [
            ("📊 Stock Summary", "Complete inventory summary"),
            ("⚠️ Low Stock Alert", "Items below minimum quantity"),
            ("📅 Monthly Usage", "Monthly consumption report"),
            ("👥 User Activity", "User borrowing patterns"),
            ("📦 Item History", "Complete history for specific item"),
            ("💰 Valuation", "Inventory valuation report"),
        ]

        # Create 2x3 grid of report cards
        for i, (title, description) in enumerate(report_cards):
            card = ctk.CTkFrame(
                reports_frame,
                width=250,
                height=120,
                corner_radius=12,
                border_width=1,
                border_color="#3a3a3a",
            )
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            ctk.CTkLabel(card, text=title, font=("Arial", 14, "bold")).pack(
                pady=(15, 5)
            )
            ctk.CTkLabel(
                card,
                text=description,
                font=("Arial", 11),
                text_color="gray",
                wraplength=200,
            ).pack(pady=5)

            ctk.CTkButton(
                card, text="Generate", width=100, height=30, font=("Arial", 11)
            ).pack(pady=10)

        # Configure grid
        for i in range(2):
            reports_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            reports_frame.grid_columnconfigure(i, weight=1)

    def _show_alerts(self):
        """Show alerts"""
        self.view_title.configure(text="🔔 Alerts")
        self._clear_content()

        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Alerts Interface\n(Coming Soon)",
            font=("Arial", 16),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _show_users(self):
        """Show user management (admin only)"""
        self.view_title.configure(text="👥 User Management")
        self._clear_content()

        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="User Management Interface\n(Coming Soon)",
            font=("Arial", 16),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _show_backup(self):
        """Show backup system (admin only)"""
        self.view_title.configure(text="💾 Backup System")
        self._clear_content()

        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Backup Interface\n(Coming Soon)",
            font=("Arial", 16),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _show_settings(self):
        """Show settings (admin only)"""
        self.view_title.configure(text="⚙️ System Settings")
        self._clear_content()

        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Settings Interface\n(Coming Soon)",
            font=("Arial", 16),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _show_audit_log(self):
        """Show audit log (admin only)"""
        self.view_title.configure(text="📋 Audit Log")
        self._clear_content()

        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Audit Log Interface\n(Coming Soon)",
            font=("Arial", 16),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _show_sync_tools(self):
        """Show sync tools (admin only)"""
        self.view_title.configure(text="🔄 Sync Tools")
        self._clear_content()

        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Sync Tools Interface\n(Coming Soon)",
            font=("Arial", 16),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _show_maintenance(self):
        """Show maintenance tools (admin only)"""
        self.view_title.configure(text="🔧 Maintenance")
        self._clear_content()

        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Maintenance Interface\n(Coming Soon)",
            font=("Arial", 16),
            text_color="gray",
        )
        placeholder.pack(pady=100)

    def _add_spare(self):
        """Add new spare"""
        print("Add spare functionality to be implemented")

    def _process_borrow(self):
        """Process borrow request"""
        print("Borrow functionality to be implemented")

    def _process_return(self):
        """Process return request"""
        print("Return functionality to be implemented")

    def _logout(self):
        """logout"""
        print("🔄 Logging out...")

        # Cancel all pending after() events
        try:
            # Get all pending after events
            after_ids = self.tk.eval("after info").split()
            for after_id in after_ids:
                try:
                    self.after_cancel(after_id)
                except (ValueError, tkinter.TclError):
                    pass  # after_id might be invalid already
        except (AttributeError, tkinter.TclError):
            pass  # No after events or tk not available

        # Unbind any global events
        try:
            self.unbind_all("<Key>")
            self.unbind_all("<Button>")
        except (AttributeError, tkinter.TclError):
            pass

        # Destroy window
        try:
            self.destroy()
        except (AttributeError, tkinter.TclError):
            pass

        # Force exit the app completely
        import sys

        sys.exit(0)

    def _show_simple_history(self):
        """Fallback simple history view"""
        # Create a simple frame as placeholder
        placeholder = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        placeholder.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            placeholder, text="📜 History View", font=("Arial", 24, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            placeholder,
            text="Comprehensive history view is loading...",
            font=("Arial", 14),
            text_color="gray",
        ).pack()

        # You could also reuse the borrow form's history dialog here
        ctk.CTkButton(
            placeholder,
            text="View Borrow History",
            width=200,
            height=40,
            font=("Arial", 14),
            command=self._show_borrow_history_simple,
        ).pack(pady=20)

    def _show_simple_borrow_history(self):
        """Show simple borrow history (reusing borrow form's method)"""
        # This would show the same dialog as the borrow form button
        from UI.borrow_form import BorrowForm

        # Create a temporary borrow form just to call its history method
        temp_frame = ctk.CTkFrame(self.content_frame)
        temp_form = BorrowForm(temp_frame, self.user_info)
        temp_form.show_borrow_history()

    def _cleanup_and_exit(self):
        """Clean up before exiting"""
        self.logout()

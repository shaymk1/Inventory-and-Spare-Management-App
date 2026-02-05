"""
Main dashboard with navigation
"""

import tkinter
import customtkinter as ctk
from logic.db import db

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
        self.protocol("WM_DELETE_WINDOW", self.cleanup_and_exit)

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
        self.protocol("WM_DELETE_WINDOW", self.logout)

        # Load initial dashboard view
        self.launch_dashboard()

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
            ("📊 Dashboard", self.launch_dashboard),
            ("📦 Manage Spares", self.show_spares),
            ("⬇️ Borrow Items", self.show_borrow),
            ("⬆️ Return Items", self.show_return),
            ("📜 View History", self.show_history),
            ("📈 Reports", self.show_reports),
            ("🔔 Alerts", self.show_alerts),
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
            command=self.logout,
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

    def launch_dashboard(self):
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

    def show_spares(self):
        """Show spare management interface"""
        self.view_title.configure(text="📦 Manage Spares")
        self._clear_content()

        # Create a tabbed interface for spares
        tabview = ctk.CTkTabview(self.content_frame)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Add tabs
        tabview.add("View Spares")
        tabview.add("Add New")
        tabview.add("Search")

        # View Spares tab
        view_frame = tabview.tab("View Spares")

        # Create a scrollable table for spares
        scrollable_frame = ScrollableFrame(view_frame, height=400)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add sample data (replace with actual database query)
        headers = ["ID", "Name", "Code", "Quantity", "Min Qty", "Location"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                scrollable_frame, text=header, font=("Arial", 12, "bold"), width=100
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")

        # Sample data rows
        sample_data = [
            [1, "Bolt M6", "BLT-M6-50", 150, 50, "Shelf A1"],
            [2, "Washer 10mm", "WSH-10", 80, 30, "Shelf A2"],
            [3, "Nut M8", "NUT-M8", 200, 40, "Shelf B1"],
        ]

        for row, data in enumerate(sample_data, start=1):
            for col, value in enumerate(data):
                label = ctk.CTkLabel(
                    scrollable_frame, text=str(value), font=("Arial", 11), width=100
                )
                label.grid(row=row, column=col, padx=5, pady=2, sticky="w")

        # Add New tab
        add_frame = tabview.tab("Add New")

        # Form for adding new spare
        form_frame = ctk.CTkFrame(add_frame)
        form_frame.pack(pady=50, padx=50, fill="both", expand=True)

        fields = [
            ("Spare Name:", ctk.CTkEntry),
            ("Spare Code:", ctk.CTkEntry),
            ("Quantity:", ctk.CTkEntry),
            ("Minimum Quantity:", ctk.CTkEntry),
            ("Location:", ctk.CTkEntry),
        ]

        for i, (label_text, widget_type) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label_text, font=("Arial", 12)).grid(
                row=i, column=0, pady=10, padx=10, sticky="e"
            )
            entry = widget_type(form_frame, width=200)
            entry.grid(row=i, column=1, pady=10, padx=10, sticky="w")

        # Add button
        add_btn = ctk.CTkButton(
            form_frame,
            text="➕ Add Spare",
            command=self.add_spare,
            width=150,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#4CAF50",
        )
        add_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def show_borrow(self):
        """Show borrow interface"""
        self.view_title.configure(text="⬇️ Borrow Items")
        self._clear_content()

        # Borrow form
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(pady=50, padx=100, fill="both", expand=True)

        ctk.CTkLabel(
            form_frame, text="Borrow Items Form", font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(pady=20)

        fields = [
            ("Select Spare:", ctk.CTkComboBox),
            ("Borrower Name:", ctk.CTkEntry),
            ("Quantity to Borrow:", ctk.CTkEntry),
            ("Purpose:", ctk.CTkTextbox),
        ]

        for i, (label_text, widget_type) in enumerate(fields):
            ctk.CTkLabel(fields_frame, text=label_text, font=("Arial", 12)).grid(
                row=i, column=0, pady=10, padx=10, sticky="e"
            )

            if widget_type == ctk.CTkTextbox:
                widget = widget_type(fields_frame, width=200, height=60)
            elif widget_type == ctk.CTkComboBox:
                widget = widget_type(
                    fields_frame, width=200, values=["Bolt M6", "Washer 10mm", "Nut M8"]
                )
                widget.set("Select spare...")
            else:
                widget = widget_type(fields_frame, width=200)

            widget.grid(row=i, column=1, pady=10, padx=10, sticky="w")

        # Borrow button
        borrow_btn = ctk.CTkButton(
            form_frame,
            text="✅ Borrow Items",
            command=self.process_borrow,
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#2196F3",
        )
        borrow_btn.pack(pady=30)

    def show_return(self):
        """Show return interface"""
        self.view_title.configure(text="⬆️ Return Items")
        self._clear_content()

        # Similar to borrow but for returns
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(pady=50, padx=100, fill="both", expand=True)

        ctk.CTkLabel(
            form_frame, text="Return Items Form", font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Placeholder content
        ctk.CTkLabel(
            form_frame,
            text="This interface will show:\n\n• List of borrowed items\n• Quantity to return\n• Condition check\n• Return confirmation",
            font=("Arial", 14),
            justify="left",
        ).pack(pady=30)

        return_btn = ctk.CTkButton(
            form_frame,
            text="🔄 Process Return",
            command=self.process_return,
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#FF9800",
        )
        return_btn.pack(pady=20)

    def show_history(self):
        """Show movement history"""
        self.view_title.configure(text="📜 Movement History")
        self._clear_content()

        # History interface with filters
        filter_frame = ctk.CTkFrame(self.content_frame, height=60)
        filter_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Filter options
        ctk.CTkLabel(filter_frame, text="Filter by:", font=("Arial", 12)).pack(
            side="left", padx=10
        )

        filter_options = ["Today", "Last 7 days", "This month", "All time"]
        filter_combo = ctk.CTkComboBox(filter_frame, values=filter_options, width=150)
        filter_combo.pack(side="left", padx=10)
        filter_combo.set("Today")

        ctk.CTkButton(filter_frame, text="🔍 Apply Filter", width=120, height=35).pack(
            side="left", padx=10
        )

        # History table
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Create scrollable history
        history_scroll = ScrollableFrame(table_frame, height=400)
        history_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Table headers
        headers = ["Date", "Time", "Type", "Spare", "Quantity", "User", "Notes"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                history_scroll,
                text=header,
                font=("Arial", 11, "bold"),
                width=100 if col < 4 else 150,
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")

        # Sample history data
        sample_history = [
            [
                "2024-01-15",
                "09:30",
                "Borrow",
                "Bolt M6",
                10,
                "John Doe",
                "For machine repair",
            ],
            [
                "2024-01-15",
                "11:15",
                "Return",
                "Washer 10mm",
                5,
                "Jane Smith",
                "Partial return",
            ],
            [
                "2024-01-14",
                "14:20",
                "Borrow",
                "Nut M8",
                20,
                "Bob Wilson",
                "Maintenance work",
            ],
        ]

        for row, data in enumerate(sample_history, start=1):
            for col, value in enumerate(data):
                label = ctk.CTkLabel(
                    history_scroll,
                    text=str(value),
                    font=("Arial", 10),
                    width=100 if col < 4 else 150,
                )
                label.grid(row=row, column=col, padx=5, pady=2, sticky="w")

    def show_reports(self):
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

    # Other methods remain the same as before...
    def show_alerts(self):
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

    def show_users(self):
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

    def show_backup(self):
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

    def show_settings(self):
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

    def show_audit_log(self):
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

    def show_sync_tools(self):
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

    def show_maintenance(self):
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

    def add_spare(self):
        """Add new spare"""
        print("Add spare functionality to be implemented")

    def process_borrow(self):
        """Process borrow request"""
        print("Borrow functionality to be implemented")

    def process_return(self):
        """Process return request"""
        print("Return functionality to be implemented")

    def logout(self):
        """Clean logout without Tkinter errors"""
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

    def cleanup_and_exit(self):
        """Clean up before exiting"""
        self.logout()

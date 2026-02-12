
@echo off
echo 📦 Committing today's work...

REM 1. Borrower name system
git add logic/db.py sql/create_movements.sql UI/borrow_form.py UI/return_form.py
git commit -m "feat: Add borrower name tracking to movements table

- Added borrower_name column with auto-migration
- Updated borrow form to save borrower names
- Fixed return form to preserve borrower names
- Backfilled existing records from notes"

REM 2. Comprehensive history module
git add UI/history.py UI/dashboard.py
git commit -m "feat: Complete movement history system

- Added comprehensive history view with filters
- Implemented CSV export functionality
- Added borrower filter and statistics
- Connected sidebar history button"

REM 3. Simple borrow history fix
git add UI/borrow_form.py
git commit -m "fix: Show borrower names in simple borrow history

- Added borrower_name to SELECT query
- Added Borrower column to table
- Fixed SQL syntax error"

REM 4. Spare management - Edit/Delete system
git add UI/spare_form.py
git commit -m "feat: Click-to-edit spare management

- Made spares clickable in view tab
- Added full edit dialog with name, code, quantity
- Implemented soft delete for spares with history
- Added duplicate code validation
- Made dialog scrollable"

REM 5. Push to remote
echo 🚀 Pushing to remote...
git push

echo ✅ Done! All changes committed and pushed.
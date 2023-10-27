venv:
	@echo "Creating virtual environment..."
	@python3 -m venv venv
	@echo "Activating virtual environment..."
	@source venv/bin/activate

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt
	@echo "Installation done."

run:
	@echo "Running application..."
	@python3 main.py

start:
	@echo "Starting project..."
	@make venv
	@make install
	@make run
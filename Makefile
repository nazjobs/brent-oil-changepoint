# Simple automation for the project

setup:
	pip install -r requirements.txt

test:
	python -m unittest discover tests

run-dashboard-backend:
	cd dashboard/backend && python app.py

run-dashboard-frontend:
	cd dashboard/frontend && npm start

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache

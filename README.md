# The Joy of Painting Database and Web Application

## **Overview**
This project is a web application and database designed to manage and display episodes of *The Joy of Painting*. It includes functionality to filter episodes by attributes such as color, subject, and season, and is built with Flask, SQLite, and Bootstrap for a clean and user-friendly interface.

---

## **Features**
- **Database Management:**
  - Organizes episode information including titles, seasons, episode numbers, and broadcast dates.
  - Links episodes to associated colors and subjects used in Bob Ross's paintings.
- **User Interface:**
  - Built with Flask and Bootstrap for a responsive and modern design.
  - Dropdown menus for filtering by colors, subjects, and seasons.
- **API Integration:**
  - Provides endpoints for filtering episodes using various criteria.
- **Data Processing:**
  - Extracts and cleans raw data from `.txt` files, loading it into the database.
  - Deduplication ensures data integrity and consistency.